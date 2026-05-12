# PASO 2.2 — Conectar Service Account a Cloud Run MCP

**Para:** Luis (administrador COMPASS)  
**Tiempo:** 10-15 minutos  
**Requisito:** Haber completado PASO 2.1 (MCP desplegado)  
**Objetivo:** Que el MCP pueda acceder a Gmail, Sheets, Drive

---

## 📋 Lo que haremos

El MCP en Cloud Run necesita credenciales para acceder a los servicios Google (Gmail, Sheets, etc.). Vamos a:

1. Crear un secreto en Google Secret Manager con credenciales
2. Montar ese secreto en el servicio Cloud Run
3. Verificar que funciona

---

## ✅ Información que necesitas

Antes de empezar, reúne:

- [ ] URL del MCP (de PASO 2.1, ej: `https://retarget-mcp-xxxxx.run.app`)
- [ ] Archivo de credenciales: `/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json`
- [ ] Acceso a `gcloud` CLI

---

## 🔐 PASO 1: Crear secreto en Secret Manager

### 1.1 Habilitar API

```bash
gcloud services enable secretmanager.googleapis.com
```

### 1.2 Crear el secreto

```bash
PROJECT_ID="retarget-mcp"

gcloud secrets create retarget-mcp-credentials \
  --data-file=/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json \
  --replication-policy="automatic" \
  --project=$PROJECT_ID
```

**Resultado esperado:**
```
Created secret [retarget-mcp-credentials]
```

- [ ] Secreto creado

### 1.3 Dar acceso a Cloud Run

```bash
PROJECT_ID="retarget-mcp"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding retarget-mcp-credentials \
  --member=serviceAccount:$CLOUD_RUN_SA \
  --role=roles/secretmanager.secretAccessor \
  --project=$PROJECT_ID
```

**Resultado esperado:**
```
Updated IAM policy for secret [retarget-mcp-credentials]
```

- [ ] Permisos asignados

---

## ☁️ PASO 2: Montar secreto en Cloud Run

### 2.1 Obtener nombre del servicio

```bash
gcloud run services list --region=us-central1 --filter="name:retarget-mcp" --format='value(name)'
# Debe mostrar: retarget-mcp
```

### 2.2 Actualizar servicio con secreto

```bash
gcloud run services update retarget-mcp \
  --region=us-central1 \
  --update-secrets="/var/secrets/cloud.google.com/service_account/key.json=retarget-mcp-credentials:latest" \
  --update-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/cloud.google.com/service_account/key.json,RAILS_ENV=production" \
  --quiet
```

**Resultado esperado:**
```
Updating Cloud Run service... Done
```

Esto tarda ~2 minutos mientras Cloud Run redeploy la aplicación.

- [ ] Servicio actualizado

### 2.3 Verificar que el secreto está montado

```bash
gcloud run services describe retarget-mcp \
  --region=us-central1 \
  --format='value(spec.template.spec.containers[0].volumeMounts)'
```

Debe mostrar algo como:
```
[{'name': 'secret', 'path': '/var/secrets/cloud.google.com/service_account/key.json', ...}]
```

---

## ✔️ PASO 3: Verificar acceso a Google APIs

Una vez que el secreto está montado, verifica que el MCP puede acceder a Google:

### 3.1 Test simple (health check)

```bash
MCP_URL="https://retarget-mcp-xxxxx.run.app"  # Tu URL de PASO 2.1

curl $MCP_URL/health
# Debe responder: {"status":"healthy"}
```

- [ ] Health check OK

### 3.2 Test con acceso a Google (contexto del usuario)

```bash
# Reemplaza USER_ID con un número (ej: 1 para test)
curl -H "Content-Type: application/json" \
  "$MCP_URL/api/v1/context/1"
```

**Resultado esperado:**
- Si devuelve `{"context": {...}}` → ✅ Acceso a Google OK
- Si devuelve `{"error": "User not found"}` → Es normal (usuario aún no existe en DB, se crea en PASO 2.3)
- Si devuelve error de credenciales → ❌ Problema con el secreto

---

## 🗄️ PASO 4: Configurar Database (PostgreSQL)

El MCP usa una base de datos PostgreSQL para auditoría y tracking. Necesitamos asegurar que está disponible.

### 4.1 Verificar que Cloud SQL existe (si es necesario)

Si el MCP necesita persistencia:

```bash
gcloud sql instances list --project=retarget-mcp
# Debe mostrar: retarget-mcp-db (o similar)
```

Si no existe, créalo:
```bash
gcloud sql instances create retarget-mcp-db \
  --database-version=POSTGRES_14 \
  --region=us-central1 \
  --tier=db-f1-micro
```

### 4.2 Conectar database a Cloud Run (OPCIONAL por ahora)

En PASO 2.3 crearemos un usuario en la DB. Por ahora, solo asegúrate que existe.

- [ ] Cloud SQL disponible (o SKIP si no es necesario)

---

## 🎯 Checklist para PASO 2.2

**Secret Manager:**
- [ ] API habilitada
- [ ] Secreto `retarget-mcp-credentials` creado
- [ ] Permisos asignados a Cloud Run

**Cloud Run:**
- [ ] Servicio actualizado con secreto montado
- [ ] Variables de entorno configuradas

**Verificación:**
- [ ] Health check responde ✅
- [ ] MCP puede acceder a Google APIs

---

## 🆘 Si algo falla

### Error: "Secret not found"
**Solución:** Verifica que el secreto existe:
```bash
gcloud secrets list --project=retarget-mcp | grep credentials
```

### Error: "Permission denied" en Cloud Run
**Solución:** Verifica que los permisos están bien:
```bash
gcloud secrets get-iam-policy retarget-mcp-credentials --project=retarget-mcp
# Debe mostrar serviceAccount con rol secretmanager.secretAccessor
```

### Error: "GOOGLE_APPLICATION_CREDENTIALS not found" en logs
**Solución:** Verifica la actualización del servicio:
```bash
gcloud run services describe retarget-mcp --region=us-central1 --format='value(spec.template.spec.containers[0].env)'
```

Debe mostrar:
```
[{'name': 'GOOGLE_APPLICATION_CREDENTIALS', 'value': '/var/secrets/cloud.google.com/service_account/key.json'}, ...]
```

### Error: "Connection refused" a Cloud SQL
**Solución:** Por ahora, SKIP. Configuraremos en PASO 2.3 si es necesario.

---

## 📊 Resumen

Cuando PASO 2.2 esté completo:

✅ MCP en Cloud Run  
✅ Credenciales Google montadas en secreto  
✅ MCP puede acceder a Gmail, Sheets, Drive  
✅ Ready para crear usuarios  

**Próximo:** PASO 2.3 — Crear usuario de test en Database

---

**Creado:** 2026-05-11  
**Versión:** 1.0  
**Para:** Luis (COMPASS Admin)
