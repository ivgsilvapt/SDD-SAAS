# Helpers — Mocking, Dados de Teste, Anti-patterns e Cobertura

> Excerto temático de `TESTING_GUIDE.md` (fonte completa) — seções harness test-helpers, 3, 6, 8, 9.

## Usando @harness/test-helpers (harness v2.0+)

O harness fornece helpers de teste prontos em `harness/lib/test-helpers/`. **Não reimplemente** `InMemoryRepository`, builders ou fakes — importe do harness.

```typescript
import { createInMemoryRepository, aTenant, FakeMailer } from '@harness/test-helpers';

const subscriptionRepo = createInMemoryRepository<Subscription>();
const tenant = aTenant().withPlan('pro').build();

const mailer = new FakeMailer();
await mailer.send({ to: 'user@test.com', subject: 'Welcome' });
mailer.assertSentTo('user@test.com');

afterEach(() => {
  subscriptionRepo._reset();
  mailer.clear();
});
```

Python: `from harness_test_helpers import create_in_memory_repository, a_tenant, FakeMailer`

**Por que isso importa:** bug clássico em testes multi-tenant é `InMemoryRepository.findById(id)` retornar a entidade sem verificar `tenantId`. O `createInMemoryRepository` do harness sempre verifica — o bug é impossível por design.

## Mocking — O Que Mockar

| Fronteira | Estratégia | Onde usar |
|---|---|---|
| Repository interfaces (domínio) | InMemoryRepository (classe concreta) | Unit tests de application |
| Repository interfaces (domínio) | Mock do framework | Integration tests de presentation |
| Serviços externos (mail, pagamento) | Mock do framework | Unit tests de application e integration |
| Use Cases | Mock do framework | Integration tests de presentation |
| Entidades de domínio | **Nunca mockar** | — |
| Value Objects | **Nunca mockar** | — |

**Regra fundamental:** mocke na fronteira da arquitetura, nunca dentro dela.

```
// CORRETO
const repo = new InMemorySubscriptionRepository()
const useCase = new CancelSubscriptionUseCase(repo, mockEventBus)

// ERRADO
const subscription = mock<Subscription>() // nunca faça isso
```

`InMemoryRepository`s ficam em `tests/helpers/`, implementam a mesma interface do repositório real, armazenam em `Map<id, Entity>`, e filtram por `tenantId` (o isolamento também deve ser testado).

## Dados de Teste — Builders e Fixtures

```typescript
// tests/helpers/builders/subscription-builder.ts
class SubscriptionBuilder {
  private props = defaultSubscriptionProps()
  withStatus(status: SubscriptionStatus): this { this.props.status = status; return this }
  withTenantId(tenantId: string): this { this.props.tenantId = tenantId; return this }
  build(): Subscription { return Subscription.create(this.props) }
}
```

Fixtures para dados complexos e recorrentes em `tests/fixtures/{tenants,subscriptions,invoices}.ts`.

**Regras:** nunca use dados de produção em testes; nunca use IDs hardcoded compartilhados entre testes; sempre use `tenantId` de teste diferente do padrão para testes de isolamento.

## Anti-patterns de Testes

| Anti-pattern | Por que evitar | Alternativa |
|---|---|---|
| Mockar entidades de domínio | Esconde bugs de lógica de negócio | Use instâncias reais |
| Testar implementação interna | Teste frágil — quebra com refactor | Teste comportamento observável |
| Teste que testa tudo junto | Difícil de diagnosticar | Um cenário por teste |
| Setup global compartilhado | Acoplamento entre testes | Setup local por teste ou suite |
| Assert em múltiplos comportamentos | Falha ambígua | Um comportamento por assert |
| Ignorar o cenário de erro | Deixa bugs de path alternativo | Teste sempre sucesso E falha |
| Banco de desenvolvimento em testes | Dados poluídos, falsos positivos | Banco isolado ou em memória |

## Cobertura de Testes

| Camada | Cobertura mínima |
|---|---|
| Domain (entities, value objects) | 90%+ |
| Application (use cases) | 85%+ |
| Application (jobs) | 80%+ (idempotência e isolamento obrigatórios) |
| Infrastructure (repositories) | 70%+ (queries críticas 100%) |
| Presentation (controllers) | 80%+ |

Cobertura de linha não garante qualidade — meça também: cenários GWT cobertos (rastreabilidade SPEC → teste), caminhos de erro testados, invariantes de domínio validadas.
