# E2E Tests

> Excerto temático de `TESTING_GUIDE.md` (fonte completa) — seção 2.6.

**O que testar:** happy path dos fluxos de negócio críticos (ex: criar conta → assinar plano → pagar → cancelar), fluxos que cruzam múltiplos bounded contexts, fluxos com integrações externas (use sandbox/mock do gateway).

**O que NÃO testar em E2E:** todos os cenários de erro (use integration), lógica de negócio detalhada (use unit), performance (use ferramentas específicas).

```
tests/e2e/
├── subscription-lifecycle.test.ts
└── onboarding-flow.test.ts
```
