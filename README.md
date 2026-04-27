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
