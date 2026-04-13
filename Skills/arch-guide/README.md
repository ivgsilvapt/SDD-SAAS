# arch-guide — Skill de Arquitetura de Software para GSD2

> Uma skill que traz os princípios de **Clean Architecture + DDD** para qualquer projeto GSD2,
> sem conflitar com o fluxo autônomo do GSD2.
> Para instalar: copie a pasta arch-guide para C:\Users\[seu-usuario]\.claude\skills\ — o GSD2 e o Claude Code reconhecem esse caminho automaticamente

---

## Por que esta skill existe?

O **GSD2** é excelente em executar tarefas de código de forma autônoma — ele planeja, implementa, testa e comita sem precisar de aprovação a cada passo. Mas, por padrão, o GSD2 não sabe *onde* cada pedaço de código deve ficar dentro do seu projeto.

Sem uma estrutura arquitetural clara, projetos crescidos com IA tendem a acumular problemas sérios:

- Lógica de negócio espalhada por controllers e banco de dados
- Código difícil de testar porque mistura regras de negócio com detalhes de banco
- Mudanças simples que quebram partes não relacionadas do sistema
- Dificuldade crescente de entender o que o sistema faz

A skill **arch-guide** resolve isso ao instalar um conjunto de documentos e regras que ensinam o GSD2 a respeitar a **Clean Architecture** e os padrões de **Domain-Driven Design (DDD)** — para que cada agente autônomo saiba, em todo momento, em qual "gaveta" o código pertence.

---

## O que a skill faz

| Comando | O que acontece |
|---|---|
| `/arch-guide init` | Configura pastas, `ARCHITECTURE.md`, glossários e registro de decisões para o projeto |
| `/arch-guide guide` | Responde dúvidas de design: "onde fica esse código?", "qual padrão usar?" |
| `/arch-guide review` | Revisa arquivos de código e aponta violações arquiteturais com severidade e correção |

### O que a skill NÃO faz

- Não bloqueia o GSD2 ou exige aprovações manuais
- Não cria arquivos SPEC ou cerimônia de planejamento
- Não implementa código — ela orienta e revisa
- Não substitui o GSD2 — trabalha *junto* com ele

---

## Como instalar

A skill precisa ser copiada para a pasta de skills do seu sistema. O GSD2 procura skills em dois locais:

- `C:\Users\[seu-usuario]\.agents\skills\` (pasta principal do GSD2)
- `C:\Users\[seu-usuario]\.claude\skills\` (pasta do Claude Code, também lida pelo GSD2)

**Passo 1 — Copie a pasta `arch-guide` para o local de skills:**

```
# Opção A: pasta do Claude Code (funciona com ambos Claude Code e GSD2)
Copie a pasta "arch-guide" para:
C:\Users\[seu-usuario]\.claude\skills\arch-guide\

# Opção B: pasta principal do GSD2
Copie a pasta "arch-guide" para:
C:\Users\[seu-usuario]\.agents\skills\arch-guide\
```

Após copiar, a estrutura deve ficar assim:
```
C:\Users\[seu-usuario]\.claude\skills\
└── arch-guide\
    ├── SKILL.md
    ├── README.md
    ├── workflows\
    │   ├── init-project.md
    │   ├── guide-design.md
    │   └── review-code.md
    ├── references\
    │   ├── clean-architecture.md
    │   ├── ddd-patterns.md
    │   ├── phase-guards.md
    │   └── testing-strategy.md
    └── templates\
        ├── ARCHITECTURE.md
        └── GLOSSARY.md
```

**Passo 2 — Confirme que o GSD2 encontrou a skill:**

Abra o GSD2 em qualquer projeto e pergunte:
```
Quais skills você tem disponíveis?
```
A skill `arch-guide` deve aparecer na lista.

---

## Exemplo Prático: TaskFlow — SaaS de Checklist To-Do

A seguir, um guia completo do zero ao código, usando o GSD2 com a skill `arch-guide` para construir um SaaS de listas de tarefas chamado **TaskFlow**.

**O que é o TaskFlow:**
- Usuários criam conta e fazem login
- Cada usuário tem suas listas de tarefas
- Dentro de cada lista há itens (tarefas) com título, prioridade e status
- Tarefas podem ser concluídas, editadas e excluídas

---

### Etapa 1 — Criar a pasta do projeto

Antes de qualquer coisa, crie uma pasta vazia para o projeto e inicialize o git:

```bash
mkdir taskflow
cd taskflow
git init
```

Isso cria um diretório limpo. O GSD2 e a skill trabalharão dentro desta pasta.

---

### Etapa 2 — Inicializar o GSD2 no projeto

Com o GSD2 instalado globalmente (`npm install -g gsd-pi@latest`), inicie-o na pasta do projeto:

```bash
gsd
```

O GSD2 vai perguntar sobre o projeto. Responda:
- **Nome:** TaskFlow
- **Descrição:** SaaS de listas de tarefas com autenticação

O GSD2 criará a pasta `.gsd/` com seus arquivos de estado. A estrutura do projeto agora é:

```
taskflow/
└── .gsd/
    ├── STATE.md          ← painel de estado atual do projeto
    └── DECISIONS.md      ← registro de decisões (começa vazio)
```

---

### Etapa 3 — Configurar a arquitetura com arch-guide

Agora diga ao GSD2 para inicializar a arquitetura:

```
/arch-guide init
```

O GSD2 vai invocar a skill e perguntar:

```
Para configurar a arquitetura do projeto, preciso de algumas informações:

1. Nome do projeto: TaskFlow

2. Stack tecnológico:
   - Linguagem:  TypeScript
   - Framework:  NestJS
   - ORM:        Prisma
   - Banco:      PostgreSQL
   - Testes:     Jest

3. Bounded contexts:
   - auth — autenticação, login, gerenciamento de conta
   - tasks — listas de tarefas, itens, status e prioridades
```

Após confirmar, a skill cria automaticamente:

```
taskflow/
├── src/
│   ├── domain/
│   │   ├── auth/         ← aqui ficam as regras de autenticação
│   │   └── tasks/        ← aqui ficam as regras de tarefas
│   ├── application/
│   │   ├── auth/         ← aqui ficam os Use Cases de auth
│   │   └── tasks/        ← aqui ficam os Use Cases de tarefas
│   ├── infrastructure/
│   │   ├── auth/         ← aqui fica o banco de dados de auth
│   │   └── tasks/        ← aqui fica o banco de dados de tarefas
│   └── presentation/
│       └── ...           ← aqui ficam os controllers HTTP
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── auth/
│   │   └── GLOSSARY.md   ← vocabulário do contexto de auth
│   ├── tasks/
│   │   └── GLOSSARY.md   ← vocabulário do contexto de tarefas
│   └── ARCH-CONTEXT-SNIPPET.md  ← trecho para colar nos milestones
├── ARCHITECTURE.md        ← a "constituição" do projeto
└── .gsd/
    ├── STATE.md
    └── DECISIONS.md       ← já pré-populado com decisões arquiteturais
```

**O que cada arquivo significa:**

- **`ARCHITECTURE.md`** — O documento mais importante. Define todas as regras do projeto: quais camadas existem, o que pode importar o quê, como nomear cada conceito. Os agentes do GSD2 vão ler este arquivo antes de implementar qualquer coisa.

- **`docs/tasks/GLOSSARY.md`** — Dicionário do contexto de tarefas. Define que "Tarefa" é o nome correto (não "Todo", não "Item", não "Card"). Os agentes usam esse vocabulário no código.

- **`.gsd/DECISIONS.md`** — Já contém duas decisões registradas: "Adotamos Clean Architecture" e "Dividimos em bounded contexts auth e tasks". Isso evita que futuros agentes questionem ou mudem essas decisões.

- **`docs/ARCH-CONTEXT-SNIPPET.md`** — Um trecho de texto que você vai colar em cada `M###-CONTEXT.md` do GSD2. Isso faz com que os agentes leiam o `ARCHITECTURE.md` antes de planejar qualquer milestone.

---

### Etapa 4 — Preencher o vocabulário do domínio

Antes de implementar qualquer coisa, abra `docs/tasks/GLOSSARY.md` e defina os termos:

```markdown
| Termo (use no código) | Definição de negócio | Termos a EVITAR |
|---|---|---|
| **Lista** | Agrupamento de tarefas criado por um usuário | Projeto, Board, Folder |
| **Tarefa** | Item de trabalho dentro de uma Lista com título e status | Todo, Item, Card, Task |
| **StatusTarefa** | Estado da tarefa: PENDENTE, EM_ANDAMENTO, CONCLUIDA | Done, Complete, Finished |
| **Prioridade** | Nível de importância: BAIXA, MEDIA, ALTA | Level, Priority, Urgency |
```

Isso pode parecer burocrático, mas é crítico: quando o GSD2 implementar o código, ele usará exatamente esses nomes. Código que usa `Todo` em um arquivo e `Tarefa` em outro cria confusão impossível de rastrear.

---

### Etapa 5 — Planejar o primeiro Milestone com GSD2

Agora sim, planejamento com GSD2:

```
/gsd
```

O GSD2 vai perguntar o que você quer construir. Descreva:

```
Quero construir o MVP do TaskFlow com:
- Cadastro e login de usuário
- Criar, listar, editar e excluir listas
- Criar, concluir e excluir tarefas dentro de uma lista
```

O GSD2 criará `.gsd/milestones/M001/M001-ROADMAP.md`.

**IMPORTANTE — cole o trecho arquitetural:**

Abra o arquivo `M001-CONTEXT.md` que o GSD2 criou (ou crie-o se não existir) e cole o conteúdo de `docs/ARCH-CONTEXT-SNIPPET.md`:

```markdown
## Architecture Reference

Before planning any implementation for this milestone, read:
- `ARCHITECTURE.md` — Architecture constitution: layer rules, DDD patterns, critical violations
- `docs/tasks/GLOSSARY.md` — Canonical terms for the tasks bounded context
- `.gsd/DECISIONS.md` — Prior architectural decisions that must be respected

This project follows Clean Architecture + DDD. The domain layer has zero external dependencies.
Dependencies flow inward: Presentation → Application → Domain ← Infrastructure.
```

**Por que isso é crucial?** A partir deste momento, cada agente do GSD2 que trabalhar neste milestone lerá o `ARCHITECTURE.md` antes de escrever qualquer linha de código. Sem isso, o GSD2 não tem como saber que não pode colocar lógica de negócio no controller.

---

### Etapa 6 — Implementar com GSD2 (a skill em ação)

Com o milestone planejado, execute o GSD2 em modo automático:

```
/gsd auto
```

O GSD2 começa a implementar. Internamente, como ele lê o `M001-CONTEXT.md`, ele sabe que deve:

1. Criar a entidade `Tarefa` primeiro (camada Domain), antes de criar o controller
2. Criar a interface `TarefaRepository` em `src/domain/tasks/` antes da implementação Prisma
3. Criar o Use Case `CriarTarefa` em `src/application/tasks/` antes do controller HTTP
4. Só então criar `TarefaController` em `src/presentation/`

Enquanto o GSD2 trabalha, você verá commits como:

```
feat(S01/T01): add Tarefa entity with invariants
feat(S01/T02): add TarefaRepository interface
feat(S01/T03): add CriarTarefaUseCase
feat(S01/T04): add PrismaTarefaRepository
feat(S01/T05): add TarefaController
```

Essa ordem — Domain primeiro, Infrastructure por último — é exatamente o que o `ARCHITECTURE.md` instrui. Sem a skill, o GSD2 poderia criar o controller primeiro e depois tentar encaixar a lógica de negócio dentro dele.

---

### Etapa 7 — Tirar dúvidas de design com arch-guide

Durante a implementação, surge uma dúvida:

> "A lógica de reordenar tarefas por prioridade — isso fica no Use Case ou na entidade Lista?"

Pergunte ao GSD2:

```
/arch-guide guide

Preciso implementar a reordenação de tarefas por prioridade dentro de uma lista.
A lógica de ordenar pertence à entidade Lista, ao Use Case, ou ao Domain Service?
```

A skill responde consultando `references/ddd-patterns.md`:

```
A lógica de ordenação pertence à entidade Lista se:
- A Lista precisa garantir algum invariante sobre a ordem (ex: não pode ter duas tarefas
  com mesma prioridade na mesma posição)

Pertence a um Domain Service se:
- A operação envolve múltiplas entidades que precisam coordenar juntas sem que nenhuma
  seja a "dona" natural dessa regra

Pertence ao Use Case se:
- É apenas uma transformação de apresentação (ordenar para exibir), sem regra de negócio

Recomendação para o TaskFlow: como a ordenação é uma preferência do usuário e não uma
regra de consistência do negócio, coloque no Use Case como OrdenarTarefasUseCase.
A Lista não precisa impor invariante sobre a ordem.

Registrei em .gsd/DECISIONS.md:
"Reordenação de tarefas é responsabilidade do Use Case (OrdenarTarefasUseCase), 
não da entidade Lista — é preferência de usuário, não regra de consistência."
```

A decisão fica registrada automaticamente em `.gsd/DECISIONS.md`, então futuros agentes do GSD2 não vão questionar isso novamente.

---

### Etapa 8 — Revisar código com arch-guide

Após o GSD2 implementar um slice, peça uma revisão arquitetural:

```
/arch-guide review

Revise os arquivos criados no slice S01: src/application/tasks/ e src/presentation/
```

A skill lê `ARCHITECTURE.md` e os arquivos especificados e produz um relatório:

```markdown
## Revisão Arquitetural — src/application/tasks/ + src/presentation/

### Violações CRÍTICAS (bloqueiam entrega)
Nenhuma encontrada.

### Violações ADVISORY (melhorar na próxima oportunidade)
- src/application/tasks/CriarTarefaUseCase.ts
  Problema: Use Case retorna o objeto de domínio `Tarefa` diretamente, sem mapear para DTO.
  Correção: Crie `TarefaResponseDto` e mapeie antes de retornar.

### Em Conformidade
- src/application/tasks/ListarTarefasUseCase.ts — camada correta, sem imports de infra ✓
- src/presentation/TarefaController.ts — só chama Use Case, sem lógica de negócio ✓
- src/presentation/schemas/ — validação de entrada isolada da lógica ✓

### Próximo Passo
Crie um /gsd quick task: "Adicionar TarefaResponseDto e mapear no CriarTarefaUseCase"
```

---

### Etapa 9 — Corrigir violações com GSD2

Com o relatório em mãos, crie a task de correção:

```
/gsd quick Adicionar TarefaResponseDto e mapear retorno no CriarTarefaUseCase
```

O GSD2 cria e implementa a correção. Por já ter lido o `ARCHITECTURE.md`, sabe exatamente:
- Onde criar o DTO (`src/application/tasks/dtos/TarefaResponseDto.ts`)
- Que o DTO é uma classe simples, sem lógica
- Que o mapeamento ocorre dentro do Use Case, antes de retornar

---

### Etapa 10 — Continuar com lições acumuladas

Ao longo do projeto, toda vez que uma decisão ou lição surgir, ela fica registrada:

- Decisões arquiteturais → `.gsd/DECISIONS.md` (registradas pela skill arch-guide)
- Lições aprendidas → `.gsd/KNOWLEDGE.md` (registradas pelo GSD2 e pela skill)

Na próxima sessão de trabalho, o GSD2 lê esses arquivos automaticamente e não repete os mesmos erros nem questiona as mesmas decisões.

---

## Fluxo Resumido

```
1. Criar pasta + git init
        ↓
2. gsd  (inicializa GSD2 no projeto)
        ↓
3. /arch-guide init  (configura arquitetura)
        ↓
4. Preencher GLOSSARY.md  (vocabulário do domínio)
        ↓
5. /gsd  (planeja milestone)
   ↳ Colar ARCH-CONTEXT-SNIPPET.md no M###-CONTEXT.md
        ↓
6. /gsd auto  (implementa autonomamente)
        ↓
7. /arch-guide guide  (dúvidas de design, quando surgirem)
        ↓
8. /arch-guide review  (revisar código, a cada slice)
        ↓
9. /gsd quick [corrigir violações]  (se houver)
        ↓
10. Repetir 5-9 para próximos milestones
```

---

## Referência dos Arquivos da Skill

| Arquivo | Para que serve |
|---|---|
| `SKILL.md` | Ponto de entrada — roteamento de intenção e princípios essenciais |
| `workflows/init-project.md` | Instruções do workflow de inicialização |
| `workflows/guide-design.md` | Instruções do workflow de orientação de design |
| `workflows/review-code.md` | Instruções do workflow de revisão de código |
| `references/clean-architecture.md` | Regras de camadas, o que pertence onde |
| `references/ddd-patterns.md` | Padrões DDD táticos com exemplos de código |
| `references/phase-guards.md` | O que agentes GSD2 devem/não devem fazer em cada fase |
| `references/testing-strategy.md` | Estratégia de testes por camada |
| `templates/ARCHITECTURE.md` | Template da constituição arquitetural do projeto |
| `templates/GLOSSARY.md` | Template do glossário de bounded context |

---

## Princípios que esta skill traz ao GSD2

| Princípio | De onde vem | Como se integra |
|---|---|---|
| Clean Architecture (4 camadas) | Robert C. Martin (Uncle Bob) | `ARCHITECTURE.md` + regras de import |
| Domain-Driven Design tático | Eric Evans | `ddd-patterns.md` + exemplos de código |
| Phase Guards por agente | Padrão operacional SDD-SAAS | `phase-guards.md` como orientações |
| Vocabulário ubíquo | DDD — Ubiquitous Language | `GLOSSARY.md` por bounded context |
| Registro de decisões | ADR (Architecture Decision Records) | `.gsd/DECISIONS.md` nativo do GSD2 |
| Lições acumuladas | GSD2 KNOWLEDGE.md | `.gsd/KNOWLEDGE.md` nativo do GSD2 |
| Testes por camada | Pirâmide de testes | `testing-strategy.md` |

---

## Perguntas Frequentes

**"O GSD2 vai parar para pedir aprovação a cada passo?"**
Não. A skill funciona como documentação e orientação — os agentes do GSD2 leem as regras e as seguem autonomamente. Não há aprovações manuais.

**"Preciso usar todos os padrões DDD?"**
Não. Comece com Entity, Repository e Use Case. Domain Events e Aggregates complicados só quando o negócio exigir.

**"E se o GSD2 violar as regras mesmo com a skill?"**
Use `/arch-guide review` após cada slice. Se houver violação, crie uma quick task para corrigir. Com o tempo, o `.gsd/KNOWLEDGE.md` acumula os padrões corretos e os agentes aprendem a evitá-los.

**"Posso usar com projetos que já têm código (brownfield)?"**
Sim. O workflow `init` instala a documentação sem apagar código existente. Após instalar, use `/arch-guide review src/` para ter um mapa das violações atuais e corrija progressivamente.

**"Esta skill funciona sem o GSD2, só com Claude Code?"**
Sim. Como a skill também é instalada em `~/.claude/skills/`, o Claude Code a reconhece. O fluxo é o mesmo: `/arch-guide init`, `/arch-guide guide`, `/arch-guide review`.
