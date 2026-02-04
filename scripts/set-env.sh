#!/usr/bin/env bash
PORTAL_TITLE="${1:-Portal de Conferência Tributária}"
SIMPLES_URL="${2:-https://simplesdash.manus.space}"
IRPJ_URL="${3:-https://calc-fiscal-2etwmuhb.manus.space/}"
PORTAL_DESCRIPTION="${4:-Portal stateless para acesso rápido aos módulos tributários.}"

cat <<EOF > config.env
PORTAL_TITLE="$PORTAL_TITLE"
SIMPLES_URL="$SIMPLES_URL"
IRPJ_URL="$IRPJ_URL"
PORTAL_DESCRIPTION="$PORTAL_DESCRIPTION"
EOF
