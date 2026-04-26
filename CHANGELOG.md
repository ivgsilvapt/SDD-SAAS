# Changelog

Todas as mudanças notáveis do SDD-SAAS Kit são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).
Versionamento semântico: MAJOR.MINOR.PATCH — MINOR para novas features, PATCH para correções e documentação.

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
