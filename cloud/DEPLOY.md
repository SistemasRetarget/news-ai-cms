# 🚀 COMPASS Cloud Deployment

Cloud Function + Cloud Scheduler para responder automáticamente a Mauricio/Leig.

---

## 📋 Requisitos previos

```bash
# 1. Instalar Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 2. Configurar proyecto
gcloud init
gcloud config set project retarget-mcp

# 3. Autenticar
gcloud auth login
gcloud auth application-default login
```

---

## 🔑 Paso 1: Setup OAuth para Gmail (Una sola vez)

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/cloud

# Crear OAuth credentials en Google Cloud Console
# https://console.cloud.google.com/apis/credentials
# → Create OAuth 2.0 Client ID (Desktop app)
# → Descargar JSON

python3 setup-gmail-oauth.py
```

**Qué hace:**
- Abre navegador para que autorices
- Obtiene refresh token de Gmail
- Guarda en Secret Manager (o .env.local si prefieres)

---

## 🎯 Paso 2: Deploy Cloud Function

```bash
gcloud functions deploy compass-email-responder \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --source ./cloud \
  --entry-point main \
  --memory 512MB \
  --timeout 60s \
  --set-env-vars SHEETS_ID="1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY" \
  --service-account compass-function@retarget-mcp.iam.gserviceaccount.com
```

**Anotá la URL que retorna:**
```
https://[REGION]-retarget-mcp.cloudfunctions.net/compass-email-responder
```

---

## ⏰ Paso 3: Cloud Scheduler (Cada 5 minutos)

```bash
gcloud scheduler jobs create http compass-responder-trigger \
  --schedule="*/5 * * * *" \
  --timezone="America/Santiago" \
  --http-method=GET \
  --uri=https://[REGION]-retarget-mcp.cloudfunctions.net/compass-email-responder \
  --location=us-central1
```

---

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
gcloud functions logs read compass-email-responder --limit 50 --follow
```

### Ver ejecuciones de Scheduler

```bash
gcloud scheduler jobs describe compass-responder-trigger --location=us-central1
```

### Ejecutar manualmente (testing)

```bash
gcloud functions call compass-email-responder --region=[REGION]
```

---

## 📈 Cómo funciona

```
Mauricio/Leig envía email
        ↓
Cloud Scheduler (cada 5 min) lee Gmail
        ↓
Encuentra emails sin responder
        ↓
Clasifica: ¿Corrección? ¿Reporte?
        ↓
Lee Sheets vivo → stats (✅ 5 completadas, ⏳ 3 en progreso)
        ↓
Responde con template + stats
        ↓
Registra T-XX en Sheets ("Pendiente Luis - Detalles")
        ↓
Marca email como procesado
        ↓
Espera 5 min para siguiente ejecución
```

---

## 🛠️ Troubleshooting

### Error: "Permission denied"

```bash
# Asegurar que el service account tenga permisos
gcloud iam service-accounts add-iam-policy-binding \
  compass-function@retarget-mcp.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor \
  --member serviceAccount:compass-function@retarget-mcp.iam.gserviceaccount.com
```

### Error: "Gmail API not enabled"

```bash
gcloud services enable gmail.googleapis.com
gcloud services enable sheets.googleapis.com
```

### Error: "Secret not found"

```bash
# Ver secrets disponibles
gcloud secrets list

# Crear secret manualmente
gcloud secrets create gmail-refresh-token \
  --data-file=- <<< "YOUR_REFRESH_TOKEN_HERE"
```

---

## 📝 Variables de Ambiente

Actualizar en deploy si es necesario:

```env
SHEETS_ID="1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY"
SHEET_NAME="Retarget-Mayo-2026"
ALLOWED_FROM="['mauricio@', 'leig@']"
SCHEDULER_INTERVAL=5  # minutos
```

---

## 🔐 Seguridad

- ✅ Refresh token en Secret Manager (encriptado)
- ✅ Service account con permisos mínimos
- ✅ Cloud Function sin acceso público (requiere auth) — CAMBIAR SI NECESARIO
- ✅ Logs en Cloud Logging (auditable)

---

## 📅 Próximos pasos

1. ✅ Setup OAuth
2. ✅ Deploy Cloud Function
3. ✅ Crear Scheduler
4. 📊 Monitorear primeras ejecuciones
5. 🎯 Ajustar templates/criterios según feedback
6. 📈 Agregar más sitios/contactos en ALLOWED_FROM

---

*Creado: 2026-05-13 | COMPASS Cloud Auto-Responder*
