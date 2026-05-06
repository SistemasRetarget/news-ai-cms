# Despliegue a Google Cloud Run — Pasos Exactos
## MCP Rails en Google Cloud

**Fecha:** 2026-04-28  
**Objetivo:** Desplegar MCP a Cloud Run  
**Tiempo estimado:** 30-45 minutos

---

## PASO 1: Preparar Proyecto Rails Localmente

### 1.1 Verificar que tienes todo

```bash
# Verifica que existen estos archivos:
ls -la /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp/

Deberías ver:
├─ Gemfile
├─ Dockerfile
├─ .gcloudignore
├─ config/
│  ├─ database.yml
│  ├─ routes.rb
│  └─ initializers/
│     ├─ google_cloud.rb
│     └─ cors.rb
├─ app/
│  ├─ controllers/
│  ├─ models/
│  └─ services/
└─ db/migrate/
```

### 1.2 Crear Gemfile.lock

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp

# Instalar bundler
gem install bundler

# Crear Gemfile.lock (sin instalar gemas localmente)
bundle lock --no-update
```

---

## PASO 2: Configurar gcloud CLI

### 2.1 Verificar gcloud está instalado

```bash
gcloud --version

Deberías ver algo como:
Google Cloud SDK 123.0.0
```

### 2.2 Configurar proyecto

```bash
# Establecer proyecto
gcloud config set project retarget-mcp

# Verificar
gcloud config list

Deberías ver:
[core]
account = tu-email@gmail.com
project = retarget-mcp
```

### 2.3 Autenticarse

```bash
gcloud auth login

# Sigue las instrucciones en el navegador
# Selecciona tu cuenta Google
```

---

## PASO 3: Habilitar Cloud Run API (si no está habilitada)

```bash
gcloud services enable run.googleapis.com

# Verificar
gcloud services list --enabled | grep run
```

---

## PASO 4: Crear Imagen Docker y Deployar

### 4.1 Opción A: Deploy directo (Recomendado para primera vez)

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp

# Deploy directo a Cloud Run
gcloud run deploy retarget-mcp \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 256Mi \
  --cpu 1 \
  --timeout 3600 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars "RAILS_ENV=production,GOOGLE_CLOUD_PROJECT=retarget-mcp" \
  --set-secrets DATABASE_URL=DATABASE_URL:latest \
  --set-secrets GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest \
  --set-secrets GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest \
  --set-secrets RAILS_MASTER_KEY=RAILS_MASTER_KEY:latest \
  --allow-unauthenticated

# ESPERAR: 5-10 minutos mientras construye y deploya
```

### 4.2 Opción B: Build manual + Deploy (Si Opción A falla)

```bash
# Paso 1: Build imagen
gcloud builds submit --tag gcr.io/retarget-mcp/retarget-mcp

# ESPERAR: 3-5 minutos

# Paso 2: Deploy
gcloud run deploy retarget-mcp \
  --image gcr.io/retarget-mcp/retarget-mcp \
  --platform managed \
  --region us-central1 \
  --memory 256Mi \
  --cpu 1 \
  --timeout 3600 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars "RAILS_ENV=production,GOOGLE_CLOUD_PROJECT=retarget-mcp" \
  --set-secrets DATABASE_URL=DATABASE_URL:latest \
  --set-secrets GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest \
  --set-secrets GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest \
  --set-secrets RAILS_MASTER_KEY=RAILS_MASTER_KEY:latest \
  --allow-unauthenticated
```

---

## PASO 5: Obtener URL del Servicio

```bash
# Obtener URL
gcloud run services describe retarget-mcp \
  --region us-central1 \
  --format='value(status.url)'

# Resultado será algo como:
# https://retarget-mcp-XXXXXXX.run.app

# Guarda esta URL, la necesitarás
```

---

## PASO 6: Ejecutar Migraciones

### 6.1 Opción A: Cloud SQL Proxy (Recomendado)

```bash
# Instalar Cloud SQL Proxy
curl https://dl.google.com/cloudsql/cloud_sql_proxy.mac.x64 -o cloud_sql_proxy
chmod +x cloud_sql_proxy

# Ejecutar proxy en terminal separada
./cloud_sql_proxy -instances=retarget-mcp:us-central1:retarget-mcp-db=tcp:5432

# En otra terminal, ejecutar migraciones
gcloud run jobs create retarget-mcp-migrate \
  --image gcr.io/retarget-mcp/retarget-mcp \
  --region us-central1 \
  --set-env-vars "RAILS_ENV=production,GOOGLE_CLOUD_PROJECT=retarget-mcp" \
  --set-secrets DATABASE_URL=DATABASE_URL:latest \
  --set-secrets RAILS_MASTER_KEY=RAILS_MASTER_KEY:latest \
  --command "bundle exec rails db:migrate"

# Ejecutar el job
gcloud run jobs execute retarget-mcp-migrate --region us-central1
```

### 6.2 Opción B: Ejecutar localmente (Si tienes acceso a BD)

```bash
# Si Cloud SQL está accesible localmente
DATABASE_URL="postgresql://rails:PASSWORD@IP_PUBLICA:5432/retarget_mcp" \
  bundle exec rails db:migrate
```

---

## PASO 7: Testear el Servicio

### 7.1 Health Check

```bash
# Reemplaza URL con la que obtuviste en Paso 5
curl https://retarget-mcp-XXXXXXX.run.app/health

# Deberías ver:
# {"status":"ok","timestamp":"2026-04-28T...","environment":"production"}
```

### 7.2 Crear Usuario de Prueba

```bash
# Conectarse a Cloud SQL
gcloud sql connect retarget-mcp-db --user=rails

# En psql, ejecutar:
INSERT INTO users (email, name, role, ai_tool, is_ai_user, active, created_at, updated_at)
VALUES ('luis@retarget.cl', 'Luis', 2, 0, true, true, NOW(), NOW());

# Verificar
SELECT * FROM users;

# Salir
\q
```

### 7.3 Testear Endpoint

```bash
# Obtener contexto del usuario
curl -X GET \
  "https://retarget-mcp-XXXXXXX.run.app/api/v1/context/1" \
  -H "Content-Type: application/json" \
  -H "X-AI-Tool: claude"

# Deberías ver JSON con contexto del usuario
```

### 7.4 Enviar Feedback

```bash
curl -X POST \
  "https://retarget-mcp-XXXXXXX.run.app/api/v1/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "type": "suggestion",
    "content": "Sería útil incluir GitHub commits",
    "ai_tool": "claude"
  }'

# Deberías ver: {"status":"ok","feedback_id":1}
```

---

## PASO 8: Ver Logs

```bash
# Logs en tiempo real
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=retarget-mcp" \
  --limit 50 \
  --format json

# O en Cloud Console
# Ve a: https://console.cloud.google.com
# Busca: Cloud Logging
# Filtra por servicio: retarget-mcp
```

---

## PASO 9: Configurar Monitoreo

### 9.1 Crear Alerta de Errores

```bash
gcloud alpha monitoring policies create \
  --display-name="MCP Error Rate High" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

### 9.2 Ver Métricas

```bash
# En Cloud Console:
# Ve a: Cloud Monitoring > Dashboards
# Busca: retarget-mcp
```

---

## PASO 10: Configurar Dominio Personalizado (Opcional)

```bash
# Si tienes dominio personalizado (ej: api.retarget.cl)
gcloud run domain-mappings create \
  --service=retarget-mcp \
  --domain=api.retarget.cl \
  --region=us-central1

# Seguir instrucciones para configurar DNS
```

---

## CHECKLIST: DEPLOYMENT COMPLETADO

```
✅ Proyecto Rails preparado
✅ Dockerfile creado
✅ gcloud CLI configurado
✅ Cloud Run API habilitada
✅ Imagen Docker deployada
✅ URL del servicio obtenida
✅ Migraciones ejecutadas
✅ Health check funcionando
✅ Endpoint /api/v1/context testado
✅ Endpoint /api/v1/feedback testado
✅ Logs visibles
✅ Monitoreo configurado
```

---

## TROUBLESHOOTING

### Error: "Permission denied"

```bash
# Verificar permisos
gcloud projects get-iam-policy retarget-mcp

# Si falta permisos, agregar role
gcloud projects add-iam-policy-binding retarget-mcp \
  --member=user:tu-email@gmail.com \
  --role=roles/editor
```

### Error: "Database connection failed"

```bash
# Verificar que Cloud SQL está accesible
gcloud sql instances describe retarget-mcp-db

# Verificar que SECRET DATABASE_URL está correcto
gcloud secrets versions access latest --secret="DATABASE_URL"
```

### Error: "Secret not found"

```bash
# Verificar que secrets existen
gcloud secrets list

# Si falta alguno, crear:
echo "postgresql://rails:PASSWORD@IP:5432/retarget_mcp" | \
  gcloud secrets create DATABASE_URL --data-file=-
```

### Error: "Timeout during build"

```bash
# Aumentar timeout
gcloud run deploy retarget-mcp \
  --source . \
  --region us-central1 \
  --timeout 3600 \
  ... (otros parámetros)
```

---

## PRÓXIMOS PASOS

Una vez deployado:

1. **Crear usuarios de prueba**
   ```bash
   gcloud sql connect retarget-mcp-db --user=rails
   # INSERT usuarios (Barbana, Mauricio, Luis, Daniel, Alejandra)
   ```

2. **Integrar Google Workspace APIs**
   - Gmail API
   - Google Chat API
   - Google Calendar API

3. **Configurar webhooks**
   - Gmail webhooks
   - Chat webhooks
   - Calendar webhooks

4. **Crear dashboard de reportes**
   - Adopción
   - Mejoras MCP
   - ROI

5. **Reunión con equipo**
   - Demo del MCP
   - Feedback inicial
   - Capacitación

---

## COMANDOS RÁPIDOS (Copiar y Pegar)

```bash
# Setup completo
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp
gcloud config set project retarget-mcp

# Deploy
gcloud run deploy retarget-mcp \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 256Mi \
  --set-env-vars "RAILS_ENV=production,GOOGLE_CLOUD_PROJECT=retarget-mcp" \
  --set-secrets DATABASE_URL=DATABASE_URL:latest \
  --set-secrets GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest \
  --set-secrets GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest \
  --set-secrets RAILS_MASTER_KEY=RAILS_MASTER_KEY:latest \
  --allow-unauthenticated

# Obtener URL
gcloud run services describe retarget-mcp --region us-central1 --format='value(status.url)'

# Ver logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=retarget-mcp" --limit 50 --format json
```

---

**¿Listo para deployar? ¿Necesitas ayuda en algún paso?**
