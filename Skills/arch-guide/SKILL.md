---
name: arch-guide
description: Configuração e orientação de Clean Architecture + DDD para projetos GSD2. Use ao inicializar a arquitetura do projeto, tomar decisões de design sobre camadas ou modelos de domínio, ou revisar código em busca de violações arquiteturais.
---

<principios_essenciais>
## O que esta Skill faz

arch-guide traz os princípios de Clean Architecture + Domain-Driven Design (DDD) para projetos GSD2 sem adicionar cerimônia ou conflitar com o fluxo autônomo do GSD2.

**Três modos de uso:**
- **Init**: Configura estrutura de pastas, ARCHITECTURE.md e GLOSSARY.md para um projeto novo ou existente
- **Orientar**: Responde dúvidas de arquitetura, valida designs contra regras de camadas e padrões DDD
- **Revisar**: Inspeciona código em busca de violações de camada, lógica no lugar errado e uso incorreto de DDD

**Contratos fundamentais — nunca quebre:**
- A camada Domain não tem nenhuma dependência de infraestrutura, framework ou UI
- As dependências fluem para dentro: Presentation → Application → Domain ← Infrastructure
- Regras de negócio vivem no Domain. Detalhes de infraestrutura ficam no Infrastructure.
- Em dúvida sobre onde o código pertence: "Mudaria se eu trocasse de framework?" → Infrastructure. "Mudaria se eu trocasse de banco?" → Infrastructure. Nenhum dos dois → Domain.

**Integração com GSD2 (sem conflitos):**
- `ARCHITECTURE.md` na raiz do projeto é a constituição de arquitetura — referencie-a em todo `M###-CONTEXT.md` para que os agentes GSD2 a leiam durante o planejamento
- `.gsd/DECISIONS.md` é onde as decisões de arquitetura são registradas (registro nativo do GSD2 — use-o, não crie arquivo separado)
- `.gsd/KNOWLEDGE.md` é onde as lições aprendidas são registradas (registro nativo do GSD2)
- Os phase guards são orientações, não bloqueios de execução — o GSD2 permanece totalmente autônomo
- Sem arquivos SPEC, sem aprovações manuais, sem cerimônia de HANDOFF — esses são específicos do SDD-SAAS
</principios_essenciais>

<roteamento>
## Roteamento por Intenção do Usuário

**"Init" / "inicializar" / "configurar projeto" / "adicionar arquitetura":**
→ Leia `workflows/init-project.md`

**"Como eu design X?" / "Onde fica Y?" / "Qual padrão para Z?" / "Esta abordagem está correta?":**
→ Leia `workflows/guide-design.md`

**"Verifique este código" / "Revise estes arquivos" / "Tem violações?" / "A arquitetura está correta?":**
→ Leia `workflows/review-code.md`

**Intenção não clara:** Faça uma pergunta: "Você quer (1) configurar arquitetura para um projeto, (2) obter orientação de design, ou (3) revisar código existente?"
</roteamento>

<referencia_rapida>
## Referência Rápida de Camadas

| Camada | Localização | Depende de | Contém |
|---|---|---|---|
| **Domain** | `src/domain/` | nada | Entidades, Value Objects, Aggregates, interfaces de Repositório, Domain Events, Domain Services |
| **Application** | `src/application/` | Domain apenas | Use Cases, DTOs, Application Services, ports |
| **Infrastructure** | `src/infrastructure/` | Domain (implementa interfaces) | Repositórios ORM, adapters de DB, HTTP clients, serviços externos |
| **Presentation** | `src/presentation/` | Application apenas | Controllers, rotas, schemas de request/response, middleware |

**Imports que indicam violação CRÍTICA:**
- `domain/` importando de `infrastructure/` ou `presentation/` ou `application/`
- `application/` importando de `infrastructure/` ou `presentation/`
- Qualquer camada importando de uma camada que deveria depender dela
</referencia_rapida>

<indice_referencias>
## Conhecimento de Domínio

- `references/clean-architecture.md` — Regras de camadas, direção de dependências, o que pertence onde
- `references/ddd-patterns.md` — Entity, Value Object, Aggregate, Repository, Domain Event, Domain Service
- `references/phase-guards.md` — O que agentes GSD2 devem/não devem fazer em cada fase de execução
- `references/testing-strategy.md` — Abordagem de testes por camada (unitário → integração → e2e)
</indice_referencias>

<indice_workflows>
## Workflows

| Workflow | Quando usar |
|---|---|
| `workflows/init-project.md` | Configurar arquitetura para um projeto novo ou existente |
| `workflows/guide-design.md` | Dúvidas de design arquitetural e validação de design |
| `workflows/review-code.md` | Revisão de código contra as regras de arquitetura |
</indice_workflows>

<criterios_de_sucesso>
Um projeto GSD2 bem arquitetado com a arch-guide:
- Tem `ARCHITECTURE.md` na raiz do projeto, referenciado em cada `M###-CONTEXT.md`
- A camada Domain não tem imports de infrastructure, framework ou camadas de UI
- Toda operação de persistência tem uma interface Repository em `domain/` e implementação em `infrastructure/`
- Toda operação entre camadas é orquestrada por um Use Case em `application/`
- `.gsd/DECISIONS.md` registra as principais decisões de arquitetura tomadas durante o projeto
- `.gsd/KNOWLEDGE.md` acumula lições aprendidas durante a implementação
</criterios_de_sucesso>
