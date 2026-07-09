# Billing — Assinatura, Cobrança e Onboarding

> Excerto temático de `SAAS_PATTERNS.md` (fonte completa) — seções: 3, 5, 6, 9.

## Subscription Lifecycle

```
criar → trialing → (trial_expired / payment_added) → active
active → (pagamento falhou) → past_due → (pagamento ok) → active
active → (cancelamento solicitado) → cancel_at_period_end → (período expirou) → canceled
```

- `trialing`: acesso completo ou limitado sem cobrança por N dias
- `active`: assinatura paga e em dia
- `past_due`: pagamento falhou — acesso degradado, alertas, retentativas automáticas
- `cancel_at_period_end`: cancelamento solicitado, mas ativo até o fim do período pago
- `canceled`: sem acesso (ou leitura apenas, para export de dados)

### Eventos de Domínio da Assinatura

> Eventos *dentro* do mesmo BC são síncronos (dispatch no Use Case). Eventos *entre BCs* são assíncronos via Outbox (ver `ARCHITECTURE.md` §19).

| Evento | Quando disparado | Consumidores típicos | Entrega |
|---|---|---|---|
| `SubscriptionTrialStarted` | Tenant criado com trial | E-mail de boas-vindas | Outbox (async) |
| `SubscriptionActivated` | Primeiro pagamento bem-sucedido | E-mail de confirmação, unlock de features | Outbox (async) |
| `SubscriptionRenewed` | Cobrança mensal/anual bem-sucedida | E-mail de recibo | Outbox (async) |
| `SubscriptionPaymentFailed` | Cobrança falhou | E-mail de alerta, degradação de acesso | Outbox (async) |
| `SubscriptionCanceled` | Cancelamento efetivado | E-mail de confirmação, offboarding | Outbox (async) |
| `SubscriptionReactivated` | Reativação após cancelamento | E-mail de boas-vindas de volta | Outbox (async) |
| `TrialExpired` | Trial expirou sem conversão | E-mail de expiração, acesso bloqueado | Outbox (async) |

## Billing Patterns

### Modelos de Cobrança

| Modelo | Como funciona | Quando usar |
|---|---|---|
| **Flat-rate** | Valor fixo por mês/ano | Produto com valor percebido constante |
| **Seat-based** | Cobrado por usuário ativo | Ferramentas de time, colaboração |
| **Usage-based (metered)** | Cobrado por unidade consumida | Plataformas de API, infra, mensageria |
| **Hybrid** | Flat-rate + overage acima do limite | Equilíbrio previsibilidade/escalabilidade |

### Integração com Gateway de Pagamento

```typescript
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
- Use `Idempotency-Key` em toda chamada ao gateway para evitar cobranças duplicadas
- Persista o resultado da cobrança **antes** de confirmar ao cliente
- Webhooks do gateway disparam eventos de domínio — nunca chamam use cases diretamente

## Onboarding — Criação de Tenant

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

**Regra de atomicidade:** os passos 3a–3d executam em uma única transação via Unit of Work (`ARCHITECTURE.md` §7). Se qualquer passo falhar, nenhum dado é persistido. `SubscriptionTrialStarted` é persistido no Outbox na mesma transação e publicado assincronamente pelo worker.

## Eventos de Domínio SaaS — Referência Geral

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
