#!/bin/bash
# COMPASS Skill - Context Loader v1.0
# Usage: /compass

set -e

WORKSPACE="/Users/spam11/Desktop/RETARGET-WORKSPACE"
LOADER="$WORKSPACE/.claude/compass-loader.js"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 COMPASS Context Loader v1.0${NC}"
echo "📚 Cargando contexto en paralelo..."
echo ""

# Ejecutar loader
node "$LOADER"

# Si llegó aquí, contexto está listo
echo ""
echo -e "${GREEN}✅ COMPASS ACTIVADO${NC}"
echo ""
echo "Tu Gantt actual:"
echo "https://docs.google.com/spreadsheets/d/1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY/edit#gid=854866235"
echo ""
echo "Protocolos disponibles:"
echo "• Flujo Completo REQ"
echo "• Toma de Requerimientos"
echo "• Monitoreo de Correos"
echo "• WordPress REST API"
echo ""
echo "¿Qué necesitas?"
