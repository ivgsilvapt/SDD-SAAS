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
@ARCHITECTURE.md — Constituição do projeto (obrigatório em toda sessão)
@STATE.md — Memória persistente: decisões, bloqueios, ideias adiadas (obrigatório em toda sessão)
@specs/[dominio-principal]/GLOSSARY.md — Vocabulário do domínio (substitua [dominio-principal] pelo seu bounded context)
@PROJECT.md — Visão e propósito do produto (opcional, recomendado para o Agente Spec)

Quando acionar um agente via slash command, consulte AGENTS.md para o contexto mínimo
daquele agente e inclua apenas os arquivos necessários — não inclua o kit inteiro.

## Comandos disponíveis
- /new-spec [descrição da feature] — cria novo SPEC via Agente Spec
- /impl-sprint [spec] [n] — implementa SPRINT N via Agente Implementation
- /review-arch [spec] analyze — valida consistência do SPEC via Agente Analyze
- /review-arch [spec] [n] — revisa código do SPRINT N via Agente Review
- /test-sprint [spec] [n] — gera testes do SPRINT N via Agente Testing
- /migrate-sprint [spec] [n] — gera migration SQL do SPRINT N via Agente Migration
- /quick-fix [descrição] — correção pequena (≤3 arquivos), sem cerimônia de SPEC
- /pause-session — salva o estado atual e cria HANDOFF.md para retomada posterior
- /resume-session — retoma sessão a partir do HANDOFF.md
- /map-codebase [path?] — analisa codebase existente e gera documentação em .specs/codebase/

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
