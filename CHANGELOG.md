# Changelog

Todas as mudanças notáveis do SDD-SAAS Kit são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).
Versionamento semântico: MAJOR.MINOR.PATCH — MINOR para novas features, PATCH para correções e documentação.

---

## [2.1.0] — 2026-05-02

### Adicionado
- **`Skills/context7.md`** — Skill canônica (com frontmatter `name`/`description`/`version`) para Context7 (Upstash). Lazy-loaded → só consome tokens quando invocada. Documenta os 3 modos de uso (prompt, CLI on-demand, MCP opt-in) e quando NÃO usar.
- **`harness/templates/mcp/.mcp.json`** — template **opt-in** para Context7 via MCP em modo stdio (sem necessidade de API key). Não é copiado automaticamente pelo bootstrap; usuários intensivos copiam manualmente para a raiz do projeto.
- **Passo 8/11 em `harness/scripts/bootstrap-saas.sh`** — instala a Skill Context7 em `.claude/skills/context7.md` do projeto-alvo. Passos seguintes renumerados (8→9, 9→10, 10→11); cabeçalho do script documenta o fluxo.
- **Seção "Skill Recomendada: Context7" em `AGENTS.md`** — lista os 7 agentes que mais se beneficiam (Implementation, Testing, DevOps, Security Audit, API Docs, SRE, Migration) e diferencia Skill (default) vs MCP (opt-in).
- **`README.md`** ganhou seções **"Frameworks e Metodologias Absorvidos"** (12 itens em formato tabela) e **"Princípios de Arquitetura Observados"** (agrupados em 7 categorias didáticas).
- **`ORIENTACAO.md` §2.7** — Context7 como pilar de "documentação sempre atualizada"; explica trade-off Skill (lazy-loaded) vs MCP (always-on, custa tokens em todo system prompt) e modo HTTP+API key opcional para rate limit maior.

### Alterado
- **`Scripts/validate-kit.py`** — Check 5 valida `harness/templates/mcp/.mcp.json` e `Skills/context7.md` na lista `HARNESS_REQUIRED_PATHS`.
- **Bumps de versão** — VERSION (2.0.1 → 2.1.0), ARCHITECTURE.md, ORIENTACAO.md e os 6 manifests de libs (`@harness/test-helpers`, `@harness/saas-core`, `@harness/observability` em Node + Python) sincronizados em 2.1.0.

---

## [2.0.1] — 2026-04-27

### Corrigido
- **`ORIENTACAO.md`** sincronizado para v2.0.0 (cabeçalho, contagem de agentes 6 → 12, fluxo de bootstrap)
- **`Scripts/validate-kit.py`** ganhou Check 5 que valida estrutura completa de `harness/` (scripts, templates Docker/CI/env/git-hooks/github/devcontainer/vscode/.editorconfig, libs e versões em manifests)

### Adicionado
- **`README.md`** na raiz com quick-start orientado a `/bootstrap-saas` e árvore do repo
- **`AGENTS.md`** ganhou seção "Harness Lifecycle (v2.0.0+)" mapeando `/bootstrap-saas`, `/upgrade-kit` e `/update-kit` com diferenciação clara entre upgrade-kit e update-kit
- **`ORIENTACAO.md` Seção 4.0** descreve `/bootstrap-saas` como caminho recomendado para projetos novos em v2.0.0+

### Alterado
- **`Skills/init-sdd-saas.md`** marcada como fallback manual com disclaimer recomendando `/bootstrap-saas` em v2.0.0+
- **Checklist da Fase A em `ORIENTACAO.md`** reorganizado para listar Opção 0 (`/bootstrap-saas`) antes da Opção A (`/init-sdd-saas`)

---

## [2.0.0] — 2026-04-27

### Mudança Conceitual
Transformação do kit de **gerador via LLM** para **harness reutilizável**. A partir desta versão, projetos herdam artefatos físicos determinísticos em vez de regenerar tudo via prompt a cada execução.

### Adicionado
- **`harness/templates/docker/`** — Dockerfiles multi-stage versionados para Node.js, Python e Go; docker-compose dev e test; .dockerignore padrão
- **`harness/templates/ci/github/`** — 5 GitHub Actions workflows: CI (lint+test+build), CD staging, CD prod (com approval), security scan semanal, semantic-release
- **`harness/templates/ci/gitlab/`** — `.gitlab-ci.yml` equivalente ao pipeline GitHub
- **`harness/templates/env/`** — `.env.example` e `.env.test.example` padronizados para SaaS
- **`harness/templates/git-hooks/`** — Husky (Node.js) e pre-commit (Python) com commitlint, lint-staged e typecheck
- **`harness/templates/github/`** — CODEOWNERS, dependabot.yml, PR template, issue templates (bug/feature/spec), branch-protection.sh
- **`harness/templates/devcontainer/`** — devcontainer.json para GitHub Codespaces/VS Code Dev Containers
- **`harness/templates/vscode/`** — settings.json e extensions.json padronizados
- **`harness/templates/.editorconfig`** — EditorConfig unificado Node.js + Python
- **`harness/lib/test-helpers/node/`** — `@harness/test-helpers`: createInMemoryRepository, TenantBuilder, FakeMailer (TypeScript)
- **`harness/lib/test-helpers/python/`** — `harness-test-helpers`: equivalente Python
- **`harness/lib/saas-core/node/`** — `@harness/saas-core`: TenantId, TenantAwareEntity, TenantContext, TenantAwareRepository, tenant middleware (TypeScript)
- **`harness/lib/saas-core/python/`** — `harness-saas-core`: equivalente Python
- **`harness/lib/observability/node/`** — `@harness/observability`: logger (pino+redact), metrics (prom-client), tracer (OpenTelemetry), correlation (AsyncLocalStorage), health endpoints (TypeScript)
- **`harness/lib/observability/python/`** — `harness-observability`: equivalente Python
- **`harness/scripts/bootstrap-saas.sh`** — script idempotente de bootstrap completo; grava `.harness/installed-version` no projeto
- **`harness/scripts/upgrade-kit.sh`** — gerencia upgrade de versão do harness instalado via `.harness/installed-version`
- **`harness/scripts/setup.sh`** — sobe Docker dev, espera banco, roda migrations e seed
- **Slash command `/bootstrap-saas`** — bootstrap de novo projeto SaaS em ~30 segundos
- **Slash command `/upgrade-kit`** — upgrade do harness instalado no projeto (diferente de `/update-kit`)
- **Skill `bootstrap-saas`** — instalável globalmente, chamável de qualquer projeto novo
- **Skill `upgrade-kit`** — gerencia migrações entre versões do harness

### Alterado
- **`Skills/init-sdd-saas.md`** — refatorado para usar templates físicos de `harness/templates/` em vez de gerar Docker/CI/env via LLM
- **`AGENTS.md`** — Agente DevOps atualizado para selecionar templates em vez de gerar do zero
- **`TESTING_GUIDE.md`** — nova seção sobre uso de `@harness/test-helpers` com exemplos de import
- **`SAAS_PATTERNS.md`** — seção multi-tenancy atualizada com referência a `@harness/saas-core`

### Migração de v1.x → v2.0
Projetos criados com `/init-sdd-saas` em versões anteriores continuam funcionando. Para adotar o harness em um projeto existente, use `/upgrade-kit 2.0.0` com `.harness/installed-version` apontando para a versão instalada.

---

## [1.4.0] — 2026-04-18

### Adicionado
- **6 novos agentes** no fluxo SDD:
  - Agente Discovery (`/discover`) — valida problema/ideia antes do primeiro SPEC; gera `DISCOVERY.md` com personas, hipóteses e veredicto go/no-go
  - Agente DevOps (`/init-devops`, `/update-pipeline`) — gera CI/CD, Dockerfile, `.env.example` e IaC (suporte: AWS, GCP, Azure, Fly, Render, Railway, VPS)
  - Agente Security Audit (`/security-audit`) — threat modeling e análise OWASP Top 10
  - Agente SRE (`/define-slo`) — definição de SLOs, error budgets e runbooks
  - Agente API Docs (`/generate-api-docs`) — geração de documentação OpenAPI
  - Agente Retrospectiva (`/retrospect`) — análise de velocidade pós-milestone e atualização de KNOWLEDGE.md
- **8 novos slash commands**: `discover.md`, `init-devops.md`, `update-pipeline.md`, `security-audit.md`, `define-slo.md`, `generate-api-docs.md`, `retrospect.md` e atualização de `CLAUDE.md`
- **3 novos templates**: `DISCOVERY_TEMPLATE.md` (validação de problema), `PROJECT_TEMPLATE.md` (personas + North Star), `ROADMAP_TEMPLATE.md` (RICE Score)
- **ARCHITECTURE.md Seção 17** — Resoluções de Conflito: TDD vs YAGNI, Fail Fast vs Resilience, KISS vs Clean Architecture (Trivial Query Path), Multi-Model Routing
- **ARCHITECTURE.md Seção 21** — Privacy by Design: `@pii` tags, PII access logging, checklist no SPEC
- **ARCHITECTURE.md Seção 22** — ADRs (Architecture Decision Records) em formato padronizado em `docs/adr/`
- **SAAS_PATTERNS.md Seções 11–13** — Tenant Provisioning Queue, Data Residency, Tenant Migration/Export
- **SPEC_TEMPLATE.md** — novas seções: Business Hypotheses, Success Metrics, UX Impact
- **TESTING_GUIDE.md** — Seções 10 (property-based testing) e 11 (mutation testing)
- **Tabela de Model Minimum Rules** em AGENTS.md — regra: Analyze e Review devem usar modelo ≥ ao da Implementação

---

## [1.3.0] — 2026-04-13

### Adicionado
- **Skill `arch-guide`** — skill globalmente instalável para Clean Architecture + DDD em projetos GSD2; 11 arquivos em `Skills/arch-guide/` com 3 modos: `init`, `guide`, `review`
- **8 padrões operacionais do GSD2** absorvidos nos arquivos do kit (ARCHITECTURE.md, AGENTS.md, SAAS_PATTERNS.md)
- Diagrama do fluxo de agentes atualizado em AGENTS.md
- Tabela de contexto mínimo por agente expandida em AGENTS.md

---

## [1.2.0] — 2026-04-12

### Adicionado
- **Skill `init-sdd-saas`** (`Skills/init-sdd-saas.md`) — skill de inicialização automática de novo projeto SaaS em 9 passos; cria estrutura de pastas, copia arquivos do kit, gera CLAUDE.md, STATE.md, PROJECT.md e GLOSSARY.md por bounded context

---

## [1.1.0] — 2026-04-12

### Adicionado
- **8 padrões operacionais do `tlc-spec-driven`** absorvidos: Phase Guards por agente, Token Profiles, Multi-Model Routing, Outbox Pattern, Unit of Work, Background Jobs com isolamento por tenant, GDPR Erasure Pattern, Feature Flags por tenant
- Novos slash commands: `forensics-sprint.md`, `pause-session.md`, `resume-session.md`, `map-codebase.md`, `quick-fix.md`
- `CODEBASE_MAPPING_GUIDE.md` — guia para adoção do kit em projetos com código existente
- `HANDOFF_TEMPLATE.md` e `STATE_TEMPLATE.md` — gestão de estado entre sessões

---

## [1.0.0] — 2026-04-12

### Adicionado
- Versão inicial do SDD-SAAS Kit
- **6 arquivos de arquitetura base**: `ARCHITECTURE.md`, `AGENTS.md`, `SPEC_TEMPLATE.md`, `TESTING_GUIDE.md`, `SAAS_PATTERNS.md`, `GLOSSARY_TEMPLATE.md`
- **4 slash commands iniciais**: `new-spec.md`, `impl-sprint.md`, `review-arch.md`, `test-sprint.md`, `migrate-sprint.md`
- `GIT_WORKFLOW.md` — estratégia de branches por SPEC (`spec/<slug>`)
- `KNOWLEDGE_TEMPLATE.md` — registro append-only de lições aprendidas
- Fluxo SDD completo: Spec → Analyze → Implementation → Testing → Review → Migration
- Abordagem TDD aplicada dentro de cada SPRINT (após fase de domínio)
