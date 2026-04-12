# CLAUDE.md — [Nome do Projeto]

## Arquitetura
Leia ARCHITECTURE.md antes de qualquer ação. Este projeto segue Clean Architecture + DDD com desenvolvimento guiado por especificações (SDD via Spec-Kit).

## Regras obrigatórias
- Nunca escreva código sem um SPEC aprovado em specs/
- Sempre siga a ordem Domain-First nos SPRINTs (1=Domínio, 2=Application, 3=Infra, 4=Presentation)
- Consulte specs/[dominio-principal]/GLOSSARY.md para nomenclatura correta — use somente os termos definidos ali
- Domínio multi-tenant: toda entidade tem tenantId, todo repositório filtra por tenantId via TenantContext

## Contexto automático — leia estes arquivos antes de qualquer ação
@ARCHITECTURE.md — Constituição do projeto (obrigatório em toda sessão)
@specs/[dominio-principal]/GLOSSARY.md — Vocabulário do domínio (substitua [dominio-principal] pelo seu bounded context)

Quando acionar um agente via slash command, consulte AGENTS.md para o contexto mínimo
daquele agente e inclua apenas os arquivos necessários — não inclua o kit inteiro.

## Comandos disponíveis
- /new-spec [descrição da feature] — cria novo SPEC via Agente Spec
- /impl-sprint [spec] [n] — implementa SPRINT N via Agente Implementation
- /review-arch [spec] analyze — valida consistência do SPEC via Agente Analyze
- /review-arch [spec] [n] — revisa código do SPRINT N via Agente Review
- /test-sprint [spec] [n] — gera testes do SPRINT N via Agente Testing
- /migrate-sprint [spec] [n] — gera migration SQL do SPRINT N via Agente Migration

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
