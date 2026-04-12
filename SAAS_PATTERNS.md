# SAAS_PATTERNS.md

Padrões arquiteturais específicos para SaaS. Complementa `ARCHITECTURE.md` (seção 15).
Consulte este arquivo antes de modelar qualquer domínio multi-tenant, de billing ou com feature flags.

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
