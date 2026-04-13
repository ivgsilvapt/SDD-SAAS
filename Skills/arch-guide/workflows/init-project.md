---
name: init-project
description: Sets up Clean Architecture + DDD structure for a GSD2 project — folders, ARCHITECTURE.md, GLOSSARY.md per bounded context, and initial DECISIONS.md entries.
---

<objective>
Set up architecture documentation and folder structure for a GSD2 project so every GSD2 agent reads and respects Clean Architecture + DDD principles during planning and implementation.
</objective>

<required_reading>
Read `references/clean-architecture.md` and `references/ddd-patterns.md` before executing this workflow.
Also load `templates/ARCHITECTURE.md` and `templates/GLOSSARY.md` — you will use them to generate project files.
</required_reading>

<intake>
Ask the user for the following before proceeding. Ask all questions in one round:

```
Para configurar a arquitetura do projeto, preciso de algumas informações:

1. Nome do projeto (ex: BillingHub, OrderFlow, TaskManager):

2. Stack tecnológico:
   - Linguagem:  TypeScript / Python / Java / Go / outro?
   - Framework:  NestJS / FastAPI / Spring / Gin / outro?
   - ORM:        Prisma / SQLAlchemy / Hibernate / GORM / outro?
   - Banco:      PostgreSQL / MySQL / MongoDB / outro?
   - Testes:     Jest / Pytest / JUnit / outro?

3. Bounded contexts (domínios do negócio):
   Liste cada bounded context com uma frase descrevendo sua responsabilidade.
   Exemplo:
   - auth — autenticação, login, sessões
   - billing — assinaturas, cobranças, planos
   - orders — pedidos, itens, fulfillment

Confirme com "ok" quando quiser prosseguir.
```

Wait for user confirmation before proceeding.
</intake>

<process>
Execute these steps in order. Do not skip steps.

**STEP 1 — Create folder structure**

Create the following directories at the project root:

```
src/domain/
src/application/
src/infrastructure/
src/presentation/
tests/unit/
tests/integration/
tests/e2e/
docs/
```

For each bounded context provided by the user, also create:
```
src/domain/[context]/
src/application/[context]/
src/infrastructure/[context]/
docs/[context]/
```

**STEP 2 — Create ARCHITECTURE.md**

Read `templates/ARCHITECTURE.md`.
Create `ARCHITECTURE.md` at the project root, replacing all `[PLACEHOLDER]` values with the information collected in intake:
- `[NOME_DO_PROJETO]` → project name
- `[LINGUAGEM]` → language
- `[FRAMEWORK]` → framework
- `[ORM]` → ORM
- `[BANCO]` → database
- `[TEST_RUNNER]` → test framework
- `[BOUNDED_CONTEXTS]` → list each context as `- nome — descrição`

**STEP 3 — Create GLOSSARY.md per bounded context**

For each bounded context:
1. Read `templates/GLOSSARY.md`
2. Create `docs/[context]/GLOSSARY.md`
3. Replace `[BOUNDED_CONTEXT]` with the context name in the header

**STEP 4 — Seed .gsd/DECISIONS.md**

If `.gsd/DECISIONS.md` does not exist, create it. If it exists, append to it.

Add the following entries (fill in the date and project name):

```markdown
## [DATE] — Adoção de Clean Architecture + DDD

**Decisão:** Este projeto segue Clean Architecture com camadas Domain, Application, Infrastructure e Presentation. Dependências fluem para dentro: Presentation → Application → Domain ← Infrastructure.

**Motivação:** Isolar regras de negócio de detalhes técnicos. O domínio não depende de framework, ORM ou banco de dados — pode ser testado em memória pura.

**Consequências:** Toda entidade de banco tem um Repository interface no domain/ e uma implementação no infrastructure/. Nenhuma lógica de negócio nos controllers.

---

## [DATE] — Modelagem DDD por Bounded Context

**Decisão:** O projeto é dividido nos bounded contexts: [BOUNDED_CONTEXTS]. Cada contexto tem sua própria pasta em domain/, application/, infrastructure/ e seu próprio GLOSSARY.md em docs/[context]/.

**Motivação:** Isolar linguagem ubíqua e modelos por contexto de negócio. Evitar que um "User" em billing signifique a mesma coisa que um "User" em auth.

**Consequências:** Termos definidos em docs/[context]/GLOSSARY.md são os termos canônicos para aquele contexto. Use somente esses termos no código do contexto correspondente.
```

**STEP 5 — Create M001-CONTEXT.md snippet**

Create a file `docs/ARCH-CONTEXT-SNIPPET.md` with content the user should paste into every future `M###-CONTEXT.md`:

```markdown
## Architecture Reference

Before planning any implementation for this milestone, read:
- `ARCHITECTURE.md` — Architecture constitution: layer rules, DDD patterns, critical violations
- `docs/[relevant-context]/GLOSSARY.md` — Canonical terms for the bounded context being worked on
- `.gsd/DECISIONS.md` — Prior architectural decisions that must be respected

This project follows Clean Architecture + DDD. The domain layer has zero external dependencies.
Dependencies flow inward: Presentation → Application → Domain ← Infrastructure.
```

Instruct the user: "Cole o conteúdo de `docs/ARCH-CONTEXT-SNIPPET.md` em cada `M###-CONTEXT.md` que você criar. Isso garante que os agentes do GSD2 leiam as regras de arquitetura antes de planejar qualquer milestone."
</process>

<confirmation>
After completing all steps, present this summary:

```
✅ Arquitetura configurada para [NOME_DO_PROJETO].

Estrutura criada:
[NOME_DO_PROJETO]/
├── src/
│   ├── domain/          ← entidades, VOs, interfaces de repositório, eventos
│   │   └── [contexts]/
│   ├── application/     ← use cases, DTOs, application services
│   │   └── [contexts]/
│   ├── infrastructure/  ← ORM, DB, HTTP clients, external services
│   │   └── [contexts]/
│   └── presentation/    ← controllers, routes, request/response schemas
├── tests/
│   ├── unit/            ← testes de domain (sem mocks de infra)
│   ├── integration/     ← testes de infrastructure (banco real)
│   └── e2e/             ← testes de presentation (servidor real)
├── docs/
│   └── [contexts]/
│       └── GLOSSARY.md  ← vocabulário canônico do bounded context
│   └── ARCH-CONTEXT-SNIPPET.md  ← cole em todo M###-CONTEXT.md
├── ARCHITECTURE.md      ← constituição do projeto (lida por agentes GSD2)
└── .gsd/
    └── DECISIONS.md     ← decisões de arquitetura registradas ✓

Próximos passos:
1. Cole docs/ARCH-CONTEXT-SNIPPET.md em cada M###-CONTEXT.md que criar
2. Preencha docs/[context]/GLOSSARY.md com os termos do seu domínio
3. Use /arch-guide guide quando tiver dúvidas de design
4. Use /arch-guide review para validar código contra as regras de arquitetura
```
</confirmation>
