#!/usr/bin/env bash
# Harness Template: branch-protection.sh
# Configura proteções da branch main via gh CLI.
# Uso: bash branch-protection.sh owner/repo
# Requer: gh CLI autenticado (gh auth login)

set -euo pipefail

REPO="${1:?Uso: branch-protection.sh owner/repo (ex: meu-usuario/meu-projeto)}"

echo "Configurando branch protection para: ${REPO} (branch: main)"

gh api -X PUT "repos/${REPO}/branches/main/protection" \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Lint, Test & Build"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "require_last_push_approval": true
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true
}
JSON

echo "✔ Branch protection configurada em ${REPO}/main"
echo ""
echo "Regras aplicadas:"
echo "  - CI obrigatório (status check: 'Lint, Test & Build')"
echo "  - 1 review aprovado obrigatório"
echo "  - Dismiss de reviews obsoletos ao novo push"
echo "  - CODEOWNERS review obrigatório"
echo "  - Linear history (no merge commits)"
echo "  - Force push bloqueado"
echo "  - Admin não pode bypassar"
