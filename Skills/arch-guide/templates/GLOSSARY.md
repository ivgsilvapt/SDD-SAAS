# GLOSSARY — [BOUNDED_CONTEXT]

**Projeto:** [nome do projeto]
**Bounded Context:** [BOUNDED_CONTEXT]
**Versão:** 1.0
**Atualizado em:** [data]

---

## Instrução para Agentes GSD2

Ao receber este arquivo (via `M###-CONTEXT.md` ou `S##-CONTEXT.md`), use **exclusivamente** os termos definidos aqui para nomear entidades, eventos, comandos, queries, value objects e serviços dentro deste bounded context.

**Se precisar de um conceito não listado:** adicione-o neste glossário antes de usá-lo no código. Nunca invente termos ad-hoc.

---

## 1. Termos do Domínio

| Termo (use no código) | Definição de negócio | Termos a EVITAR | Padrão DDD | Exemplo de uso |
|---|---|---|---|---|
| **[Termo]** | [O que significa no contexto do negócio deste contexto] | [sinônimos incorretos a evitar] | Entity / VO / Aggregate / Event | [onde aparece: `Order`, `OrderPlaced`, etc.] |
| | | | | |
| | | | | |

---

## 2. Eventos de Domínio

> Eventos que este bounded context emite (outros contextos podem ouvir).

| Evento | Quando é emitido | Dados incluídos |
|---|---|---|
| `[NomeEvento]` | [condição que dispara o evento] | [campos relevantes] |

---

## 3. Interfaces de Repositório

> Uma linha por aggregate root que precisa de persistência.

| Interface | Localização | Aggregate Root |
|---|---|---|
| `[Nome]Repository` | `src/domain/[context]/` | `[NomeEntidade]` |

---

## 4. Limites do Contexto

**Este contexto é responsável por:**
- [responsabilidade 1]
- [responsabilidade 2]

**Este contexto NÃO gerencia:**
- [o que pertence a outro contexto]

**Comunicação com outros contextos:**
- Recebe eventos de: [contextos que alimentam este]
- Emite eventos para: [contextos que dependem deste]

---

## 5. Convenções de Nomenclatura deste Contexto

| Conceito | Padrão | Exemplo |
|---|---|---|
| Entity | PascalCase, substantivo singular | `Order`, `Customer` |
| Value Object | PascalCase | `Money`, `OrderStatus` |
| Domain Event | PascalCase, passado | `OrderPlaced`, `OrderCancelled` |
| Use Case | verbo + substantivo | `CreateOrder`, `CancelOrder` |
| Repository interface | nome + `Repository` | `OrderRepository` |
| DTO | nome + `Dto` | `CreateOrderDto`, `OrderDto` |
| Error code | `CONTEXT_ENTITY_CONDITION` | `ORDERS_ORDER_NOT_FOUND` |

---

## 6. Changelog do Glossário

| Data | Mudança | Motivo | Impacto no código |
|---|---|---|---|
| [data] | [ex: Renomeado `X` para `Y`] | [alinhamento com negócio] | [arquivos afetados] |
