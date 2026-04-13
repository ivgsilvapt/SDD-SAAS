# ARCHITECTURE.md — [NOME_DO_PROJETO]

> **Como usar este documento:**
> Cole o trecho abaixo em cada `M###-CONTEXT.md` para que os agentes GSD2 leiam esta constituição antes de planejar qualquer milestone:
>
> ```
> ## Architecture Reference
> Read `ARCHITECTURE.md` before planning. This project follows Clean Architecture + DDD.
> Read `docs/[relevant-context]/GLOSSARY.md` for canonical domain terms.
> Read `.gsd/DECISIONS.md` for prior architectural decisions.
> ```

---

## 0. Princípios Fundamentais

Este projeto segue **Clean Architecture + Domain-Driven Design (DDD)**.

**A regra central:** Dependências fluem para dentro. Camadas internas não conhecem camadas externas.

```
Presentation → Application → Domain ← Infrastructure
```

**Antes de criar qualquer arquivo, responda:**
1. A qual camada este código pertence? (domain / application / infrastructure / presentation)
2. Este código importa algo de uma camada mais externa? Se sim, mova ou refatore.
3. Existe um conceito de domínio aqui? Se sim, ele está modelado com o padrão DDD correto?
4. O termo que estou usando está no GLOSSARY.md do bounded context? Se não, adicione primeiro.

---

## 1. Regras Imperativas

### 1.1 Regras Críticas — nunca viole

**Separação de camadas:**
- Nunca importe `infrastructure/` dentro de `domain/` ou `application/`
- Nunca coloque lógica de negócio em Controller, route handler, ou ORM model
- Nunca acesse o banco de dados diretamente de um objeto de domínio
- Nunca crie a implementação de Repository antes de criar sua interface em `domain/`

**DDD:**
- Nunca exponha entidades internas de um Aggregate diretamente — passe pelo Aggregate Root
- Nunca crie entidade sem identidade (use Value Object)
- Nunca crie Value Object mutável (use `readonly` / `final` / imutabilidade da linguagem)

**Use Cases:**
- Nunca chame um Use Case de dentro de outro Use Case — use Application Service para orquestração
- Nunca retorne objetos de domínio de um Use Case — mapeie para DTO antes de retornar

### 1.2 Boas práticas — respeite sempre que possível

- Domain-First: modele o domínio antes de criar esquema de banco ou rotas HTTP
- Prefira Value Objects a strings primitivas para conceitos de negócio (`Money`, `Email`, `OrderId`)
- Emita Domain Events para mudanças de estado que outros contextos possam se importar
- Use `.gsd/DECISIONS.md` para registrar decisões arquiteturais não-óbvias
- Use `.gsd/KNOWLEDGE.md` para registrar lições aprendidas durante a implementação

---

## 2. Estrutura de Pastas

```
[NOME_DO_PROJETO]/
├── src/
│   ├── domain/              ← Entidades, VOs, Aggregates, Repository interfaces, Domain Events
│   │   └── [context]/
│   ├── application/         ← Use Cases, DTOs, Application Services
│   │   └── [context]/
│   ├── infrastructure/      ← ORM, DB, HTTP clients, adapters externos
│   │   └── [context]/
│   └── presentation/        ← Controllers, routes, request/response schemas
├── tests/
│   ├── unit/                ← domain (sem mocks) + application (repos fake)
│   ├── integration/         ← infrastructure (banco real)
│   └── e2e/                 ← presentation (servidor real)
└── docs/
    └── [context]/
        └── GLOSSARY.md      ← vocabulário canônico do bounded context
```

---

## 3. Camada Domain — `src/domain/`

**Contém:**
- **Entities:** objetos com identidade que persistem ao longo do tempo
- **Value Objects:** objetos sem identidade, definidos pelos atributos, imutáveis
- **Aggregate Roots:** fronteiras de consistência que contêm outras entidades
- **Domain Events:** registros imutáveis de algo que aconteceu (tempo passado)
- **Repository interfaces:** abstrações de coleção — sem nenhum import de ORM
- **Domain Services:** operações de domínio que não pertencem a uma única entidade

**Não contém:**
- Nenhum import de `infrastructure/`, `application/`, ou `presentation/`
- Nenhuma anotação de ORM, decorator HTTP, ou dependência de framework
- Nenhuma operação de I/O (rede, disco, console)

**Testes:** unitários puros, sem mocks (o domínio não tem dependências externas).

---

## 4. Camada Application — `src/application/`

**Contém:**
- **Use Cases:** um por operação iniciada pelo usuário ou sistema
- **DTOs:** containers de dados simples, sem lógica
- **Application Services:** orquestram múltiplos Use Cases quando necessário
- **Mappers:** transformações Domain ↔ DTO

**Não contém:**
- Nenhum import de `infrastructure/` ou `presentation/`
- Queries diretas ao banco — use Repository interfaces do `domain/`
- Lógica de negócio — pertence ao `domain/`

**Padrão de Use Case:** recebe DTO → carrega via Repository → chama métodos de domínio → salva via Repository → publica Domain Events → retorna DTO.

**Testes:** unitários com Repository mockado (fake in-memory).

---

## 5. Camada Infrastructure — `src/infrastructure/`

**Contém:**
- Implementações de Repository (implementam interfaces do `domain/`)
- Models de ORM e mapeamentos
- Migrations de banco de dados
- HTTP clients para APIs externas
- Adapters de file system, email, SMS, cache, filas

**Não contém:**
- Lógica de negócio — se você tem um if/else que representa uma regra, mova para `domain/`
- Orquestração de Use Cases — pertence a `application/`

**Inversão de dependência:** Infrastructure depende de Domain (não o contrário). Implementa interfaces definidas no domínio.

**Testes:** integração com dependências reais (banco real, HTTP real).

---

## 6. Camada Presentation — `src/presentation/`

**Contém:**
- HTTP Controllers / route handlers
- Definição de rotas
- Schemas de request/response (validação, serialização)
- Middleware de entrada (autenticação, rate limiting, logging)
- WebSocket handlers, CLI commands, GraphQL resolvers

**Não contém:**
- Lógica de negócio — controllers chamam Use Cases, nada mais
- Acesso direto a Repository — sempre passe por Use Cases
- Objetos de domínio nas respostas — mapeie para DTO/schema primeiro

**Padrão:** recebe input → valida → chama Use Case → mapeia resultado → retorna resposta.

**Testes:** integração/E2E com servidor real.

---

## 7. Padrões DDD — Referência Rápida

| Conceito | Localização | Identidade | Mutável | Exemplo |
|---|---|---|---|---|
| Entity | `domain/` | Sim | Sim | `Order`, `Customer` |
| Value Object | `domain/` | Não | Não | `Money`, `EmailAddress` |
| Aggregate Root | `domain/` | Sim (root) | Sim | `Order` (root do aggregate) |
| Domain Event | `domain/events/` | Não | Não | `OrderPlaced`, `UserCreated` |
| Repository interface | `domain/` | — | — | `OrderRepository` |
| Repository impl | `infrastructure/` | — | — | `PrismaOrderRepository` |
| Use Case | `application/` | — | — | `CreateOrder`, `CancelSubscription` |
| DTO | `application/` | — | — | `CreateOrderDto`, `OrderResponseDto` |

---

## 8. Estratégia de Testes

| Camada | Tipo de teste | Dependências | Velocidade |
|---|---|---|---|
| Domain | Unitário puro | Nenhuma | Muito rápido |
| Application | Unitário com fake repo | Fake/in-memory | Rápido |
| Infrastructure | Integração | Banco real | Médio |
| Presentation | E2E / Integração HTTP | Servidor real + banco | Lento |

**Proporção sugerida:** ~60% unitários (domain + application), ~30% integração (infra), ~10% E2E (presentation).

---

## 9. Convenções de Nomenclatura

| Conceito | Sufixo | Exemplo |
|---|---|---|
| Entity | (nenhum) | `Order`, `Customer` |
| Value Object | (nenhum ou descritivo) | `Money`, `Email` |
| Aggregate Root | (nenhum) | `Order` |
| Repository interface | `Repository` | `OrderRepository` |
| Repository impl | prefixo tecnologia | `PrismaOrderRepository` |
| Use Case | verbo + substantivo | `CreateOrder`, `CancelSubscription` |
| Domain Event | tempo passado | `OrderPlaced`, `SubscriptionCancelled` |
| Domain Service | substantivo + `Service` | `PricingService` |
| DTO | `Dto` | `CreateOrderDto` |
| Controller | `Controller` | `OrderController` |

---

## 10. Convenções de Commit (GSD2)

Este projeto usa o padrão de commits do GSD2:

```
{type}(S01/T02): descrição em uma linha

Layer: domain | application | infrastructure | presentation
Context: [bounded-context]
```

**Tipos:** `feat`, `fix`, `test`, `refactor`, `docs`, `perf`, `chore`

**Trailers opcionais (recomendados para trabalho arquitetural):**
- `Layer:` — qual camada foi modificada
- `Context:` — qual bounded context

**Exemplos:**
```
feat(S01/T01): add Order entity with invariants

Layer: domain
Context: orders

feat(S01/T02): add PrismaOrderRepository

Layer: infrastructure
Context: orders
```

---

## 11. Tecnologias deste Projeto

- **Linguagem:** [LINGUAGEM]
- **Framework:** [FRAMEWORK]
- **ORM:** [ORM]
- **Banco:** [BANCO]
- **Testes:** [TEST_RUNNER]

---

## 12. Bounded Contexts

[BOUNDED_CONTEXTS]

Cada bounded context tem seu GLOSSARY.md em `docs/[context]/GLOSSARY.md`.
Use **somente** os termos definidos no GLOSSARY.md ao nomear entidades, métodos e variáveis dentro daquele contexto.

---

## 13. Decisões e Lições Acumuladas

Todas as decisões arquiteturais estão em `.gsd/DECISIONS.md`.
Todas as lições aprendidas estão em `.gsd/KNOWLEDGE.md`.
Estes são os registros canônicos — consulte-os antes de tomar decisões não-óbvias.
