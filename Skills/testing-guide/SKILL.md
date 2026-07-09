---
name: testing-guide
description: Estratégia de testes por camada (unit de domínio/aplicação, integração de infra/presentation, e2e, mocking, builders/fixtures, cobertura). Use ao gerar ou revisar testes para um SPRINT implementado.
---

# testing-guide

Roteador para os padrões de `TESTING_GUIDE.md` (fonte completa, leitura humana). Carregue apenas a referência da camada relevante ao SPRINT atual — não leia `TESTING_GUIDE.md` inteiro por padrão.

## Roteamento

| Se o SPRINT é... | Leia |
|---|---|
| Domínio (entidades, value objects) ou Application (use cases, jobs) — TDD obrigatório | `references/unit-domain.md` |
| Infraestrutura (repositórios reais) ou Presentation (controllers, endpoints) — testes gerados após implementação | `references/integration-infra.md` |
| Fluxo de negócio completo, ponta a ponta | `references/e2e.md` |
| Dúvida sobre o que mockar, builders/fixtures, anti-patterns ou meta de cobertura | `references/helpers.md` |

## Referência Rápida (sem abrir arquivo nenhum)

- Ciclo TDD: RED (teste falha) → GREEN (implementação mínima) → REFACTOR (limpa sem quebrar).
- TDD é obrigatório em Domain e Application; opcional (mas recomendado se houver `if/else` de regra) em Infra/Presentation.
- Mocke apenas nas fronteiras da arquitetura (interfaces de repositório, serviços externos) — nunca entidades de domínio.
- Cada cenário Given-When-Then do SPEC gera pelo menos 1 teste — sem teste correspondente, o SPRINT não está completo.

## Quando NÃO usar

Regras gerais de arquitetura estão em `ARCHITECTURE.md` / `ARCHITECTURE_DIGEST.md` — não aqui. Este skill é específico de estratégia e implementação de testes.
