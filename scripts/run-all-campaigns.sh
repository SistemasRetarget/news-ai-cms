#!/bin/bash
# Detecta campañas activas en todos los sitios WP y corre SEO + CTA report en cada una.
# Resultados van a Google Sheets tab "SEO Reports" + output en terminal.
#
# Usage:
#   bash scripts/run-all-campaigns.sh
#   bash scripts/run-all-campaigns.sh --dry-run   # solo muestra URLs detectadas

set -e

DRY_RUN=false
[ "$1" = "--dry-run" ] && DRY_RUN=true

echo "🔍 Detectando campañas activas en Puyehue, TAC y Futangue..."
echo ""

CAMPAIGNS_JSON=$(python3 scripts/wp-campaign-discovery.py --json 2>/dev/null)
CAMPAIGN_COUNT=$(echo "$CAMPAIGNS_JSON" | python3 -c "import json,sys; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "0")

if [ "$CAMPAIGN_COUNT" = "0" ]; then
  echo "⚠️  No campaign pages detected."
  exit 0
fi

echo "🎯 $CAMPAIGN_COUNT campaña(s) encontrada(s):"
echo "$CAMPAIGNS_JSON" | python3 -c "
import json, sys
for c in json.load(sys.stdin):
    print(f\"  [{c['site']}] {c['url']}\")
"
echo ""

if [ "$DRY_RUN" = "true" ]; then
  echo "(--dry-run: no se corrieron los reportes)"
  exit 0
fi

# Correr reporte completo en cada URL
PASS=0
FAIL=0

echo "$CAMPAIGNS_JSON" | python3 -c "
import json, sys
for c in json.load(sys.stdin):
    print(c['url'])
" | while read -r URL; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🚀 Validando: $URL"
  bash scripts/post-deploy-seo-report.sh "$URL" || echo "⚠️  Error en $URL"
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Todos los reportes guardados en Google Sheets:"
echo "   https://docs.google.com/spreadsheets/d/1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY"
