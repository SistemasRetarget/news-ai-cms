#!/bin/bash

# COMPASS Cloud Deployment
# Uso: bash deploy.sh

set -e

PROJECT_ID="retarget-mcp"
FUNCTION_NAME="compass-email-responder"
REGION="us-central1"
SCHEDULER_NAME="compass-responder-trigger"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║      COMPASS: Deploying Cloud Function                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# 1️⃣  Verificar gcloud
echo ""
echo "📍 Verificando Google Cloud CLI..."
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud no instalado. Instalar desde https://cloud.google.com/sdk"
    exit 1
fi

# 2️⃣ Configurar proyecto
echo "📍 Configurando proyecto: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# 3️⃣ Habilitar APIs
echo "📍 Habilitando APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable gmail.googleapis.com
gcloud services enable sheets.googleapis.com
gcloud services enable secretmanager.googleapis.com

# 4️⃣ Deploy Cloud Function
echo ""
echo "📍 Desplegando Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --source ./cloud \
  --entry-point main \
  --memory 512MB \
  --timeout 60s \
  --region $REGION \
  --set-env-vars \
    GCP_PROJECT_ID=$PROJECT_ID,\
    SHEETS_ID=1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY,\
    SHEET_NAME=Retarget-Mayo-2026 \
  --service-account default

# Obtener URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region $REGION --format='value(httpsTrigger.url)')

echo "✅ Cloud Function desplegada"
echo "   URL: $FUNCTION_URL"

# 5️⃣ Crear Scheduler
echo ""
echo "📍 Creando Cloud Scheduler..."

# Verificar si ya existe
if gcloud scheduler jobs describe $SCHEDULER_NAME --location $REGION &> /dev/null; then
    echo "ℹ️  Job ya existe. Actualizando..."
    gcloud scheduler jobs update http $SCHEDULER_NAME \
      --location $REGION \
      --uri=$FUNCTION_URL \
      --http-method=GET \
      --schedule="*/5 * * * *" \
      --timezone="America/Santiago" \
      --oidc-service-account-email=default@$PROJECT_ID.iam.gserviceaccount.com
else
    echo "Creando nuevo job..."
    gcloud scheduler jobs create http $SCHEDULER_NAME \
      --location $REGION \
      --uri=$FUNCTION_URL \
      --http-method=GET \
      --schedule="*/5 * * * *" \
      --timezone="America/Santiago" \
      --oidc-service-account-email=default@$PROJECT_ID.iam.gserviceaccount.com
fi

echo "✅ Cloud Scheduler configurado"
echo "   Job: $SCHEDULER_NAME"
echo "   Intervalo: cada 5 minutos"

# 6️⃣ Resumen
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          ✅ DEPLOYMENT COMPLETADO                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"

echo ""
echo "📊 Próximos pasos:"
echo ""
echo "1. Setup OAuth (una sola vez):"
echo "   cd cloud && python3 setup-gmail-oauth.py"
echo ""
echo "2. Verificar logs:"
echo "   gcloud functions logs read $FUNCTION_NAME --limit 50 --follow"
echo ""
echo "3. Ejecutar manualmente (testing):"
echo "   gcloud functions call $FUNCTION_NAME"
echo ""
echo "4. Cloud Scheduler (automático cada 5 min):"
echo "   gcloud scheduler jobs describe $SCHEDULER_NAME --location $REGION"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "URL de Cloud Function:"
echo "   $FUNCTION_URL"
echo ""
