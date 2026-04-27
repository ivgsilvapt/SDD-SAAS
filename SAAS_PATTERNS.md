# SAAS_PATTERNS.md

Padrões arquiteturais específicos para SaaS. Complementa `ARCHITECTURE.md` (seção 15).
Consulte este arquivo antes de modelar qualquer domínio multi-tenant, de billing ou com feature flags.

---

## Usando @harness/saas-core (harness v2.0+)

O harness fornece primitivas multi-tenant prontas em `harness/lib/saas-core/`. **Não reimplemente** TenantContext, TenantAwareEntity ou TenantAwareRepository — importe do harness.

### Instalação (Node.js)
```typescript
// package.json
"@harness/saas-core": "file:path/to/sdd-saas/harness/lib/saas-core/node"
```

### Uso essencial
```typescript
import {
  TenantAwareEntity,
  TenantAwareRepository,
  TenantContext,
  tenantMiddleware,
} from '@harness/saas-core';

// Entidade: tenantId obrigatório por design
class Subscription extends TenantAwareEntity {
  constructor(id: string, tenantId: string, public readonly plan: string) {
    super(id, tenantId);
  }
}

// Repositório: filtro de tenant automático
class PrismaSubscriptionRepository extends TenantAwareRepository<Subscription> {
  async findById(id: string): Promise<Subscription | null> {
    const tenantId = this.currentTenantId; // automático
    const row = await prisma.subscription.findFirst({ where: { id, tenantId } });
    return row ? new Subscription(row.id, row.tenantId, row.plan) : null;
  }
  // ... outros métodos
}

// Middleware: registra tenantId no contexto por request
app.use(tenantMiddleware); // extrai tenant_id do JWT
```

### Instalação (Python)
```python
from harness_saas_core import TenantAwareEntity, TenantAwareRepository, TenantContext, require_tenant
```

### Por que isso importa
**Bug clássico de multi-tenant:** repositório sem filtro `tenantId` retorna dados de outro tenant. Com `TenantAwareRepository`, o campo `currentTenantId` está sempre disponível e o filtro é estruturalmente obrigatório — você não _pode_ esquecer.

---

## 1. Multi-tenancy

### Comparativo de Estratégias

| Estratégia | Como funciona | Isolamento | Custo operacional | Quando usar |
|---|---|---|---|---|
| **Row-level isolation** | Todos os tenants no mesmo banco, `tenantId` em cada linha | Médio (app-level) | Baixo | Maioria dos SaaS — padrão recomendado |
| **Schema-per-tenant** | Um schema por tenant no mesmo banco | Alto (DB-level) | Médio | Quando compliance exige separação lógica |
| **Database-per-tenant** | Um banco por tenant | Muito alto | Alto | Regulamentação estrita, clientes enterprise |

**Recomendação padrão:** Row-level isolation com `tenantId` em todas as tabelas. Simples de operar, escala bem para centenas de tenants.

---

### 1.1 Row-Level Isolation — Implementação

**Regra:** Todo repositório filtra `tenantId` em **toda** query. Sem exceção.

**Modelo de dados:** Toda tabela de dados de negócio tem `tenant_id` como coluna obrigatória com índice.

```sql
-- Toda tabela de domínio
CREATE TABLE subscriptions (
  id          UUID PRIMARY KEY,
  tenant_id   UUID NOT NULL REFERENCES tenants(id),
  ...
  created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_subscriptions_tenant_id ON subscriptions(tenant_id);
```

**Repository Implementation:**
```
// Correto: TenantContext injetado no repositório via DI
class SubscriptionRepository implements ISubscriptionRepository {
  constructor(private db: Database, private tenantCtx: TenantContext) {}

  findById(id: SubscriptionId): Subscription | null {
    return this.db.query(
      'SELECT * FROM subscriptions WHERE id = ? AND tenant_id = ?',
      [id.value, this.tenantCtx.tenantId]
    )
  }
}
```

---

### 1.2 TenantContext — Propagação pela Arquitetura

```
HTTP Request
     │
     ▼
Middleware Auth
     │  extrai tenantId do JWT (claim: "tenant_id")
     │  ou do subdomínio (acme.app.com → "acme")
     │  ou do header (X-Tenant-Id para APIs internas)
     ▼
TenantContext registrado no container DI (escopo: requisição)
     │
     ▼
Use Case recebe TenantContext via construtor (DI)
     │
     ▼
Repository recebe TenantContext via construtor (DI)
     │  filtra toda query com tenantId
     ▼
Dados do tenant retornados
```

**Interface do TenantContext:**
```
interface ITenantContext {
  tenantId: TenantId
  tenantSlug: string
  plan: SubscriptionPlan
}
```

**Regras:**
- TenantContext é sempre **read-only** após criação no middleware
- TenantId nunca é passado como parâmetro de método — está no contexto
- Operações administrativas (admin interno) usam um SystemTenantContext especial com bypass documentado

---

### 1.3 Checklist de Isolamento de Tenant

Aplique antes de aceitar qualquer código de repositório:

- [ ] Toda query inclui filtro por `tenantId`?
- [ ] TenantContext é injetado via DI, não lido de variável global?
- [ ] Nenhum endpoint retorna dados de múltiplos tenants sem autorização explícita de admin?
- [ ] Operações de escrita verificam que o recurso pertence ao tenant antes de modificar?
- [ ] Testes de repositório incluem teste de isolamento (tenant A não acessa dados do tenant B)?

---

## 2. Modelo de Domínio — Tenant e Workspace

```
Tenant (Aggregate Root)
├── id: TenantId
├── slug: TenantSlug       ← identificador único de URL (ex: "acme")
├── name: string
├── status: TenantStatus   ← active | suspended | churned
├── plan: SubscriptionPlan ← referência ao plano contratado
└── settings: TenantSettings

Workspace (opcional — para SaaS com múltiplos workspaces por tenant)
├── id: WorkspaceId
├── tenantId: TenantId
├── name: string
└── members: WorkspaceMember[]
```

---

## 3. Subscription Lifecycle

### Estados e Transições

```
                   ┌─────────────┐
      criar        │             │
  ──────────────→  │   trialing  │ ←── trial gratuito (sem pagamento)
                   │             │
                   └──────┬──────┘
                          │ trial_expired / payment_added
                          ▼
                   ┌─────────────┐
                   │             │    pagamento falhou
                   │   active    │ ─────────────────────→ ┌───────────┐
                   │             │                         │ past_due  │
                   └──────┬──────┘ ←───────────────────── └───────────┘
                          │              pagamento ok
                          │ cancelamento solicitado
                          ▼
                   ┌─────────────┐
                   │             │  (permanece ativo até fim do período pago)
                   │ cancel_at   │
                   │ period_end  │
                   └──────┬──────┘
                          │ período expirou
                          ▼
                   ┌─────────────┐
                   │             │
                   │  canceled   │
                   │             │
                   └─────────────┘
```

**Notas:**
- `trialing`: acesso completo ou limitado sem cobrança por N dias
- `active`: assinatura paga e em dia
- `past_due`: pagamento falhou — acesso degradado, alertas enviados, retentativas automáticas
- `cancel_at_period_end`: solicitou cancelamento mas continua ativo até o fim do período pago
- `canceled`: sem acesso (ou apenas leitura para export de dados)

### Eventos de Domínio da Assinatura

> **Sync vs Async:** Eventos *dentro* do mesmo BC são síncronos (dispatch no Use Case). Eventos *entre BCs* são assíncronos via Outbox (ver `ARCHITECTURE.md` seção 19).

| Evento | Quando disparado | Consumidores típicos | Entrega |
|---|---|---|---|
| `SubscriptionTrialStarted` | Tenant criado com trial | E-mail de boas-vindas | Outbox (async) |
| `SubscriptionActivated` | Primeiro pagamento bem-sucedido | E-mail de confirmação, unlock de features | Outbox (async) |
| `SubscriptionRenewed` | Cobrança mensal/anual bem-sucedida | E-mail de recibo | Outbox (async) |
| `SubscriptionPaymentFailed` | Cobrança falhou | E-mail de alerta, degradação de acesso | Outbox (async) |
| `SubscriptionCanceled` | Cancelamento efetivado | E-mail de confirmação, offboarding | Outbox (async) |
| `SubscriptionReactivated` | Reativação após cancelamento | E-mail de boas-vindas de volta | Outbox (async) |
| `TrialExpired` | Trial expirou sem conversão | E-mail de expiração, acesso bloqueado | Outbox (async) |

---

## 4. Feature Flags

Feature flags permitem rollout gradual, testes A/B e diferenciação por plano.

### Interface no Domínio

```
// domain/shared/feature-flags/IFeatureFlagService.ts
interface IFeatureFlagService {
  isEnabled(flag: FeatureFlag, tenantId: TenantId): boolean
}

// Enum de feature flags — defina aqui todas as flags do produto
enum FeatureFlag {
  ADVANCED_REPORTS   = 'advanced_reports',
  API_ACCESS         = 'api_access',
  CUSTOM_DOMAIN      = 'custom_domain',
  TEAM_MEMBERS       = 'team_members',
  EXPORT_CSV         = 'export_csv',
}
```

### Uso no Use Case

```
// Exemplo de verificação de feature flag em um use case
class ExportReportUseCase {
  constructor(
    private featureFlags: IFeatureFlagService,
    private tenantCtx: ITenantContext,
    private reportRepo: IReportRepository
  ) {}

  execute(): Result<ReportData> {
    if (!this.featureFlags.isEnabled(FeatureFlag.ADVANCED_REPORTS, this.tenantCtx.tenantId)) {
      return Result.fail(new AuthorizationError('FEATURE_NOT_AVAILABLE_ON_PLAN'))
    }
    // ...
  }
}
```

### Fontes de Feature Flags (Infrastructure)

| Fonte | Quando usar |
|---|---|
| Banco de dados (tabela `tenant_features`) | Feature flags por tenant ou por plano — padrão |
| Variável de ambiente | Feature flags globais (liga/desliga para todos) |
| Serviço externo (LaunchDarkly, Unleash) | Rollout gradual com percentual, A/B testing |

---

## 5. Billing Patterns

### Modelos de Cobrança

| Modelo | Como funciona | Quando usar |
|---|---|---|
| **Flat-rate** | Valor fixo por mês/ano, independente do uso | Produto com valor percebido constante |
| **Seat-based** | Cobrado por usuário ativo | Ferramentas de time, colaboração |
| **Usage-based (metered)** | Cobrado por unidade consumida (API calls, GB, e-mails) | Plataformas de API, infra, mensageria |
| **Hybrid** | Flat-rate + overage para uso acima do limite | Equilíbrio previsibilidade/escalabilidade |

### Integração com Gateway de Pagamento

```
// Domain: interface — não conhece Stripe, Braintree, etc.
interface IPaymentGateway {
  createCustomer(tenant: Tenant): Result<CustomerId>
  createSubscription(customerId: CustomerId, plan: PlanId): Result<ExternalSubscriptionId>
  cancelSubscription(externalSubscriptionId: ExternalSubscriptionId): Result<void>
  chargeInvoice(invoiceId: InvoiceId): Result<ChargeResult>
}

// Infrastructure: implementação concreta
class StripePaymentGateway implements IPaymentGateway { ... }
```

**Regras de billing:**
- A cobrança é sempre iniciada por um Use Case — nunca por um event handler diretamente
- Use Idempotency-Key em todas as chamadas ao gateway para evitar cobranças duplicadas
- Persista o resultado da cobrança **antes** de confirmar ao cliente
- Webhooks do gateway disparam eventos de domínio — nunca chamam use cases diretamente

---

## 6. Onboarding — Criação de Tenant

### Fluxo padrão

```
1. Usuário preenche formulário (nome, e-mail, empresa, plano)
2. Command Object valida dados
3. CreateTenantUseCase:
   a. Cria Tenant (status: trialing)
   b. Cria conta de Admin do Tenant
   c. Cria Workspace padrão
   d. Registra no gateway de pagamento (customer sem cobrança imediata)
   e. Emite SubscriptionTrialStarted
4. Middleware de e-mail consome SubscriptionTrialStarted → envia e-mail de boas-vindas
5. Redireciona para o dashboard do tenant
```

**Regra de atomicidade:** Os passos 3a–3d devem ser executados em uma única transação via **Unit of Work** (ver `ARCHITECTURE.md` seção 7). Se qualquer passo falhar, nenhum dado deve ser persistido. O evento `SubscriptionTrialStarted` é persistido no Outbox na mesma transação e publicado de forma assíncrona pelo worker.

---

## 7. LGPD / GDPR — Conformidade de Dados

### Dados Pessoais (PII)

Defina no SPEC ou no GLOSSARY quais campos são PII:
- Nome completo, e-mail, telefone, CPF/CNPJ
- IP de acesso, device ID, dados de comportamento

### Padrões de Conformidade

| Requisito | Implementação |
|---|---|
| **Direito ao esquecimento** | Soft delete com `deletedAt`; anonimização de PII após N dias |
| **Portabilidade de dados** | Use Case `ExportTenantDataUseCase` — retorna todos os dados do tenant em JSON/CSV |
| **Consentimento** | Registre consentimento com timestamp e versão da política |
| **Retenção** | Defina TTL por tipo de dado; purge automático via job |
| **Acesso por terceiros** | API de dados só acessível pelo próprio tenant |
| **Log de acesso a PII** | Auditoria de quem acessou quais dados pessoais e quando |

### Soft Delete vs Hard Delete

```
// Soft delete — padrão para entidades com PII
Entity:
  deletedAt: Date | null
  deletedBy: UserId | null
```

**Comportamento explícito do repositório** (ver `ARCHITECTURE.md` seção 11):

| Método | Comportamento |
|---|---|
| `findById(id)` | Retorna `NotFoundError` se `deletedAt IS NOT NULL` |
| `findAll(filter)` | Filtra automaticamente `WHERE deletedAt IS NULL` |
| `findByIdIncludeDeleted(id)` | Retorna mesmo que deletado — apenas para auditoria/LGPD |
| `delete(id)` | Seta `deletedAt = now()` — nunca executa `DELETE` físico |

```
// Após TTL de retenção, anonimiza os dados pessoais (não deleta o registro)
AnonimizationJob:
  - Substitui nome por "Usuário removido"
  - Substitui e-mail por hash irreversível
  - Remove telefone, CPF, endereço
```

Hard delete físico é permitido apenas via `PurgePersonalDataJob`, com log de auditoria obrigatório.

---

## 8. Rate Limiting por Tenant

Rate limiting protege o sistema de uso abusivo e garante equidade entre tenants.

### Dimensões de Limitação

| Dimensão | Exemplo | Onde implementar |
|---|---|---|
| Por tenant + endpoint | 100 req/min para `/api/v1/invoices` | Middleware de rate limit |
| Por plano | Free: 1.000 req/dia; Pro: 100.000 req/dia | Middleware com lookup de plano |
| Por feature | 10 exports/hora | Use Case com verificação de quota |

### Headers de Resposta (convencional)

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1705312800
```

Quando o limite é excedido, retorne **HTTP 429** com `Retry-After` e error code `RATE_LIMIT_EXCEEDED`.

---

## 10. Background Jobs — Padrões Multi-Tenant

Background jobs em SaaS multi-tenant exigem cuidado especial para não processar dados de um tenant com o contexto de outro.

### Padrão: Iteração por Tenant

Para jobs que processam todos os tenants (ex: renovação de assinaturas):

```
class RenewSubscriptionsJob {
  constructor(
    private tenantRepo: ITenantRepository,
    private subscriptionService: SubscriptionRenewalService,
    private tenantContextFactory: ITenantContextFactory
  ) {}

  async execute(): Promise<void> {
    const activeTenants = await this.tenantRepo.findAllActive()

    for (const tenant of activeTenants) {
      const ctx = this.tenantContextFactory.create(tenant.id)
      await this.subscriptionService.renewDue(ctx)
      // Cada tenant tem seu próprio contexto — sem vazamento entre iterações
    }
  }
}
```

### Regras Multi-Tenant para Jobs

| Regra | Detalhe |
|---|---|
| **Nunca processe sem TenantContext** | Mesmo em jobs, injete ou construa um TenantContext por iteração |
| **Idempotência por tenant** | Job deve poder ser reexecutado para um tenant sem duplicar efeitos |
| **Falha isolada por tenant** | Erro em um tenant não deve interromper o processamento dos demais — use try/catch por iteração |
| **Log com tenantId** | Todo log de execução de job inclui `tenantId` e `jobName` |
| **Sem processamento cruzado** | Repositórios dentro de um job sempre filtram por `tenantId` do TenantContext atual |

### Jobs SaaS Comuns

| Job | Frequência | Idempotência |
|---|---|---|
| `RenewSubscriptionsJob` | Diária | Verifica se já renovado no período atual antes de cobrar |
| `GenerateMonthlyInvoicesJob` | Mensal | Verifica se invoice do período já existe antes de criar |
| `SendPaymentReminderJob` | Diária | Verifica se lembrete já enviado (flag `reminderSentAt`) |
| `PurgeExpiredDataJob` | Semanal | Verifica TTL antes de anonimizar |
| `OutboxWorkerJob` | Contínuo (polling) | Verifica `processed_at IS NULL` antes de publicar |

---

## 11. Tenant Provisioning Queue

O fluxo de onboarding de tenant envolve múltiplas operações (criação de conta, registro no gateway de pagamento, envio de e-mail de boas-vindas, setup de dados iniciais). Se todas forem síncronas no request de signup, o usuário espera vários segundos e qualquer falha de serviço externo quebra o cadastro.

### O Problema

```
POST /signup
  └─ CreateTenantUseCase
       ├─ INSERT tenant (< 50ms)
       ├─ RegisterOnStripe (200–800ms, pode falhar)
       ├─ SendWelcomeEmail (100–500ms, pode falhar)
       └─ SetupDefaultData (100–300ms)
  Total: 400ms–1.6s, qualquer falha = 500 para o usuário
```

### A Solução: Provisioning Assíncrono

```
POST /signup
  └─ CreateTenantUseCase
       ├─ INSERT tenant (status: provisioning) + TenantProvisioningRequested no Outbox
       └─ Retorna 201 imediatamente (< 100ms)

Worker (async)
  └─ Consome TenantProvisioningRequested
       ├─ RegisterOnStripe (com retry)
       ├─ SendWelcomeEmail (com retry)
       ├─ SetupDefaultData
       └─ UPDATE tenant (status: active) + TenantProvisioned no Outbox
```

### Estados do Provisioning

| Status | Significado | Acesso do tenant |
|---|---|---|
| `provisioning` | Conta criada, setup em andamento | Limitado (só tela de "configurando sua conta...") |
| `active` | Provisioning concluído | Total |
| `provisioning_failed` | Provisioning falhou após N tentativas | Suporte humano necessário |

### Regras de Implementação

- **Idempotência obrigatória:** o worker pode reprocessar o evento — cada passo verifica se já foi feito antes de executar
- **Retry com backoff:** 1s, 5s, 30s, 5min, 1h — desiste após 6 tentativas e seta `provisioning_failed`
- **Timeout por etapa:** cada operação externa tem timeout individual (não deixe Stripe segurar o worker indefinidamente)
- **Feedback em tempo real:** o frontend faz polling de `/tenants/me/status` até o status ser `active`
- **Never block signup:** se o provisioning falhar, o tenant deve conseguir entrar em contato com o suporte — não apenas ver uma tela de erro

### Interface do Worker

```typescript
// application/jobs/provision-tenant.job.ts
class ProvisionTenantJob {
  async execute(event: TenantProvisioningRequested): Promise<void> {
    const steps: ProvisioningStep[] = [
      new RegisterOnGatewayStep(this.paymentGateway),
      new SendWelcomeEmailStep(this.mailer),
      new SetupDefaultDataStep(this.defaultDataService),
    ]

    for (const step of steps) {
      if (await step.isAlreadyDone(event.tenantId)) continue
      await step.execute(event.tenantId)
    }

    await this.tenantRepo.updateStatus(event.tenantId, TenantStatus.ACTIVE)
  }
}
```

---

## 12. Data Residency

Clientes enterprise podem exigir que seus dados sejam armazenados em uma região geográfica específica (BR, EU, US). Isso impacta onde o banco e os serviços de storage são provisionados.

### Quando implementar

Implemente Data Residency quando:
- O contrato com o cliente especificar região de armazenamento
- A regulamentação aplicável exigir (ex: dados de saúde no Brasil devem permanecer no Brasil)
- O modelo de negócio incluir clientes enterprise com exigências de compliance

Para early-stage SaaS com clientes SMB: adie. Adicione apenas a **coluna de região** no tenant para facilitar a migração futura.

### Estratégia Simples: Região por Tenant

```sql
ALTER TABLE tenants ADD COLUMN data_region VARCHAR(10) NOT NULL DEFAULT 'br-east';
-- Valores possíveis: 'br-east', 'us-east', 'eu-west'
```

O `TenantContext` passa a incluir a região, e a camada de infraestrutura roteia para o banco correto:

```typescript
interface ITenantContext {
  tenantId: TenantId
  tenantSlug: string
  plan: SubscriptionPlan
  dataRegion: DataRegion  // novo campo
}
```

### Arquitetura de Roteamento por Região

```
Request chega → Middleware de Auth → TenantContext criado com dataRegion
                                          │
                                          ▼
                                  DatabaseRouter
                                  ├── 'br-east' → pool de conexão BR
                                  ├── 'us-east' → pool de conexão US
                                  └── 'eu-west' → pool de conexão EU
```

### Restrições de Design

- **Nenhum dado cross-region:** repositórios nunca fazem query em banco diferente do `dataRegion` do TenantContext
- **Backups na mesma região:** snapshots do banco ficam na mesma região que os dados
- **Metadados centralizados:** informações de roteamento (qual tenant está em qual região) podem ficar em um banco central global — apenas os dados de negócio são regionalizados
- **Logs e traces:** verificar se o serviço de observabilidade também permite residência regional

### Checklist de Data Residency

- [ ] Coluna `data_region` na tabela `tenants`
- [ ] `DatabaseRouter` na infraestrutura roteia por `TenantContext.dataRegion`
- [ ] Testes de isolamento verificam que tenant BR não acessa pool EU
- [ ] Backups configurados na mesma região dos dados
- [ ] Contrato e política de privacidade especificam as regiões disponíveis

---

## 13. Tenant Migration / Export / Import

Mover um tenant entre ambientes (staging → produção, região BR → região EU) ou exportar dados para portabilidade LGPD/GDPR exige um padrão consistente.

### Casos de Uso

| Operação | Quando | Risco |
|---|---|---|
| **Export** | Pedido LGPD/GDPR de portabilidade; cliente pedindo backup | Baixo — apenas leitura |
| **Import** | Migrar de ambiente staging para produção | Médio — cria dados |
| **Migration** | Mover tenant entre regiões (Data Residency) | Alto — envolve dois bancos |

### Padrão: Export

```typescript
// application/use-cases/export-tenant-data.use-case.ts
class ExportTenantDataUseCase {
  async execute(tenantId: TenantId): Promise<TenantExport> {
    // Coleta dados de todos os bounded contexts do tenant
    // Inclui todos os campos marcados com @pii
    // Gera JSON estruturado por bounded context
    // Registra AuditLog com action: 'export'
    return {
      exportedAt: new Date(),
      tenantId: tenantId.value,
      data: {
        auth: await this.authRepo.exportForTenant(tenantId),
        billing: await this.billingRepo.exportForTenant(tenantId),
        // ... demais bounded contexts
      }
    }
  }
}
```

**Regras do Export:**
- Sempre registra `AuditLog` com `action: 'export'`
- Inclui todos os campos PII sem anonimização (é para o próprio tenant)
- Retorna JSON estruturado — nunca SQL dump direto
- Export assíncrono para tenants com muitos dados: usa job + notificação por e-mail quando pronto

### Padrão: Tenant Migration entre Regiões

```
1. Cria snapshot dos dados do tenant na região de origem (Export)
2. Seta tenant.status = 'migrating' (bloqueia escrita durante migração)
3. Importa snapshot na região de destino
4. Verifica integridade: contagem de registros por entidade
5. Atualiza tenant.data_region = nova_região
6. Seta tenant.status = 'active'
7. Remove dados da região de origem (com AuditLog)
```

**Cuidados:**
- A janela de migração (status `migrating`) deve ser de minutos, não horas — planeje o tempo de cada etapa
- Comunicar o tenant com antecedência sobre a janela de indisponibilidade
- Manter rollback: se a etapa 4 falhar, o tenant continua na região original
- Nunca deletar dados da origem antes de confirmar integridade no destino

### Interface de Repositório para Export

Cada repositório de domínio deve implementar o método de export:

```typescript
interface ISubscriptionRepository {
  // ... métodos existentes ...
  exportForTenant(tenantId: TenantId): Promise<SubscriptionExportData[]>
}
```

O método `exportForTenant` retorna todos os dados do tenant sem paginação — é para export completo, não para listagem de UI.

---

## 9. Eventos de Domínio SaaS — Referência

Além dos eventos de Subscription (seção 3), eventos comuns em SaaS:

| Evento | Domínio | Payload mínimo |
|---|---|---|
| `TenantCreated` | tenant | tenantId, plan, ownerEmail |
| `TenantSuspended` | tenant | tenantId, reason |
| `UserInvited` | auth | tenantId, inviteeEmail, role |
| `UserJoined` | auth | tenantId, userId |
| `UserRemoved` | auth | tenantId, userId |
| `InvoiceIssued` | billing | tenantId, invoiceId, amount |
| `InvoicePaid` | billing | tenantId, invoiceId, paidAt |
| `InvoiceOverdue` | billing | tenantId, invoiceId, dueDate |
| `PlanUpgraded` | billing | tenantId, fromPlan, toPlan |
| `PlanDowngraded` | billing | tenantId, fromPlan, toPlan |
| `DataExportRequested` | compliance | tenantId, requestedBy |
| `DataDeleted` | compliance | tenantId, deletedBy, scope |
