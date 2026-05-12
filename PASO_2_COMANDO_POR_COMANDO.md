# PASO 2 — Comando por Comando

**Guía de referencia rápida para ejecutar PASO 2**

**Abre esto en otra ventana/monitor mientras ejecutas**

---

## 🎯 FASE 1: Deploy MCP a Cloud Run (15 min)

### Paso 1.1: Clonar repositorio

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE
git clone https://github.com/SistemasRetarget/retarget-mcp-new.git
cd retarget-mcp-new
```

**Verificar:**
```bash
ls -la
# Deberías ver: Dockerfile, cloudbuild.yaml, Gemfile, app/, config/
```

### Paso 1.2: Ejecutar deploy

```bash
./deploy-cloud-run.sh retarget-mcp
```

**Qué pasará:**
- Habilita APIs (Cloud Run, Artifact Registry)
- Crea repositorio en Artifact Registry
- Construye imagen Docker
- Despliega a Cloud Run
- Verifica health check

**Tiempo:** ~10-12 minutos mientras Cloud Build construye

**Resultado esperado:**
```
✅ Despliegue completado!
📍 URL del servicio:
   https://retarget-mcp-xxxxx.run.app
```

**⭐ COPIA ESTA URL — LA NECESITARÁS EN FASE 2**

---

## 🔐 FASE 2: Conectar Service Account (10 min)

### Paso 2.1: Verificar que gcloud está configurado

```bash
gcloud auth list
# Debe mostrar tu cuenta @retarget.cl como ACTIVE

gcloud config get-value project
# Debe mostrar: retarget-mcp
```

Si no está configurado:
```bash
gcloud auth login
gcloud config set project retarget-mcp
```

### Paso 2.2: Crear secreto en Secret Manager

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

### Paso 2.3: Dar acceso a Cloud Run

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

### Paso 2.4: Montar secreto en Cloud Run

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

Tarda ~2-3 minutos mientras redeploy.

- [ ] Servicio actualizado

### Paso 2.5: Verificar

```bash
# Reemplaza xxxxx con tu URL real de Paso 1.2
curl https://retarget-mcp-xxxxx.run.app/health

# Debe responder: {"status":"healthy"}
```

- [ ] Health check OK

---

## 🗄️ FASE 3: Crear usuario en Database (5 min)

### Paso 3.1: Conectarse a PostgreSQL

```bash
gcloud sql connect retarget-mcp-db \
  --user=postgres \
  --project=retarget-mcp
```

**Resultado esperado:**
```
Connecting to database with SQL user [postgres]...
[Cloud SQL Proxy]

Password for user postgres: [no hay contraseña, presiona Enter]

postgres=>  # Ahora estás en psql
```

- [ ] Conectado a PostgreSQL

### Paso 3.2: Crear usuario de test

En el prompt de `psql`, escribe:

```sql
INSERT INTO users (
  name, 
  email, 
  role, 
  ai_tool, 
  created_at, 
  updated_at
) VALUES (
  'Test User',
  'test@retarget.cl',
  'user',
  'claude-code',
  NOW(),
  NOW()
);
```

**Resultado esperado:**
```
INSERT 0 1
```

- [ ] Usuario insertado

### Paso 3.3: Obtener USER_ID

```sql
SELECT id FROM users WHERE email = 'test@retarget.cl';
```

**Resultado esperado:**
```
 id
----
  1
(1 row)
```

**⭐ COPIA ESTE ID (ej: 1) — LO NECESITARÁS PARA OTROS USUARIOS**

- [ ] USER_ID obtenido

### Paso 3.4: Salir de psql

```sql
\q
```

---

## ✅ Checklist Final

**FASE 1 (Deploy):**
- [ ] Repositorio clonado
- [ ] Script ejecutado
- [ ] URL del MCP obtenida (ej: `https://retarget-mcp-xxxxx.run.app`)

**FASE 2 (Credenciales):**
- [ ] Secreto creado
- [ ] Permisos asignados
- [ ] Servicio actualizado
- [ ] Health check OK

**FASE 3 (Database):**
- [ ] Conectado a PostgreSQL
- [ ] Usuario creado
- [ ] USER_ID obtenido (ej: 1)

---

## 📊 Datos Importantes a Guardar

```
URL del MCP:
https://retarget-mcp-xxxxx.run.app

USER_ID de test:
1

Credenciales archivo:
/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json
```

Estos datos necesitarás darle a otros usuarios para que se conecten.

---

## 🚀 Siguiente: Setup para otro usuario

Cuando otro usuario quiera usar COMPASS:

```bash
# Otro usuario en su máquina:
git clone https://github.com/SistemasRetarget/news-ai-cms.git
cd news-ai-cms/COMPASS

mkdir -p ~/.compass

cat > ~/.compass/config.json << 'EOF'
{
  "mcp_url": "https://retarget-mcp-xxxxx.run.app",  # TU URL
  "user_id": 1                                        # TU USER_ID
}
EOF

# En Claude Code:
# COMPASS MODE

# ✅ Conectado
```

---

## 🆘 Errores comunes

| Error | Solución |
|---|---|
| "bash: ./deploy-cloud-run.sh: command not found" | `chmod +x deploy-cloud-run.sh` |
| "Secret not found" | Esperar 30 seg después de crear |
| "Connection refused" a MCP | Esperar 5 min después de deploy |
| "psql: could not connect" | `gcloud sql instances list` y verificar que existe |
| "User not found (401)" al probar /api/v1/context/1 | Normal, usuario aún no existe en DB |

---

**Creado:** 2026-05-11  
**Para:** Ejecución rápida de PASO 2  
**Tener abierto:** En otra ventana/monitor mientras ejecutas
