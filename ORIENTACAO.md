# ORIENTACAO.md

Guia completo do Kit de Arquitetura SaaS para desenvolvimento com IA (vibe coding).
Leia este arquivo antes de iniciar qualquer novo projeto SaaS com este kit.

---

## Sumário

1. [Apresentação — O que é este Kit](#1-apresentação--o-que-é-este-kit)
   - [Para quem é este kit](#para-quem-é-este-kit)
   - [O que você consegue com este kit](#o-que-você-consegue-com-este-kit)
   - [Pré-requisitos](#pré-requisitos)
   - [Exemplo: AçãoPlus (SaaS 5W2H)](#exemplo-açãoplus-saas-5w2h)
2. [Conceitos Fundamentais](#2-conceitos-fundamentais)
   - [2.1 SDD — Specification-Driven Development](#21-sdd--specification-driven-development)
   - [2.2 Spec-Kit](#22-spec-kit)
   - [2.3 Clean Architecture + DDD](#23-clean-architecture--ddd)
   - [2.4 Domain-First](#24-domain-first)
   - [2.5 TDD — Test-Driven Development](#25-tdd--test-driven-development)
   - [2.6 Vibe Coding com IA](#26-vibe-coding-com-ia)
3. [Os Arquivos do Kit — o que é cada um e quando usar](#3-os-arquivos-do-kit)
   - [3.1 ARCHITECTURE.md — A Constituição](#31-architecturemd--a-constituição)
   - [3.2 AGENTS.md — Os 6 Agentes do Fluxo](#32-agentsmd--os-6-agentes-do-fluxo)
   - [3.3 SPEC_TEMPLATE.md — O Formato das Especificações](#33-spec_templatemd--o-formato-das-especificações)
   - [3.4 TESTING_GUIDE.md — Estratégia de Testes](#34-testing_guidemd--estratégia-de-testes)
   - [3.5 SAAS_PATTERNS.md — Padrões Específicos de SaaS](#35-saas_patternsmd--padrões-específicos-de-saas)
   - [3.6 GLOSSARY_TEMPLATE.md — Ubiquitous Language](#36-glossary_templatemd--ubiquitous-language)
4. [Preparando um Novo Projeto SaaS](#4-preparando-um-novo-projeto-saas)
   - [Passo 1: Criar a estrutura de pastas](#passo-1-criar-a-estrutura-de-pastas)
   - [Passo 2: Copiar os arquivos do kit](#passo-2-copiar-os-arquivos-do-kit)
   - [Passo 3: Criar o CLAUDE.md](#passo-3-criar-o-claudemd)
   - [Passo 4: Criar o GLOSSARY.md do projeto](#passo-4-criar-o-glossarymd-do-projeto)
   - [Passo 5: Criar os slash commands](#passo-5-criar-os-slash-commands-veja-seção-7)
   - [Exemplo: AçãoPlus — Preparação do Projeto](#exemplo-açãoplus--preparação-do-projeto)
5. [Fluxo Completo de Desenvolvimento](#5-fluxo-completo-de-desenvolvimento)
   - [Fase 0: Concepção da Ideia](#fase-0-concepção-da-ideia)
   - [Fase 1: Preencher o GLOSSARY.md](#fase-1-preencher-o-glossarymd)
   - [Fase 2: Criar o primeiro SPEC com o Agente Spec](#fase-2-criar-o-primeiro-spec-com-o-agente-spec)
   - [Fase 3: Revisar e Aprovar o SPEC](#fase-3-revisar-e-aprovar-o-spec)
   - [Fase 4: Validar com o Agente Analyze](#fase-4-validar-com-o-agente-analyze)
   - [Fase 5: Implementar SPRINT 1 — Domínio](#fase-5-implementar-sprint-1--domínio)
   - [Fase 6: Gerar Testes do SPRINT 1 com o Agente Testing](#fase-6-gerar-testes-do-sprint-1-com-o-agente-testing)
   - [Fase 7: Revisar SPRINT 1 com o Agente Review](#fase-7-revisar-sprint-1-com-o-agente-review)
   - [Fase 8: Gerar Migration com o Agente Migration](#fase-8-gerar-migration-com-o-agente-migration)
   - [Fase 9: Repetir SPRINTs 2 a 5](#fase-9-repetir-sprints-2-a-5)
   - [Fase 10: Checklist Final e Próxima Feature](#fase-10-checklist-final-e-próxima-feature)
6. [Comandos Claude Code — Referência Completa](#6-comandos-claude-code--referência-completa)
7. [Configurando os Agentes como Slash Commands](#7-configurando-os-agentes-como-slash-commands)
   - [O que são Slash Commands no Claude Code](#o-que-são-slash-commands-no-claude-code)
   - [Usando os arquivos prontos da pasta "Slash Commands"](#usando-os-arquivos-prontos-da-pasta-slash-commands)
   - [Criando os comandos manualmente](#criando-os-6-comandos-do-kit)
   - [Como usar os slash commands](#como-usar-os-slash-commands)
   - [Exemplo: AçãoPlus — Slash Commands configurados](#exemplo-açãoplus--slash-commands-configurados)
   - [Índice de Exemplos do AçãoPlus](#índice-de-exemplos-do-açãoplus-neste-guia)
8. [Recuperação de Problemas Comuns](#8-recuperação-de-problemas-comuns)
9. [Checklist Completo — Do Zero ao Sistema em Produção](#9-checklist-completo--do-zero-ao-sistema-em-produção)
   - [Fase A: Preparação do Ambiente](#fase-a-preparação-do-ambiente-faça-uma-vez-por-projeto)
   - [Fase B: Glossário e Vocabulário](#fase-b-glossário-e-vocabulário-faça-antes-do-primeiro-spec)
   - [Fase C: Para cada Nova Feature (SPEC)](#fase-c-para-cada-nova-feature-spec)
   - [Fase D: Para cada SPRINT (Implementação)](#fase-d-para-cada-sprint-implementação)
   - [Fase E: Fechando uma Feature](#fase-e-fechando-uma-feature)
   - [Fase F: Manutenção e Evolução](#fase-f-manutenção-e-evolução-do-projeto)
10. [Glossário de Termos Técnicos](#10-glossário-de-termos-técnicos)
    - [Metodologia de Desenvolvimento](#metodologia-de-desenvolvimento)
    - [Arquitetura de Software](#arquitetura-de-software)
    - [SaaS e Multi-tenancy](#saas-e-multi-tenancy)
    - [Desenvolvimento Técnico](#desenvolvimento-técnico)

---

## 1. Apresentação — O que é este Kit

Este kit é um conjunto de **6 arquivos de referência arquitetural** que funcionam como a "Constituição" de qualquer SaaS que você desenvolver com auxílio de IA. O objetivo é garantir que toda a IA (Claude Code, ChatGPT, Copilot, etc.) que você usar no projeto siga as mesmas regras de arquitetura, gere código consistente, e produza um software mantível e escalável — independente de quantas sessões de vibe coding você fizer.

### Para quem é este kit

Este kit é para você que:
- Usa IA para programar (vibe coding) e quer que o código gerado tenha qualidade profissional
- Quer desenvolver múltiplos SaaS com a mesma base arquitetural
- Não quer perder tempo re-explicando as regras de arquitetura para a IA a cada nova sessão
- Quer rastrear cada funcionalidade do sistema por especificação antes de implementar

### O que você consegue com este kit

- Código com separação de camadas (nunca mistura banco de dados com regra de negócio)
- Especificações completas antes de qualquer linha de código ser escrita
- Testes gerados automaticamente para cada funcionalidade
- Ciclo de desenvolvimento previsível: Especificar → Analisar → Implementar → Testar → Revisar
- Documentação de domínio (linguagem de negócio) separada de detalhes técnicos
- Padrões prontos para [multi-tenancy](#multi-tenant), billing, GDPR e feature flags

### Pré-requisitos

- Claude Code instalado (CLI ou extensão VS Code)
- Conhecimento básico de programação (não precisa saber arquitetura — o kit ensina)
- Um editor de código (VS Code recomendado)
- Node.js ou a tecnologia de sua escolha para o SaaS

---

### Exemplo: AçãoPlus (SaaS 5W2H)

Ao longo deste guia, usaremos como exemplo o **AçãoPlus** — um SaaS de gerenciamento de planos de ação baseado na metodologia **5W2H**.

**O que é 5W2H?**
É uma metodologia de gestão de tarefas que responde 7 perguntas para cada ação:

| Sigla | Pergunta | Exemplo |
|---|---|---|
| **What** (O quê?) | O que precisa ser feito? | Contratar 3 desenvolvedores sêniores |
| **Why** (Por quê?) | Por que é necessário? | Para escalar o time de engenharia no Q2 |
| **Who** (Quem?) | Quem é o responsável? | Maria Silva (RH) |
| **Where** (Onde?) | Onde será executado? | Escritório SP + remoto |
| **When** (Quando?) | Qual o prazo? | Até 30/06/2025 |
| **How** (Como?) | Como será feito? | LinkedIn Recruiter + headhunter |
| **How Much** (Quanto?) | Quanto vai custar? | R$ 15.000 (headhunter) |

**O problema que o AçãoPlus resolve:**
Equipes de gestão criam planos de ação no Excel e perdem o controle. O AçãoPlus é um SaaS [multi-tenant](#multi-tenant) que permite criar, atribuir, acompanhar e reportar planos de ação 5W2H com visibilidade para toda a equipe.

**[Bounded contexts](#bounded-context-contexto-delimitado) identificados:**
- `auth` — autenticação e gerenciamento de contas
- `tenant` — onboarding, workspaces, membros da equipe
- `action-plan` — o core do produto: planos e tarefas 5W2H
- `billing` — assinaturas, planos e cobranças

---

## 2. Conceitos Fundamentais

Antes de mergulhar nos arquivos e comandos, entenda os conceitos por trás do kit.

### 2.1 SDD — Specification-Driven Development

**O que é:** Uma metodologia de desenvolvimento onde nenhuma linha de código é escrita sem um SPEC (especificação) aprovado que descreve o comportamento esperado.

**Por que usar:** Quando você usa IA para programar, a IA tende a gerar código imediatamente sem entender o contexto completo. O SDD força a IA a primeiro entender e documentar o que precisa ser feito — reduzindo retrabalho, código desnecessário e desvios de escopo.

**A regra de ouro do SDD:**
```
Toda funcionalidade nova = SPEC aprovado → Analyze → Implement → Test → Review
Nunca: "IA, implemente [X]" sem SPEC
```

---

### 2.2 Spec-Kit

**O que é:** Uma metodologia de especificação de software que estrutura o processo de criar especificações funcionais de forma consistente e rastreável. Referência: [github.com/github/spec-kit](https://github.com/github/spec-kit)

**Os 5 passos do Spec-Kit:**

| Passo | O que faz |
|---|---|
| **Specify** | Cria User Stories, Requisitos Funcionais e critérios de aceitação |
| **Clarify** | Identifica e resolve ambiguidades antes de implementar |
| **Checklist** | Garante que todo FR tem User Story e critério de aceitação |
| **Analyze** | Valida a consistência cruzada entre todos os artefatos do SPEC |
| **Implement** | Implementa por [SPRINTs](#sprint) em ordem Domain-First |

Neste kit, cada passo do Spec-Kit é executado por um **Agente** (definido em `AGENTS.md`) acionado por um **comando Claude Code** (ex: `/new-spec`, `/impl-sprint`).

---

### 2.3 Clean Architecture + DDD

**Clean Architecture** organiza o código em camadas concêntricas, onde as camadas internas não conhecem as externas:

```
┌─────────────────────────────────────┐
│          Presentation               │  ← Controllers, Views, ViewModels
│  ┌───────────────────────────────┐  │
│  │        Application            │  │  ← Use Cases, Commands, Queries
│  │  ┌─────────────────────────┐  │  │
│  │  │        Domain           │  │  │  ← Entidades, Value Objects, Regras de Negócio
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│          Infrastructure             │  ← Banco, E-mail, APIs externas
└─────────────────────────────────────┘
```

**Regra fundamental:** O código interno nunca depende do externo. O Domínio não sabe que existe um banco de dados. A Application não sabe que existe um Controller HTTP.

**[DDD (Domain-Driven Design)](#domain-driven-design-ddd)** complementa a Clean Architecture com:
- **[Bounded Contexts](#bounded-context-contexto-delimitado):** Cada "domínio" do negócio tem seu próprio modelo independente. No AçãoPlus, `action-plan` e `billing` são contextos separados que se comunicam apenas via eventos.
- **[Ubiquitous Language](#ubiquitous-language-linguagem-ubíqua):** Nomes de código refletem o vocabulário do negócio. Não `UserPlan`, mas `Subscription`. Não `Record`, mas `ActionPlan`.
- **[Aggregate Root](#aggregate-root):** Entidade principal de um grupo de objetos relacionados. `ActionPlan` é o Aggregate Root que controla suas `Tasks`.
- **[Unit of Work](#unit-of-work):** Quando um Use Case precisa persistir em dois repositórios na mesma transação, usa-se o padrão Unit of Work — uma interface definida no domínio/shared que agrupa operações atômicas sem acoplar o Use Case à infraestrutura (ver `ARCHITECTURE.md` seção 7).
- **Domain Events — Sync vs Async:** Eventos dentro do mesmo bounded context são disparados sincronamente no Use Case. Eventos entre bounded contexts diferentes usam o Outbox Pattern para garantia de entrega (ver `ARCHITECTURE.md` seção 19).

---

### 2.4 Domain-First

A ordem de implementação dos [SPRINTs](#sprint) é sempre:

```
SPRINT 1: Domínio      → Entidades, Value Objects, interfaces de repositório
SPRINT 2: Application  → Use Cases (Commands + Queries) + Job Use Cases (se houver background jobs)
SPRINT 3: Infra        → Repositórios concretos, ORM, banco de dados + Workers/Scheduler
SPRINT 4: Apresentação → Controllers, ViewModels, API REST, i18n + Health Checks
SPRINT 5: Transversal  → Middleware, rate limit, logging específico (opcional)
```

**Por que esta ordem?** Se você começa pelo banco de dados ou pela tela, acaba com lógica de negócio espalhada em lugares errados. Começando pelo domínio, você modela as regras de negócio antes de pensar em como persistir ou exibir os dados.

---

### 2.5 TDD — Test-Driven Development

**O que é:** Uma prática de desenvolvimento onde cada unidade de código de produção é precedida por um teste que falha. O ciclo é: **Red** (teste falha) → **Green** (código mínimo passa) → **Refactor** (limpa sem quebrar).

**Por que usar com este kit:** Os cenários [Given-When-Then](#given-when-then-gwt) do SPEC já são especificações de teste. O TDD fecha o ciclo naturalmente: o Agente Implementation traduz cada GWT em um teste falhando *antes* de escrever qualquer código de produção.

**Relação com SDD:**
```
SDD define O QUÊ:   SPEC com cenários GWT ──→ contrato de comportamento
TDD executa O COMO: GWT → [RED] teste falha → [GREEN] código passa → [REFACTOR] limpa
```

**Onde se aplica neste kit:**
- **Domínio e Application:** TDD obrigatório — zero dependências externas facilitam o ciclo
- **Infrastructure e Presentation:** TDD opcional — o Agente Testing gera estes testes após a implementação

---

### 2.6 Vibe Coding com IA

**Vibe coding** é a prática de desenvolver software descrevendo o que você quer em linguagem natural para uma IA e revisando o código gerado. Com este kit, o ciclo funciona assim:

```
Você descreve a feature
       ↓
IA (Agente Spec) gera o SPEC
       ↓
Você revisa e aprova o SPEC
       ↓
IA (Agente Analyze) valida consistência
       ↓
IA (Agente Implementation) escreve o código SPRINT por SPRINT
   [TDD: para cada FR → teste falhando → implementação mínima → refactor]
       ↓
IA (Agente Testing) valida cobertura GWT e gera testes de integração
       ↓
IA (Agente Review) revisa o código contra as regras
       ↓
Você aprova e avança para a próxima feature
```

O kit garante que a IA siga as mesmas regras arquiteturais em todas as sessões, mesmo que você mude de sessão, mude de IA, ou retome o projeto semanas depois.

---

## 3. Os Arquivos do Kit

O kit contém 6 arquivos que trabalham em conjunto. Cada um tem um papel específico.

---

### 3.1 ARCHITECTURE.md — A Constituição

**O que é:** O arquivo de regras imperativas que toda IA deve ler antes de qualquer sessão de código. Define a arquitetura, estrutura de pastas, regras invioláveis, padrões de erro, API, testes, segurança, resiliência e mais.

**Por que fazer:**
Sem este arquivo, cada sessão com a IA pode gerar código num estilo diferente: um dia ela usa uma camada, outro dia não usa, um dia retorna `null`, outro dia usa `Result`. Com o ARCHITECTURE.md, todas as sessões seguem o mesmo contrato arquitetural.

**O que acontece se não fizer:**
A IA começa a inventar padrões. Em 5 sessões você terá 5 formas diferentes de tratar erros, 3 formas diferentes de organizar pastas, e código que mistura banco de dados com regra de negócio. Refatorar isso no futuro custa mais do que desenvolver do zero.

**Quando usar:** Sempre. É o primeiro arquivo a ser fornecido para qualquer agente de IA, em qualquer sessão.

**Como usar:**
1. Copie para a raiz do seu projeto SaaS
2. Adicione-o ao `CLAUDE.md` do projeto para que o Claude Code o leia automaticamente
3. Nas sessões de vibe coding, forneça as seções relevantes (não o arquivo inteiro — veja a tabela de contexto mínimo em `AGENTS.md`)

**Estrutura das seções principais:**

| Seção | O que contém |
|---|---|
| **0. Início de Sessão** | Checklist de perguntas que a IA deve responder antes de codificar |
| **1. Regras Imperativas** | O que a IA NUNCA pode fazer (violações críticas) |
| **2. Estrutura de Pastas** | Onde cada arquivo do projeto deve viver |
| **3. Camadas** | Responsabilidades de cada camada (presentation, application, domain, infra) |
| **4. Comunicação entre Camadas** | Como as camadas se conversam (interfaces, eventos) |
| **5. Checklist de Revisão** | Lista de verificação para o Agente Review |
| **8. Tratamento de Erros** | Padrão Result\<T,E\>, hierarquia de erros, error codes |
| **9. Design de API** | Versionamento, paginação, idempotência, convenções REST |
| **10. Observabilidade** | Logging estruturado, Correlation ID, métricas |
| **11. Segurança** | JWT, RBAC, Defense in Depth, OWASP |
| **12. Resiliência** | Circuit Breaker, Retry, Timeout |
| **13. Migrations** | Regras para migrations de banco de dados seguras |
| **14. Estratégia de Testes** | Pirâmide de testes resumida |
| **15. Padrões SaaS** | [Multi-tenancy](#multi-tenant), [TenantContext](#tenantcontext), Feature Flags |
| **16. Otimização de Tokens** | Qual contexto fornecer para cada agente |
| **17. Princípios** | SOLID, DRY, YAGNI e outros princípios com hierarquia de desempate |
| **18. i18n** | Estrutura de arquivos de tradução e convenção de chaves |
| **19. Background Jobs e Outbox** | Job Use Cases, workers multi-tenant, Outbox Pattern para eventos entre BCs |

---

#### Exemplo: AçãoPlus — ARCHITECTURE.md

Para o AçãoPlus, você copia o `ARCHITECTURE.md` para a raiz do projeto `acaoplus/` sem modificações. Ele já está configurado para SaaS [multi-tenant](#multi-tenant) com as regras corretas.

Se precisar personalizar alguma regra (ex: a empresa usa MongoDB em vez de PostgreSQL), documente a exceção no início do arquivo com um comentário `// EXCEÇÃO DESTE PROJETO:` — nunca remova as regras originais.

---

### 3.2 AGENTS.md — Os 6 Agentes do Fluxo

**O que é:** Define os 6 agentes especializados do fluxo SDD, com seus prompts completos, regras de entrada/saída, contexto mínimo necessário e anti-patterns a evitar.

**Por que fazer:**
Cada agente tem uma responsabilidade única. Usar o agente certo para cada etapa garante que a IA não misture responsabilidades (ex: implementar código enquanto faz análise do SPEC).

**O que acontece se não fizer:**
Sem os agentes definidos, você acaba pedindo para a mesma IA "criar SPEC E implementar ao mesmo tempo". O resultado é um SPEC incompleto com código misturado, sem critérios de aceitação, sem separação de camadas. Os problemas só aparecem semanas depois quando o código já está grande demais para corrigir.

**Quando usar:** Consulte este arquivo para copiar o prompt do agente antes de iniciar cada etapa. Na prática, se você configurar os slash commands ([seção 7](#7-configurando-os-agentes-como-slash-commands)), não precisará abrir este arquivo — os prompts já estarão nos comandos.

**Os 6 agentes:**

| Agente | Responsabilidade | Acionado por |
|---|---|---|
| **Spec** | Transforma descrição em linguagem natural em SPEC estruturado | `/new-spec` |
| **Analyze** | Valida consistência cruzada do SPEC antes da implementação | `/review-arch [spec] analyze` |
| **Implementation** | Implementa um [SPRINT](#sprint) específico do SPEC | `/impl-sprint [spec] [n]` |
| **Testing** | Gera testes para o [SPRINT](#sprint) implementado | `/test-sprint [spec] [n]` |
| **Review** | Valida código e testes contra ARCHITECTURE.md | `/review-arch [spec] [n]` |
| **Migration** | Gera scripts SQL de migration | `/migrate-sprint [spec] [n]` |

**Contexto mínimo por agente (economize tokens):**

| Agente | Contexto obrigatório |
|---|---|
| Spec | `ARCHITECTURE.md` seções 0–3 + `SPEC_TEMPLATE.md` + `GLOSSARY.md` do projeto |
| Analyze | SPEC completo + `ARCHITECTURE.md` seções 1 e 5 |
| Implementation | `ARCHITECTURE.md` seções 0–5 + [SPRINT](#sprint) N do SPEC |
| Testing | Código do SPRINT + cenários [GWT](#given-when-then-gwt) + `TESTING_GUIDE.md` |
| Review | Código + testes + SPRINT N + `ARCHITECTURE.md` seções 1 e 5 |
| Migration | Entidades do SPRINT + "Impacto em Banco" do SPEC + `ARCHITECTURE.md` seção 13 |

**Fluxo visual entre agentes:**

```
Você descreve a feature
        │
        ▼
  [Agente Spec]  → gera SPEC completo
        │
        │ você revisa e muda Status para "aprovado"
        ▼
 [Agente Analyze] → valida consistência → PRONTO PARA IMPLEMENTAR
        │
        ▼ (por SPRINT)
[Agente Implementation] → implementa SPRINT N
        │
        ▼
  [Agente Testing] → gera testes do SPRINT N
        │
        ▼
  [Agente Review] → valida código + testes → APROVADO
        │
        ▼
   próximo SPRINT (ou próxima feature)
```

---

#### Exemplo: AçãoPlus — AGENTS.md

Para o AçãoPlus, você usará todos os 6 agentes ao longo do desenvolvimento. O Agente Migration será acionado especialmente nos [SPRINTs](#sprint) 1 e 3, quando as tabelas `action_plans` e `tasks` forem criadas no banco.

---

### 3.3 SPEC_TEMPLATE.md — O Formato das Especificações

**O que é:** Template obrigatório para todos os SPECs do projeto. Define exatamente quais seções um SPEC deve ter, em qual ordem, e o que preencher em cada uma.

**Por que fazer:**
Padroniza a comunicação entre você e a IA. Quando todo SPEC tem o mesmo formato, o Agente Implementation sempre sabe onde encontrar os Critérios de Aceitação, e o Agente Review sempre sabe onde verificar os cenários [Given-When-Then](#given-when-then-gwt).

**O que acontece se não fizer:**
Cada SPEC gerado terá uma estrutura diferente. O Agente Implementation não encontra os critérios de aceitação, o Agente Analyze não sabe onde verificar os [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais), e você passa mais tempo explicando onde encontrar cada informação do que desenvolvendo.

**Quando usar:** O Agente Spec usa automaticamente este template ao gerar um SPEC. Você também usa diretamente quando criar um SPEC manualmente.

**Convenção de nome e localização:**
```
specs/[bounded-context]/[verbo]-[substantivo].md
```
Exemplos:
```
specs/action-plan/create-action-plan.md
specs/auth/reset-password.md
specs/billing/create-subscription.md
```

**Seções do template:**

| Seção | O que é | Obrigatória? |
|---|---|---|
| Cabeçalho | Status, versão, data, dependências | Sim |
| Visão Geral | 2–4 frases descrevendo a feature | Sim |
| User Stories | Quem usa, o quê quer, por quê (P1/P2/P3) | Sim |
| [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais) | Performance, segurança, disponibilidade mensuráveis | Sim |
| Requisitos Funcionais | Lista numerada de comportamentos esperados | Sim |
| Clarify | Ambiguidades a resolver antes de continuar | Sim se houver |
| Critérios de Aceitação | [Given-When-Then](#given-when-then-gwt) por FR | Sim |
| Checklist de Cobertura | Todo FR tem User Story e GWT? | Sim |
| Contexto Arquitetural | Camadas, [multi-tenant](#multi-tenant), eventos, integrações | Sim |
| [SPRINTs](#sprint) 1–5 | Detalhes de implementação por camada | Sim |
| Analyze | Tabela de validação cruzada | Sim |
| Checklist Final | Verificação antes de fechar o SPEC | Sim |

**O que cada [SPRINT](#sprint) contém:**

```
SPRINT 1 (Domínio):
  - Entidades e Value Objects
  - Eventos de Domínio
  - Interfaces de Repositório
  - Impacto em Banco de Dados
  - Critérios de Aceitação do SPRINT
  - Plano de Testes do SPRINT

SPRINT 2 (Application):
  - Commands (operações de escrita)
  - Queries (operações de leitura)
  - Critérios de Aceitação
  - Plano de Testes

SPRINT 3 (Infrastructure):
  - Implementações de Repositório
  - Integrações Externas
  - Impacto em Banco de Dados
  - Critérios de Aceitação
  - Plano de Testes

SPRINT 4 (Presentation):
  - Command Object (validação de entrada)
  - Contrato de API (endpoints, request/response, status codes)
  - Controller
  - ViewModel
  - Chaves i18n
  - Critérios de Aceitação
  - Plano de Testes

SPRINT 5 (Transversal — opcional):
  - Middleware / Interceptadores
  - Critérios de Aceitação
  - Plano de Testes
```

---

#### Exemplo: AçãoPlus — SPEC_TEMPLATE.md

Para o AçãoPlus, cada feature que você criar (ex: "criar plano de ação", "adicionar tarefa", "marcar tarefa como concluída") gerará um arquivo SPEC baseado neste template. O primeiro SPEC do projeto seria:

```
specs/action-plan/create-action-plan.md
```

---

### 3.4 TESTING_GUIDE.md — Estratégia de Testes

**O que é:** Guia completo da estratégia de testes para o projeto, explicando o que testar em cada camada, como criar [InMemoryRepositories](#inmemoryrepository), nomenclatura de testes e como mapear cenários [GWT](#given-when-then-gwt) do SPEC para testes.

**Por que fazer:**
Sem um guia claro, a IA gera testes que testam implementação interna (frágeis), usa banco de dados real em testes unitários (lentos), ou cria testes sem relação com os critérios de aceitação do SPEC.

**O que acontece se não fizer:**
Você terá centenas de testes que quebram a cada refatoração (porque testam detalhes internos, não comportamento), testes unitários lentos por conectar ao banco, e nenhuma garantia de que os critérios de aceitação do negócio foram realmente testados.

**Quando usar:** O Agente Testing lê este arquivo antes de gerar qualquer teste. Consulte também quando revisar a qualidade dos testes gerados.

**A [Pirâmide de Testes](#pirâmide-de-testes):**

```
           /\
          /E2E\          ← 5–10% dos testes
         /------\          Fluxos críticos completos
        /Integra-\       ← 20–30%
       / ção Tests \       Repositórios, endpoints, integrações
      /-------------\
     /  Unit  Tests  \   ← 60–70%
    /                 \    Domínio puro, use cases com repositórios em memória
   /___________________\
```

**O que testar em cada camada:**

| Camada | O que testar | Exemplo |
|---|---|---|
| Domain (unit) | Invariantes de entidades, validações de Value Objects, transições de estado | `ActionPlan_Complete_WhenAllTasksDone_ShouldTransitionToCompleted` |
| Application (unit) | Orquestração do Use Case (chama repositório certo? emite evento certo?) | `CreateActionPlanUseCase_Execute_ShouldPersistAndEmitEvent` |
| Application Jobs (unit) | Idempotência, isolamento de falha por tenant, comportamento sem tenants ativos | `RenewSubscriptionsJob_Execute_WhenAlreadyRenewed_ShouldSkip` |
| Infrastructure (integration) | Repositórios contra banco real, mapeamento [ORM](#orm--object-relational-mapper), isolamento de tenant | `ActionPlanRepository_FindById_ShouldNotReturnOtherTenantData` |
| Presentation (integration) | Status HTTP, body da resposta, autenticação, validação de input | `POST_action_plans_ShouldReturn201_WithValidBody` |
| E2E | Fluxos completos: criar plano → adicionar tarefas → concluir | `ActionPlan_FullLifecycle_CreateToComplete` |

**[InMemoryRepository](#inmemoryrepository) — o padrão para testes unitários:**

Em vez de conectar ao banco de dados em testes unitários, você cria uma implementação falsa do repositório que armazena dados em memória:

```typescript
// tests/helpers/in-memory-action-plan-repository.ts
class InMemoryActionPlanRepository implements IActionPlanRepository {
  private plans = new Map<string, ActionPlan>()

  async findById(id: ActionPlanId, tenantId: TenantId): Promise<ActionPlan | null> {
    const plan = this.plans.get(id.value)
    if (!plan || !plan.tenantId.equals(tenantId)) return null
    return plan
  }

  async save(plan: ActionPlan): Promise<void> {
    this.plans.set(plan.id.value, plan)
  }
}

// Uso no teste:
const repo = new InMemoryActionPlanRepository()
const useCase = new CreateActionPlanUseCase(repo, mockEventBus)
const result = await useCase.execute(command)
```

**Nomenclatura obrigatória:**
```
[UnidadeSobTeste]_[Cenário]_[ComportamentoEsperado]

Exemplos:
ActionPlan_Complete_WhenAllTasksDone_ShouldTransitionToCompleted
ActionPlan_Complete_WhenHasPendingTasks_ShouldReturnError
CreateActionPlanUseCase_Execute_ShouldPersistActionPlan
POST_action_plans_WithoutToken_ShouldReturn401
```

---

#### Exemplo: AçãoPlus — TESTING_GUIDE.md

Os testes do AçãoPlus seguirão esta estrutura de pastas:

```
tests/
├── unit/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── action-plan.test.ts     ← testa entidade ActionPlan
│   │   │   └── task.test.ts            ← testa entidade Task
│   │   └── value-objects/
│   │       ├── deadline.test.ts        ← valida regras de prazo
│   │       └── budget.test.ts          ← valida regras de orçamento
│   └── application/
│       └── commands/
│           ├── create-action-plan.test.ts
│           └── complete-task.test.ts
├── integration/
│   ├── infrastructure/
│   │   └── repositories/
│   │       └── action-plan-repository.test.ts
│   └── presentation/
│       └── action-plans.controller.test.ts
└── e2e/
    └── action-plan-lifecycle.test.ts
```

---

### 3.5 SAAS_PATTERNS.md — Padrões Específicos de SaaS

**O que é:** Referência de padrões arquiteturais específicos para produtos SaaS: [multi-tenancy](#multi-tenant), ciclo de vida de assinaturas, feature flags, billing, LGPD/GDPR, onboarding e rate limiting.

**Por que fazer:**
Desenvolver SaaS tem particularidades que não existem em sistemas internos. Se a IA não conhecer estes padrões, ela cria código que não isola dados entre clientes, não respeita o plano de cada tenant, ou não cumpre requisitos legais de privacidade.

**O que acontece se não fizer:**
O código gerado mistura dados de clientes diferentes (violação crítica de segurança e privacidade), cobra clientes errados ou não cobra, não respeita limites de plano (qualquer usuário usa feature Pro de graça), e não cumpre LGPD — problemas que são muito caros de corrigir depois que o sistema está em produção com clientes reais.

**Quando usar:**
- Ao modelar qualquer domínio [multi-tenant](#multi-tenant) (consulte antes do [SPRINT](#sprint) 1)
- Ao implementar o domínio de billing e subscription
- Ao implementar onboarding (criação de novo tenant)
- Ao implementar GDPR/LGPD (exportação e exclusão de dados)

**Padrões cobertos:**

| Padrão | O que define |
|---|---|
| **Row-level isolation** | Toda tabela tem `tenant_id`; todo repositório filtra por `tenantId` |
| **[TenantContext](#tenantcontext)** | Como o `tenantId` flui da requisição HTTP até o repositório via injeção de dependência |
| **Subscription lifecycle** | Estados: `trialing → active → past_due → cancel_at_period_end → canceled` |
| **Feature Flags** | Interface `IFeatureFlagService` no domínio; implementação na infraestrutura |
| **Billing patterns** | Flat-rate, seat-based, usage-based — interface `IPaymentGateway` |
| **Onboarding** | Fluxo atômico de criação de Tenant + Admin + Workspace + Trial (via [Unit of Work](#unit-of-work)) |
| **LGPD/GDPR** | Soft delete com comportamento explícito do repositório, anonimização de PII, exportação de dados |
| **Rate Limiting** | Por tenant, por plano, por feature — headers X-RateLimit-* |
| **Background Jobs [multi-tenant](#multi-tenant)** | Padrão de iteração por tenant com [TenantContext](#tenantcontext) isolado por iteração; idempotência obrigatória |

**[TenantContext](#tenantcontext) — como funciona:**

```
Requisição HTTP chega
       ↓
Middleware extrai tenantId do JWT (claim "tenant_id")
       ↓
TenantContext é registrado no container DI (escopo: requisição)
       ↓
Use Case recebe TenantContext pelo construtor (DI)
       ↓
Repositório recebe TenantContext pelo construtor (DI)
       ↓
Toda query filtra automaticamente por tenantId
```

Isso significa que o `tenantId` nunca é passado como parâmetro de método — ele está disponível automaticamente para qualquer repositório ou use case que precisar.

---

#### Exemplo: AçãoPlus — SAAS_PATTERNS.md

O AçãoPlus usa row-level isolation: toda tabela (`action_plans`, `tasks`, `team_members`) terá a coluna `tenant_id UUID NOT NULL`.

O ciclo de assinatura do AçãoPlus:
- Novo tenant começa em `trialing` (14 dias grátis)
- Após trial, precisa adicionar cartão para ir para `active`
- Se pagamento falhar, vai para `past_due` (acesso degradado por 7 dias)
- Se não resolver, `canceled` (apenas leitura)

Feature flags do AçãoPlus:
- `EXPORT_PDF` — disponível apenas no plano Pro e acima
- `TEAM_MEMBERS` — limitado por plano (Free: 3, Pro: ilimitado)
- `ADVANCED_REPORTS` — apenas plano Enterprise

---

### 3.6 GLOSSARY_TEMPLATE.md — Ubiquitous Language

**O que é:** Template para documentar o vocabulário do domínio de cada SaaS. Define quais termos usar no código, quais evitar, e o mapa de [bounded contexts](#bounded-context-contexto-delimitado).

**Por que fazer:**
A IA tende a usar termos genéricos (`User`, `Record`, `Manager`, `Data`) que criam ambiguidade e violam o [DDD](#domain-driven-design-ddd). Com o Glossário preenchido, a IA usa os termos corretos do negócio em todo o código gerado — e você entende o código sem precisar decifrar o que cada variável significa.

**O que acontece se não fizer:**
Em 20 SPECs sem GLOSSARY, você terá: `User` em billing significando uma coisa, `User` em auth significando outra, `UserPlan` e `Plan` e `Subscription` para o mesmo conceito. Corrigir isso exige renomear centenas de arquivos e atualizar o banco de dados — um trabalho que poderia ter sido evitado com 30 minutos de preenchimento inicial.

**Quando usar:**
- **Antes de criar o primeiro SPEC** de qualquer [bounded context](#bounded-context-contexto-delimitado) do projeto
- Forneça ao Agente Spec junto com o ARCHITECTURE.md *(veja "Como fornecer" abaixo)*
- Atualize sempre que novos termos forem descobertos durante o desenvolvimento *(veja "Como atualizar" abaixo)*

> **Como fornecer ao Agente Spec:**
> Se estiver usando o slash command `/new-spec`, o Claude Code lerá automaticamente o `@ARCHITECTURE.md` definido no `CLAUDE.md`. Para incluir o `GLOSSARY.md` automaticamente em toda sessão, adicione esta linha no seu `CLAUDE.md`:
> ```
> @specs/[dominio-principal]/GLOSSARY.md
> ```
> Se preferir fornecer manualmente: no chat do Claude Code, antes de digitar `/new-spec`, escreva:
> "Leia também o conteúdo de `specs/[dominio]/GLOSSARY.md`."
> Ou arraste o arquivo diretamente para a janela do chat do Claude Code.

> **Como atualizar o GLOSSARY quando novos termos surgem:**
> Durante a revisão de um SPEC ([Fase 3](#fase-3-revisar-e-aprovar-o-spec)), se o Agente Spec usar um termo que não está no GLOSSARY:
> 1. Abra `specs/[dominio]/GLOSSARY.md` no VS Code
> 2. Localize a tabela do [bounded context](#bounded-context-contexto-delimitado) correspondente
> 3. Adicione uma nova linha com: termo, definição de negócio, termos a evitar, exemplo de uso
> 4. Atualize o campo `Atualizado em:` no cabeçalho do arquivo
> 5. Na próxima sessão com o Agente Spec, o GLOSSARY atualizado já estará disponível automaticamente

**Como usar:**

> **Quando fazer o passo 1 abaixo:** Execute logo após o [Passo 3 (criar CLAUDE.md)](#passo-3-criar-o-claudemd) e **ANTES** de criar qualquer SPEC. Este é o [Passo 4](#passo-4-criar-o-glossarymd-do-projeto) da preparação do projeto.

1. No terminal, dentro da pasta do seu projeto, execute:
   ```bash
   mkdir -p specs/[dominio-principal]
   cp GLOSSARY_TEMPLATE.md specs/[dominio-principal]/GLOSSARY.md
   ```
   Substitua `[dominio-principal]` pelo nome do seu [bounded context](#bounded-context-contexto-delimitado) principal. Para o AçãoPlus seria `action-plan`.

2. Abra `specs/[dominio-principal]/GLOSSARY.md` no VS Code e preencha o mapa de [bounded contexts](#bounded-context-contexto-delimitado). Veja o [exemplo preenchido do AçãoPlus](#exemplo-açãoplus--fase-1) para entender como preencher cada seção.

3. Para cada [bounded context](#bounded-context-contexto-delimitado), preencha a tabela de termos com: o termo que será usado no código, sua definição de negócio, os termos que devem ser **evitados** e um exemplo de uso no código.

4. Inclua os termos comuns SaaS (já pré-preenchidos no template): `Tenant`, `Subscription`, `Plan`, `Invoice`, etc.

5. Documente termos proibidos (o que NÃO usar) com a alternativa correta.

**Estrutura do Glossário:**

```
GLOSSARY.md
├── 1. Mapa de Bounded Contexts   ← diagrama ASCII das relações
├── 2. Glossário por Context      ← tabela: termo → definição → evitar → uso
├── 3. Termos SaaS Comuns         ← Tenant, Subscription, Plan, etc. (pré-preenchidos)
├── 4. Convenções de Nomenclatura ← PascalCase, [Entidade][Verbo], etc.
├── 5. Termos Proibidos           ← User (em billing), Record, Data, Manager, etc.
└── 6. Changelog                  ← registro de renomeações que impactam o código
```

---

#### Exemplo: AçãoPlus — GLOSSARY.md Preenchido

O arquivo `specs/action-plan/GLOSSARY.md` do AçãoPlus completo está demonstrado na [Fase 1](#exemplo-açãoplus--fase-1) da seção 5, com todas as seções preenchidas — incluindo o mapa de bounded contexts, tabela de termos de cada contexto, termos proibidos e convenções de nomenclatura.

A tabela do [bounded context](#bounded-context-contexto-delimitado) `action-plan` contém:

| Termo (use no código) | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **ActionPlan** | Conjunto de ações 5W2H com objetivo e prazo definidos | Plan, Project, Record | Entidade: `ActionPlan`, Evento: `ActionPlanCreated` |
| **Task** | Uma ação específica dentro de um ActionPlan, respondendo as 7 perguntas 5W2H | Item, Activity, Record | Entidade: `Task`, Evento: `TaskCompleted` |
| **Responsible** | Pessoa responsável pela execução de uma Task | Owner, User, Assignee | Value Object: `Responsible` |
| **Deadline** | Prazo de execução de uma Task (data + contexto) | DueDate, Date, Expiry | Value Object: `Deadline` |
| **Budget** | Custo estimado e real de uma Task | Cost, Value, Amount | Value Object: `Budget` |
| **ActionPlanStatus** | Estado atual de um ActionPlan (draft, active, completed, archived) | Status, State | Value Object: `ActionPlanStatus` |
| **TeamMember** | Conta de usuário com acesso a um Workspace específico | User, Member, Account | Entidade: `TeamMember` |

---

## 4. Preparando um Novo Projeto SaaS

Siga estes passos ao iniciar qualquer novo projeto SaaS com o kit. Cada passo referencia o anterior — execute nesta ordem.

---

### Passo 1: Criar a estrutura de pastas

**O que fazer:**
Você vai criar as pastas do projeto manualmente. Abra o terminal no local onde quer criar o projeto e execute os comandos abaixo.

**Por que fazer:**
Esta estrutura de pastas espelha exatamente as camadas da [Clean Architecture](#clean-architecture). Se você criar pastas com nomes diferentes (ex: `controllers/` em vez de `presentation/`), a IA não saberá onde colocar cada arquivo e começará a criar estruturas aleatórias.

**O que acontece se não fizer:**
Sem a estrutura correta, o ARCHITECTURE.md perde validade — a IA não consegue seguir as regras de onde cada arquivo deve estar. O código começa a se acumular em pastas genéricas como `src/` sem separação de camadas.

Execute no terminal:
```bash
# Criar a pasta raiz e entrar nela (substitua "meu-saas" pelo nome do seu projeto)
mkdir meu-saas
cd meu-saas

# Criar toda a estrutura de uma vez
mkdir -p src/presentation
mkdir -p src/application
mkdir -p src/domain
mkdir -p src/infrastructure
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e
mkdir -p specs
mkdir -p .claude/commands
```

> Pasta criada. Agora abra a pasta do projeto no VS Code com o comando:
> ```bash
> code .
> ```
> (Se o VS Code não abrir, abra manualmente: File → Open Folder → selecione `meu-saas/`)

A estrutura que você terá:
```
meu-saas/
├── .claude/
│   └── commands/           ← slash commands do Claude Code (criados no Passo 5)
├── src/
│   ├── presentation/
│   ├── application/
│   ├── domain/
│   └── infrastructure/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── specs/                  ← todos os SPECs do projeto ficam aqui
```

---

### Passo 2: Copiar os arquivos do kit

**O que fazer:**
Copie os 6 arquivos do kit para a raiz do seu projeto. Eles são a base arquitetural.

**Por que fazer:**
Estes 6 arquivos precisam estar na raiz do projeto porque o Claude Code os lê automaticamente via o `CLAUDE.md`. Se ficarem em outro lugar, a IA não os encontrará.

**O que acontece se não fizer:**
Sem os arquivos do kit, cada sessão com a IA começa do zero — você precisará re-explicar toda a arquitetura, os padrões de erro, as regras de [multi-tenancy](#multi-tenant) e os padrões de testes a cada nova conversa.

No terminal, dentro da pasta `meu-saas/`, execute (ajuste o caminho `../kit/` para onde você salvou os arquivos do kit):
```bash
cp /caminho/para/o/kit/ARCHITECTURE.md .
cp /caminho/para/o/kit/AGENTS.md .
cp /caminho/para/o/kit/SPEC_TEMPLATE.md .
cp /caminho/para/o/kit/TESTING_GUIDE.md .
cp /caminho/para/o/kit/SAAS_PATTERNS.md .
cp /caminho/para/o/kit/GLOSSARY_TEMPLATE.md .
```

> Arquivos copiados. No VS Code você verá os 6 arquivos na raiz do projeto. Verifique com `ls` no terminal.

---

### Passo 3: Criar o CLAUDE.md

**O que fazer:**
Crie manualmente o arquivo `CLAUDE.md` na raiz do projeto. Este arquivo é lido pelo Claude Code automaticamente a cada sessão.

**Por que fazer:**
O `CLAUDE.md` é a "memória permanente" do projeto para o Claude Code. Sem ele, cada nova sessão começa sem contexto — você precisa repetir as tecnologias, as regras e os comandos disponíveis.

**O que acontece se não fizer:**
O Claude Code não saberá nada sobre o seu projeto: qual tecnologia usa, quais bounded contexts existem, quais regras seguir. Você vai ficar digitando o mesmo contexto no início de cada sessão.

No VS Code, clique com o botão direito na raiz do projeto → **New File** → Digite `CLAUDE.md` → Pressione Enter.

Cole o conteúdo abaixo e salve com **Ctrl+S**:

```markdown
# CLAUDE.md — [Nome do Projeto]

## Arquitetura
Leia ARCHITECTURE.md antes de qualquer ação. Este projeto segue MVC + Clean Architecture + DDD com SDD via spec-kit.

## Regras obrigatórias
- Nunca escreva código sem SPEC aprovado em specs/
- Sempre siga a ordem Domain-First nos SPRINTs
- Consulte specs/[dominio]/GLOSSARY.md para nomenclatura correta

## Contexto automático — leia estes arquivos antes de qualquer ação
@ARCHITECTURE.md — Constituição do projeto (obrigatório em toda sessão)
@specs/[dominio-principal]/GLOSSARY.md — Vocabulário do domínio

## Comandos disponíveis
- /new-spec — cria novo SPEC
- /impl-sprint — implementa SPRINT
- /review-arch — executa Analyze ou Review
- /test-sprint — gera testes do SPRINT
- /migrate-sprint — gera migration de banco

## Tecnologias deste projeto
- Linguagem: [TypeScript / Python / etc.]
- Framework: [NestJS / FastAPI / etc.]
- ORM: [Prisma / SQLAlchemy / etc.]
- Banco: [PostgreSQL / MySQL / etc.]
```

> CLAUDE.md criado. Lembre de substituir `[Nome do Projeto]`, `[dominio-principal]` e as tecnologias pelos valores reais do seu projeto.

---

### Passo 4: Criar o GLOSSARY.md do projeto

**O que fazer:**
Copie o `GLOSSARY_TEMPLATE.md` para dentro da pasta `specs/` e preencha com os termos do seu domínio.

**Por que fazer:**
Este arquivo ensina à IA o vocabulário específico do seu negócio. Sem ele, a IA inventa nomes genéricos que criam confusão no código.

**O que acontece se não fizer:**
Veja ["O que acontece se não fizer" na seção 3.6](#36-glossary_templatemd--ubiquitous-language) — é o mesmo risco, e o custo de corrigir depois é muito maior do que preencher agora.

Execute no terminal (dentro da pasta `meu-saas/`):
```bash
# Crie a pasta do seu bounded context principal (ex: action-plan, billing, tasks, etc.)
mkdir -p specs/[dominio-principal]

# Copie o template e renomeie para GLOSSARY.md
cp GLOSSARY_TEMPLATE.md specs/[dominio-principal]/GLOSSARY.md
```

> Arquivo copiado. Abra `specs/[dominio-principal]/GLOSSARY.md` no VS Code e preencha:
> 1. O mapa de [bounded contexts](#bounded-context-contexto-delimitado) (quais domínios seu SaaS tem e como se relacionam)
> 2. Os termos do domínio principal
> 3. Os termos SaaS comuns já pré-preenchidos no template — revise se fazem sentido para o seu projeto

**Regra:** Preencha o GLOSSARY antes de criar o primeiro SPEC. Não inverta esta ordem.

---

### Passo 5: Criar os slash commands (veja [seção 7](#7-configurando-os-agentes-como-slash-commands))

**O que fazer:**
Copie os arquivos de comando da pasta `Slash Commands/` do kit para `.claude/commands/` do seu projeto.

**Por que fazer:**
Os slash commands transformam comandos longos em atalhos de uma linha. Em vez de copiar e colar prompts inteiros, você digita `/new-spec [descrição]` e o agente correto é acionado com o contexto certo.

**O que acontece se não fizer:**
Você precisará abrir o `AGENTS.md`, copiar o prompt do agente manualmente, colar no chat, adicionar o contexto — toda vez que quiser usar um agente. É funcional, mas demorado e sujeito a esquecer algum contexto obrigatório.

Execute no terminal (dentro da pasta `meu-saas/`), ajustando o caminho do kit:
```bash
# Copie os 5 arquivos de comando para .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/new-spec.md .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/impl-sprint.md .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/review-arch.md .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/test-sprint.md .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/migrate-sprint.md .claude/commands/
```

> Comandos copiados. Verifique no terminal: `ls .claude/commands/`
> Você deve ver: `new-spec.md`, `impl-sprint.md`, `review-arch.md`, `test-sprint.md`, `migrate-sprint.md`
>
> Se quiser confirmar que funcionam, abra o Claude Code no projeto e digite `/` — os comandos aparecerão na lista de sugestões.

Para instruções detalhadas sobre como criar ou personalizar os comandos, veja a [seção 7](#7-configurando-os-agentes-como-slash-commands).

---

### Exemplo: AçãoPlus — Preparação do Projeto

```
acaoplus/
├── .claude/
│   └── commands/           ← 5 arquivos copiados de "Slash Commands/"
│       ├── new-spec.md
│       ├── impl-sprint.md
│       ├── review-arch.md
│       ├── test-sprint.md
│       └── migrate-sprint.md
├── src/
│   ├── presentation/
│   ├── application/
│   ├── domain/
│   └── infrastructure/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── specs/
│   └── action-plan/
│       └── GLOSSARY.md     ← preenchido com os termos do AçãoPlus (ver Fase 1)
├── ARCHITECTURE.md
├── AGENTS.md
├── SPEC_TEMPLATE.md
├── TESTING_GUIDE.md
├── SAAS_PATTERNS.md
├── GLOSSARY_TEMPLATE.md
└── CLAUDE.md
```

**CLAUDE.md do AçãoPlus:**
```markdown
# CLAUDE.md — AçãoPlus

## Arquitetura
Leia ARCHITECTURE.md antes de qualquer ação. SaaS multi-tenant de gestão de planos de ação 5W2H.

## Regras obrigatórias
- Nunca escreva código sem SPEC aprovado em specs/
- Consulte specs/action-plan/GLOSSARY.md para nomenclatura
- Domínio multi-tenant: sempre use TenantContext (consulte SAAS_PATTERNS.md)

## Contexto automático
@ARCHITECTURE.md
@specs/action-plan/GLOSSARY.md

## Tecnologias
- TypeScript + NestJS
- Prisma ORM
- PostgreSQL
- Jest (testes)

## Bounded Contexts
- auth — autenticação e sessões
- tenant — onboarding e team members
- action-plan — core do produto: ActionPlan, Task
- billing — Subscription, Invoice, Plan
```

---

## 5. Fluxo Completo de Desenvolvimento

Esta seção descreve o ciclo completo do zero até uma feature funcionando, passo a passo.

---

### Fase 0: Concepção da Ideia

**O que fazer:**
1. Defina o problema que o SaaS resolve em uma frase
2. Identifique o público-alvo
3. Liste as features principais (não mais de 5 para o MVP)
4. Identifique os [bounded contexts](#bounded-context-contexto-delimitado) (domínios do negócio)

**Por que fazer:**
Sem esta etapa, você começa a criar SPECs sem saber o escopo do produto. A IA precisa saber qual é o negócio central do SaaS para criar [bounded contexts](#bounded-context-contexto-delimitado) corretos e usar a [Ubiquitous Language](#ubiquitous-language-linguagem-ubíqua) adequada.

**O que acontece se não fizer:**
Você começa criando SPECs isolados sem conexão entre si. Depois de 3 features, percebe que os [bounded contexts](#bounded-context-contexto-delimitado) estão errados e precisa refatorar tudo. Esta etapa leva 30 minutos e economiza dias de retrabalho.

**Como identificar [bounded contexts](#bounded-context-contexto-delimitado):**
Pergunte: "Quais são as áreas de negócio independentes do meu SaaS?" Cada área que tem seu próprio vocabulário, regras e ciclo de vida é um [bounded context](#bounded-context-contexto-delimitado).

```
Sinais de um bounded context:
- Tem entidades próprias (não compartilhadas com outros contextos)
- Tem regras de negócio próprias
- Poderia ser um time separado cuidando dele
- Comunica-se com os outros via eventos, não chamadas diretas
```

**Mapa de bounded contexts — como desenhar:**

```
┌────────────┐  UserJoined    ┌─────────────────┐
│    auth    │ ────────────→  │     tenant      │
│  Account   │                │  Tenant,        │
│  Session   │                │  TeamMember     │
└────────────┘                └────────┬────────┘
                                       │ TenantCreated
                                       ▼
                              ┌─────────────────┐
                              │  action-plan    │
                              │  ActionPlan,    │
                              │  Task           │
                              └────────┬────────┘
                                       │
┌────────────┐  SubscriptionActivated  │
│  billing   │ ◄───────────────────────┘
│  Subscr.   │  (feature flags por plano)
│  Invoice   │
└────────────┘
```

---

#### Exemplo: AçãoPlus — Fase 0

**Problema:** Equipes de gestão criam planos de ação no Excel e perdem o controle de execução.

**Público:** Gestores de equipe em empresas de médio porte.

**Features MVP:**
1. Criar e gerenciar planos de ação 5W2H
2. Atribuir tarefas a membros da equipe
3. Acompanhar status de cada tarefa
4. Dashboard de progresso por plano
5. Exportar plano em PDF (feature do plano Pro)

**[Bounded contexts](#bounded-context-contexto-delimitado):**
- `auth` — autenticação (login, cadastro, recuperação de senha)
- `tenant` — onboarding, team members, workspaces
- `action-plan` — o core: ActionPlan, Task, relatórios
- `billing` — Subscription, Plan, Invoice

---

### Fase 1: Preencher o GLOSSARY.md

**O que fazer:**
1. O arquivo `specs/[dominio-principal]/GLOSSARY.md` já foi criado no [Passo 4](#passo-4-criar-o-glossarymd-do-projeto) da preparação. Abra-o agora no VS Code.
2. Preencha o mapa de [bounded contexts](#bounded-context-contexto-delimitado) usando o diagrama ASCII que você desenhou na Fase 0
3. Para cada [bounded context](#bounded-context-contexto-delimitado), preencha a tabela de termos
4. Defina quais termos são proibidos (evite User, Record, Data, Manager)
5. Defina as convenções de nomenclatura do projeto

**Por que fazer:**
Se você criar um SPEC sem o GLOSSARY, o Agente Spec inventará nomes. Depois de 10 SPECs com nomes diferentes para o mesmo conceito, o código fica inconsistente e difícil de manter.

**O que acontece se não fizer:**
A IA usa termos genéricos que não refletem o negócio: `User` em vez de `TeamMember`, `Plan` em vez de `ActionPlan`, `Item` em vez de `Task`. Quando você lê o código depois, não consegue entender o que cada entidade representa no contexto do negócio. E quando pede à IA para modificar algo, ela fica confusa sobre qual `User` você está falando.

**Dica:** Você não precisa preencher o GLOSSARY completo antes de começar. Preencha o [bounded context](#bounded-context-contexto-delimitado) que vai trabalhar primeiro e adicione os outros à medida que avançar.

---

#### Exemplo: AçãoPlus — Fase 1

Arquivo `specs/action-plan/GLOSSARY.md` do AçãoPlus, completo e preenchido:

```markdown
# GLOSSARY: AçãoPlus

**Projeto:** AçãoPlus — SaaS de Gestão de Planos de Ação 5W2H
**Versão:** 1.0
**Atualizado em:** 2025-04-07

---

## Instrução para IA

Ao receber este arquivo, use **exclusivamente** os termos definidos aqui para nomear
entidades, eventos, comandos, queries, value objects e serviços. Se precisar de um
conceito não listado, pergunte antes de inventar um nome.

---

## 1. Mapa de Bounded Contexts

┌────────────┐  UserJoined    ┌─────────────────┐
│    auth    │ ────────────→  │     tenant      │
│  Account   │                │  Tenant,        │
│  Session   │                │  TeamMember     │
└────────────┘                └────────┬────────┘
                                       │ TenantCreated
                                       ▼
                              ┌─────────────────┐
                              │  action-plan    │
                              │  ActionPlan,    │
                              │  Task           │
                              └────────┬────────┘
                                       │
┌────────────┐  SubscriptionActivated  │
│  billing   │ ◄───────────────────────┘
│  Subscr.   │
│  Invoice   │
└────────────┘

**Regra:** Contextos se comunicam via eventos — nunca compartilham entidades diretamente.

---

## 2. Glossário por Bounded Context

### 2.1 auth

| Termo | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **Account** | Identidade de um usuário no sistema com credenciais de acesso | User, Person, Profile | Entidade: `Account`, Evento: `AccountCreated` |
| **Session** | Sessão ativa de um Account autenticado | Token, Login, Auth | Value Object: `SessionToken` |
| **Role** | Conjunto de permissões dentro de um Tenant | Permission, Access, Level | Value Object: `Role` (admin, member, viewer) |
| **Credential** | Par email+senha de um Account | Password, Login, Auth | Value Object: `Credential` |

### 2.2 tenant

| Termo | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **Tenant** | Organização ou empresa que contrata o AçãoPlus | Company, Client, Customer, Organization | Entidade: `Tenant`, Evento: `TenantCreated` |
| **Workspace** | Ambiente de trabalho de um Tenant (um Tenant pode ter múltiplos) | Project, Space, Area | Entidade: `Workspace` |
| **TeamMember** | Conta de usuário (Account) com acesso a um Workspace | User, Member, Employee, Collaborator | Entidade: `TeamMember`, Evento: `TeamMemberInvited` |
| **Invitation** | Convite enviado a um email para entrar em um Workspace | Invite, Request, Email | Entidade: `Invitation` |

### 2.3 action-plan

| Termo | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **ActionPlan** | Conjunto de ações 5W2H com objetivo e prazo definidos | Plan, Project, Record, Document | Entidade: `ActionPlan`, Evento: `ActionPlanCreated` |
| **Task** | Uma ação específica dentro de um ActionPlan respondendo as 7 perguntas 5W2H | Item, Activity, Record, Todo, Step | Entidade: `Task`, Evento: `TaskCompleted` |
| **Responsible** | Pessoa responsável pela execução de uma Task | Owner, User, Assignee, Person | Value Object: `Responsible` |
| **Deadline** | Prazo de execução de uma Task (data + contexto) | DueDate, Date, Expiry, Limit | Value Object: `Deadline` |
| **Budget** | Custo estimado e real de uma Task (valor + moeda) | Cost, Value, Amount, Price | Value Object: `Budget` |
| **ActionPlanStatus** | Estado atual de um ActionPlan: draft, active, completed, archived | Status, State, Stage, Phase | Value Object: `ActionPlanStatus` |
| **TaskStatus** | Estado atual de uma Task: pending, in_progress, done, blocked | Status, State, Progress | Value Object: `TaskStatus` |
| **CompletionPercentage** | Percentual de Tasks com status "done" em um ActionPlan | Progress, Rate, Percentage | Calculado em `ActionPlan.completionPercentage` |

### 2.4 billing

| Termo | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **Subscription** | Contrato ativo entre um Tenant e um Plan, com ciclo de cobrança | UserPlan, Contract, License, Agreement | Entidade: `Subscription`, Evento: `SubscriptionActivated` |
| **Plan** | Conjunto de features e limites oferecido por um preço | Package, Bundle, Tier, Product | Entidade: `Plan` (free, pro, enterprise) |
| **Invoice** | Documento de cobrança gerado por ciclo de renovação | Bill, Receipt, Charge, Payment | Entidade: `Invoice`, Evento: `InvoiceIssued` |
| **Trial** | Período de 14 dias de uso gratuito do plano Pro | Demo, Test, Free, Sample | Value Object: `TrialPeriod` |

---

## 3. Termos SaaS Comuns (adaptados para AçãoPlus)

| Termo | Definição | Bounded Context |
|---|---|---|
| **Tenant** | Organização que contrata o AçãoPlus; unidade de isolamento de dados | tenant |
| **Account** | Usuário individual com credenciais de acesso | auth |
| **Subscription** | Contrato ativo de uso com ciclo de cobrança | billing |
| **Plan** | Conjunto de features por preço (Free, Pro, Enterprise) | billing |
| **Feature Flag** | Controla acesso a features por plano (ex: EXPORT_PDF só no Pro) | shared |
| **TenantContext** | Mecanismo que injeta o tenantId em toda operação de negócio | shared |
| **Unit of Work** | Agrupa operações de múltiplos repositórios em uma transação | shared |

---

## 4. Convenções de Nomenclatura

- **Entidades:** PascalCase, substantivo singular — `ActionPlan`, `Task`, `TeamMember`
- **Value Objects:** PascalCase, substantivo — `Deadline`, `Budget`, `Responsible`
- **Eventos de Domínio:** [Entidade][VerboPasado] — `ActionPlanCreated`, `TaskCompleted`
- **Use Cases (Commands):** [Verbo][Entidade]UseCase — `CreateActionPlanUseCase`, `CompleteTaskUseCase`
- **Use Cases (Queries):** Get[Entidade]Query, List[Entidade]sQuery — `GetActionPlanQuery`
- **Repositórios (interface):** I[Entidade]Repository — `IActionPlanRepository`
- **Repositórios (implementação):** Prisma[Entidade]Repository — `PrismaActionPlanRepository`
- **Arquivos:** kebab-case — `action-plan.ts`, `create-action-plan-use-case.ts`

---

## 5. Termos Proibidos

| Termo proibido | Usar em vez disso | Contexto |
|---|---|---|
| `User` (em qualquer bounded context) | `Account` (auth), `TeamMember` (tenant) | Ambíguo — não reflete o papel no negócio |
| `Project` | `ActionPlan` | "Projeto" é diferente de "Plano de Ação" no negócio |
| `Item`, `Record`, `Data` | `Task`, `ActionPlan` | Genérico — sem significado de negócio |
| `Manager` | Use o caso de uso específico | Anti-pattern DDD: cria classe "faz-tudo" |
| `UserPlan`, `UserSubscription` | `Subscription` | O contrato é do Tenant, não do User |

---

## 6. Changelog

| Data | Termo alterado | De → Para | Impacto |
|---|---|---|---|
| 2025-04-07 | Criação inicial | — | Todos os bounded contexts definidos |
```

---

### Fase 2: Criar o primeiro SPEC com o Agente Spec

**O que fazer:**
Acione o Agente Spec com uma descrição da feature em linguagem natural. O agente gerará um SPEC completo seguindo o `SPEC_TEMPLATE.md`.

**Por que fazer:**
O SPEC é o contrato entre o que você quer e o que a IA vai implementar. Sem ele, a IA implementa o que acha que você quer — e você só descobre que está errado quando o código já está pronto.

**O que acontece se não fizer:**
A IA implementa diretamente sem especificação. Sem [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais), ela não considera performance. Sem [Given-When-Then](#given-when-then-gwt), ela não gera testes adequados. Sem a seção Clarify, ela assume respostas para perguntas que só você pode responder — e assume errado 30% das vezes.

**Contexto a fornecer:**
```
- ARCHITECTURE.md (seções 0–3)
- SPEC_TEMPLATE.md
- specs/[dominio]/GLOSSARY.md do projeto
- Descrição da feature em linguagem natural
```

**Comando:**
```
/new-spec [descrição da feature]
```

**Ou manualmente, abra uma nova conversa no Claude Code e forneça:**
```
[Cole o conteúdo do ARCHITECTURE.md seções 0–3]
[Cole o conteúdo do SPEC_TEMPLATE.md]
[Cole o conteúdo do GLOSSARY.md]

Agente Spec: gere um SPEC para a feature a seguir.
Bounded context: action-plan

Feature: Criar um plano de ação 5W2H. O usuário deve poder definir um título, 
uma descrição opcional, e adicionar tarefas respondendo as 7 perguntas 5W2H 
(O quê, Por quê, Quem, Onde, Quando, Como, Quanto). O plano deve ser associado 
ao tenant do usuário logado.
```

**O que revisar no SPEC gerado:**
- Seção **Clarify**: todas as ambiguidades identificadas estão listadas? Você consegue respondê-las?
- **User Stories**: fazem sentido para o negócio? Estão priorizadas corretamente?
- **[NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais)**: têm critérios de aceitação mensuráveis?
- **Critérios de Aceitação**: os [Given-When-Then](#given-when-then-gwt) descrevem o comportamento esperado?
- **[SPRINTs](#sprint)**: a divisão Domain-First faz sentido? Todos os FRs estão cobertos?

---

#### Exemplo: AçãoPlus — SPEC de "Criar Plano de Ação" (resumo)

```markdown
# SPEC: Criar Plano de Ação 5W2H

**Bounded Context:** action-plan
**Status:** rascunho
**Depende de:** specs/auth/login.md, specs/tenant/create-workspace.md

## User Stories
| ID  | Prioridade | Story |
| US-01 | P1 | Como gestor, quero criar um plano de ação 5W2H com título e descrição, para organizar as ações da minha equipe |
| US-02 | P1 | Como gestor, quero adicionar tarefas ao plano respondendo as 7 perguntas 5W2H, para que cada ação tenha clareza de execução |
| US-03 | P2 | Como gestor, quero ver o progresso do plano em % de tarefas concluídas, para acompanhar a execução |

## NFRs
| ID | Categoria | Requisito | Critério de Aceitação |
| NFR-001 | Performance | Criação de plano retorna em até 300ms | Medido com 1.000 planos no banco |
| NFR-002 | Segurança | Apenas membros do tenant podem acessar seus planos | Teste de autorização: tenant B não acessa dados do tenant A |

## Requisitos Funcionais
| ID | Descrição | User Story | Prioridade |
| FR-001 | Sistema cria ActionPlan com título, descrição opcional e status "draft" | US-01 | P1 |
| FR-002 | Sistema associa ActionPlan ao TenantId do usuário logado | US-01 | P1 |
| FR-003 | Sistema adiciona Task ao ActionPlan com as 7 respostas 5W2H | US-02 | P1 |
| FR-004 | Sistema calcula % de conclusão baseada nas Tasks com status "done" | US-03 | P2 |

## Contexto Arquitetural
| Campo | Valor |
| Multi-tenant | sim |
| Eventos gerados | ActionPlanCreated, TaskAdded |
| PII envolvido | Responsible (nome da pessoa responsável) |
| Feature flags | nenhuma |

## SPRINT 1 — Domínio
**Entidades:**
- ActionPlan: id, tenantId, title, description, status, completionPercentage, createdAt
- Task: id, actionPlanId, what, why, who (Responsible), where, when (Deadline), how, howMuch (Budget), status

**Value Objects:**
- ActionPlanId, TaskId, ActionPlanStatus, TaskStatus, Responsible, Deadline, Budget

**Eventos:**
- ActionPlanCreated: { actionPlanId, tenantId, title }
- TaskAdded: { taskId, actionPlanId, what }

**Interface de Repositório:**
interface IActionPlanRepository {
  findById(id: ActionPlanId, tenantId: TenantId): Promise<ActionPlan | null>
  save(plan: ActionPlan): Promise<void>
  findByTenant(tenantId: TenantId, pagination: Pagination): Promise<ActionPlan[]>
}

**Impacto em Banco:**
| Tabela | Operação | Colunas principais |
| action_plans | CREATE | id UUID, tenant_id UUID NOT NULL, title TEXT, description TEXT, status VARCHAR, created_at TIMESTAMP |
| tasks | CREATE | id UUID, action_plan_id UUID, tenant_id UUID, what TEXT, why TEXT, who TEXT, where TEXT, when_date DATE, how TEXT, how_much DECIMAL, status VARCHAR |
```

---

### Fase 3: Revisar e Aprovar o SPEC

**O que fazer:**
1. Leia o SPEC completo gerado pelo Agente Spec
2. Resolva todas as ambiguidades na seção **Clarify** (responda cada item na coluna "Decisão / Resposta")
3. Verifique se o **Checklist de Cobertura** pode ser marcado (todo FR tem User Story e [GWT](#given-when-then-gwt))
4. Ajuste qualquer User Story, FR ou cenário que não reflita corretamente o negócio
5. Altere o Status para `aprovado` e preencha a data

**Por que fazer:**
Você é o único que sabe as regras do seu negócio. A IA pode ter gerado FRs desnecessários (YAGNI), esquecido casos de borda importantes, ou assumido respostas erradas para as perguntas da seção Clarify. Se você aprovar um SPEC com ambiguidades, a IA vai implementar com base nas suposições dela — e você só descobre o erro no [SPRINT](#sprint) 4, quando o código já está pronto.

**O que acontece se não fizer:**
Avançar para implementação com SPEC incompleto é a principal causa de retrabalho em vibe coding. Problemas descobertos no [SPRINT](#sprint) 1 custam 1 hora para corrigir. Os mesmos problemas descobertos no [SPRINT](#sprint) 4 custam 1 dia — porque exigem mudanças em 4 camadas de código ao mesmo tempo.

**Regra importante:** Você é o árbitro. A IA pode ter gerado FRs desnecessários ([YAGNI](#yagni)) ou ter deixado ambiguidades. Não avance sem resolver.

**Sinais de que um SPEC não está pronto para aprovação:**
- Qualquer item em **Clarify** com "Decisão: pendente"
- Critérios de aceitação vagos ("o sistema deve funcionar corretamente")
- [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais) sem critério mensurável ("deve ser rápido")
- Mais de 5 FRs em P1 no mesmo SPEC (sintoma de SPEC grande demais — considere dividir)

---

#### Exemplo: AçãoPlus — Fase 3

Perguntas a fazer sobre o SPEC antes de aprovar:
- "FR-003 diz que todas as 7 respostas são obrigatórias. Mas na prática, `where` (Onde?) pode ser irrelevante para algumas ações. Confirme: as 7 respostas são obrigatórias ou opcionais?"
- "O cálculo de % (FR-004) considera tarefas arquivadas como concluídas?"
- "Quem pode criar planos? Qualquer membro do tenant ou apenas quem tem role de Gestor?"

Após responder estas perguntas, atualize a seção Clarify e aprove o SPEC.

---

### Fase 4: Validar com o Agente Analyze

**O que fazer:**
Após aprovar o SPEC, acione o Agente Analyze para validar a consistência interna antes de qualquer implementação.

**Por que fazer:**
Mesmo um SPEC bem escrito pode ter inconsistências sutis: um FR sem cenário [GWT](#given-when-then-gwt), um [SPRINT](#sprint) sem o FR correspondente, um [NFR](#nfrs--non-functional-requirements-requisitos-não-funcionais) sem critério mensurável. O Agente Analyze encontra esses problemas em segundos — e corrigi-los no SPEC é muito mais rápido do que corrigi-los no código.

**O que acontece se não fizer:**
O Agente Implementation encontra os problemas no meio da implementação e começa a tomar decisões sozinho para preencher as lacunas — muitas vezes de forma incorreta. Você descobre isso quando revisa o código e encontra comportamentos que não estavam no SPEC.

**Contexto a fornecer:**
```
- SPEC aprovado (arquivo completo)
- ARCHITECTURE.md (seções 1 e 5)
```

**Comando:**
```
/review-arch specs/action-plan/create-action-plan.md analyze
```

**O Agente Analyze verifica:**
- Todo FR está rastreado a pelo menos uma User Story?
- Todo FR tem pelo menos um cenário [GWT](#given-when-then-gwt)?
- Todo cenário é testável independentemente?
- Cada FR aparece em pelo menos um [SPRINT](#sprint)?
- Os FRs respeitam as regras críticas do ARCHITECTURE.md?
- Os [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais) têm critério mensurável?
- O Contrato de API cobre todos os FRs de apresentação?
- O Plano de Testes de cada [SPRINT](#sprint) cobre os cenários [GWT](#given-when-then-gwt)?
- As migrations cobrem todas as entidades?

**Como interpretar o resultado:**

```
PRONTO PARA IMPLEMENTAR
→ Execute /impl-sprint [spec] 1 para iniciar o SPRINT 1

REQUER CORREÇÃO NO SPEC
→ Corrija os itens listados no SPEC
→ Execute /review-arch [spec] analyze novamente
→ NÃO comece a implementar antes do veredicto PRONTO
```

---

#### Exemplo: AçãoPlus — Fase 4

Possíveis inconsistências que o Analyze encontraria:

- "FR-004 (calcular % de conclusão) não aparece em nenhum SPRINT. Adicione-o ao SPRINT 1 (como comportamento da entidade ActionPlan) ou ao SPRINT 2 (como query)."
- "O cenário GWT de FR-002 ('plano é associado ao tenant') não tem teste planejado no Plano de Testes do SPRINT 1. Adicione."
- "A tabela `tasks` no Impacto em Banco não tem índice em `action_plan_id`. Adicione na seção de migrations."

Após corrigir, o Analyze retornaria `PRONTO PARA IMPLEMENTAR`.

---

### Fase 5: Implementar SPRINT 1 — Domínio

**O que fazer:**
Acione o Agente Implementation para o [SPRINT](#sprint) 1. Ele implementa apenas o domínio: entidades, value objects, eventos e interfaces de repositório. Nenhuma conexão com banco, HTTP ou framework.

**Por que fazer:**
O domínio é o coração do software — é aqui que vivem as regras de negócio. Implementar o domínio primeiro, sem nenhuma dependência externa, garante que as regras estejam corretas antes de adicionar complexidade de banco e HTTP. Se a lógica de negócio do [SPRINT](#sprint) 1 estiver errada, é simples corrigir. Se estiver errada no [SPRINT](#sprint) 4, você precisa corrigir em 4 camadas ao mesmo tempo.

**O que acontece se não fizer:**
Se você pular o domínio e começar pelo banco ou pela API, a lógica de negócio acaba parar dentro do Controller ou nas migrations. Isso é uma violação crítica da Clean Architecture e o código se torna impossível de testar, reutilizar ou modificar sem quebrar outras partes.

**Contexto a fornecer:**
```
- ARCHITECTURE.md (seções 0–5)
- SPRINT 1 do SPEC (apenas a seção do SPRINT 1, não o SPEC inteiro)
```

**Comando:**
```
/impl-sprint specs/action-plan/create-action-plan.md 1
```

**O que esperar como saída:**

```
src/domain/action-plan/
├── entities/
│   ├── action-plan.ts          ← entidade ActionPlan com regras de negócio
│   └── task.ts                 ← entidade Task
├── value-objects/
│   ├── action-plan-id.ts
│   ├── action-plan-status.ts
│   ├── task-id.ts
│   ├── task-status.ts
│   ├── responsible.ts
│   ├── deadline.ts
│   └── budget.ts
├── events/
│   ├── action-plan-created.ts
│   └── task-added.ts
└── repositories/
    └── i-action-plan-repository.ts   ← apenas a interface, sem implementação
```

**[TDD](#tdd--test-driven-development) dentro do [SPRINT](#sprint):**
Para cada FR do SPRINT 1, o Agente Implementation segue o ciclo:
1. Lê o cenário [GWT](#given-when-then-gwt) do FR no Plano de Testes
2. Escreve o teste unitário correspondente (RED — falha esperada)
3. Implementa o mínimo para o teste passar (GREEN)
4. Refatora sem quebrar (REFACTOR)
5. Avança para o próximo FR

O Agente Testing ([Fase 6](#fase-6-gerar-testes-do-sprint-1-com-o-agente-testing)) valida a cobertura [GWT](#given-when-then-gwt) completa e complementa testes faltantes.

**Como verificar que o SPRINT 1 está correto:**
- Abra qualquer arquivo em `src/domain/` e verifique que não há `import` de arquivos de `infrastructure/`, [ORM](#orm--object-relational-mapper), banco, HTTP client, etc.
- As entidades têm comportamentos (métodos), não são apenas estruturas de dados ([POJOs/DTOs](#pojos--dtos))?
- Os Value Objects validam seus invariantes no construtor?
- Erros retornam [`Result<T, E>`](#padrão-result), não `null`?
- Cada comportamento implementado tem um teste unitário correspondente a um cenário [GWT](#given-when-then-gwt)?

---

#### Exemplo: AçãoPlus — SPRINT 1 (fragmento de código esperado)

```typescript
// src/domain/action-plan/entities/action-plan.ts

export class ActionPlan {
  private constructor(
    readonly id: ActionPlanId,
    readonly tenantId: TenantId,
    private _title: string,
    private _description: string | null,
    private _status: ActionPlanStatus,
    private _tasks: Task[],
    readonly createdAt: Date
  ) {}

  static create(props: CreateActionPlanProps): Result<ActionPlan, DomainError> {
    if (!props.title || props.title.trim().length === 0) {
      return Result.fail(new DomainError('ACTION_PLAN_TITLE_REQUIRED'))
    }
    const plan = new ActionPlan(
      ActionPlanId.generate(),
      props.tenantId,
      props.title.trim(),
      props.description ?? null,
      ActionPlanStatus.draft(),
      [],
      new Date()
    )
    plan.addDomainEvent(new ActionPlanCreated({ actionPlanId: plan.id, tenantId: plan.tenantId, title: plan.title }))
    return Result.ok(plan)
  }

  addTask(taskProps: AddTaskProps): Result<Task, DomainError> {
    // regra de negócio: só adiciona tarefas se plano estiver ativo
    if (this._status.isCanceled()) {
      return Result.fail(new DomainError('ACTION_PLAN_CANNOT_ADD_TASK_WHEN_CANCELED'))
    }
    const task = Task.create({ ...taskProps, actionPlanId: this.id })
    if (task.isFailure()) return Result.fail(task.error)
    this._tasks.push(task.value)
    this.addDomainEvent(new TaskAdded({ taskId: task.value.id, actionPlanId: this.id }))
    return Result.ok(task.value)
  }

  get completionPercentage(): number {
    if (this._tasks.length === 0) return 0
    const done = this._tasks.filter(t => t.status.isDone()).length
    return Math.round((done / this._tasks.length) * 100)
  }
}
```

Observe:
- `ActionPlan` tem comportamentos reais (`addTask`, `completionPercentage`)
- Retorna [`Result<T, E>`](#padrão-result), não `null`
- Emite eventos de domínio (`ActionPlanCreated`, `TaskAdded`)
- Zero imports de infraestrutura

---

### Fase 6: Gerar Testes do SPRINT 1 com o Agente Testing

**O que fazer:**
Após o [SPRINT](#sprint) 1 implementado, acione o Agente Testing para gerar os testes correspondentes.

**Por que fazer:**
Os testes são a prova de que o código faz o que o SPEC prometeu. Sem eles, você não tem como garantir que o domínio está correto — e qualquer mudança futura pode quebrar silenciosamente regras de negócio importantes.

**O que acontece se não fizer:**
Sem testes do domínio, qualquer refatoração futura pode quebrar regras de negócio sem que você perceba. Você só descobre o problema quando um cliente reclama que um plano de ação está calculando o percentual de conclusão errado — em produção, com dados reais.

**Contexto a fornecer:**
```
- Código gerado no SPRINT 1 (arquivos de domínio)
- Cenários GWT do SPRINT 1 no SPEC
- TESTING_GUIDE.md
```

**Comando:**
```
/test-sprint specs/action-plan/create-action-plan.md 1
```

**O que esperar como saída:**

```
tests/unit/domain/
├── entities/
│   ├── action-plan.test.ts       ← cobre cada cenário GWT de FR-001, FR-002, FR-004
│   └── task.test.ts              ← cobre cada cenário GWT de FR-003
└── value-objects/
    ├── deadline.test.ts
    └── budget.test.ts

tests/helpers/
└── in-memory-action-plan-repository.ts   ← criado para uso nos testes de application (SPRINT 2)
```

**Verifique a cobertura [GWT](#given-when-then-gwt):**
O Agente Testing lista ao final quais cenários GWT foram cobertos e quais não foram. Se algum ficou sem cobertura, solicite ao agente que implemente o teste faltante antes de avançar.

---

#### Exemplo: AçãoPlus — Testes do SPRINT 1

```typescript
// tests/unit/domain/entities/action-plan.test.ts

describe('ActionPlan', () => {

  describe('create', () => {
    it('ActionPlan_Create_WithValidTitle_ShouldReturnDraftActionPlan', () => {
      // Given
      const props = { title: 'Contratar desenvolvedores', tenantId: TenantId.create('tenant-1') }

      // When
      const result = ActionPlan.create(props)

      // Then
      expect(result.isOk()).toBe(true)
      expect(result.value.status.isDraft()).toBe(true)
      expect(result.value.title).toBe('Contratar desenvolvedores')
    })

    it('ActionPlan_Create_WithEmptyTitle_ShouldReturnError', () => {
      // Given
      const props = { title: '', tenantId: TenantId.create('tenant-1') }

      // When
      const result = ActionPlan.create(props)

      // Then
      expect(result.isFailure()).toBe(true)
      expect(result.error.code).toBe('ACTION_PLAN_TITLE_REQUIRED')
    })
  })

  describe('addTask', () => {
    it('ActionPlan_AddTask_WhenActive_ShouldAddTaskAndEmitEvent', () => {
      // Given
      const plan = ActionPlan.create({ title: 'Plano teste', tenantId: TenantId.create('t-1') }).value
      plan.activate()

      // When
      const result = plan.addTask({ what: 'Contratar dev', /* ... */ })

      // Then
      expect(result.isOk()).toBe(true)
      expect(plan.tasks).toHaveLength(1)
      expect(plan.domainEvents).toContainEqual(expect.objectContaining({ type: 'TaskAdded' }))
    })
  })

  describe('completionPercentage', () => {
    it('ActionPlan_CompletionPercentage_WhenHalfDone_ShouldReturn50', () => {
      // Given: plano com 2 tasks, 1 done, 1 pending
      const plan = /* ... plano com 2 tasks ... */

      // When / Then
      expect(plan.completionPercentage).toBe(50)
    })
  })
})
```

---

### Fase 7: Revisar SPRINT 1 com o Agente Review

**O que fazer:**
Acione o Agente Review para validar o código e os testes contra o ARCHITECTURE.md e os critérios de aceitação.

**Por que fazer:**
O Agente Review é o "inspetor de qualidade". Ele verifica se o código gerado realmente segue as regras do ARCHITECTURE.md — coisas que você talvez não perceba ao ler o código, como um import de [ORM](#orm--object-relational-mapper) escondido no meio do domínio ou um `null` retornado silenciosamente.

**O que acontece se não fizer:**
Violações arquiteturais se acumulam silenciosamente. Depois de 10 SPECs sem Review, você tem ORM no domínio, lógica no Controller, e `null` espalhado pelo código. Corrigir isso retrospectivamente é um projeto de semanas.

**Contexto a fornecer:**
```
- Código do SPRINT 1
- Testes do SPRINT 1
- Seção SPRINT 1 do SPEC (critérios de aceitação + cenários GWT)
- ARCHITECTURE.md (seções 1 e 5)
```

**Comando:**
```
/review-arch specs/action-plan/create-action-plan.md 1
```

**Como interpretar o resultado:**

| Veredicto | Significado | O que fazer |
|---|---|---|
| `APROVADO` | Sem violações críticas, todos os GWT cobertos | Avance para o SPRINT 2 |
| `APROVADO COM RESSALVAS` | Sem violações críticas, mas boas práticas melhoráveis | Registre as ressalvas no SPEC, avance para o SPRINT 2 |
| `REPROVADO` | Violação crítica ou GWT sem cobertura | Corrija as violações, re-execute `/review-arch [spec] 1` |

**Violações críticas (resultam em REPROVADO):**
- Import de [ORM](#orm--object-relational-mapper)/banco dentro do domínio
- Lógica de negócio no Controller
- `null` retornado silenciosamente em vez de [`Result.fail()`](#padrão-result)
- `tenantId` sem filtro em domínio [multi-tenant](#multi-tenant)
- Input concatenado em query SQL

---

#### Exemplo: AçãoPlus — Review do SPRINT 1

O Agente Review do AçãoPlus pode retornar:

```
## Violações Críticas
nenhuma

## Violações de Boas Práticas
- action-plan.ts:47 — método `activate()` tem mais de uma responsabilidade (muda status e calcula %).
  Sugestão: extrair o cálculo de % para um método separado `recalculateCompletion()`.

## Conformidade com Cenários GWT
- FR-001 / Cenário principal: COBERTO (ActionPlan_Create_WithValidTitle...)
- FR-001 / Cenário alternativo (título vazio): COBERTO (ActionPlan_Create_WithEmptyTitle...)
- FR-002 / Cenário principal: COBERTO (ActionPlan_Create_ShouldAssociateToTenant...)
- FR-003 / Cenário principal: COBERTO (ActionPlan_AddTask_WhenActive...)
- FR-004 / Cenário principal: COBERTO (ActionPlan_CompletionPercentage_WhenHalfDone...)

## Veredicto
APROVADO COM RESSALVAS

## Próximo passo
Execute /impl-sprint specs/action-plan/create-action-plan.md 2 para o SPRINT 2
```

---

### Fase 8: Gerar Migration com o Agente Migration

**O que fazer:**
Após o [SPRINT](#sprint) 1 (e novamente após o SPRINT 3), acione o Agente Migration para gerar os scripts SQL.

**Por que fazer:**
O banco de dados precisa refletir as entidades do domínio. O Agente Migration garante que as tabelas sigam as regras do ARCHITECTURE.md: toda tabela com `tenant_id`, índices corretos, nomenclatura padronizada. Fazer isso manualmente é lento e sujeito a erros.

**O que acontece se não fizer:**
Sem a migration, o banco não tem as tabelas necessárias e o [SPRINT](#sprint) 3 (Infrastructure) vai falhar. Se você criar as tabelas manualmente sem seguir o padrão, o isolamento [multi-tenant](#multi-tenant) pode estar incorreto — todos os clientes vendo os dados uns dos outros.

**Contexto a fornecer:**
```
- Entidades e Value Objects criados no SPRINT 1
- Seção "Impacto em Banco" do SPRINT 1 no SPEC
- Schema atual do banco (DDL existente, ou "banco novo")
- ARCHITECTURE.md (seção 13)
```

**Comando:**
```
/migrate-sprint specs/action-plan/create-action-plan.md 1
```

**O que esperar como saída:**

```
src/infrastructure/database/migrations/
└── 20250405_143000_create_action_plans_and_tasks.sql
```

**Regras que o Agente Migration segue:**
- Uma migration por responsabilidade
- Nomenclatura: `YYYYMMDD_HHMMSS_descricao_snake_case.sql`
- Toda tabela tem `id UUID`, `tenant_id UUID NOT NULL`, `created_at`, `updated_at`
- Índice em `tenant_id` em toda tabela de domínio
- Forward-only (sem rollback automático)

---

#### Exemplo: AçãoPlus — Migration do SPRINT 1

```sql
-- 20250405_143000_create_action_plans_and_tasks.sql

CREATE TABLE action_plans (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id   UUID NOT NULL,
  title       TEXT NOT NULL,
  description TEXT,
  status      VARCHAR(50) NOT NULL DEFAULT 'draft',
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_action_plans_tenant_id ON action_plans(tenant_id);

CREATE TABLE tasks (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action_plan_id UUID NOT NULL REFERENCES action_plans(id) ON DELETE CASCADE,
  tenant_id      UUID NOT NULL,
  what           TEXT NOT NULL,
  why            TEXT,
  responsible    TEXT,
  location       TEXT,
  deadline_date  DATE,
  how_to         TEXT,
  budget_amount  DECIMAL(15,2),
  budget_currency VARCHAR(3) DEFAULT 'BRL',
  status         VARCHAR(50) NOT NULL DEFAULT 'pending',
  created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_tenant_id ON tasks(tenant_id);
CREATE INDEX idx_tasks_action_plan_id ON tasks(action_plan_id);
```

---

### Fase 9: Repetir SPRINTs 2 a 5

Para cada [SPRINT](#sprint) seguinte, o ciclo é o mesmo:

```
/impl-sprint [spec] [n]       → Implementa o SPRINT
       ↓
/test-sprint [spec] [n]       → Gera testes
       ↓
/review-arch [spec] [n]       → Revisa código + testes
       ↓
(se SPRINT 3 com banco)
/migrate-sprint [spec] [n]    → Gera migration adicional
       ↓
avança para o próximo SPRINT
```

**O que cada [SPRINT](#sprint) entrega para o AçãoPlus:**

| SPRINT | Entrega |
|---|---|
| **SPRINT 2 — Application** | `CreateActionPlanUseCase`, `AddTaskUseCase`, `GetActionPlanQuery`, `ListActionPlansQuery` |
| **SPRINT 3 — Infrastructure** | `PrismaActionPlanRepository`, `PrismaTaskRepository`, migrations de índices adicionais |
| **SPRINT 4 — Presentation** | `POST /api/v1/action-plans`, `GET /api/v1/action-plans/:id`, `POST /api/v1/action-plans/:id/tasks`, ViewModels, chaves i18n |
| **SPRINT 5 — Transversal** | Rate limiting para criação de planos, logging de auditoria |

#### Exemplo: AçãoPlus — Sequência de Features do MVP

**Sequência recomendada para o AçãoPlus:**

```
1. specs/auth/login.md                           → autenticação
2. specs/tenant/onboarding.md                    → criação de tenant + trial
3. specs/action-plan/create-action-plan.md       → feature principal (exemplo acima)
4. specs/action-plan/manage-tasks.md             → adicionar/editar/concluir tarefas
5. specs/action-plan/list-action-plans.md        → listar e filtrar planos
6. specs/action-plan/action-plan-dashboard.md    → dashboard de progresso
7. specs/billing/create-subscription.md         → billing e planos
8. specs/action-plan/export-pdf.md              → feature Pro (feature flag)
```

---

### Fase 10: Checklist Final e Próxima Feature

**O que fazer:**
1. Execute o **Checklist Final** do SPEC (seção ao final do arquivo SPEC):
   - Todos os critérios de aceitação de cada [SPRINT](#sprint) satisfeitos?
   - Todos os Planos de Testes executados com cobertura [GWT](#given-when-then-gwt) completa?
   - `/review-arch` executado sem violações críticas?
   - [NFRs](#nfrs--non-functional-requirements-requisitos-não-funcionais) validados (performance medida, segurança testada)?
   - Chaves i18n adicionadas em todos os locales?
   - Migrations executadas e testadas em staging?

2. Atualize o SPEC: `Status: concluído` e preencha `Aprovado em:` com a data

3. Para a próxima feature, repita desde a [Fase 2](#fase-2-criar-o-primeiro-spec-com-o-agente-spec)

**Por que fazer:**
Fechar formalmente um SPEC cria um registro histórico: quando foi concluído, quais decisões foram tomadas, quais ressalvas existem. Isso é essencial quando você retoma o projeto depois de semanas ou quando onboarda uma nova pessoa no time.

**O que acontece se não fizer:**
Sem o fechamento formal, você não sabe o que foi ou não foi implementado. Em 3 meses, você vai perguntar: "essa feature já foi implementada? os testes passaram? o NFR de performance foi validado?" — e não terá como responder sem reler todo o código.

---

## 6. Comandos Claude Code — Referência Completa

| Comando | Agente acionado | Quando usar | Contexto obrigatório a fornecer |
|---|---|---|---|
| `/new-spec [descrição]` | Agente Spec | Nova feature a especificar | `ARCHITECTURE.md` seções 0–3 + `SPEC_TEMPLATE.md` + `GLOSSARY.md` |
| `/review-arch [spec] analyze` | Agente Analyze | Antes do 1º [SPRINT](#sprint) (SPEC aprovado) | SPEC completo + `ARCHITECTURE.md` seções 1 e 5 |
| `/impl-sprint [spec] [n]` | Agente Implementation | Implementar [SPRINT](#sprint) N | `ARCHITECTURE.md` seções 0–5 + [SPRINT](#sprint) N do SPEC |
| `/test-sprint [spec] [n]` | Agente Testing | Após implementar [SPRINT](#sprint) N | Código do SPRINT + [GWT](#given-when-then-gwt) do SPRINT + `TESTING_GUIDE.md` |
| `/review-arch [spec] [n]` | Agente Review | Após gerar testes do [SPRINT](#sprint) N | Código + testes + SPRINT N do SPEC + `ARCHITECTURE.md` seções 1 e 5 |
| `/migrate-sprint [spec] [n]` | Agente Migration | [SPRINT](#sprint) 1 e/ou 3 com impacto em banco | Entidades + "Impacto em Banco" do SPRINT + `ARCHITECTURE.md` seção 13 |

**Observações importantes:**
- `[spec]` é o caminho relativo para o arquivo SPEC, ex: `specs/action-plan/create-action-plan.md`
- `[n]` é o número do [SPRINT](#sprint), de 1 a 5
- Se o comando não existir como slash command configurado, copie o prompt correspondente do `AGENTS.md` e use diretamente no chat do Claude Code, incluindo o contexto mínimo

---

## 7. Configurando os Agentes como Slash Commands

Claude Code permite criar comandos customizados em Markdown que ficam disponíveis como `/nome-do-comando` em qualquer conversa do projeto. Cada arquivo em `.claude/commands/` se torna um slash command.

### O que são Slash Commands no Claude Code

Um slash command é um arquivo `.md` em `.claude/commands/` que:
- Contém um prompt reutilizável
- Pode receber argumentos (referenciados como `$ARGUMENTS` no arquivo)
- É executado quando você digita `/nome-do-arquivo` no chat

### Usando os arquivos prontos da pasta "Slash Commands"

Este kit já vem com todos os 5 comandos prontos para uso na pasta `Slash Commands/`. Para utilizá-los no seu projeto:

**Passo 1:** Certifique-se de que a pasta `.claude/commands/` existe no seu projeto. Se não existir, crie-a:
```bash
mkdir -p .claude/commands
```

**Passo 2:** Copie os arquivos de comando do kit para o seu projeto (ajuste o caminho conforme onde você salvou o kit):
```bash
cp /caminho/para/o/kit/Slash\ Commands/new-spec.md     .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/impl-sprint.md  .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/review-arch.md  .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/test-sprint.md  .claude/commands/
cp /caminho/para/o/kit/Slash\ Commands/migrate-sprint.md .claude/commands/
```

**Passo 3:** Verifique que os arquivos foram copiados:
```bash
ls .claude/commands/
```
Você deve ver: `new-spec.md`, `impl-sprint.md`, `review-arch.md`, `test-sprint.md`, `migrate-sprint.md`

**Passo 4:** Para o CLAUDE.md inicial do seu projeto, use o template em `Slash Commands/CLAUDE.md` como base — copie, renomeie e preencha com os dados do seu projeto:
```bash
cp /caminho/para/o/kit/Slash\ Commands/CLAUDE.md ./CLAUDE.md
```
Depois abra `CLAUDE.md` no VS Code e preencha `[Nome do Projeto]`, as tecnologias, e os bounded contexts.

---

### Criando os 6 Comandos do Kit

Se preferir criar os arquivos manualmente em vez de copiar da pasta `Slash Commands/`, use o conteúdo abaixo.

**Localização:** `.claude/commands/[nome-do-comando].md`

**`.claude/commands/new-spec.md`**
```markdown
Você é o Agente Spec. Sua única responsabilidade é gerar SPECs.

Leia o ARCHITECTURE.md (seções 0–3) e o SPEC_TEMPLATE.md antes de qualquer ação.
Leia o GLOSSARY.md do projeto para usar a Ubiquitous Language correta.

Tarefa: gere um SPEC para a seguinte funcionalidade:
$ARGUMENTS

Siga rigorosamente as regras do Agente Spec definidas em AGENTS.md.
```

**`.claude/commands/impl-sprint.md`**
```markdown
Você é o Agente Implementation. Sua única responsabilidade é implementar SPRINTs.

Leia o ARCHITECTURE.md (seções 0–5) antes de qualquer ação.

Tarefa: implemente o SPRINT indicado no seguinte SPEC:
$ARGUMENTS

(Formato esperado: [caminho-do-spec] [número-do-sprint])

Siga rigorosamente as regras do Agente Implementation definidas em AGENTS.md.
```

**`.claude/commands/review-arch.md`**
```markdown
Você é o Agente Analyze (se o argumento terminar em "analyze") ou o Agente Review (se terminar em número).

$ARGUMENTS

Siga rigorosamente as regras do agente correspondente definidas em AGENTS.md.
```

**`.claude/commands/test-sprint.md`**
```markdown
Você é o Agente Testing. Sua única responsabilidade é gerar testes para SPRINTs implementados.

Leia o TESTING_GUIDE.md antes de qualquer ação.

Tarefa: gere os testes para:
$ARGUMENTS

(Formato esperado: [caminho-do-spec] [número-do-sprint])

Siga rigorosamente as regras do Agente Testing definidas em AGENTS.md.
```

**`.claude/commands/migrate-sprint.md`**
```markdown
Você é o Agente Migration. Sua única responsabilidade é gerar scripts de migration de banco de dados.

Leia o ARCHITECTURE.md (seção 13) antes de qualquer ação.

Tarefa: gere as migrations para:
$ARGUMENTS

(Formato esperado: [caminho-do-spec] [número-do-sprint])

Siga rigorosamente as regras do Agente Migration definidas em AGENTS.md.
```

### Como usar os slash commands

Após criar os arquivos acima, no chat do Claude Code:

```
/new-spec Funcionalidade de criar plano de ação 5W2H para o bounded context action-plan
```

```
/impl-sprint specs/action-plan/create-action-plan.md 1
```

```
/review-arch specs/action-plan/create-action-plan.md analyze
```

```
/test-sprint specs/action-plan/create-action-plan.md 2
```

```
/review-arch specs/action-plan/create-action-plan.md 2
```

```
/migrate-sprint specs/action-plan/create-action-plan.md 1
```

### Dica: Contexto automático via CLAUDE.md

Para que os arquivos do kit sejam incluídos automaticamente como contexto, adicione ao seu `CLAUDE.md`:

```markdown
## Contexto automático — leia estes arquivos antes de qualquer ação

@ARCHITECTURE.md — Constitution do projeto (obrigatório em toda sessão)
@specs/[dominio-principal]/GLOSSARY.md — Vocabulário do domínio

Quando acionar um agente via slash command, consulte AGENTS.md para o contexto mínimo
daquele agente e inclua apenas os arquivos necessários — não inclua o kit inteiro.
```

**Nota sobre `@` no CLAUDE.md:** O prefixo `@` antes de um nome de arquivo instrui o Claude Code a incluir o conteúdo do arquivo no contexto automaticamente.

---

### Exemplo: AçãoPlus — Slash Commands configurados

```
acaoplus/
└── .claude/
    ├── commands/
    │   ├── new-spec.md
    │   ├── impl-sprint.md
    │   ├── review-arch.md
    │   ├── test-sprint.md
    │   └── migrate-sprint.md
    └── settings.json
```

Após esta configuração, o desenvolvimento do AçãoPlus segue este ritmo:

```
> /new-spec Criar plano de ação 5W2H com título e tarefas
```
→ Consulte [Fase 2: Criar o primeiro SPEC com o Agente Spec](#fase-2-criar-o-primeiro-spec-com-o-agente-spec)
```
[Agente Spec gera specs/action-plan/create-action-plan.md]

> [você revisa e aprova o SPEC]
```
→ Consulte [Fase 3: Revisar e Aprovar o SPEC](#fase-3-revisar-e-aprovar-o-spec)
```
> /review-arch specs/action-plan/create-action-plan.md analyze
```
→ Consulte [Fase 4: Validar com o Agente Analyze](#fase-4-validar-com-o-agente-analyze)
```
[Agente Analyze valida — PRONTO PARA IMPLEMENTAR]

> /impl-sprint specs/action-plan/create-action-plan.md 1
```
→ Consulte [Fase 5: Implementar SPRINT 1 — Domínio](#fase-5-implementar-sprint-1--domínio)
```
[Agente Implementation cria domínio em src/domain/action-plan/]

> /migrate-sprint specs/action-plan/create-action-plan.md 1
```
→ Consulte [Fase 8: Gerar Migration com o Agente Migration](#fase-8-gerar-migration-com-o-agente-migration)
```
[Agente Migration cria migration SQL]

> /test-sprint specs/action-plan/create-action-plan.md 1
```
→ Consulte [Fase 6: Gerar Testes do SPRINT 1 com o Agente Testing](#fase-6-gerar-testes-do-sprint-1-com-o-agente-testing)
```
[Agente Testing cria tests/unit/domain/entities/...]

> /review-arch specs/action-plan/create-action-plan.md 1
```
→ Consulte [Fase 7: Revisar SPRINT 1 com o Agente Review](#fase-7-revisar-sprint-1-com-o-agente-review)
```
[Agente Review — APROVADO]

> /impl-sprint specs/action-plan/create-action-plan.md 2
[...]
```

---

### Índice de Exemplos do AçãoPlus neste guia

Use esta tabela para encontrar rapidamente qualquer exemplo do AçãoPlus:

| Onde no guia | O que demonstra | Link |
|---|---|---|
| Seção 1 | Visão geral do AçãoPlus (5W2H, problema, bounded contexts) | [ver exemplo](#exemplo-açãoplus-saas-5w2h) |
| Seção 3.1 | Como usar o ARCHITECTURE.md no AçãoPlus | [ver exemplo](#exemplo-açãoplus--architecturemd) |
| Seção 3.2 | Quando o AçãoPlus usa cada agente (especialmente Migration) | [ver exemplo](#exemplo-açãoplus--agentsmd) |
| Seção 3.3 | Convenção de nome do primeiro SPEC do AçãoPlus | [ver exemplo](#exemplo-açãoplus--spec_templatemd) |
| Seção 3.4 | Estrutura completa de testes do AçãoPlus | [ver exemplo](#exemplo-açãoplus--testing_guidemd) |
| Seção 3.5 | Ciclo de assinatura e feature flags do AçãoPlus | [ver exemplo](#exemplo-açãoplus--saas_patternsmd) |
| Seção 3.6 | Tabela de termos do bounded context action-plan | [ver exemplo](#exemplo-açãoplus--glossarymd-preenchido) |
| Seção 4 | Estrutura de pastas e CLAUDE.md do AçãoPlus | [ver exemplo](#exemplo-açãoplus--preparação-do-projeto) |
| Fase 0 | Concepção: problema, público, features, bounded contexts | [ver exemplo](#exemplo-açãoplus--fase-0) |
| Fase 1 | GLOSSARY.md completo e preenchido | [ver exemplo](#exemplo-açãoplus--fase-1) |
| Fase 2 | SPEC resumido de "Criar Plano de Ação" | [ver exemplo](#exemplo-açãoplus--spec-de-criar-plano-de-ação-resumo) |
| Fase 3 | Perguntas de aprovação do SPEC | [ver exemplo](#exemplo-açãoplus--fase-3) |
| Fase 4 | Resultado do Analyze com inconsistências encontradas | [ver exemplo](#exemplo-açãoplus--fase-4) |
| Fase 5 | Código TypeScript do SPRINT 1 (domínio ActionPlan) | [ver exemplo](#exemplo-açãoplus--sprint-1-fragmento-de-código-esperado) |
| Fase 6 | Testes unitários do SPRINT 1 | [ver exemplo](#exemplo-açãoplus--testes-do-sprint-1) |
| Fase 7 | Resultado do Review com veredicto e ressalvas | [ver exemplo](#exemplo-açãoplus--review-do-sprint-1) |
| Fase 8 | Script SQL de migration das tabelas | [ver exemplo](#exemplo-açãoplus--migration-do-sprint-1) |
| Fase 9 | Sequência completa de features do MVP | [ver exemplo](#exemplo-açãoplus--sequência-de-features-do-mvp) |
| Seção 7 | Slash commands configurados no projeto | [ver exemplo](#exemplo-açãoplus--slash-commands-configurados) |

---

## 8. Recuperação de Problemas Comuns

| Problema | Causa provável | O que fazer |
|---|---|---|
| Agente gerou código fora do escopo do [SPRINT](#sprint) | Prompt incompleto ou agente não leu os FRs do SPRINT | Remova o código fora do escopo. Re-execute `/impl-sprint` fornecendo explicitamente apenas os FRs do SPRINT atual |
| Review retornou REPROVADO | Violação crítica no código ([ORM](#orm--object-relational-mapper) no domínio, null retornado, etc.) | Corrija APENAS as violações críticas listadas. Re-execute `/review-arch [spec] [n]` — NÃO crie um novo SPRINT |
| Analyze retornou REQUER CORREÇÃO | SPEC inconsistente (FR sem [GWT](#given-when-then-gwt), SPRINT sem FR, etc.) | Corrija os itens no SPEC. Re-execute `/review-arch [spec] analyze` antes de implementar |
| Contexto muito grande / sessão lenta | Fornecendo arquivos desnecessários para o agente | Use a tabela de contexto mínimo de `AGENTS.md` — forneça só o necessário para cada agente |
| Agente inventou termos de domínio | GLOSSARY.md não foi fornecido | Atualize o GLOSSARY.md com os termos corretos e forneça-o ao agente na próxima sessão |
| SPEC tem mais de 10 FRs | Feature muito grande | Divida em dois SPECs menores. Regra: um SPEC por fluxo de negócio isolado |
| Testes falham após implementação | [InMemoryRepository](#inmemoryrepository) incompleto ou [GWT](#given-when-then-gwt) mal escrito | Revise o InMemoryRepository: ele implementa todos os métodos da interface? Filtra por `tenantId`? |
| IA viola regras da arquitetura repetidamente | ARCHITECTURE.md não está no contexto da sessão | Certifique-se que `@ARCHITECTURE.md` está no `CLAUDE.md` ou forneça-o explicitamente |
| Migration gerou colunas diferentes da entidade | Agente de Migration não leu o código das entidades | Forneça as entidades concretas (não só o SPEC) ao Agente Migration |
| Novo [bounded context](#bounded-context-contexto-delimitado) sem GLOSSARY | GLOSSARY.md não existe para o novo domínio | Crie `specs/[novo-dominio]/GLOSSARY.md` antes do primeiro SPEC desse contexto |
| IA criou interface/entidade duplicada | Agente não verificou se já existia | Remova a duplicata. Lembre o agente da regra: "pesquise antes de criar" (ARCHITECTURE.md seção 0) |
| Job duplica execução (cobrança dupla, e-mail duplicado) | Job não implementa idempotência | Adicione verificação de estado antes de agir (ex: `invoice.isPaidInPeriod()`). Consulte SAAS_PATTERNS.md seção 10 |
| Evento entre [bounded contexts](#bounded-context-contexto-delimitado) se perdeu (processo crashou) | Evento disparado diretamente sem Outbox | Implemente Outbox Pattern (ARCHITECTURE.md seção 19) — evento persiste na mesma transação do aggregate |
| Use Case abre transação em dois repositórios separados | Falta [Unit of Work](#unit-of-work) | Extraia `IUnitOfWork`, injete via DI e envolva as duas operações em `begin/commit` (ARCHITECTURE.md seção 7) |

---

## 9. Checklist Completo — Do Zero ao Sistema em Produção

Use este checklist para acompanhar o progresso do seu projeto. Cada item tem um link para o tópico correspondente neste guia. Com apenas este checklist, você deve conseguir executar todos os procedimentos sem precisar reler o documento.

---

### Fase A: Preparação do Ambiente (faça uma vez por projeto)

- [ ] **Ambiente configurado:** Claude Code instalado (CLI ou extensão VS Code), Node.js instalado, VS Code aberto
- [ ] **Estrutura de pastas criada:** Execute os comandos do [Passo 1](#passo-1-criar-a-estrutura-de-pastas): `mkdir -p src/{presentation,application,domain,infrastructure}`, `mkdir -p tests/{unit,integration,e2e}`, `mkdir -p specs`, `mkdir -p .claude/commands`
- [ ] **Arquivos do kit copiados:** Execute os comandos do [Passo 2](#passo-2-copiar-os-arquivos-do-kit): todos os 6 arquivos (`ARCHITECTURE.md`, `AGENTS.md`, `SPEC_TEMPLATE.md`, `TESTING_GUIDE.md`, `SAAS_PATTERNS.md`, `GLOSSARY_TEMPLATE.md`) estão na raiz do projeto
- [ ] **CLAUDE.md criado:** Crie o arquivo conforme o [Passo 3](#passo-3-criar-o-claudemd): nome do projeto, `@ARCHITECTURE.md`, tecnologias e bounded contexts preenchidos
- [ ] **Slash commands configurados:** Execute os comandos do [Passo 5](#passo-5-criar-os-slash-commands-veja-seção-7): 5 arquivos `.md` copiados para `.claude/commands/`. Teste digitando `/` no Claude Code — os comandos devem aparecer

---

### Fase B: Glossário e Vocabulário (faça antes do primeiro SPEC)

- [ ] **Bounded contexts identificados:** Liste os domínios do negócio conforme a [Fase 0](#fase-0-concepção-da-ideia) (mínimo: auth, tenant, core do produto, billing)
- [ ] **Diagrama de contextos desenhado:** Diagrama ASCII mostrando como os bounded contexts se comunicam via eventos (ver modelo da [Fase 0](#fase-0-concepção-da-ideia))
- [ ] **GLOSSARY.md criado:** Execute `mkdir -p specs/[dominio-principal]` e `cp GLOSSARY_TEMPLATE.md specs/[dominio-principal]/GLOSSARY.md` conforme o [Passo 4](#passo-4-criar-o-glossarymd-do-projeto)
- [ ] **Mapa de bounded contexts preenchido:** Seção 1 do GLOSSARY.md preenchida com o diagrama ASCII (ver [exemplo do AçãoPlus na Fase 1](#exemplo-açãoplus--fase-1))
- [ ] **Termos do domínio principal definidos:** Tabela da Seção 2 do GLOSSARY.md preenchida com: termo, definição, termos a evitar, exemplo de uso
- [ ] **Termos SaaS comuns revisados:** Seção 3 do GLOSSARY.md revisada (pré-preenchida no template — confirme que os termos fazem sentido para o seu produto)
- [ ] **Termos proibidos listados:** Seção 5 do GLOSSARY.md preenchida com o que NÃO usar e a alternativa correta (ex: `User` → `TeamMember`)

---

### Fase C: Para cada Nova Feature (SPEC)

*Repita este bloco para cada nova funcionalidade do produto.*

- [ ] **SPEC gerado:** Execute [`/new-spec [descrição da feature]`](#fase-2-criar-o-primeiro-spec-com-o-agente-spec) ou crie manualmente baseado no `SPEC_TEMPLATE.md`. Arquivo salvo em `specs/[bounded-context]/[verbo]-[substantivo].md`
- [ ] **Seção Clarify resolvida:** Todas as ambiguidades identificadas pelo Agente Spec têm resposta na coluna "Decisão / Resposta" (ver [Fase 3](#fase-3-revisar-e-aprovar-o-spec))
- [ ] **User Stories revisadas:** Fazem sentido para o negócio? Estão priorizadas corretamente (P1/P2/P3)?
- [ ] **NFRs têm critério mensurável:** Nenhum NFR com "deve ser rápido" ou "deve funcionar" — cada um tem número concreto (ver [NFRs no glossário](#nfrs--non-functional-requirements-requisitos-não-funcionais))
- [ ] **Checklist de Cobertura preenchido:** Todo FR tem pelo menos uma User Story e pelo menos um cenário [GWT](#given-when-then-gwt)
- [ ] **SPEC aprovado:** Status alterado para `aprovado`, data de aprovação preenchida (ver [Fase 3](#fase-3-revisar-e-aprovar-o-spec))
- [ ] **Analyze executado e aprovado:** Execute [`/review-arch [spec] analyze`](#fase-4-validar-com-o-agente-analyze) — veredicto deve ser **PRONTO PARA IMPLEMENTAR** antes de avançar

---

### Fase D: Para cada SPRINT (Implementação)

*Repita este bloco para cada SPRINT (1 a 5) de cada SPEC.*

- [ ] **Implementation executado:** Execute [`/impl-sprint [spec] [n]`](#fase-5-implementar-sprint-1--domínio) — código criado nas pastas corretas (`src/domain/`, `src/application/`, etc.)
- [ ] **Migration gerada (se SPRINT 1 ou 3 com banco):** Execute [`/migrate-sprint [spec] [n]`](#fase-8-gerar-migration-com-o-agente-migration) — arquivo SQL criado em `src/infrastructure/database/migrations/`
- [ ] **Testes gerados:** Execute [`/test-sprint [spec] [n]`](#fase-6-gerar-testes-do-sprint-1-com-o-agente-testing) — todos os cenários [GWT](#given-when-then-gwt) do SPRINT têm teste correspondente
- [ ] **Tabela de rastreabilidade GWT verificada:** Agente Testing listou todos os cenários como "coberto" — se algum ficou sem cobertura, solicite o teste faltante antes de avançar
- [ ] **Review executado e aprovado:** Execute [`/review-arch [spec] [n]`](#fase-7-revisar-sprint-1-com-o-agente-review) — veredicto deve ser **APROVADO** ou **APROVADO COM RESSALVAS** (nunca avance com REPROVADO)
- [ ] **Ressalvas registradas (se houver):** Ressalvas do Review anotadas na seção correspondente do SPEC para acompanhamento

---

### Fase E: Fechando uma Feature

*Faça ao concluir todos os SPRINTs de um SPEC.*

- [ ] **Todos os SPRINTs aprovados:** Todos os 5 (ou menos) SPRINTs do SPEC têm veredicto APROVADO ou APROVADO COM RESSALVAS do Agente Review (ver [Fase 10](#fase-10-checklist-final-e-próxima-feature))
- [ ] **Checklist Final do SPEC marcado:** A seção "Checklist Final" ao final do arquivo SPEC está totalmente preenchida
- [ ] **NFRs validados:** Performance medida (ex: carga real no banco de testes), segurança testada (ex: tenant B não acessa dados de tenant A)
- [ ] **Migrations executadas em staging:** Os scripts SQL foram rodados em ambiente de staging e testados — não apenas gerados
- [ ] **Background jobs validados (se houver):** Idempotência testada (execução dupla não duplica dados), isolamento por tenant verificado
- [ ] **Chaves i18n adicionadas:** Todos os textos expostos ao usuário têm chave i18n em todos os locales configurados
- [ ] **SPEC fechado:** Status alterado para `concluído`, campo `Aprovado em:` preenchido com a data
- [ ] **GLOSSARY atualizado (se novos termos surgiram):** Novos termos descobertos durante o desenvolvimento adicionados ao `specs/[dominio]/GLOSSARY.md` conforme [instruções da seção 3.6](#36-glossary_templatemd--ubiquitous-language)

---

### Fase F: Manutenção e Evolução do Projeto

*Faça conforme o projeto evolui.*

- [ ] **GLOSSARY atualizado para novo bounded context:** Ao iniciar um novo domínio (ex: `notifications`), crie `specs/notifications/GLOSSARY.md` antes do primeiro SPEC desse contexto
- [ ] **CLAUDE.md atualizado:** Novos bounded contexts, tecnologias adicionadas ou regras específicas do projeto adicionadas ao `CLAUDE.md`
- [ ] **Problemas recorrentes documentados:** Se a IA repetir o mesmo erro (ex: [ORM](#orm--object-relational-mapper) no domínio), verifique a [seção 8](#8-recuperação-de-problemas-comuns) e adicione uma regra explícita no ARCHITECTURE.md com `// REGRA ADICIONADA:`
- [ ] **SPECs de features antigas revisitados (se necessário):** Ao modificar uma feature existente, crie um novo SPEC (`update-[feature].md`) em vez de alterar o SPEC original — mantenha o histórico de decisões

---

## Referência Rápida dos Arquivos do Kit

| Arquivo | Papel | Quem usa | Quando |
|---|---|---|---|
| `ARCHITECTURE.md` | Constitution do projeto | Todos os agentes | Toda sessão de vibe coding |
| `AGENTS.md` | Prompts e fluxo dos 6 agentes | Você (para copiar prompts) | Ao acionar cada agente |
| `SPEC_TEMPLATE.md` | Formato padrão de SPEC | Agente Spec | Ao criar cada SPEC |
| `TESTING_GUIDE.md` | Estratégia de testes | Agente Testing | Ao gerar testes de cada [SPRINT](#sprint) |
| `SAAS_PATTERNS.md` | Padrões [multi-tenant](#multi-tenant), billing, GDPR, background jobs | Agente Spec + Impl | Features SaaS-específicas e background jobs |
| `GLOSSARY_TEMPLATE.md` | Template de vocabulário de domínio | Você (para criar GLOSSARY) | Antes do 1º SPEC de cada contexto |

---

## Resumo do Ciclo de Desenvolvimento

```
[Você] Ideia de feature
       ↓
[/new-spec] Agente Spec → specs/[dominio]/[feature].md (Status: rascunho)
       ↓
[Você] Revisa, resolve Clarify, aprova → Status: aprovado
       ↓
[/review-arch analyze] Agente Analyze → PRONTO PARA IMPLEMENTAR
       ↓ (repete para cada SPRINT de 1 a 5)
[/impl-sprint N] Agente Implementation → código na camada correta
[/migrate-sprint N] Agente Migration → SQL em infrastructure/migrations/ (se banco)
[/test-sprint N] Agente Testing → testes em tests/unit/ ou tests/integration/
[/review-arch N] Agente Review → APROVADO
       ↓
[Você] Checklist Final → Status: concluído
       ↓
[Próxima feature → volta ao /new-spec]
```

---

## 10. Glossário de Termos Técnicos

Este glossário explica os termos técnicos usados neste guia em linguagem acessível. Cada termo inclui sua definição, por que importa neste kit e um exemplo prático usando o AçãoPlus.

---

### Metodologia de Desenvolvimento

---

#### SDD — Specification-Driven Development

**O que é (em linguagem simples):**
"Desenvolvimento Guiado por Especificação". É uma forma de trabalhar onde você **escreve o que quer** antes de pedir para a IA escrever o código. O "o que você quer" se chama SPEC.

**Por que importa neste kit:**
A IA é muito rápida em gerar código, mas gera o que **acha** que você quer se não tiver instruções claras. O SDD garante que você e a IA estejam de acordo sobre o que será feito antes de qualquer linha de código.

**O que é na Prática:**
Antes de pedir `/impl-sprint`, você sempre tem um arquivo `.md` aprovado em `specs/` que descreve exatamente o comportamento esperado, quem pode usar, quais são os limites de performance e como testar que funcionou.

**Exemplo:**
Antes de implementar "criar plano de ação", você tem `specs/action-plan/create-action-plan.md` com:
- Quem pode criar (apenas membros do tenant)
- O que é obrigatório (título) e o que é opcional (descrição)
- Quanto tempo pode demorar (máximo 300ms)
- Como testar que está correto (cenários Given-When-Then)

---

#### TDD — Test-Driven Development

**O que é (em linguagem simples):**
"Desenvolvimento Guiado por Testes". É uma prática onde você escreve o **teste antes** de escrever o código. O código só é escrito para fazer o teste passar.

**Por que importa neste kit:**
Os cenários [Given-When-Then](#given-when-then-gwt) do SPEC são naturalmente especificações de teste. O TDD conecta o SPEC (o que deve acontecer) com o código (como vai acontecer).

**O que é na Prática:**
O Agente Implementation, para cada comportamento do SPRINT, faz:
1. Escreve um teste que descreve o comportamento (o teste falha porque o código não existe — RED)
2. Escreve o mínimo de código para o teste passar (GREEN)
3. Limpa o código sem quebrar o teste (REFACTOR)

**Exemplo:**
Para o comportamento "ActionPlan não pode ter título vazio":
1. RED: escreve `expect(ActionPlan.create({ title: '' })).toBeFailure()`
2. GREEN: adiciona `if (!props.title) return Result.fail(...)`
3. REFACTOR: extrai a validação para um método separado se ficar complexa

---

#### Spec-Kit

**O que é (em linguagem simples):**
Uma metodologia de 5 passos para criar especificações de software de forma estruturada e rastreável. Cada passo tem um agente dedicado neste kit.

**Por que importa neste kit:**
Sem uma metodologia de especificação, as features ficam mal descritas e incompletas. O Spec-Kit garante que cada feature passe por: criar → esclarecer → verificar cobertura → validar consistência → implementar.

**O que é na Prática:**
Os 5 passos do Spec-Kit mapeiam diretamente para os comandos do kit:
- Specify → `/new-spec`
- Clarify → você responde a seção Clarify do SPEC
- Checklist → Agente Spec preenche a cobertura de FRs
- Analyze → `/review-arch analyze`
- Implement → `/impl-sprint`

---

#### Vibe Coding

**O que é (em linguagem simples):**
"Programar no flow com a IA". É desenvolver software descrevendo o que você quer em linguagem natural para uma IA e revisando o código gerado, sem necessariamente conhecer todos os detalhes de implementação.

**Por que importa neste kit:**
O kit foi criado especificamente para vibe coding. Ele garante que mesmo desenvolvendo "no flow", o código gerado siga regras profissionais de arquitetura — algo que normalmente exigiria anos de experiência.

**Exemplo:**
Sem o kit, você digita: "IA, crie um endpoint para criar planos de ação" → código gerado sem testes, sem isolamento multi-tenant, sem tratamento de erros.

Com o kit, você tem o SPEC aprovado antes, e o comando `/impl-sprint` garante que a IA siga todas as regras — mesmo que você não saiba quais são essas regras.

---

### Arquitetura de Software

---

#### Clean Architecture

**O que é (em linguagem simples):**
Uma forma de organizar o código em "camadas" onde cada camada tem uma responsabilidade específica e as camadas internas não dependem das externas. É como uma cebola: o núcleo (regras de negócio) não sabe que existe casca (banco de dados, HTTP).

**Por que importa neste kit:**
A Clean Architecture é a espinha dorsal do ARCHITECTURE.md. Sem ela, a IA mistura banco de dados com regras de negócio, HTTP com cálculos, e o código vira um emaranhado impossível de testar e modificar.

**O que é na Prática:**
Quatro camadas, nesta ordem de "mais interno para mais externo":
1. **Domain** (`src/domain/`) — regras de negócio puras, sem dependências externas
2. **Application** (`src/application/`) — casos de uso que orquestram o domínio
3. **Infrastructure** (`src/infrastructure/`) — banco de dados, APIs externas, email
4. **Presentation** (`src/presentation/`) — HTTP, controllers, validação de entrada

**Exemplo:**
No AçãoPlus, a regra "um ActionPlan cancelado não pode receber novas Tasks" vive em `src/domain/action-plan/entities/action-plan.ts`. Ela não sabe nada sobre PostgreSQL, NestJS ou HTTP. Isso significa que você pode trocar o banco de dados sem tocar nessa regra.

---

#### Domain-Driven Design (DDD)

**O que é (em linguagem simples):**
"Design Guiado pelo Domínio". Uma abordagem de desenvolvimento onde o código reflete o vocabulário e as regras do negócio — não os detalhes técnicos. O código "fala" a língua do negócio.

**Por que importa neste kit:**
O DDD garante que quando você lê o código, você entende o negócio. `ActionPlan.addTask()` é imediatamente compreensível. `UserRepository.insertRecord()` não é.

---

##### Bounded Context (Contexto Delimitado)

**O que é (em linguagem simples):**
Um "bounded context" é uma fronteira clara dentro do seu sistema onde um conjunto de regras de negócio e vocabulário é válido. Dentro dessa fronteira, os termos têm significado preciso. Fora dela, o mesmo termo pode significar outra coisa.

**Por que importa neste kit:**
Sem bounded contexts, você tem um único modelo gigante onde `User` significa coisas diferentes em autenticação, em billing e em gestão de planos. Isso cria confusão, dependências desnecessárias e código frágil.

**O que é Bounded Context na Prática:**
Cada bounded context vira uma pasta dentro de `src/domain/` e `src/application/`. Contextos diferentes se comunicam apenas via eventos de domínio — nunca acessam as entidades uns dos outros diretamente. Cada contexto tem seu próprio `GLOSSARY.md`.

**Exemplo no AçãoPlus:**
- No contexto `auth`, existe `Account` (identidade com credenciais)
- No contexto `tenant`, existe `TeamMember` (Account com acesso a um Workspace)
- No contexto `billing`, existe `Subscription` (contrato de pagamento do Tenant)

O mesmo ser humano é um `Account` quando faz login, um `TeamMember` quando cria um plano de ação, e não tem representação direta em `billing` (quem paga é o `Tenant`, não a pessoa).

Se você usasse `User` para tudo, como saberia qual `User` é o responsável pela assinatura?

---

##### Ubiquitous Language (Linguagem Ubíqua)

**O que é (em linguagem simples):**
É o vocabulário compartilhado entre você (o dono do negócio) e o código. Os mesmos termos que você usa para falar sobre o negócio devem aparecer no código — sem tradução.

**Por que importa neste kit:**
O GLOSSARY.md é a implementação da Ubiquitous Language. Quando você diz "preciso adicionar uma Task ao ActionPlan", a IA sabe exatamente qual entidade modificar porque o código usa esses mesmos termos.

**Exemplo:**
No AçãoPlus, você diz "5W2H". O código tem `ActionPlan`, `Task`, `Deadline`, `Responsible` — não `Plan`, `Todo`, `Date`, `Owner`. Quando você pede "mostre todos os ActionPlans ativos do tenant", a IA não precisa perguntar o que você quer dizer.

---

##### Aggregate Root

**O que é (em linguagem simples):**
É a entidade "chefe" de um grupo de objetos relacionados. Só se acessa os objetos do grupo através do chefe — nunca diretamente.

**Por que importa neste kit:**
O Aggregate Root garante que as regras de negócio do grupo sejam sempre respeitadas. Você não pode adicionar uma Task diretamente — só através do `ActionPlan`, que verifica se o plano está no estado correto.

**Exemplo:**
`ActionPlan` é o Aggregate Root do grupo `ActionPlan + Tasks`. Para adicionar uma Task, você chama `actionPlan.addTask(props)` — não `taskRepository.save(task)` diretamente. Isso garante que a regra "não se pode adicionar tasks a um plano cancelado" seja sempre verificada.

---

##### Domain Events (Eventos de Domínio)

**O que é (em linguagem simples):**
É uma notificação de que algo importante aconteceu no negócio. "Um ActionPlan foi criado", "Uma Task foi concluída". Outros partes do sistema podem "ouvir" esses eventos e reagir.

**Por que importa neste kit:**
Os eventos permitem que [bounded contexts](#bounded-context-contexto-delimitado) se comuniquem sem depender um do outro. O contexto `billing` não precisa conhecer o código do `action-plan` — ele apenas escuta o evento `TenantCreated` e cria a assinatura trial.

**Exemplo:**
Quando `ActionPlan.create()` é chamado, ele emite o evento `ActionPlanCreated`. O sistema de notificações pode ouvir esse evento e enviar um email para o time — sem que o domínio `action-plan` saiba que existe um sistema de notificações.

---

##### Unit of Work

**O que é (em linguagem simples):**
É um "pacote de operações" que devem acontecer juntas ou não acontecem nenhuma. Se uma falhar, todas falham e o banco de dados volta ao estado anterior.

**Por que importa neste kit:**
Algumas operações precisam de garantia "tudo ou nada". Criar um Tenant E criar a Subscription trial deve acontecer na mesma transação — se a Subscription falhar, o Tenant não deve existir.

**Exemplo:**
No onboarding do AçãoPlus:
```typescript
await unitOfWork.begin()
await tenantRepo.save(tenant)
await subscriptionRepo.save(trialSubscription)
await unitOfWork.commit()  // ← só aqui os dois são salvos
// se commit falhar, os dois são desfeitos
```

---

### SaaS e Multi-tenancy

---

#### Multi-tenant

**O que é (em linguagem simples):**
"Multi-inquilino". É quando o mesmo software serve múltiplos clientes (empresas) ao mesmo tempo, mantendo os dados de cada um completamente separados — como um prédio de apartamentos onde cada inquilino tem seu espaço privado.

**Por que importa neste kit:**
A maioria dos SaaS é multi-tenant. Se o código não foi feito para isso desde o início, os dados de clientes diferentes podem se misturar — um bug crítico que quebra a confiança do produto.

**O que é na Prática:**
Toda tabela do banco tem uma coluna `tenant_id`. Toda query filtra por `tenant_id`. Nunca há uma query sem filtro de tenant (exceto nas próprias tabelas de tenants).

**Exemplo:**
A empresa "Construtora ABC" e a empresa "Farmácia XYZ" usam o AçãoPlus. Quando o gestor da Construtora entra, ele só vê os `ActionPlans` com `tenant_id = 'construtora-abc'`. Mesmo que ele tente acessar um plan da Farmácia pela URL, o sistema retorna 404 — porque o repositório sempre filtra por tenant.

---

#### TenantContext

**O que é (em linguagem simples):**
É o mecanismo que "lembra" qual empresa está sendo atendida durante uma requisição. Quando o usuário da Construtora faz login, o TenantContext guarda `tenant_id = 'construtora-abc'` e injeta esse valor automaticamente em todos os repositórios durante aquela requisição.

**Por que importa neste kit:**
Sem o TenantContext, cada método precisaria receber o `tenantId` como parâmetro — o que é trabalhoso e fácil de esquecer. Com ele, o isolamento acontece automaticamente.

**O que é na Prática:**
O TenantContext é criado pelo middleware de autenticação e injetado via injeção de dependência (DI). Todo repositório recebe o TenantContext no construtor e usa o `tenantId` em todas as queries.

**Exemplo no AçãoPlus:**
```typescript
// Middleware cria o TenantContext
const context = new TenantContext(jwt.claims.tenant_id)

// Repositório usa automaticamente
class PrismaActionPlanRepository {
  constructor(private tenantContext: TenantContext) {}
  
  async findAll() {
    return this.db.actionPlan.findMany({
      where: { tenantId: this.tenantContext.tenantId }  // ← automático
    })
  }
}
```

---

#### Row-level Isolation (Isolamento por Linha)

**O que é (em linguagem simples):**
"Isolamento em nível de linha". É a estratégia de separar dados de tenants diferentes na mesma tabela, usando a coluna `tenant_id` para filtrar. É a estratégia mais comum em SaaS.

**Por que importa neste kit:**
É mais simples e escalável do que criar um banco de dados separado por cliente. Toda tabela tem `tenant_id`, toda query filtra por ele.

**Exemplo:**
A tabela `action_plans` tem registros de todos os tenants, mas a coluna `tenant_id` garante que cada um acesse apenas os seus:
```sql
SELECT * FROM action_plans WHERE tenant_id = 'construtora-abc';
-- só retorna planos da Construtora ABC
```

---

#### Feature Flags

**O que é (em linguagem simples):**
"Interruptores de funcionalidade". São configurações que ligam ou desligam uma feature para um cliente específico ou para um plano de assinatura.

**Por que importa neste kit:**
Permitem que você lance uma feature apenas para clientes Pro, ou para testar com um cliente piloto, sem precisar alterar o código.

**Exemplo no AçãoPlus:**
A feature `EXPORT_PDF` só está disponível no plano Pro. Quando um usuário do plano Free tenta exportar:
```typescript
if (!featureFlags.isEnabled('EXPORT_PDF', tenant)) {
  return Result.fail(new PermissionError('FEATURE_NOT_AVAILABLE_IN_FREE_PLAN'))
}
```

---

### Desenvolvimento Técnico

---

#### SPRINT

**O que é (em linguagem simples):**
Neste kit, um SPRINT é uma **etapa de implementação** que corresponde a uma camada da arquitetura. Não é o Sprint do Scrum (período de 2 semanas) — é uma divisão lógica do trabalho de implementação de uma feature.

**Por que importa neste kit:**
Dividir a implementação em SPRINTs garante que você implemente na ordem correta (Domain-First), que cada camada seja testada antes da próxima, e que a IA não misture responsabilidades de camadas diferentes.

**O que é na Prática:**
Cada feature tem 5 SPRINTs possíveis:
- SPRINT 1: Domínio (entidades, regras de negócio)
- SPRINT 2: Application (casos de uso)
- SPRINT 3: Infrastructure (banco de dados, APIs externas)
- SPRINT 4: Presentation (HTTP, controllers, API REST)
- SPRINT 5: Transversal (middleware, rate limit — opcional)

**Exemplo:**
Para a feature "criar plano de ação" do AçãoPlus, você executa:
1. `/impl-sprint specs/action-plan/create-action-plan.md 1` → cria `ActionPlan`, `Task`, regras de negócio
2. `/impl-sprint specs/action-plan/create-action-plan.md 2` → cria `CreateActionPlanUseCase`
3. `/impl-sprint specs/action-plan/create-action-plan.md 3` → cria `PrismaActionPlanRepository`
4. `/impl-sprint specs/action-plan/create-action-plan.md 4` → cria `POST /api/v1/action-plans`

---

#### NFRs — Non-Functional Requirements (Requisitos Não-Funcionais)

**O que é (em linguagem simples):**
São os requisitos de **como** o sistema deve funcionar, não **o quê** ele faz. Enquanto um Requisito Funcional diz "o sistema cria um plano de ação", um NFR diz "o sistema cria um plano de ação **em menos de 300ms** com **1.000 registros no banco**".

**Por que importa neste kit:**
Sem NFRs, a IA não considera performance, segurança ou disponibilidade. O resultado é código que funciona no desenvolvimento mas falha em produção com usuários reais.

**O que é na Prática:**
Todo SPEC tem uma seção de NFRs com:
- **Categoria**: Performance, Segurança, Disponibilidade, etc.
- **Requisito**: Descrição mensurável
- **Critério de Aceitação**: Como medir que foi atingido

**Exemplo:**
```
| NFR-001 | Performance | Criação de ActionPlan retorna em ≤ 300ms | Medido com 1.000 registros no banco de testes |
| NFR-002 | Segurança   | Tenant B nunca acessa dados de Tenant A  | Teste automatizado de cross-tenant access    |
```
NFR ruim (não aceito): "deve ser rápido", "deve ser seguro"
NFR bom: "retorna em ≤ 300ms medido com load test de 1.000 registros"

---

#### Given-When-Then (GWT)

**O que é (em linguagem simples):**
É um formato de escrever cenários de teste em linguagem quase natural. **Given** (Dado que) descreve o estado inicial. **When** (Quando) descreve a ação. **Then** (Então) descreve o resultado esperado.

**Por que importa neste kit:**
Os cenários GWT são a ponte entre o SPEC e os testes. O Agente Testing transforma cada cenário GWT do SPEC em um teste unitário ou de integração. Se o GWT está claro, o teste fica claro.

**O que é na Prática:**
Cada Requisito Funcional no SPEC tem pelo menos um cenário GWT — o cenário principal e os cenários alternativos (casos de erro).

**Exemplo no AçãoPlus:**
```
FR-001: Sistema cria ActionPlan com título válido

Cenário Principal:
  Given: gestor autenticado, tenant ativo, título "Contratar devs"
  When:  POST /api/v1/action-plans com { title: "Contratar devs" }
  Then:  HTTP 201, ActionPlan criado com status "draft", evento ActionPlanCreated emitido

Cenário Alternativo (título vazio):
  Given: gestor autenticado, tenant ativo
  When:  POST /api/v1/action-plans com { title: "" }
  Then:  HTTP 422, body { error: "ACTION_PLAN_TITLE_REQUIRED" }
```

---

#### POJOs / DTOs

**O que é (em linguagem simples):**
- **POJO** (Plain Old JavaScript/Java Object): Um objeto simples que só guarda dados, sem lógica. É como uma ficha de formulário — só tem campos.
- **DTO** (Data Transfer Object): Um objeto usado para transferir dados entre camadas, sem regras de negócio.

**Por que importa neste kit:**
No domínio, as entidades **não devem ser POJOs**. Uma entidade `ActionPlan` com comportamento real (`addTask()`, `complete()`) é diferente de um POJO `{ id, title, tasks }`. O Agente Review verifica se as entidades têm comportamentos — não são apenas estruturas de dados passivas.

**O que é na Prática:**
- **DTOs são usados em**: Presentation (request/response), Application (Commands e Queries)
- **Entidades de Domínio não são DTOs**: elas têm métodos, validações e emitem eventos
- Se uma entidade não tem nenhum método, é sinal de que a lógica está vazando para fora do domínio

**Exemplo:**
```typescript
// ❌ POJO — NÃO use para entidade de domínio
interface ActionPlan {
  id: string
  title: string
  tasks: Task[]
}

// ✅ Entidade com comportamento — use isto
class ActionPlan {
  addTask(props): Result<Task, Error>  // ← comportamento real
  complete(): Result<void, Error>      // ← regra de negócio
  get completionPercentage(): number   // ← cálculo no domínio
}
```

---

#### ORM — Object-Relational Mapper

**O que é (em linguagem simples):**
É uma ferramenta que traduz entre o banco de dados relacional (tabelas e linhas) e os objetos do código (classes e instâncias). Em vez de escrever SQL manualmente, você usa o ORM para salvar e buscar objetos.

**Por que importa neste kit:**
O ORM vive na camada de **Infrastructure**, nunca no **Domain**. Um dos erros mais comuns da IA é importar o ORM dentro do domínio — o que cria uma dependência direta do banco dentro das regras de negócio.

**O que é na Prática:**
No AçãoPlus com Prisma:
- `src/infrastructure/repositories/prisma-action-plan-repository.ts` ← usa Prisma ✅
- `src/domain/entities/action-plan.ts` ← NÃO importa Prisma ✅

**Exemplo de violação que o Review detecta:**
```typescript
// ❌ VIOLAÇÃO CRÍTICA — ORM no domínio
import { PrismaClient } from '@prisma/client'  // ← import de ORM no domínio

export class ActionPlan {
  async save() {
    const prisma = new PrismaClient()  // ← banco no domínio
    await prisma.actionPlan.create(...)
  }
}
```

---

#### Pirâmide de Testes

**O que é (em linguagem simples):**
É uma representação visual da distribuição ideal de tipos de teste: muitos testes unitários (rápidos e baratos), menos testes de integração, e poucos testes E2E (lentos e caros).

**Por que importa neste kit:**
Seguir a pirâmide garante que os testes sejam rápidos de executar e fáceis de manter. Projetos com muitos testes E2E e poucos testes unitários são lentos e frágeis.

**O que é na Prática:**
```
      /E2E\          5–10% — testa o sistema completo (Playwright, Cypress)
     /------\
    /Integra-\       20–30% — testa repositórios + endpoints reais
   / ção Tests \
  /-------------\
 /  Unit  Tests  \   60–70% — testa domínio + use cases com repositórios em memória
```

**Exemplo no AçãoPlus:**
- Unit: `ActionPlan_AddTask_WhenCanceled_ShouldReturnError` → roda em milissegundos
- Integration: `PrismaActionPlanRepository_FindById_ShouldNotReturnOtherTenantData` → precisa do banco
- E2E: `ActionPlan_FullLifecycle_CreateToComplete` → roda o sistema inteiro

---

#### InMemoryRepository

**O que é (em linguagem simples):**
É uma implementação "falsa" do repositório que guarda os dados na memória do computador em vez de no banco de dados. Usado exclusivamente nos testes unitários para evitar a necessidade de conectar ao banco.

**Por que importa neste kit:**
Testes unitários com banco de dados real são lentos (100x mais lentos) e dependem de infraestrutura externa. Com o InMemoryRepository, os testes de domínio e application rodam em milissegundos sem nenhuma dependência.

**O que é na Prática:**
O Agente Testing cria um arquivo `tests/helpers/in-memory-[entidade]-repository.ts` que implementa a mesma interface do repositório real, mas guarda os dados em um `Map` na memória.

**Exemplo:**
```typescript
// A interface é a mesma do repositório real
class InMemoryActionPlanRepository implements IActionPlanRepository {
  private plans = new Map<string, ActionPlan>()
  
  async findById(id, tenantId) {
    const plan = this.plans.get(id.value)
    // ← mesmo comportamento de isolamento de tenant!
    if (!plan || !plan.tenantId.equals(tenantId)) return null
    return plan
  }
  
  async save(plan) {
    this.plans.set(plan.id.value, plan)
  }
}
```

---

#### Padrão Result

**O que é (em linguagem simples):**
`Result<T, E>` é uma forma de retornar um valor que pode ser **sucesso** (`T`) ou **falha** (`E`), sem usar exceções e sem retornar `null`. É como uma caixa que contém "deu certo + o valor" ou "deu errado + o motivo".

**Por que importa neste kit:**
Retornar `null` é perigoso porque o código que chama não sabe se `null` significa "não encontrado" ou "ocorreu um erro". Lançar exceções para erros esperados (validação de input) é errado — exceções são para o inesperado. `Result<T, E>` torna o contrato explícito.

**O que é na Prática:**
Todo método de entidade que pode falhar retorna `Result<T, E>`:
```typescript
// ✅ Correto — contrato explícito
static create(props): Result<ActionPlan, DomainError>

// Quem chama sabe exatamente o que fazer:
const result = ActionPlan.create(props)
if (result.isFailure()) return Result.fail(result.error)
return Result.ok(result.value)
```

**Exemplo:**
```typescript
const result = ActionPlan.create({ title: '' })
result.isOk()      // false
result.isFailure() // true
result.error.code  // 'ACTION_PLAN_TITLE_REQUIRED'
```

---

#### YAGNI

**O que é (em linguagem simples):**
"You Aren't Gonna Need It" — "Você não vai precisar disso". É o princípio de não adicionar funcionalidade antes de precisar dela.

**Por que importa neste kit:**
A IA tende a gerar código "completo" com funcionalidades que você não pediu. Na revisão do SPEC ([Fase 3](#fase-3-revisar-e-aprovar-o-spec)), verifique se há FRs que ninguém pediu. Na revisão do Review ([Fase 7](#fase-7-revisar-sprint-1-com-o-agente-review)), verifique se há código que não está no SPEC.

**Exemplo:**
Você pediu "criar ActionPlan com título e descrição". A IA gerou também: tags, categorias, template de plano, duplicar plano, exportar para CSV. Tudo isso é YAGNI — remova do SPEC até que seja realmente necessário.

---

#### SOLID / DRY

**O que é (em linguagem simples):**
Dois conjuntos de princípios de design de código:

**SOLID** — 5 princípios para escrever código flexível e mantível:
- **S**ingle Responsibility: cada classe faz uma coisa só
- **O**pen/Closed: aberto para extensão, fechado para modificação
- **L**iskov Substitution: subclasses podem substituir a classe pai
- **I**nterface Segregation: interfaces pequenas e específicas
- **D**ependency Inversion: dependa de abstrações, não implementações

**DRY** (Don't Repeat Yourself): Não duplique lógica. Se o mesmo cálculo aparece em dois lugares, extraia para um método compartilhado.

**Por que importa neste kit:**
O ARCHITECTURE.md define a hierarquia de princípios (seção 17). O Agente Review verifica violações de SOLID (especialmente Single Responsibility e Dependency Inversion). O DRY previne que a mesma regra de negócio seja implementada em dois lugares e depois divergindo.

**Exemplo de violação que o Review detecta:**
```typescript
// ❌ Viola Single Responsibility — método faz duas coisas
activate() {
  this._status = ActionPlanStatus.active()
  this._completionPercentage = this.calculateCompletion() // ← responsabilidade diferente
}

// ✅ Correto — cada método faz uma coisa
activate() {
  this._status = ActionPlanStatus.active()
}
recalculateCompletion() {
  this._completionPercentage = this.calculateCompletion()
}
```

---

*Este guia cobre o kit completo. Para dúvidas específicas sobre cada padrão, consulte o arquivo correspondente. Para dúvidas sobre Claude Code, consulte a documentação oficial do Claude Code.*
