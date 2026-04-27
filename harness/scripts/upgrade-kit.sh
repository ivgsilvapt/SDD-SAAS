#!/usr/bin/env bash
# harness/scripts/upgrade-kit.sh
# Gerencia upgrade de versão do harness instalado no projeto.
# Lê .harness/installed-version, compara com versão alvo e aplica migrações.
# DIFERENTE de /update-kit (que sincroniza docs metodológicos do kit).
# Uso: bash harness/scripts/upgrade-kit.sh [target-version] [kit-path]

set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✔${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
err()  { echo -e "${RED}✘${NC} $1" >&2; exit 1; }

TARGET_VERSION="${1:-}"
KIT_PATH="${2:-}"

# ── Validações ────────────────────────────────────────────────────────────────
HARNESS_DIR="${PWD}/.harness"
INSTALLED_FILE="${HARNESS_DIR}/installed-version"

[[ -f "${INSTALLED_FILE}" ]] || \
  err ".harness/installed-version não encontrado. Este projeto foi bootstrapped com o harness?"

INSTALLED_VERSION="$(cat "${INSTALLED_FILE}")"

if [[ -z "${TARGET_VERSION}" ]]; then
  if [[ -n "${KIT_PATH}" ]]; then
    TARGET_VERSION="$(cat "${KIT_PATH}/VERSION" 2>/dev/null || echo '')"
  fi
  [[ -z "${TARGET_VERSION}" ]] && \
    err "Informe a versão alvo: bash upgrade-kit.sh 2.1.0 /path/to/sdd-saas"
fi

if [[ -z "${KIT_PATH}" ]]; then
  read -rp "Caminho para o kit SDD-SAAS: " KIT_PATH
fi

[[ -f "${KIT_PATH}/VERSION" ]] || err "Kit não encontrado em: ${KIT_PATH}"
KIT_AVAILABLE_VERSION="$(cat "${KIT_PATH}/VERSION")"

echo ""
echo "════════════════════════════════════════════════"
echo "  Upgrade SDD-SAAS Harness"
echo "  Instalado : ${INSTALLED_VERSION}"
echo "  Alvo      : ${TARGET_VERSION}"
echo "  Kit       : ${KIT_PATH} (v${KIT_AVAILABLE_VERSION})"
echo "════════════════════════════════════════════════"

# ── Comparação de versões ─────────────────────────────────────────────────────
version_lte() {
  printf '%s\n%s\n' "$1" "$2" | sort -V | head -1 | grep -qxF "$1"
}

if [[ "${INSTALLED_VERSION}" == "${TARGET_VERSION}" ]]; then
  ok "Já na versão ${TARGET_VERSION} — nada a fazer."
  exit 0
fi

version_lte "${TARGET_VERSION}" "${INSTALLED_VERSION}" && \
  err "Versão alvo (${TARGET_VERSION}) é menor ou igual à instalada (${INSTALLED_VERSION}). Use a versão correta."

echo ""
warn "Aplicando upgrade de v${INSTALLED_VERSION} → v${TARGET_VERSION}"
warn "Arquivos atualizados serão listados abaixo. Conflitos pausam para revisão."
echo ""

# ── Aplicar migrações de templates ────────────────────────────────────────────
TEMPLATES_SRC="${KIT_PATH}/harness/templates"
CONFLICTS=0

update_template() {
  local src="$1" dst="$2" label="$3"
  if [[ ! -f "${dst}" ]]; then
    cp "${src}" "${dst}"
    ok "Adicionado: ${label}"
  elif diff -q "${src}" "${dst}" &>/dev/null; then
    warn "Sem alterações: ${label}"
  else
    BACKUP="${dst}.backup-${INSTALLED_VERSION}"
    cp "${dst}" "${BACKUP}"
    echo ""
    warn "CONFLITO em: ${label}"
    warn "  Backup: ${BACKUP}"
    diff "${src}" "${dst}" || true
    read -rp "  Sobrescrever com versão do kit? [s/N] " resp
    if [[ "${resp,,}" == "s" ]]; then
      cp "${src}" "${dst}"
      ok "  Atualizado: ${label}"
    else
      warn "  Mantido arquivo local. Revise o diff manualmente."
      CONFLICTS=$((CONFLICTS + 1))
    fi
  fi
}

# Templates Docker
update_template "${TEMPLATES_SRC}/docker/Dockerfile.node" "Dockerfile" "Dockerfile" 2>/dev/null || true

# CI workflows
for wf in ci cd-staging cd-prod security release; do
  update_template \
    "${TEMPLATES_SRC}/ci/github/${wf}.yml" \
    ".github/workflows/${wf}.yml" \
    ".github/workflows/${wf}.yml"
done

# Docs de metodologia do kit
KIT_DOCS=(ARCHITECTURE.md AGENTS.md SAAS_PATTERNS.md TESTING_GUIDE.md)
for doc in "${KIT_DOCS[@]}"; do
  update_template "${KIT_PATH}/${doc}" ".claude/${doc}" ".claude/${doc}"
done

# ── Atualizar versão instalada ────────────────────────────────────────────────
echo "${TARGET_VERSION}" > "${INSTALLED_FILE}"
ok "Gravado: .harness/installed-version = ${TARGET_VERSION}"

echo ""
echo "════════════════════════════════════════════════"
if [[ "${CONFLICTS}" -gt 0 ]]; then
  echo -e "  ${YELLOW}Upgrade concluído com ${CONFLICTS} conflito(s)${NC}"
  echo "  Revise os arquivos .backup-${INSTALLED_VERSION}"
  echo "  e resolva os diffs manualmente."
else
  echo -e "  ${GREEN}Upgrade concluído sem conflitos!${NC}"
fi
echo "  ${INSTALLED_VERSION} → ${TARGET_VERSION}"
echo "════════════════════════════════════════════════"
