# SDD-SAAS Harness

**Versão atual:** ver [`VERSION`](VERSION) — mudanças em [`CHANGELOG.md`](CHANGELOG.md)

Harness reutilizável para construir SaaS multi-tenant com IA (vibe coding) seguindo Clean Architecture + DDD + SDD (Specification-Driven Development). Combina **arquivos de metodologia** (ARCHITECTURE.md, AGENTS.md, templates de SPEC), **templates físicos versionados** (Dockerfiles, CI workflows, devcontainer, git hooks) e **libs importáveis** (`@harness/test-helpers`, `@harness/saas-core`, `@harness/observability` em Node.js e Python).

---

## Quick start

Dentro de uma pasta vazia destinada ao novo projeto:

```bash
# 1. Instale a skill bootstrap-saas (uma vez por máquina)
cp Skills/bootstrap-saas.md ~/.claude/skills/

# 2. Abra o Claude Code e bootstrape o projeto
/bootstrap-saas node-nestjs aws balanced

# 3. Suba o ambiente local
bash harness/scripts/setup.sh
```

Em ~30 segundos você terá: estrutura `src/`, Dockerfile, CI/CD, devcontainer, git hooks, libs `@harness/*` declaradas, metodologia (ARCHITECTURE/AGENTS/STATE/PROJECT), `git init` + primeiro commit, e `.harness/installed-version` para `/upgrade-kit` futuro.

> **Quer entender o que cada arquivo faz antes de bootstrapar?** Leia [`ORIENTACAO.md`](ORIENTACAO.md) — guia completo (Seção 4 cobre as 3 opções de inicialização).

---

## Estrutura do repositório

```
SDD-SAAS/
├── ARCHITECTURE.md          # Constituição arquitetural (Clean Architecture + DDD)
├── AGENTS.md                # 12 agentes do fluxo SDD (Spec, Analyze, Implementation, Testing, Review, Migration, ...)
├── ORIENTACAO.md            # Guia completo do harness (3160 linhas)
├── SAAS_PATTERNS.md         # Padrões SaaS (multi-tenancy, billing, RBAC)
├── TESTING_GUIDE.md         # Estratégia de testes
├── *_TEMPLATE.md            # Templates: SPEC, GLOSSARY, STATE, PROJECT, KNOWLEDGE, HANDOFF, DISCOVERY, ROADMAP
├── VERSION, CHANGELOG.md    # Versionamento semântico
├── harness/
│   ├── scripts/             # bootstrap-saas.sh, upgrade-kit.sh, setup.sh
│   ├── templates/           # docker/, ci/{github,gitlab}/, env/, git-hooks/, github/, devcontainer/, vscode/
│   └── lib/                 # test-helpers, saas-core, observability — para Node.js e Python
├── Slash Commands/          # 20 slash commands prontos (/new-spec, /impl-sprint, /review-arch, ...)
├── Skills/                  # Skills instaláveis: bootstrap-saas, upgrade-kit, init-sdd-saas, arch-guide
└── Scripts/validate-kit.py  # Validação automatizada de consistência interna
```

---

## Conceitos-chave

- **SDD (Specification-Driven Development):** nada é codado sem um SPEC aprovado em `specs/`. Exceção: `/quick-fix` para mudanças ≤3 arquivos sem novo domínio.
- **Domain-First:** SPRINTs são organizados por camada — Domínio → Application → Infrastructure → Presentation.
- **Multi-tenant by design:** toda entidade tem `tenantId`, todo repositório filtra por tenant via `TenantContext` (incluso em `@harness/saas-core`).
- **Conventional Commits:** mensagens padronizadas; o Agente Review sugere o commit pronto ao final de cada SPRINT aprovado.

---

## Frameworks e Metodologias Absorvidos

O harness consolida ideias de várias fontes em um conjunto coerente. Cada item abaixo influenciou diretamente a metodologia, os agentes e/ou os templates físicos do kit.

| Framework / Metodologia | O que aporta ao kit |
|---|---|
| **SDD — Specification-Driven Development** | Toda feature começa por um SPEC aprovado em `specs/` antes de qualquer linha de código. Tornado obrigatório nos agentes Spec/Analyze/Implementation. |
| **GitHub Spec-Kit** | Implementação canônica de SDD; influenciou o formato de `SPEC_TEMPLATE.md` (User Stories, NFRs, Requisitos Funcionais, Contexto Arquitetural, SPRINTs). |
| **Clean Architecture** (Robert C. Martin) | Quatro camadas (Domain → Application → Infrastructure → Presentation) com **Dependency Rule**. É a "constituição" do `ARCHITECTURE.md`. |
| **Domain-Driven Design** (Eric Evans / Vaughn Vernon) | Bounded Contexts, Ubiquitous Language (`GLOSSARY_TEMPLATE.md`), Aggregates, Value Objects, Domain Events. |
| **TDD — Test-Driven Development** (Kent Beck) | Ciclo Red-Green-Refactor obrigatório nas camadas Domain e Application; Test Pyramid documentado em `TESTING_GUIDE.md`. |
| **GSD2** | 8 padrões operacionais para escala empresarial absorvidos em `ARCHITECTURE.md`, `AGENTS.md` e `SAAS_PATTERNS.md`. |
| **tlc-spec-driven** | 8 padrões: Phase Guards por agente, Token Profiles (budget/balanced/quality), Multi-Model Routing, Outbox Pattern, Unit of Work, Background Jobs com isolamento por tenant, GDPR Erasure, Feature Flags por tenant. |
| **Conventional Commits** | Mensagens de commit padronizadas (`feat`/`fix`/`chore`/`docs`/`refactor`); o Agente Review entrega o commit pronto ao fim de cada SPRINT aprovado. |
| **Keep a Changelog** | Formato canônico do `CHANGELOG.md` (seções *Adicionado*, *Alterado*, *Corrigido*, *Removido*). |
| **Semantic Versioning (SemVer)** | `VERSION` segue `MAJOR.MINOR.PATCH`; bumps acompanhados de entrada no `CHANGELOG.md` e validados pelo `validate-kit.py`. |
| **MCP — Model Context Protocol** (Anthropic) | Protocolo aberto para conectar agentes a fontes externas (APIs, bancos, docs). Disponível como template opt-in em `harness/templates/mcp/`. |
| **Context7** (Upstash) | RAG de documentação **versionada e atualizada** de bibliotecas open-source via Skill (default, lazy-loaded) ou MCP (opt-in). Resolve cutoff de treinamento. Skill em `Skills/context7.md`. |

---

## Princípios de Arquitetura Observados

Princípios que estruturam o código gerado pelos agentes do kit. Agrupados por dimensão para facilitar onboarding.

### Estrutura
- **Dependency Rule** — dependências apontam apenas para dentro: Presentation → Application → Domain (Domain não conhece nada externo).
- **Layered Architecture** — quatro camadas isoladas com contratos explícitos via interfaces.
- **SOLID** — SRP, OCP, LSP, ISP e DIP aplicados em todas as camadas.
- **Domain-First Development** — SPRINTs de cada SPEC começam pela camada de Domínio (entidades + invariantes) antes de Application/Infrastructure/Presentation.

### Modelagem de Domínio
- **Bounded Contexts** — limites explícitos entre subdomínios; cada um com seu próprio `GLOSSARY.md`.
- **Ubiquitous Language** — vocabulário compartilhado entre código e negócio, vivo no glossário por bounded context.
- **Aggregates & Value Objects** — invariantes encapsulados; identidade vs. igualdade estrutural; raízes de agregado controlam consistência.

### Multi-tenancy & Privacidade
- **Multi-tenancy by Design** — toda entidade carrega `tenantId`; todo repositório filtra via `TenantContext` (`@harness/saas-core`).
- **Privacy by Design / GDPR Erasure** — direito ao esquecimento como padrão operacional; tags `@pii`; logging de acesso a PII.
- **Security by Default** — RBAC, isolamento de tenant, secrets nunca em logs (pino+redact / structlog), defesa em profundidade.

### Confiabilidade
- **Outbox Pattern** — consistência transacional entre banco de dados e mensageria/eventos.
- **Unit of Work** — atomicidade de mutações de domínio dentro de uma transação.
- **Idempotency** — operações de escrita são idempotentes (chaves de idempotência em writes externas).
- **Eventual Consistency** — projeções e read models toleram delay; SLOs explícitos.
- **Resilience Patterns** — Circuit Breaker, Retry com backoff exponencial, Timeout em toda chamada externa.
- **Background Jobs tenant-isolated** — filas particionadas por tenant evitam ruidoso-vizinho.

### Observabilidade
- **Three Pillars** — logs estruturados + métricas + traces (OpenTelemetry) via `@harness/observability`.
- **Correlation IDs** — propagados via AsyncLocalStorage (Node) / contextvars (Python) entre camadas.
- **Health endpoints** — `/health/live` e `/health/ready` padronizados para orquestradores (k8s, ECS).

### Qualidade
- **Test Pyramid** — muitas unit, médio integration, poucas e2e (definido em `TESTING_GUIDE.md`).
- **TDD (Red-Green-Refactor)** — obrigatório nas camadas Domain e Application.
- **Given-When-Then (GWT)** — cenários do SPEC viram especificações executáveis de teste.

### Operação Inteligente (vibe coding disciplinado)
- **Phase Guards** — cada agente valida pré-condições (ex.: Implementation só roda após Analyze aprovado).
- **Token Profiles** — três perfis (budget/balanced/quality) controlam custo de LLM por sessão.
- **Multi-Model Routing** — modelo certo para a tarefa certa (Analyze e Review ≥ Implementation).
- **Feature Flags tenant-scoped** — releases progressivas por tenant; rollback granular.

### Integração com IA
- **Skills lazy-loaded** — capacidades carregadas sob demanda (descoberta por nome+descrição) → economia de tokens.
- **MCP — Model Context Protocol** (opt-in) — sempre-disponível para uso intensivo; custo de tokens em todo system prompt.
- **RAG via Context7** — documentação de libs externas sempre atualizada e versionada.
- **Vibe Coding disciplinado** — IA opera dentro de contratos explícitos (`ARCHITECTURE.md` + `AGENTS.md`), não livre.

---

## Documentação

| Arquivo | Propósito |
|---|---|
| [ORIENTACAO.md](ORIENTACAO.md) | Guia completo: conceitos, fluxo, exemplos, checklists |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Constituição arquitetural — regras invioláveis |
| [AGENTS.md](AGENTS.md) | Os 12 agentes do fluxo SDD e seus contratos |
| [SAAS_PATTERNS.md](SAAS_PATTERNS.md) | Padrões específicos de SaaS (multi-tenancy, billing, RBAC) |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Estratégia de testes (unit, integration, e2e) |
| [GIT_WORKFLOW.md](GIT_WORKFLOW.md) | Estratégia de branches por SPEC |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de versões |

---

## Validação local

```bash
python Scripts/validate-kit.py
```

Roda 5 checks: slash commands ↔ CLAUDE.md, referências do `init-sdd-saas`, referências em ORIENTACAO.md, consistência de versão, e estrutura completa do harness (templates/libs/scripts).

---

## Licença

Uso interno. Não publicar sem revisão.
