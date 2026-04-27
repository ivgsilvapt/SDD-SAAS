Você é o Agente de Inicialização do Kit SDD-SAAS. Sua responsabilidade é configurar um novo projeto SaaS com toda a estrutura, arquivos e comandos necessários para usar o kit imediatamente — sem que o desenvolvedor precise copiar arquivos manualmente ou configurar nada.

Caminho para o kit SDD-SAAS: $ARGUMENTS

---

## PASSO 1 — Verificar pré-requisitos

Antes de qualquer ação:

1. Verifique se o argumento `$ARGUMENTS` foi fornecido. Se não foi, informe ao desenvolvedor:

   > "Para usar este comando forneça o caminho para o kit SDD-SAAS:\n`/init-sdd-saas /caminho/para/sdd-saas`\n\nExemplo: `/init-sdd-saas ~/ferramentas/SDD-SAAS`"
   >
   > Encerre a execução aqui.

2. Verifique se o diretório de kit fornecido existe e contém `ARCHITECTURE.md`. Se não encontrar, informe:

   > "Caminho `[argumento]` não encontrado ou não é um kit SDD-SAAS válido. Verifique o caminho e tente novamente."
   >
   > Encerre a execução aqui.

3. Verifique se o diretório atual **não é** o próprio kit (não copie o kit para dentro dele mesmo). Se o diretório atual for o mesmo do kit, informe:

   > "Execute este comando dentro do diretório do **novo projeto**, não dentro do kit SDD-SAAS."
   >
   > Encerre a execução aqui.

4. Liste os arquivos do kit encontrados para confirmar ao desenvolvedor o que será usado.

---

## PASSO 2 — Coletar informações do projeto

Apresente ao desenvolvedor o seguinte formulário e aguarde a resposta antes de continuar:

```
Para configurar o kit, preciso de algumas informações sobre o projeto:

1. Nome do projeto (ex: AçãoPlus, BillingHub, TaskFlow):

2. Stack tecnológico:
   a) Linguagem:  TypeScript / Python / Java / Go / outro?
   b) Framework:  NestJS / FastAPI / Spring / Gin / outro?
   c) ORM:        Prisma / SQLAlchemy / Hibernate / GORM / outro?
   d) Banco:      PostgreSQL / MySQL / MongoDB / outro?
   e) Testes:     Jest / Pytest / JUnit / outro?

3. Bounded contexts (domínios do negócio):
   Liste cada bounded context com uma frase descrevendo sua responsabilidade.
   Exemplo:
   - auth — autenticação, login, sessões
   - tenant — onboarding, workspaces, membros
   - billing — assinaturas, cobranças, planos
   - [nome-do-seu-produto] — [o core do negócio]

Responda abaixo e confirme com "ok" ou "pode prosseguir":
```

Aguarde a confirmação do desenvolvedor.

---

## PASSO 3 — Criar estrutura de pastas

Execute no diretório atual:

```bash
mkdir -p src/presentation
mkdir -p src/application
mkdir -p src/domain
mkdir -p src/infrastructure
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e
mkdir -p specs
mkdir -p .claude/commands
mkdir -p .specs/codebase
```

Confirme ao desenvolvedor quais pastas foram criadas.

---

## PASSO 4 — Copiar arquivos do kit

Usando o caminho do kit fornecido (`$ARGUMENTS`), copie os seguintes arquivos para a raiz do projeto atual:

**Arquivos de referência arquitetural (raiz):**
- `ARCHITECTURE.md`
- `AGENTS.md`
- `SPEC_TEMPLATE.md`
- `TESTING_GUIDE.md`
- `SAAS_PATTERNS.md`
- `GLOSSARY_TEMPLATE.md`
- `STATE_TEMPLATE.md`
- `PROJECT_TEMPLATE.md`
- `ROADMAP_TEMPLATE.md`
- `HANDOFF_TEMPLATE.md`
- `CODEBASE_MAPPING_GUIDE.md`
- `GIT_WORKFLOW.md`
- `KNOWLEDGE_TEMPLATE.md` → copiar como `KNOWLEDGE.md` (inicia vazio com apenas os cabeçalhos e as linhas de exemplo — o conteúdo real será preenchido durante o uso)

**Slash commands (pasta `.claude/commands/`):**
- `Slash Commands/new-spec.md`         → `.claude/commands/new-spec.md`
- `Slash Commands/impl-sprint.md`      → `.claude/commands/impl-sprint.md`
- `Slash Commands/review-arch.md`      → `.claude/commands/review-arch.md`
- `Slash Commands/test-sprint.md`      → `.claude/commands/test-sprint.md`
- `Slash Commands/migrate-sprint.md`   → `.claude/commands/migrate-sprint.md`
- `Slash Commands/quick-fix.md`        → `.claude/commands/quick-fix.md`
- `Slash Commands/pause-session.md`    → `.claude/commands/pause-session.md`
- `Slash Commands/resume-session.md`   → `.claude/commands/resume-session.md`
- `Slash Commands/map-codebase.md`     → `.claude/commands/map-codebase.md`
- `Slash Commands/forensics-sprint.md` → `.claude/commands/forensics-sprint.md`
- `Slash Commands/discover.md`         → `.claude/commands/discover.md`
- `Slash Commands/init-devops.md`      → `.claude/commands/init-devops.md`
- `Slash Commands/update-pipeline.md`  → `.claude/commands/update-pipeline.md`
- `Slash Commands/security-audit.md`   → `.claude/commands/security-audit.md`
- `Slash Commands/define-slo.md`       → `.claude/commands/define-slo.md`
- `Slash Commands/generate-api-docs.md` → `.claude/commands/generate-api-docs.md`
- `Slash Commands/retrospect.md`       → `.claude/commands/retrospect.md`
- `Slash Commands/update-kit.md`       → `.claude/commands/update-kit.md`
- `Slash Commands/bootstrap-saas.md`   → `.claude/commands/bootstrap-saas.md`
- `Slash Commands/upgrade-kit.md`      → `.claude/commands/upgrade-kit.md`

Use Read para ler cada arquivo do kit e Write para criá-lo no destino.

**Nota sobre templates físicos do harness (v2.0+):** Se o kit for v2.0+, após copiar os slash commands também copie os templates físicos para o projeto:
- `harness/templates/docker/Dockerfile.node` (ou .python / .go conforme stack do PASSO 2)
- `harness/templates/docker/docker-compose.dev.yml`
- `harness/templates/docker/docker-compose.test.yml`
- `harness/templates/docker/.dockerignore`
- `harness/templates/env/.env.example`
- `harness/templates/env/.env.test.example`
- Toda a pasta `harness/templates/ci/github/` → `.github/workflows/`

Ao copiar, substitua os placeholders `{{APP_NAME}}`, `{{NODE_VERSION}}`, `{{PORT}}`, `{{DB_NAME}}` com os valores coletados no PASSO 2. Isso garante que o projeto herda templates determinísticos em vez de gerá-los via LLM.

Crie também `.harness/installed-version` com a versão atual do kit (leia do arquivo `VERSION` na raiz do kit).

---

## PASSO 5 — Criar STATE.md

Leia `STATE_TEMPLATE.md` do kit e crie `STATE.md` na raiz do projeto com o mesmo conteúdo.

---

## PASSO 6 — Criar PROJECT.md

Leia `PROJECT_TEMPLATE.md` do kit e crie `PROJECT.md` na raiz do projeto.

Preencha automaticamente a seção de cabeçalho com o nome do projeto coletado no Passo 2.
Deixe as demais seções com os placeholders do template para o desenvolvedor preencher.

---

## PASSO 7 — Criar CLAUDE.md

Crie o arquivo `CLAUDE.md` na raiz do projeto com o conteúdo abaixo, substituindo os placeholders pelos dados coletados no Passo 2:

```markdown
# CLAUDE.md — [NOME_DO_PROJETO]

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
@specs/[BOUNDED_CONTEXT_PRINCIPAL]/GLOSSARY.md — Vocabulário do domínio
@PROJECT.md — Visão e propósito do produto (opcional, recomendado para o Agente Spec)
@KNOWLEDGE.md — Lições acumuladas de sessões anteriores (opcional — se existir, leia antes de implementar)
@GIT_WORKFLOW.md — Estratégia de branches por SPEC (leia uma vez no início do projeto, não é necessário em toda sessão)

Quando acionar um agente via slash command, consulte AGENTS.md para o contexto mínimo
daquele agente e inclua apenas os arquivos necessários — não inclua o kit inteiro.

## Comandos disponíveis

### Pré-SPEC
- /discover [ideia] — valida problema/ideia via Agente Discovery, gera DISCOVERY.md

### Ciclo SPEC → Review
- /new-spec [descrição da feature] — cria novo SPEC via Agente Spec
- /review-arch [spec] analyze — valida consistência do SPEC via Agente Analyze
- /impl-sprint [spec] [n] — implementa SPRINT N via Agente Implementation
- /test-sprint [spec] [n] — gera testes do SPRINT N via Agente Testing
- /review-arch [spec] [n] — revisa código do SPRINT N via Agente Review
- /migrate-sprint [spec] [n] — gera migration SQL do SPRINT N via Agente Migration
- /forensics-sprint [spec] [n] — diagnóstico de SPRINT com falha (Review REPROVADO ou testes persistentes)

### Pós-Review / Produção
- /init-devops [cloud] — configura CI/CD, Dockerfile e .env.example via Agente DevOps
- /update-pipeline [spec] — atualiza pipeline após novos serviços adicionados pelo SPEC
- /security-audit [spec|full] — auditoria STRIDE + OWASP via Agente Security Audit
- /define-slo [spec] — define SLOs, alertas e runbook via Agente SRE
- /generate-api-docs — gera/atualiza openapi.yaml via Agente API Docs

### Operação contínua
- /quick-fix [descrição] — correção pequena (≤3 arquivos), sem cerimônia de SPEC
- /pause-session — salva o estado atual e cria HANDOFF.md para retomada posterior
- /resume-session — retoma sessão a partir do HANDOFF.md
- /map-codebase [path?] — analisa codebase existente e gera documentação em .specs/codebase/
- /retrospect — revisão de milestone: velocity, lições, atualiza KNOWLEDGE.md
- /update-kit [caminho-do-kit] — atualiza os arquivos de referência do kit no projeto

## Tecnologias deste projeto
- Linguagem: [LINGUAGEM]
- Framework: [FRAMEWORK]
- ORM: [ORM]
- Banco: [BANCO]
- Testes: [TEST_RUNNER]

## Bounded Contexts deste projeto
[BOUNDED_CONTEXTS_LISTADOS]

## Observações específicas deste projeto
[Adicione aqui qualquer exceção às regras do ARCHITECTURE.md, tecnologias especiais,
integrações externas ou contexto de negócio que a IA precisa conhecer]
```

Substitua os valores marcados com `[MAIÚSCULAS]` pelas informações coletadas no Passo 2. Na seção "Bounded Contexts", liste cada contexto em um formato `- nome-do-contexto — descrição em uma linha`.

---

## PASSO 8 — Criar GLOSSARY.md inicial por bounded context

Para cada bounded context informado no Passo 2:

1. Crie a pasta: `specs/[nome-do-bounded-context]/`
2. Leia `GLOSSARY_TEMPLATE.md` do kit e crie `specs/[nome-do-bounded-context]/GLOSSARY.md` com o mesmo conteúdo
3. Preencha o cabeçalho do GLOSSARY.md com o nome do bounded context

---

## PASSO 9 — Confirmação e próximos passos

Apresente ao desenvolvedor o resumo final:

```
✅ Kit SDD-SAAS inicializado em [nome-do-projeto].

Estrutura criada:
meu-projeto/
├── .claude/
│   └── commands/          ← 18 slash commands prontos
│       ├── new-spec.md          ├── discover.md
│       ├── impl-sprint.md       ├── init-devops.md
│       ├── review-arch.md       ├── update-pipeline.md
│       ├── test-sprint.md       ├── security-audit.md
│       ├── migrate-sprint.md    ├── define-slo.md
│       ├── quick-fix.md         ├── generate-api-docs.md
│       ├── pause-session.md     ├── retrospect.md
│       ├── resume-session.md    ├── update-kit.md
│       ├── map-codebase.md
│       └── forensics-sprint.md
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
│   └── [bounded-contexts]/
│       └── GLOSSARY.md    ← criado para cada bounded context
├── .specs/codebase/       ← usado pelo /map-codebase
├── ARCHITECTURE.md        AGENTS.md         SPEC_TEMPLATE.md
├── TESTING_GUIDE.md       SAAS_PATTERNS.md  GLOSSARY_TEMPLATE.md
├── STATE_TEMPLATE.md      PROJECT_TEMPLATE.md ROADMAP_TEMPLATE.md
├── HANDOFF_TEMPLATE.md    CODEBASE_MAPPING_GUIDE.md
├── GIT_WORKFLOW.md        ← estratégia de branches por SPEC
├── KNOWLEDGE.md           ← registro append-only de lições aprendidas
├── STATE.md               ← memória persistente (pronta para uso)
├── PROJECT.md             ← visão do produto (preencha antes do primeiro SPEC)
└── CLAUDE.md              ← contexto automático do Claude Code ✓

Próximos passos (nesta ordem):
1. Abra PROJECT.md e preencha Vision Statement e Non-Goals do seu SaaS
2. Abra specs/[bounded-context-principal]/GLOSSARY.md e defina os termos do domínio
3. Leia GIT_WORKFLOW.md para entender o padrão de branches por SPEC (leitura única)
4. Use /new-spec [descrição] para criar sua primeira feature

Dica: Se estiver adotando o kit em um projeto que já tem código, execute primeiro:
  /map-codebase src/
Isso gera documentação do estado atual em .specs/codebase/ antes de criar novos SPECs.
```
