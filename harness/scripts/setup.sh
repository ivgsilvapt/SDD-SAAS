#!/usr/bin/env bash
# harness/scripts/setup.sh
# Sobe ambiente Docker dev, aguarda banco, executa migrations e seed.
# Chamado pelo bootstrap-saas.sh ou manualmente após clonar o projeto.

set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✔${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }

# ── Pré-requisitos ────────────────────────────────────────────────────────────
command -v docker &>/dev/null || { echo "Docker não encontrado. Instale em https://docs.docker.com/get-docker/"; exit 1; }
command -v docker compose &>/dev/null || command -v docker-compose &>/dev/null || \
  { echo "docker compose não encontrado."; exit 1; }

DC="docker compose"
command -v docker-compose &>/dev/null && DC="docker-compose"

# ── Carregar .env ─────────────────────────────────────────────────────────────
if [[ -f ".env" ]]; then
  set -a; source ".env"; set +a
  ok ".env carregado"
else
  if [[ -f ".env.example" ]]; then
    cp ".env.example" ".env"
    warn ".env criado a partir de .env.example — edite com suas credenciais"
  else
    warn ".env não encontrado — usando valores padrão dos serviços Docker"
  fi
fi

# ── Subir serviços ────────────────────────────────────────────────────────────
echo ""
echo "▶ Subindo serviços Docker..."
${DC} -f docker-compose.dev.yml up -d db redis
ok "Serviços db e redis iniciados"

# ── Aguardar banco ────────────────────────────────────────────────────────────
echo ""
echo "▶ Aguardando banco de dados ficar pronto..."
MAX_RETRIES=30
count=0
until ${DC} -f docker-compose.dev.yml exec -T db pg_isready -U postgres &>/dev/null; do
  count=$((count + 1))
  [[ "${count}" -ge "${MAX_RETRIES}" ]] && { echo "Banco não respondeu após ${MAX_RETRIES}s"; exit 1; }
  printf "."
  sleep 1
done
echo ""
ok "Banco pronto"

# ── Migrations ────────────────────────────────────────────────────────────────
echo ""
echo "▶ Executando migrations..."
if [[ -f "package.json" ]]; then
  if grep -q '"db:migrate"' package.json 2>/dev/null; then
    npm run db:migrate
    ok "Migrations concluídas (npm run db:migrate)"
  elif grep -q '"prisma"' package.json 2>/dev/null; then
    npx prisma migrate deploy
    ok "Prisma migrations concluídas"
  else
    warn "Script db:migrate não encontrado em package.json — migrations pulas"
  fi
elif [[ -f "alembic.ini" ]]; then
  alembic upgrade head
  ok "Alembic migrations concluídas"
else
  warn "Nenhum runner de migration detectado — execute manualmente"
fi

# ── Seed ──────────────────────────────────────────────────────────────────────
echo ""
echo "▶ Executando seed..."
if [[ -f "package.json" ]] && grep -q '"db:seed"' package.json 2>/dev/null; then
  npm run db:seed
  ok "Seed concluído (npm run db:seed)"
else
  warn "Script db:seed não encontrado — seed pula"
fi

echo ""
echo "════════════════════════════════════════"
echo -e "  ${GREEN}Ambiente pronto!${NC}"
echo "  App: http://localhost:${PORT:-3000}"
echo "  DB : localhost:5432"
echo "════════════════════════════════════════"
