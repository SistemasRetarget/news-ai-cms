#!/bin/bash

# FASE 2: Conectar Service Account cuando el MCP esté disponible
# Ejecutar esto DESPUÉS de que FASE 1 termine exitosamente

PROJECT_ID="retarget-mcp"

echo "🔐 FASE 2: Conectando Service Account..."
echo ""

# Paso 1: Crear secreto
echo "1️⃣ Creando secreto en Secret Manager..."
gcloud secrets create retarget-mcp-credentials \
  --data-file=/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json \
  --replication-policy="automatic" \
  --project=$PROJECT_ID

echo "✅ Secreto creado"
echo ""

# Paso 2: Dar acceso a Cloud Run
echo "2️⃣ Asignando permisos..."
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding retarget-mcp-credentials \
  --member=serviceAccount:$CLOUD_RUN_SA \
  --role=roles/secretmanager.secretAccessor \
  --project=$PROJECT_ID

echo "✅ Permisos asignados"
echo ""

# Paso 3: Montar secreto en Cloud Run
echo "3️⃣ Montando secreto en Cloud Run..."
gcloud run services update retarget-mcp \
  --region=us-central1 \
  --update-secrets="/var/secrets/cloud.google.com/service_account/key.json=retarget-mcp-credentials:latest" \
  --update-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/cloud.google.com/service_account/key.json,RAILS_ENV=production" \
  --quiet

echo "✅ Servicio actualizado"
echo ""

echo "✅ FASE 2 COMPLETADA"
echo ""

# Test
MCP_URL=$(gcloud run services describe retarget-mcp --region=us-central1 --format='value(status.url)')
echo "Testeando MCP..."
curl -s $MCP_URL/health && echo "" || echo "❌ Fallo en health check"
