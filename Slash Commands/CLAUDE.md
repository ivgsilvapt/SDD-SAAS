# CLAUDE.md — [Nome do Projeto]

## Arquitetura
Leia ARCHITECTURE.md antes de qualquer ação. Este projeto segue Clean Architecture + DDD com desenvolvimento guiado por especificações (SDD via Spec-Kit).

## Regras obrigatórias
- Nunca escreva código sem um SPEC aprovado em specs/ (exceção: use `/quick-fix` para correções ≤3 arquivos sem novo domínio)
- Sempre siga a ordem Domain-First nos SPRINTs (1=Domínio, 2=Application, 3=Infra, 4=Presentation)
- Consulte specs/[dominio-principal]/GLOSSARY.md para nomenclatura correta — use somente os termos definidos ali
- Domínio multi-tenant: toda entidade tem tenantId, todo repositório filtra por tenantId via TenantContext
- Commits seguem o padrão Conventional Commits — o Agente Review sugere a mensagem pronta ao final de cada SPRINT aprovado (ARCHITECTURE.md seção 20)
- Ao tomar decisão arquitetural não-óbvia, registre em STATE.md antes de fechar a sessão

## Contexto automático — leia estes arquivos antes de qualquer ação
@ARCHITECTURE_DIGEST.md — Regras inegociáveis do projeto, resumo de sessão (obrigatório em toda sessão)
@STATE.md — Memória persistente: decisões, bloqueios, ideias adiadas (obrigatório em toda sessão)
@specs/[dominio-principal]/GLOSSARY.md — Vocabulário do domínio (substitua [dominio-principal] pelo seu bounded context)

Quando acionar um agente via slash command, consulte AGENTS.md para o contexto mínimo
daquele agente e inclua apenas os arquivos necessários — não inclua o kit inteiro.
Quando precisar de detalhe além do digest (ex: Analyze e Review), leia diretamente as
seções do ARCHITECTURE.md completo indicadas em AGENTS.md — nunca inclua o arquivo inteiro
só porque o digest não bastou.

## Contexto sob demanda — leia apenas quando a regra abaixo se aplicar

Estes arquivos **não** usam `@` — incluí-los sempre desperdiçaria tokens em sessões que não precisam deles. Leia-os explicitamente quando a situação pedir:

- `PROJECT.md` — Agente Spec: leia antes de criar um SPEC novo (visão de produto, personas, non-goals).
- `KNOWLEDGE.md` — Qualquer agente: leia antes de implementar em área com problema já registrado (se o arquivo existir).
- `GIT_WORKFLOW.md` — Leia uma vez, no início do projeto, para adotar a estratégia de branches por SPEC. Não é necessário em toda sessão.
- `ARCHITECTURE.md` (completo) — Agente Analyze e Agente Review: sempre leem as seções completas listadas em `AGENTS.md`, nunca o digest.

## Comandos disponíveis

### Pré-SPEC
- /discover [ideia] — valida problema/ideia via Agente Discovery, gera DISCOVERY.md

### Ciclo SPEC → Review
- /new-spec [descrição da feature] — cria novo SPEC via Agente Spec
- /enrich-spec [spec] — adiciona casos de borda e estados transversais via Agente Spec Enricher (opcional, sessão nova, antes do Analyze)
- /review-arch [spec] analyze — valida consistência do SPEC via Agente Analyze
- /impl-sprint [spec] [n] — implementa SPRINT N via Agente Implementation
- /test-sprint [spec] [n] — gera testes do SPRINT N via Agente Testing
- /review-arch [spec] [n] — revisa código do SPRINT N via Agente Review
- /migrate-sprint [spec] [n] — gera migration SQL do SPRINT N via Agente Migration
- /forensics-sprint [spec] [n] — diagnóstico de SPRINT com falha (Review REPROVADO ou testes persistentes)

### Design Visual (opcional — produtos novos ou features com UI)
- /design-ui [spec] — gera briefing de design via Agente Design a partir do PROJECT.md/SPEC
- /lock-design [pasta-do-design] — valida as 13 regras e trava o design via Agente Design Lock

### Pós-Review / Produção
- /init-devops [cloud] — configura CI/CD, Dockerfile e .env.example via Agente DevOps
- /update-pipeline [spec] — atualiza pipeline após novos serviços/workers adicionados pelo SPEC
- /security-audit [spec|full] — auditoria de segurança (STRIDE + OWASP) via Agente Security Audit
- /define-slo [spec] — define SLOs, alertas e runbook via Agente SRE
- /generate-api-docs — gera/atualiza openapi.yaml via Agente API Docs

### Operação contínua
- /quick-fix [descrição] — correção pequena (≤3 arquivos), sem cerimônia de SPEC
- /pause-session — salva o estado atual e cria HANDOFF.md para retomada posterior
- /resume-session — retoma sessão a partir do HANDOFF.md
- /map-codebase [path?] — analisa codebase existente e gera documentação em .specs/codebase/
- /retrospect — revisão de milestone: velocity, lições, atualiza KNOWLEDGE.md
- /update-kit [caminho-do-kit] — atualiza os arquivos de referência do kit no projeto (docs metodológicos)
- /upgrade-kit [versão] — aplica upgrade de versão do harness via .harness/installed-version

### Harness (projetos novos)
- /bootstrap-saas [stack] [cloud] [profile] — inicializa projeto novo em ~30 segundos com templates físicos do harness

## Harness Version
- Versão instalada: `cat .harness/installed-version`
- Stack: `cat .harness/stack`
- Para upgrade: `/upgrade-kit [nova-versão]`

## Libs do Harness Disponíveis

```typescript
// Test helpers — não reimplemente InMemoryRepository ou builders
import { createInMemoryRepository, aTenant, FakeMailer } from '@harness/test-helpers';

// Primitivas multi-tenant — não reimplemente TenantContext ou TenantAwareRepository
import { TenantAwareEntity, TenantAwareRepository, TenantContext } from '@harness/saas-core';

// Observabilidade — não configure pino/prometheus/otel do zero
import { logger, Correlation, collectDefaultMetrics } from '@harness/observability';
```

```python
# Python equivalente
from harness_test_helpers import create_in_memory_repository, a_tenant, FakeMailer
from harness_saas_core import TenantAwareEntity, TenantAwareRepository, TenantContext
from harness_observability import logger, Correlation
```

## Tecnologias deste projeto
- Linguagem: [TypeScript / Python / Java / etc.]
- Framework: [NestJS / FastAPI / Spring / etc.]
- ORM: [Prisma / SQLAlchemy / Hibernate / etc.]
- Banco: [PostgreSQL / MySQL / MongoDB / etc.]
- Testes: [Jest / Pytest / JUnit / etc.]

## Bounded Contexts deste projeto
- [bounded-context-1] — [descrição em uma linha]
- [bounded-context-2] — [descrição em uma linha]
- [bounded-context-3] — [descrição em uma linha]

## Observações específicas deste projeto
[Adicione aqui qualquer exceção às regras do ARCHITECTURE.md, tecnologias especiais,
integrações externas ou contexto de negócio que a IA precisa conhecer]
