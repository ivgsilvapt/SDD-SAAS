# Unit Tests — Domain e Application

> Excerto temático de `TESTING_GUIDE.md` (fonte completa) — seções 0, 1, 2.1, 2.2, 2.5, 4, 5, 10, 11.

## TDD — Mecanismo de Execução dentro do SPRINT

Para cada cenário Given-When-Then do SPEC, aplique o ciclo:

```
[RED]      Escreva um teste que falha — cobre exatamente um cenário GWT do FR atual
[GREEN]    Escreva a implementação mínima para o teste passar — sem código extra (YAGNI)
[REFACTOR] Limpe o código (nomes, extração, simplificação) sem quebrar o teste
           ↳ Repita para o próximo cenário GWT
```

| Camada | TDD aplicável? | Observação |
|---|---|---|
| Domain (entidades, value objects) | **Sim — obrigatório** | Zero dependências externas — ciclo instantâneo |
| Application (use cases) | **Sim — obrigatório** | Use InMemoryRepository como colaborador |
| Infrastructure (repositórios) | Opcional | Testes gerados pelo Agente Testing após implementação |
| Presentation (controllers) | Opcional | Testes gerados pelo Agente Testing após implementação |

> Não escreva código de produção para um cenário GWT sem ter um teste falhando que o justifique.

## Pirâmide de Testes

```
E2E (5–10%) → Integration (20–30%) → Unit (60–70%)
```
Quanto mais alto na pirâmide, mais lento e mais caro. Prefira unitários para lógica de negócio.

## Unit Tests — Domain

**O que testar:** invariantes de entidades, validações de Value Objects, transições de estado válidas/inválidas, regras de negócio em Domain Services, lógica de Aggregate Roots.

**O que NÃO testar:** construtores simples sem lógica, getters/setters triviais, mapeamentos ORM.

```
Subscription_Cancel_ShouldTransitionToCanceledStatus
Subscription_Cancel_WhenAlreadyCanceled_ShouldReturnError
Email_WhenInvalidFormat_ShouldThrowValidationError
```

```
tests/unit/domain/
├── entities/{subscription,invoice}.test.ts
└── value-objects/{email,money}.test.ts
```

Dependências: nenhuma — teste o domínio diretamente, sem mocks.

## Unit Tests — Application

**O que testar:** orquestração do Use Case (repositório correto, evento certo, resultado esperado), casos de sucesso/falha por cenário GWT.

**O que NÃO testar:** lógica de negócio (pertence ao domínio), queries SQL ou comportamento do banco.

**Mocking:** use um `InMemoryRepository` — implementação concreta em memória da interface de repositório do domínio. Nunca mock de framework para repositórios em testes de application.

```
tests/unit/application/
├── commands/{cancel-subscription,create-subscription}.test.ts
└── queries/list-invoices.test.ts
```

## Unit Tests — Application Jobs

**O que testar:** idempotência (job não reprocessa tenant já processado), isolamento de falha (erro em um tenant não interrompe os demais), chamada correta ao TenantContext, comportamento com zero tenants ativos.

**O que NÃO testar:** scheduler/cron (config de infra), lógica de negócio (testada em domain).

**Mocking:** `InMemoryTenantRepository`, mock do serviço chamado pelo job, `FakeTenantContextFactory`.

```
RenewSubscriptionsJob_Execute_WhenTenantAlreadyRenewed_ShouldSkip
RenewSubscriptionsJob_Execute_WhenOneTenantFails_ShouldContinueOthers
```

## Nomenclatura de Testes

Padrão: `[UnidadeSobTeste]_[Cenário]_[ComportamentoEsperado]`

```
Subscription_Cancel_WhenAlreadyCanceled_ShouldReturnBusinessError
CancelSubscriptionUseCase_Execute_ShouldEmitSubscriptionCanceledEvent
POST_subscriptions_cancel_WithoutToken_ShouldReturn401
```

## Mapeamento SPEC → Testes

Cada cenário Given-When-Then do SPEC gera pelo menos 1 teste — é o contrato; o teste falhando é a primeira implementação dele.

```
// SPEC — FR-003: Dado assinatura ativa, quando cancelamento solicitado, então transita para "cancelada"
test('Subscription_Cancel_WhenActive_ShouldTransitionToCanceled', () => {
  const subscription = Subscription.create({ status: 'active', ... })
  const result = subscription.cancel()
  expect(result.isOk()).toBe(true)
  expect(subscription.status).toBe('canceled')
})
```

Se um cenário GWT não tem teste correspondente, o SPRINT não está completo — o Agente Testing verifica essa cobertura.

## Property-Based Testing (opcional — domínio crítico)

Gera centenas de inputs aleatórios para verificar que uma propriedade invariante sempre vale. Use para Value Objects com validação (`Email`, `CPF`, `Money`), cálculos financeiros, transformações reversíveis, operações comutativas/associativas. Não use para controllers/repositórios (I/O) ou lógica de estado com muitas dependências.

Ferramentas: `fast-check` (TS/JS), `hypothesis` (Python), `jqwik` (Java/Kotlin), `gopter` (Go).

```typescript
test('Money_Add_ThenSubtract_ShouldReturnOriginal', () => {
  fc.assert(fc.property(fc.integer({ min: 1, max: 1_000_000 }), fc.integer({ min: 1, max: 1_000_000 }),
    (original, addition) => {
      const result = Money.ofCents(original).add(Money.ofCents(addition)).subtract(Money.ofCents(addition))
      return result.equals(Money.ofCents(original))
    }))
})
```

## Mutation Testing (opcional — domínio de alto risco)

Mede a qualidade dos testes (não a cobertura de linha): altera o código de produção introduzindo "mutantes" e verifica se algum teste falha. Reserve para billing, autorização/RBAC, cálculos financeiros e máquinas de estado críticas — custo computacional alto, não aplique rotineiramente.

Ferramentas: `Stryker Mutator` (TS/JS), `mutmut`/`cosmic-ray` (Python), `PIT` (Java).

| Resultado | Significado | Ação |
|---|---|---|
| Mutante morto | Teste detectou a alteração | Bom — caminho protegido |
| Mutante sobrevivente | Nenhum teste detectou | Adicione um teste para este caso |
| Mutante timeout | Teste entrou em loop infinito | Investigue possível loop no código real |

Meta: ≥75% de mutantes mortos no domínio de billing e auth.
