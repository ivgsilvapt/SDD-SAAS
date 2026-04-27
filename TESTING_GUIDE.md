# TESTING_GUIDE.md

Guia de estratégia de testes para projetos com Clean Architecture + DDD + SaaS.
Complementa `ARCHITECTURE.md` (seções 14 e 5).

---

## Usando @harness/test-helpers (harness v2.0+)

O harness fornece helpers de teste prontos em `harness/lib/test-helpers/`. **Não reimplemente** `InMemoryRepository`, builders ou fakes — importe do harness.

### Instalação (Node.js)
```typescript
// package.json (devDependencies)
"@harness/test-helpers": "file:path/to/sdd-saas/harness/lib/test-helpers/node"

// ou, após publicar no npm privado:
"@harness/test-helpers": "^2.0.0"
```

### Uso
```typescript
import { createInMemoryRepository, aTenant, FakeMailer } from '@harness/test-helpers';

// Repositório in-memory com isolamento automático por tenantId
const subscriptionRepo = createInMemoryRepository<Subscription>();
const tenant = aTenant().withPlan('pro').build();

// FakeMailer — captura emails sem SMTP
const mailer = new FakeMailer();
await mailer.send({ to: 'user@test.com', subject: 'Welcome' });
mailer.assertSentTo('user@test.com');

// Reset entre testes
afterEach(() => {
  subscriptionRepo._reset();
  mailer.clear();
});
```

### Instalação (Python)
```python
# pyproject.toml (dev dependencies)
"harness-test-helpers @ {root}/path/to/sdd-saas/harness/lib/test-helpers/python"

# Uso:
from harness_test_helpers import create_in_memory_repository, a_tenant, FakeMailer

repo = create_in_memory_repository()
tenant = a_tenant().with_plan("pro").build()
mailer = FakeMailer()
```

### Por que isso importa
Bug clássico de multi-tenant em testes: `InMemorySubscriptionRepository.findById(id)` retorna a entidade **sem** verificar `tenantId`. O `createInMemoryRepository` do harness sempre verifica `tenantId` — o bug é impossível por design.

---

## 0. TDD — Mecanismo de Execução dentro do SPRINT

TDD é o mecanismo que transforma os cenários Given-When-Then do SPEC em código verificável. Para cada cenário GWT, aplique o ciclo:

### Ciclo Red → Green → Refactor

```
[RED]      Escreva um teste que falha — cobre exatamente um cenário GWT do FR atual
[GREEN]    Escreva a implementação mínima para o teste passar — sem código extra (YAGNI)
[REFACTOR] Limpe o código (nomes, extração, simplificação) sem quebrar o teste
           ↳ Repita para o próximo cenário GWT
```

### Onde aplicar TDD por camada

| Camada | TDD aplicável? | Observação |
|---|---|---|
| Domain (entidades, value objects) | **Sim — obrigatório** | Zero dependências externas — ciclo instantâneo |
| Application (use cases) | **Sim — obrigatório** | Use InMemoryRepository como colaborador |
| Infrastructure (repositórios) | Opcional | Setup de banco real dificulta o ciclo — testes gerados pelo Agente Testing |
| Presentation (controllers) | Opcional | Setup de HTTP client dificulta o ciclo — testes gerados pelo Agente Testing |

### Regra fundamental

> Não escreva código de produção para um cenário GWT sem ter um teste falhando que o justifique.

---

## 1. Pirâmide de Testes

```
            /\
           /  \
          / E2E \           ← Poucos (5–10% do total)
         /--------\           Happy path + fluxos críticos de negócio
        /Integration\       ← Médio (20–30%)
       /   Tests     \        Repositórios reais, endpoints, serviços externos
      /--------------\
     /  Unit  Tests   \     ← Maioria (60–70%)
    /                  \      Domínio puro, use cases com repositórios em memória
   /____________________\
```

**Regra:** Quanto mais alto na pirâmide, mais lento e mais caro. Prefira unitários para lógica de negócio; use integração apenas para validar fronteiras; use e2e apenas para fluxos críticos.

---

## 2. Tipos de Teste por Camada

### 2.1 Unit Tests — Domain

**O que testar:**
- Invariantes de entidades (regras que nunca devem ser violadas)
- Validações de Value Objects
- Transições de estado válidas e inválidas
- Regras de negócio em Domain Services
- Lógica de Aggregate Roots

**O que NÃO testar:**
- Construtores simples sem lógica
- Getters/setters triviais
- Mapeamentos ORM

**Exemplo de nomenclatura:**
```
Subscription_Cancel_ShouldTransitionToCanceledStatus
Subscription_Cancel_WhenAlreadyCanceled_ShouldReturnError
Email_WhenInvalidFormat_ShouldThrowValidationError
Subscription_Activate_WhenTrialExpired_ShouldRequirePaymentMethod
```

**Estrutura:**
```
tests/unit/domain/
├── entities/
│   ├── subscription.test.ts
│   └── invoice.test.ts
└── value-objects/
    ├── email.test.ts
    └── money.test.ts
```

**Dependências:** Nenhuma. O domínio não tem dependências externas — teste-o diretamente, sem mocks.

---

### 2.2 Unit Tests — Application

**O que testar:**
- Orquestração do Use Case: chama o repositório correto? Emite o evento certo? Retorna o resultado esperado?
- Casos de sucesso e de falha por cenário GWT do SPEC

**O que NÃO testar:**
- Lógica de negócio (pertence ao domínio)
- Queries SQL ou comportamento do banco

**Estratégia de mocking:**
Use um **InMemoryRepository** — uma implementação concreta em memória da interface de repositório do domínio. Nunca use um mock de framework para repositórios em testes de application.

```
// Exemplo: InMemorySubscriptionRepository implementa ISubscriptionRepository
// Armazena entidades em um Map em memória
// Usado exclusivamente em tests/unit/application/ e tests/unit/domain/
```

**Estrutura:**
```
tests/unit/application/
├── commands/
│   ├── cancel-subscription.test.ts
│   └── create-subscription.test.ts
└── queries/
    └── list-invoices.test.ts
```

---

### 2.3 Integration Tests — Infrastructure

**O que testar:**
- Repositórios concretos contra banco de dados de teste real
- Mapeamento ORM (persistência e recuperação de entidades)
- Queries com filtros, ordenação, paginação
- Que o TenantId está sendo filtrado corretamente
- Migrations executadas corretamente (schema antes e depois)

**Setup:**
- Use um banco de dados de teste isolado (em container Docker ou em memória, ex: SQLite para testes)
- Limpe o banco entre testes (transaction rollback ou truncate)
- Nunca use o banco de desenvolvimento

**Estrutura:**
```
tests/integration/infrastructure/
├── repositories/
│   ├── subscription-repository.test.ts
│   └── invoice-repository.test.ts
└── migrations/
    └── 20250115_create_subscriptions.test.ts
```

---

### 2.4 Integration Tests — Presentation

**O que testar:**
- Endpoints: status HTTP correto para cada cenário
- Corpo da resposta: campos esperados, formato do envelope
- Autenticação: 401 sem token, 403 sem permissão
- Validação de input: 400/422 para dados inválidos
- Que o controller chama o use case correto

**Setup:**
- Use um test client HTTP (sem subir servidor real)
- Mocke o Use Case (não o repositório) — você está testando a apresentação, não o domínio
- Use tokens JWT de teste com tenantId e userId fixos

**Estrutura:**
```
tests/integration/presentation/
├── subscriptions.controller.test.ts
└── invoices.controller.test.ts
```

---

### 2.5 Unit Tests — Application Jobs

**O que testar:**
- Idempotência: job não reprocessa tenant já processado no período
- Isolamento de falha: erro em um tenant não interrompe os demais
- Que o job chama os use cases corretos com o TenantContext correto
- Comportamento com zero tenants ativos

**O que NÃO testar:**
- Scheduler (cron) — é configuração de infraestrutura
- Lógica de negócio (pertence ao domínio — testada em unit tests de domain)

**Estratégia de mocking:**
- InMemoryTenantRepository para simular lista de tenants
- Mock do serviço chamado pelo job (InMemoryRepository ou mock de framework)
- FakeTenantContextFactory que cria contextos de teste

**Nomenclatura:**
```
RenewSubscriptionsJob_Execute_WhenTenantAlreadyRenewed_ShouldSkip
RenewSubscriptionsJob_Execute_WhenOneTenantFails_ShouldContinueOthers
RenewSubscriptionsJob_Execute_WithNoActiveTenants_ShouldDoNothing
```

**Estrutura:**
```
tests/unit/application/
└── jobs/
    ├── renew-subscriptions.job.test.ts
    └── generate-monthly-invoices.job.test.ts
```

---

### 2.6 E2E Tests

**O que testar:**
- Happy path dos fluxos de negócio críticos (ex: criar conta → assinar plano → pagar → cancelar)
- Fluxos que cruzam múltiplos bounded contexts
- Fluxos com integrações externas (use sandbox/mock do gateway)

**O que NÃO testar em E2E:**
- Todos os cenários de erro (use integration para isso)
- Lógica de negócio detalhada (use unit para isso)
- Performance (use ferramentas específicas)

**Estrutura:**
```
tests/e2e/
├── subscription-lifecycle.test.ts
└── onboarding-flow.test.ts
```

---

## 3. Mocking — Estratégia e Regras

### O que mockar

| Fronteira | Estratégia | Onde usar |
|---|---|---|
| Repository interfaces (domínio) | InMemoryRepository (classe concreta) | Unit tests de application |
| Repository interfaces (domínio) | Mock do framework | Integration tests de presentation |
| Serviços externos (mail, pagamento) | Mock do framework | Unit tests de application e integration |
| Use Cases | Mock do framework | Integration tests de presentation |
| Entidades de domínio | **Nunca mockar** | — |
| Value Objects | **Nunca mockar** | — |

### Regra fundamental
**Mocke na fronteira da arquitetura, nunca dentro dela.**

```
// CORRETO: mockar a interface do repositório
const repo = new InMemorySubscriptionRepository()
const useCase = new CancelSubscriptionUseCase(repo, mockEventBus)

// ERRADO: mockar uma entidade de domínio
const subscription = mock<Subscription>() // nunca faça isso
```

### InMemoryRepository
Cada domínio deve ter seus InMemoryRepositories em `tests/helpers/`:
```
tests/helpers/
├── in-memory-subscription-repository.ts
├── in-memory-invoice-repository.ts
└── fake-mailer.ts
```

Regras para InMemoryRepository:
- Implementa a mesma interface do repositório real
- Armazena entidades em `Map<id, Entity>`
- Filtra por `tenantId` (o comportamento de isolamento deve ser testado também)
- Suporta todos os métodos da interface

---

## 4. Nomenclatura de Testes

### Padrão
```
[UnidadeSobTeste]_[Cenário]_[ComportamentoEsperado]
```

### Exemplos

```
// Domínio
Subscription_Cancel_ShouldReturnCanceledStatus
Subscription_Cancel_WhenAlreadyCanceled_ShouldReturnBusinessError
Invoice_MarkAsPaid_WhenAlreadyPaid_ShouldReturnConflictError
Email_WhenFormatInvalid_ShouldThrowValidationError
Money_WhenNegativeAmount_ShouldThrowInvariantViolation

// Application
CancelSubscriptionUseCase_Execute_ShouldPersistCanceledSubscription
CancelSubscriptionUseCase_Execute_WhenSubscriptionNotFound_ShouldReturnNotFoundError
CancelSubscriptionUseCase_Execute_ShouldEmitSubscriptionCanceledEvent

// Presentation
POST_subscriptions_cancel_ShouldReturn200
POST_subscriptions_cancel_WithoutToken_ShouldReturn401
POST_subscriptions_cancel_WithInvalidId_ShouldReturn404
```

---

## 5. Mapeamento SPEC → Testes

> **TDD:** Este mapeamento define o teste que deve ser escrito **antes** da implementação do FR. O cenário GWT é o contrato — o teste falhando é a primeira implementação do contrato.

Cada cenário Given-When-Then do SPEC deve gerar pelo menos 1 teste:

```
// SPEC — FR-003, Cenário principal:
// Dado que existe uma assinatura ativa
// Quando o usuário solicita o cancelamento
// Então a assinatura deve transitar para o estado "cancelada"

// Teste correspondente:
test('Subscription_Cancel_WhenActive_ShouldTransitionToCanceled', () => {
  // Arrange (Given)
  const subscription = Subscription.create({ status: 'active', ... })

  // Act (When)
  const result = subscription.cancel()

  // Assert (Then)
  expect(result.isOk()).toBe(true)
  expect(subscription.status).toBe('canceled')
})
```

**Regra:** Se um cenário GWT não tem teste correspondente, o SPRINT não está completo. O Agente Testing verifica esta cobertura.

---

## 6. Dados de Teste

### Builders / Factories
Use builder pattern para criar objetos de teste sem repetição:

```
// tests/helpers/builders/subscription-builder.ts
class SubscriptionBuilder {
  private props = defaultSubscriptionProps()

  withStatus(status: SubscriptionStatus): this {
    this.props.status = status
    return this
  }

  withTenantId(tenantId: string): this {
    this.props.tenantId = tenantId
    return this
  }

  build(): Subscription {
    return Subscription.create(this.props)
  }
}
```

### Fixtures
Para dados complexos e recorrentes, use fixtures em `tests/fixtures/`:
```
tests/fixtures/
├── tenants.ts
├── subscriptions.ts
└── invoices.ts
```

### Regras de dados de teste
- Nunca use dados de produção em testes
- Nunca use IDs hardcoded compartilhados entre testes — gere-os por teste
- Sempre use `tenantId` de teste diferente do padrão para testes de isolamento

---

## 7. Testes de Migrations

Para cada migration que altera tabelas existentes:

```
// 1. Verifica estado do schema ANTES da migration
// 2. Executa a migration
// 3. Verifica estado do schema APÓS a migration
// 4. (Opcional) Verifica que dados existentes foram preservados/migrados corretamente
```

Migrations de criação de tabela: basta verificar que a tabela existe com as colunas corretas.
Migrations de alteração: verificar o comportamento dos dados existentes após a alteração.

---

## 8. Anti-patterns de Testes

| Anti-pattern | Por que evitar | Alternativa |
|---|---|---|
| Mockar entidades de domínio | Esconde bugs de lógica de negócio | Use instâncias reais |
| Testar implementação interna | Teste frágil — quebra com refactor | Teste comportamento observável |
| Teste que testa tudo junto | Difícil de diagnosticar | Um cenário por teste |
| Setup global compartilhado | Acoplamento entre testes | Setup local por teste ou suite |
| Assert em múltiplos comportamentos | Falha ambígua | Um comportamento por assert |
| Ignorar o cenário de erro | Deixa bugs de path alternativo | Teste sempre sucesso E falha |
| Banco de desenvolvimento em testes | Dados poluídos, falsos positivos | Banco isolado ou em memória |

---

## 9. Cobertura de Testes

### Metas por camada

| Camada | Cobertura mínima |
|---|---|
| Domain (entities, value objects) | 90%+ |
| Application (use cases) | 85%+ |
| Application (jobs) | 80%+ (cenários de idempotência e isolamento obrigatórios) |
| Infrastructure (repositories) | 70%+ (queries críticas 100%) |
| Presentation (controllers) | 80%+ |

### O que NÃO medir por cobertura de linha
- Cobertura de linha não garante qualidade. Meça também:
  - Cenários GWT cobertos (rastreabilidade SPEC → teste)
  - Caminhos de erro testados
  - Invariantes de domínio validadas

---

## 10. Property-Based Testing *(opcional — recomendado para domínio crítico)*

Property-based testing complementa os testes baseados em exemplos (GWT) ao gerar **centenas de inputs aleatórios** e verificar que uma propriedade invariante sempre vale — não apenas para os casos que o desenvolvedor imaginou.

### Quando usar

Use property-based testing para:
- **Value Objects** com regras de validação: `Email`, `CPF`, `Money`, `Percentage`
- **Cálculos financeiros**: totais de fatura, cálculo de desconto, rateio, arredondamento
- **Transformações com reversibilidade**: serialização/deserialização, codificação/decodificação
- **Operações comutativas ou associativas**: soma de Money, merge de permissões

**Não use** para:
- Controllers e repositórios (property testing não se aplica a I/O)
- Lógica de estado com muitas dependências (difícil de compor)
- Cenários que já têm exemplos suficientes e nenhum input inesperado é possível

### Ferramentas recomendadas

| Linguagem | Biblioteca |
|---|---|
| TypeScript / JavaScript | `fast-check` |
| Python | `hypothesis` |
| Java / Kotlin | `jqwik` |
| Go | `gopter` |

### Exemplo — TypeScript com fast-check

```typescript
import * as fc from 'fast-check'
import { Money } from '@/domain/billing/value-objects/money'

// Propriedade: somar Money e depois subtrair o mesmo valor retorna o original
test('Money_Add_ThenSubtract_ShouldReturnOriginal', () => {
  fc.assert(
    fc.property(
      fc.integer({ min: 1, max: 1_000_000 }), // centavos
      fc.integer({ min: 1, max: 1_000_000 }),  // centavos a somar
      (original, addition) => {
        const m1 = Money.ofCents(original)
        const m2 = Money.ofCents(addition)
        const result = m1.add(m2).subtract(m2)
        return result.equals(m1)
      }
    )
  )
})

// Propriedade: Money negativo sempre falha na criação
test('Money_WithNegativeAmount_ShouldAlwaysFailValidation', () => {
  fc.assert(
    fc.property(
      fc.integer({ max: -1 }),
      (negativeAmount) => {
        const result = Money.ofCents(negativeAmount)
        return result.isErr()
      }
    )
  )
})
```

### Localização dos testes

```
tests/unit/domain/
├── value-objects/
│   ├── email.test.ts           ← testes GWT + property
│   ├── money.property.test.ts  ← property-based dedicado
│   └── cpf.property.test.ts
```

---

## 11. Mutation Testing *(opcional — para domínio de alto risco)*

Mutation testing mede a **qualidade dos testes** — não a quantidade de linhas cobertas.
A ferramenta altera o código de produção (introduz "mutantes") e verifica se algum teste falha.
Se nenhum teste falha com o mutante, significa que seus testes não detectariam aquele bug.

### Quando usar

Use mutation testing em código de **alto risco de bug silencioso**:
- Regras de negócio de billing (cálculo de cobrança, desconto, proration)
- Lógica de autorização (RBAC, verificação de plano, isolamento de tenant)
- Algoritmos de cálculo em Value Objects financeiros
- Máquinas de estado de entidades críticas (Subscription, Invoice)

**Não aplique rotineiramente** a todo o codebase — o custo computacional é alto.
Reserve para as partes onde um bug silencioso teria consequência financeira ou de segurança.

### Ferramentas recomendadas

| Linguagem | Ferramenta |
|---|---|
| TypeScript / JavaScript | `Stryker Mutator` |
| Python | `mutmut` ou `cosmic-ray` |
| Java | `PIT (Pitest)` |

### Exemplo de configuração — Stryker (TypeScript)

```json
// stryker.config.json
{
  "mutate": [
    "src/domain/billing/**/*.ts",
    "src/domain/auth/**/*.ts"
  ],
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

### Interpretando os resultados

| Resultado | Significado | Ação |
|---|---|---|
| Mutante **morto** | Algum teste detectou a alteração | Bom — este caminho está protegido |
| Mutante **sobrevivente** | Nenhum teste detectou | Adicione um teste que pegue este caso |
| Mutante **timeout** | Teste entrou em loop infinito | Investigue o mutante — possível loop infinito no código real |

**Meta:** ≥ 75% de mutantes mortos no domínio de billing e auth. Abaixo disso, a cobertura de linha está dando falsa sensação de segurança.
