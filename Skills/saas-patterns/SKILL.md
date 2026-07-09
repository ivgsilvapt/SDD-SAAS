---
name: saas-patterns
description: Padrões arquiteturais para SaaS multi-tenant (isolamento de tenant, billing, feature flags, LGPD/GDPR). Use ao modelar domínio multi-tenant, assinatura/cobrança, feature flags por plano, soft delete ou conformidade de dados pessoais.
---

# saas-patterns

Roteador para os padrões de `SAAS_PATTERNS.md` (fonte completa, leitura humana). Carregue apenas a referência do tema relevante — não leia `SAAS_PATTERNS.md` inteiro por padrão.

## Roteamento

| Se a tarefa envolve... | Leia |
|---|---|
| Isolamento de tenant, `TenantContext`, rate limiting por tenant, jobs multi-tenant, provisioning, data residency, migração/export de tenant | `references/multi-tenant.md` |
| Ciclo de vida de assinatura, integração com gateway de pagamento, onboarding, eventos de domínio de billing | `references/billing.md` |
| Feature flags, rollout gradual, diferenciação por plano | `references/feature-flags.md` |
| LGPD/GDPR, PII, soft delete, anonimização, portabilidade de dados | `references/lgpd-soft-delete.md` |

## Referência Rápida (sem abrir arquivo nenhum)

- Multi-tenancy padrão: **row-level isolation** — todo repositório filtra `tenantId`; nunca como parâmetro de método, sempre via `TenantContext` injetado.
- Billing: cobrança sempre iniciada por Use Case; `Idempotency-Key` obrigatório; persista antes de confirmar ao cliente.
- Feature flags: interface `IFeatureFlagService` no domínio; implementação (banco/env/serviço externo) na infraestrutura.
- LGPD/GDPR: soft delete com `deletedAt`; nunca `DELETE` físico exceto em job de purge com auditoria.

## Quando NÃO usar

Regras gerais de arquitetura (camadas, DI, Result<T,E>) estão em `ARCHITECTURE.md` / `ARCHITECTURE_DIGEST.md` — não aqui. Este skill é específico de padrões SaaS.
