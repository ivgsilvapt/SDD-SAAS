#!/usr/bin/env bash
# harness/scripts/bootstrap-saas.sh
# Bootstrap de novo projeto SaaS a partir do harness SDD-SAAS.
# Idempotente: detecta estado existente e pula passos já concluídos.
# Uso: bash harness/scripts/bootstrap-saas.sh [stack] [cloud] [profile] [project_name]
# Exemplo: bash bootstrap-saas.sh node-nestjs aws balanced acaoplus
#
# Fluxo: 11 passos. O Passo 8 instala a Skill Context7 (lazy-loaded) em
# .claude/skills/context7.md. O modo MCP (always-on) é opt-in: copie
# harness/templates/mcp/.mcp.json para a raiz do projeto. Ver ORIENTACAO §2.7.

set -euo pipefail

# ── Cores ─────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✔${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
err()  { echo -e "${RED}✘${NC} $1" >&2; exit 1; }
step() { echo -e "\n${YELLOW}▶ PASSO $1${NC}"; }

# ── Localizar kit ─────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TARGET_DIR="${PWD}"

[[ "${TARGET_DIR}" == "${KIT_ROOT}" ]] && \
  err "Execute este script dentro do diretório do NOVO projeto, não dentro do kit."

# ── Parâmetros ou modo interativo ─────────────────────────────────────────────
STACK="${1:-}"
CLOUD="${2:-}"
PROFILE="${3:-}"
PROJECT_NAME="${4:-}"

collect_input() {
  if [[ -z "${STACK}" ]]; then
    echo "Stack disponíveis: node-nestjs, node-express, python-fastapi, python-django"
    read -rp "Stack: " STACK
  fi
  if [[ -z "${CLOUD}" ]]; then
    echo "Cloud disponíveis: aws, gcp, azure, fly, render, railway, vps"
    read -rp "Cloud provider: " CLOUD
  fi
  if [[ -z "${PROFILE}" ]]; then
    echo "Token profiles: budget, balanced, quality"
    read -rp "Profile: " PROFILE
  fi
  if [[ -z "${PROJECT_NAME}" ]]; then
    read -rp "Nome do projeto (ex: acaoplus): " PROJECT_NAME
  fi
}

collect_input

PROJECT_NAME_LOWER="${PROJECT_NAME,,}"
KIT_VERSION="$(cat "${KIT_ROOT}/VERSION")"

echo ""
echo "════════════════════════════════════════════════"
echo "  Bootstrap SDD-SAAS Harness v${KIT_VERSION}"
echo "  Projeto : ${PROJECT_NAME}"
echo "  Stack   : ${STACK}"
echo "  Cloud   : ${CLOUD}"
echo "  Profile : ${PROFILE}"
echo "  Destino : ${TARGET_DIR}"
echo "════════════════════════════════════════════════"
echo ""

# ── Passo 1: Estrutura de pastas ──────────────────────────────────────────────
step "1/11 — Estrutura de pastas"
dirs=(src tests specs .claude docs)
for d in "${dirs[@]}"; do
  if [[ ! -d "${TARGET_DIR}/${d}" ]]; then
    mkdir -p "${TARGET_DIR}/${d}"
    ok "Criado: ${d}/"
  else
    warn "Já existe: ${d}/"
  fi
done
mkdir -p "${TARGET_DIR}/.harness"

# ── Passo 2: Copiar templates físicos ─────────────────────────────────────────
step "2/11 — Templates físicos"

# Selecionar Dockerfile por stack
case "${STACK}" in
  node-*) DOCKERFILE_SRC="Dockerfile.node" ;;
  python-*) DOCKERFILE_SRC="Dockerfile.python" ;;
  go-*) DOCKERFILE_SRC="Dockerfile.go" ;;
  *) err "Stack não reconhecida: ${STACK}" ;;
esac

TEMPLATES_DIR="${KIT_ROOT}/harness/templates"

copy_template() {
  local src="$1" dst="$2"
  if [[ ! -f "${dst}" ]]; then
    cp "${src}" "${dst}"
    ok "Copiado: $(basename "${dst}")"
  else
    warn "Já existe (mantido): $(basename "${dst}")"
  fi
}

copy_template "${TEMPLATES_DIR}/docker/${DOCKERFILE_SRC}" "${TARGET_DIR}/Dockerfile"
copy_template "${TEMPLATES_DIR}/docker/docker-compose.dev.yml" "${TARGET_DIR}/docker-compose.dev.yml"
copy_template "${TEMPLATES_DIR}/docker/docker-compose.test.yml" "${TARGET_DIR}/docker-compose.test.yml"
copy_template "${TEMPLATES_DIR}/docker/.dockerignore" "${TARGET_DIR}/.dockerignore"
copy_template "${TEMPLATES_DIR}/env/.env.example" "${TARGET_DIR}/.env.example"
copy_template "${TEMPLATES_DIR}/env/.env.test.example" "${TARGET_DIR}/.env.test.example"

mkdir -p "${TARGET_DIR}/.github/workflows"
for wf in ci cd-staging cd-prod security release; do
  copy_template \
    "${TEMPLATES_DIR}/ci/github/${wf}.yml" \
    "${TARGET_DIR}/.github/workflows/${wf}.yml"
done

mkdir -p "${TARGET_DIR}/.github/ISSUE_TEMPLATE"
for f in CODEOWNERS dependabot.yml PULL_REQUEST_TEMPLATE.md; do
  copy_template "${TEMPLATES_DIR}/github/${f}" "${TARGET_DIR}/.github/${f}"
done
for f in bug_report.md feature_request.md spec_request.md; do
  copy_template \
    "${TEMPLATES_DIR}/github/ISSUE_TEMPLATE/${f}" \
    "${TARGET_DIR}/.github/ISSUE_TEMPLATE/${f}"
done

copy_template "${TEMPLATES_DIR}/.editorconfig" "${TARGET_DIR}/.editorconfig"

# ── Passo 3: Substituir placeholders ──────────────────────────────────────────
step "3/11 — Substituição de placeholders"

NODE_VERSION="20"
PYTHON_VERSION="3.12"
PORT="3000"

substitute() {
  local file="$1"
  [[ -f "${file}" ]] || return
  sed -i \
    -e "s/{{APP_NAME}}/${PROJECT_NAME_LOWER}/g" \
    -e "s/{{DB_NAME}}/${PROJECT_NAME_LOWER}/g" \
    -e "s/{{NODE_VERSION}}/${NODE_VERSION}/g" \
    -e "s/{{PYTHON_VERSION}}/${PYTHON_VERSION}/g" \
    -e "s/{{PORT}}/${PORT}/g" \
    -e "s/{{CLOUD_PROVIDER}}/${CLOUD}/g" \
    "${file}"
}

substitute "${TARGET_DIR}/Dockerfile"
substitute "${TARGET_DIR}/docker-compose.dev.yml"
substitute "${TARGET_DIR}/docker-compose.test.yml"
for wf in ci cd-staging cd-prod; do
  substitute "${TARGET_DIR}/.github/workflows/${wf}.yml"
done
ok "Placeholders substituídos"

# ── Passo 4: Copiar arquivos de metodologia do kit ────────────────────────────
step "4/11 — Arquivos de metodologia"
kit_files=(
  ARCHITECTURE.md AGENTS.md SPEC_TEMPLATE.md TESTING_GUIDE.md
  SAAS_PATTERNS.md GIT_WORKFLOW.md GLOSSARY_TEMPLATE.md
  HANDOFF_TEMPLATE.md KNOWLEDGE_TEMPLATE.md CODEBASE_MAPPING_GUIDE.md
)
mkdir -p "${TARGET_DIR}/.claude"
for f in "${kit_files[@]}"; do
  copy_template "${KIT_ROOT}/${f}" "${TARGET_DIR}/.claude/${f}"
done

# CLAUDE.md no destino
copy_template "${KIT_ROOT}/Slash Commands/CLAUDE.md" "${TARGET_DIR}/CLAUDE.md"

# ── Passo 5: Git init ─────────────────────────────────────────────────────────
step "5/11 — Git"
if [[ ! -d "${TARGET_DIR}/.git" ]]; then
  git -C "${TARGET_DIR}" init
  git -C "${TARGET_DIR}" checkout -b main 2>/dev/null || true
  ok "Git inicializado (branch: main)"
else
  warn "Git já existe — mantido"
fi

# Adicionar .gitignore se não existir
if [[ ! -f "${TARGET_DIR}/.gitignore" ]]; then
  cat > "${TARGET_DIR}/.gitignore" <<'GITIGNORE'
node_modules/
dist/
build/
.env
.env.*
!.env.example
!.env.test.example
coverage/
.nyc_output/
*.log
.DS_Store
__pycache__/
*.pyc
.venv/
venv/
GITIGNORE
  ok "Criado: .gitignore"
fi

# ── Passo 6: Branch protection (requer gh CLI) ────────────────────────────────
step "6/11 — Branch protection"
if command -v gh &>/dev/null; then
  REMOTE_URL="$(git -C "${TARGET_DIR}" remote get-url origin 2>/dev/null || echo '')"
  if [[ -n "${REMOTE_URL}" ]]; then
    REPO="$(echo "${REMOTE_URL}" | sed 's/.*github.com[:/]\(.*\)\.git/\1/')"
    warn "Para configurar branch protection, execute após push:"
    warn "  bash ${TEMPLATES_DIR}/github/branch-protection.sh ${REPO}"
  else
    warn "Sem remote configurado — branch protection pula (configure após push)"
  fi
else
  warn "gh CLI não encontrado — branch protection pula"
fi

# ── Passo 7: Git hooks (Husky para Node, pre-commit para Python) ──────────────
step "7/11 — Git hooks"
case "${STACK}" in
  node-*)
    if [[ -f "${TARGET_DIR}/package.json" ]]; then
      cp -r "${TEMPLATES_DIR}/git-hooks/.husky" "${TARGET_DIR}/.husky" 2>/dev/null || true
      cp "${TEMPLATES_DIR}/git-hooks/commitlint.config.js" "${TARGET_DIR}/" 2>/dev/null || true
      cp "${TEMPLATES_DIR}/git-hooks/lint-staged.config.js" "${TARGET_DIR}/" 2>/dev/null || true
      ok "Husky instalado"
    else
      warn "package.json não encontrado — husky pula (crie package.json primeiro)"
    fi ;;
  python-*)
    cp "${TEMPLATES_DIR}/git-hooks/.pre-commit-config.yaml" "${TARGET_DIR}/" 2>/dev/null || true
    ok ".pre-commit-config.yaml copiado"
    if command -v pre-commit &>/dev/null; then
      pre-commit install --install-hooks
      ok "pre-commit hooks instalados"
    else
      warn "pre-commit não encontrado — execute: pip install pre-commit && pre-commit install"
    fi ;;
esac

# ── Passo 8: Instalar Skill Context7 (project-scoped, lazy-loaded) ────────────
step "8/11 — Skill Context7"
mkdir -p "${TARGET_DIR}/.claude/skills"
copy_template "${KIT_ROOT}/Skills/context7.md" "${TARGET_DIR}/.claude/skills/context7.md"
ok "Skill Context7 instalada em .claude/skills/context7.md"
warn "Para MCP always-on (opt-in), copie ${TEMPLATES_DIR}/mcp/.mcp.json — ver ORIENTACAO §2.7"

# ── Passo 9: Instalar dependências ────────────────────────────────────────────
step "9/11 — Instalação de dependências"
case "${STACK}" in
  node-*)
    if [[ -f "${TARGET_DIR}/package.json" ]]; then
      npm --prefix "${TARGET_DIR}" install
      ok "npm install concluído"
    else
      warn "package.json não encontrado — crie e rode npm install manualmente"
    fi ;;
  python-*)
    if [[ -f "${TARGET_DIR}/requirements.txt" ]]; then
      pip install -r "${TARGET_DIR}/requirements.txt" -q
      ok "pip install concluído"
    else
      warn "requirements.txt não encontrado — crie e instale manualmente"
    fi ;;
esac

# ── Passo 10: Setup (Docker dev) ──────────────────────────────────────────────
step "10/11 — Setup do ambiente"
if [[ -f "${KIT_ROOT}/harness/scripts/setup.sh" ]]; then
  warn "Para subir o ambiente Docker, execute:"
  warn "  bash ${KIT_ROOT}/harness/scripts/setup.sh"
fi

# ── Passo 11: Gravar versão instalada + primeiro commit ───────────────────────
step "11/11 — Versão instalada e primeiro commit"
echo "${KIT_VERSION}" > "${TARGET_DIR}/.harness/installed-version"
echo "${STACK}" > "${TARGET_DIR}/.harness/stack"
echo "${CLOUD}" > "${TARGET_DIR}/.harness/cloud"
echo "${PROFILE}" > "${TARGET_DIR}/.harness/profile"
ok "Gravado: .harness/installed-version = ${KIT_VERSION}"

STAGED="$(git -C "${TARGET_DIR}" status --porcelain 2>/dev/null | wc -l)"
if [[ "${STAGED}" -gt 0 ]]; then
  git -C "${TARGET_DIR}" add -A
  git -C "${TARGET_DIR}" commit -m "chore: initial harness setup (sdd-saas v${KIT_VERSION})"
  ok "Primeiro commit criado"
else
  warn "Nada a commitar"
fi

echo ""
echo "════════════════════════════════════════════════"
echo -e "  ${GREEN}Bootstrap concluído!${NC}"
echo "  Projeto : ${PROJECT_NAME}"
echo "  Versão  : ${KIT_VERSION}"
echo ""
echo "  Próximos passos:"
echo "  1. Edite .env com suas credenciais reais"
echo "  2. bash harness/scripts/setup.sh"
echo "  3. /new-spec para criar sua primeira SPEC"
echo "════════════════════════════════════════════════"
