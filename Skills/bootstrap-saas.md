---
name: bootstrap-saas
description: Inicializa um novo projeto SaaS usando os templates físicos e scripts do harness SDD-SAAS. Instalável globalmente em ~/.claude/skills/ para ser chamado de qualquer novo projeto.
version: 2.0.0
---

Você é o Agente de Bootstrap do Harness SDD-SAAS. Inicialize um novo projeto SaaS completo usando os templates físicos e scripts do harness.

Argumento: $ARGUMENTS (formato: `[stack] [cloud] [profile]`)

---

## Fluxo de Execução

### 1. Localizar o kit

Tente em ordem:
1. `$SDD_SAAS_KIT_PATH` (variável de ambiente)
2. `$ARGUMENTS` se for um caminho válido
3. Solicite: "Informe o caminho para o kit SDD-SAAS (ex: ~/ferramentas/SDD-SAAS):"

Verifique que `[kit-path]/harness/scripts/bootstrap-saas.sh` existe. Se não, instrua o usuário a atualizar o kit para v2.0.0+.

Verifique que o diretório atual **não é** o próprio kit.

### 2. Coletar parâmetros

Parse `$ARGUMENTS`. Para cada valor ausente, apresente opções:

**Stack:**
- `node-nestjs` — NestJS (SaaS empresarial, módulos, DI nativo)
- `node-express` — Express (APIs simples, máxima flexibilidade)
- `python-fastapi` — FastAPI (ML/AI, async, validação Pydantic)
- `python-django` — Django (admin incluso, ORM maduro)

**Cloud:**
- `aws` | `gcp` | `azure` | `fly` | `render` | `railway` | `vps`

**Profile:**
- `budget` | `balanced` (recomendado) | `quality`

**Metadados do projeto:**
- Nome (kebab-case)
- Bounded contexts (vírgula-separados)

### 3. Confirmar e executar

Exiba resumo e confirme. Execute:

```bash
bash [kit-path]/harness/scripts/bootstrap-saas.sh \
  "[STACK]" "[CLOUD]" "[PROFILE]" "[PROJECT_NAME]"
```

### 4. Pós-bootstrap

Após sucesso, guie o desenvolvedor:

1. **Editar `.env`** com credenciais reais
2. **Subir ambiente**: `bash [kit-path]/harness/scripts/setup.sh`
3. **Criar primeira SPEC**: `/new-spec`
4. **Configurar GitHub**: push + branch protection + secrets

---

## Instalação Global

Para usar esta skill de qualquer novo projeto, copie para `~/.claude/skills/`:

```bash
cp [kit-path]/Skills/bootstrap-saas.md ~/.claude/skills/
```

Depois, em qualquer diretório vazio:

```
/bootstrap-saas node-nestjs aws balanced
```

---

## Contexto: O que o bootstrap cria

```
novo-projeto/
├── .harness/
│   ├── installed-version    ← versão do harness (ex: 2.0.0)
│   ├── stack                ← ex: node-nestjs
│   ├── cloud                ← ex: aws
│   └── profile              ← ex: balanced
├── .claude/
│   ├── ARCHITECTURE.md      ← copiado do kit
│   ├── AGENTS.md
│   ├── SAAS_PATTERNS.md
│   └── TESTING_GUIDE.md
├── .github/
│   ├── workflows/           ← ci, cd-staging, cd-prod, security, release
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── src/
├── tests/
├── specs/
├── Dockerfile               ← template do harness com placeholders substituídos
├── docker-compose.dev.yml
├── docker-compose.test.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── .editorconfig
└── CLAUDE.md                ← template do kit
```
