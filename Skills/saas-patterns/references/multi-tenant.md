# Multi-Tenant — Isolamento, Contexto e Operação

> Excerto temático de `SAAS_PATTERNS.md` (fonte completa) — seções: harness saas-core, 1, 1.1, 1.2, 1.3, 2, 8, 10, 11, 12, 13.

## Usando @harness/saas-core (harness v2.0+)

O harness fornece primitivas multi-tenant prontas em `harness/lib/saas-core/`. **Não reimplemente** TenantContext, TenantAwareEntity ou TenantAwareRepository — importe do harness.

```typescript
import {
  TenantAwareEntity,
  TenantAwareRepository,
  TenantContext,
  tenantMiddleware,
} from '@harness/saas-core';

class Subscription extends TenantAwareEntity {
  constructor(id: string, tenantId: string, public readonly plan: string) {
    super(id, tenantId);
  }
}

class PrismaSubscriptionRepository extends TenantAwareRepository<Subscription> {
  async findById(id: string): Promise<Subscription | null> {
    const tenantId = this.currentTenantId; // automático
    const row = await prisma.subscription.findFirst({ where: { id, tenantId } });
    return row ? new Subscription(row.id, row.tenantId, row.plan) : null;
  }
}

app.use(tenantMiddleware); // extrai tenant_id do JWT
```

Python: `from harness_saas_core import TenantAwareEntity, TenantAwareRepository, TenantContext, require_tenant`

**Por que isso importa:** bug clássico de multi-tenant é repositório sem filtro `tenantId` retornando dados de outro tenant. Com `TenantAwareRepository`, `currentTenantId` está sempre disponível e o filtro é estruturalmente obrigatório.

## Estratégias de Isolamento

| Estratégia | Como funciona | Isolamento | Custo operacional | Quando usar |
|---|---|---|---|---|
| **Row-level isolation** | Todos os tenants no mesmo banco, `tenantId` em cada linha | Médio (app-level) | Baixo | Maioria dos SaaS — padrão recomendado |
| **Schema-per-tenant** | Um schema por tenant no mesmo banco | Alto (DB-level) | Médio | Quando compliance exige separação lógica |
| **Database-per-tenant** | Um banco por tenant | Muito alto | Alto | Regulamentação estrita, clientes enterprise |

**Recomendação padrão:** Row-level isolation com `tenantId` em todas as tabelas.

## Row-Level Isolation — Implementação

**Regra:** todo repositório filtra `tenantId` em toda query, sem exceção.

```sql
CREATE TABLE subscriptions (
  id          UUID PRIMARY KEY,
  tenant_id   UUID NOT NULL REFERENCES tenants(id),
  ...
  created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_subscriptions_tenant_id ON subscriptions(tenant_id);
```

```
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

## TenantContext — Propagação pela Arquitetura

```
HTTP Request → Middleware Auth (extrai tenantId do JWT, subdomínio ou header X-Tenant-Id)
  → TenantContext registrado no container DI (escopo: requisição)
  → Use Case recebe TenantContext via construtor (DI)
  → Repository recebe TenantContext via construtor (DI), filtra toda query
  → Dados do tenant retornados
```

```
interface ITenantContext {
  tenantId: TenantId
  tenantSlug: string
  plan: SubscriptionPlan
}
```

**Regras:** TenantContext é sempre read-only após criação no middleware; tenantId nunca é parâmetro de método; operações administrativas usam um `SystemTenantContext` especial com bypass documentado.

## Checklist de Isolamento de Tenant

- [ ] Toda query inclui filtro por `tenantId`?
- [ ] TenantContext é injetado via DI, não lido de variável global?
- [ ] Nenhum endpoint retorna dados de múltiplos tenants sem autorização explícita de admin?
- [ ] Operações de escrita verificam que o recurso pertence ao tenant antes de modificar?
- [ ] Testes de repositório incluem teste de isolamento (tenant A não acessa dados do tenant B)?

## Modelo de Domínio — Tenant e Workspace

```
Tenant (Aggregate Root)
├── id: TenantId
├── slug: TenantSlug
├── name: string
├── status: TenantStatus   ← active | suspended | churned
├── plan: SubscriptionPlan
└── settings: TenantSettings

Workspace (opcional)
├── id: WorkspaceId
├── tenantId: TenantId
├── name: string
└── members: WorkspaceMember[]
```

## Rate Limiting por Tenant

| Dimensão | Exemplo | Onde implementar |
|---|---|---|
| Por tenant + endpoint | 100 req/min para `/api/v1/invoices` | Middleware de rate limit |
| Por plano | Free: 1.000 req/dia; Pro: 100.000 req/dia | Middleware com lookup de plano |
| Por feature | 10 exports/hora | Use Case com verificação de quota |

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1705312800
```

Limite excedido → HTTP 429 com `Retry-After` e error code `RATE_LIMIT_EXCEEDED`.

## Background Jobs — Padrões Multi-Tenant

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
    }
  }
}
```

| Regra | Detalhe |
|---|---|
| Nunca processe sem TenantContext | Mesmo em jobs, injete/construa um TenantContext por iteração |
| Idempotência por tenant | Job deve poder ser reexecutado para um tenant sem duplicar efeitos |
| Falha isolada por tenant | Erro em um tenant não interrompe os demais — try/catch por iteração |
| Log com tenantId | Todo log de execução inclui `tenantId` e `jobName` |
| Sem processamento cruzado | Repositórios sempre filtram por `tenantId` do TenantContext atual |

Jobs comuns: `RenewSubscriptionsJob` (diário), `GenerateMonthlyInvoicesJob` (mensal), `SendPaymentReminderJob` (diário), `PurgeExpiredDataJob` (semanal), `OutboxWorkerJob` (contínuo).

## Tenant Provisioning Queue

Onboarding síncrono (INSERT + Stripe + e-mail + setup) custa 400ms–1.6s e qualquer falha externa quebra o cadastro. Solução: provisioning assíncrono.

```
POST /signup → INSERT tenant (status: provisioning) + TenantProvisioningRequested no Outbox → 201 imediato (<100ms)

Worker (async) consome TenantProvisioningRequested:
  RegisterOnStripe (retry) → SendWelcomeEmail (retry) → SetupDefaultData
  → UPDATE tenant (status: active) + TenantProvisioned no Outbox
```

Estados: `provisioning` (acesso limitado) → `active` (total) ou `provisioning_failed` (suporte humano necessário).

Regras: idempotência obrigatória (cada passo verifica se já foi feito); retry com backoff 1s/5s/30s/5min/1h, desiste após 6 tentativas; timeout por etapa; frontend faz polling de `/tenants/me/status`; nunca bloqueie o signup em caso de falha.

## Data Residency

Implemente quando o contrato ou regulamentação exigir região específica de armazenamento; para early-stage SMB, adie e apenas adicione a coluna de região.

```sql
ALTER TABLE tenants ADD COLUMN data_region VARCHAR(10) NOT NULL DEFAULT 'br-east';
```

`TenantContext` passa a incluir `dataRegion`; a infraestrutura roteia via `DatabaseRouter` por região. Restrições: nenhum dado cross-region, backups na mesma região, metadados de roteamento podem ser centralizados.

## Tenant Migration / Export / Import

| Operação | Quando | Risco |
|---|---|---|
| **Export** | Portabilidade LGPD/GDPR, backup | Baixo — leitura |
| **Import** | Migrar staging → produção | Médio — cria dados |
| **Migration** | Mover tenant entre regiões | Alto — dois bancos |

Export: `ExportTenantDataUseCase` coleta dados de todos os BCs do tenant (incluindo campos `@pii`), registra `AuditLog action:'export'`, retorna JSON estruturado (nunca SQL dump). Migration entre regiões: snapshot → `status:migrating` (bloqueia escrita) → importa no destino → verifica integridade (contagem por entidade) → atualiza `data_region` → `status:active` → remove origem só após confirmar integridade.

Cada repositório de domínio implementa `exportForTenant(tenantId)` retornando todos os dados sem paginação.
