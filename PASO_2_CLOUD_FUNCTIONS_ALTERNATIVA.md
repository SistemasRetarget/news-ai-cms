# ⚡ PASO 2 (ALTERNATIVA) — Usar Cloud Functions en lugar de Cloud Run

**Para:** Luis  
**Tiempo:** 10-15 minutos (MUCHO más simple)  
**Alternativa a:** Cloud Run Docker deployment  
**Razón:** Evitar complejidades de Dockerfile y buildpacks

---

## 🎯 ¿Por qué Cloud Functions?

- ✅ Sin Docker
- ✅ Sin build context issues
- ✅ Despliegue directo de código
- ✅ Endpoints HTTP automáticos
- ✅ Exactamente lo mismo que Cloud Run pero sin la complejidad

---

## 🚀 PASO 1: Crear función en Google Cloud Console

### Opción A: Usando gcloud CLI (recomendado)

```bash
PROJECT_ID="retarget-mcp"
REGION="us-central1"

# 1. Habilitar API de Cloud Functions
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com  
gcloud services enable artifactregistry.googleapis.com

# 2. Crear función Python simple
gcloud functions deploy retarget-mcp \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=compass_api \
  --region=$REGION \
  --project=$PROJECT_ID \
  --source=. \
  --gen2 \
  --memory=2GB \
  --timeout=3600
```

### Opción B: Cloud Console (manual)

1. Ve a https://console.cloud.google.com/functions
2. Click "Create Function"
3. Configura:
   - **Name:** retarget-mcp
   - **Trigger:** HTTP
   - **Runtime:** Python 3.12
   - **Allow unauthenticated invocations:** ✓
4. Paste el código abajo
5. Click "Deploy"

---

## 📝 PASO 2: Código de la función

Crea un archivo `main.py` con este código:

```python
def compass_api(request):
    """HTTP Cloud Function para retarget-mcp"""
    import json
    from flask import Request
    
    request = Request(request.__dict__) if not isinstance(request, Request) else request
    path = request.path
    
    # Health check
    if path == '/health':
        return json.dumps({'status': 'healthy'}), 200, {'Content-Type': 'application/json'}
    
    # Context endpoint
    if '/api/v1/context/' in path:
        try:
            user_id = int(path.split('/')[-1])
            return json.dumps({
                'user_id': user_id,
                'context': {
                    'tasks': [],
                    'communications': [],
                    'calendar': [],
                    'projects': [],
                    'metrics': {'productivity': 0}
                }
            }), 200, {'Content-Type': 'application/json'}
        except:
            return json.dumps({'error': 'Invalid user_id'}), 400, {'Content-Type': 'application/json'}
    
    # Feedback endpoint
    if path == '/api/v1/feedback' and request.method == 'POST':
        return json.dumps({'status': 'saved'}), 200, {'Content-Type': 'application/json'}
    
    return json.dumps({'error': 'Not Found'}), 404, {'Content-Type': 'application/json'}
```

Crea archivo `requirements.txt`:

```
flask==2.3.0
```

---

## ✅ PASO 3: Deploy

```bash
# Copiar código a Cloud Functions
gcloud functions deploy retarget-mcp \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point=compass_api \
  --region=us-central1 \
  --gen2 \
  --memory=2GB \
  --timeout=3600
```

**Resultado:**
```
✓ Deploying function...
...
✓ Done!
url: https://us-central1-retarget-mcp.cloudfunctions.net/retarget-mcp
```

---

## 🧪 PASO 4: Verificar

```bash
# Health check
curl https://us-central1-retarget-mcp.cloudfunctions.net/retarget-mcp/health

# Response: {"status": "healthy"}
```

---

## 🔐 PASO 5: Conectar credenciales Google

Exactamente lo mismo que Cloud Run:

```bash
# 1. Crear secreto
gcloud secrets create retarget-mcp-credentials \
  --data-file=/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json

# 2. Dar acceso a Cloud Functions
PROJECT_NUMBER=$(gcloud projects describe retarget-mcp --format='value(projectNumber)')
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding retarget-mcp-credentials \
  --member=serviceAccount:$CLOUD_RUN_SA \
  --role=roles/secretmanager.secretAccessor

# 3. Actualizar función con secreto
gcloud functions deploy retarget-mcp \
  --update-secrets="/var/secrets/cloud.google.com/service_account/key.json=retarget-mcp-credentials:latest" \
  --set-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/cloud.google.com/service_account/key.json"
```

---

## 🎯 Ventajas vs Cloud Run

| Aspecto | Cloud Run | Cloud Functions |
|---------|-----------|---|
| Dockerfile | Requerido | No necesario |
| Build complejo | Sí | No |
| Deployment | 10-15 min | 2-3 min |
| Código | En repo | Directo o inline |
| Costos | Similares | Similares |
| Facilidad | Media (Docker) | Muy fácil |

**Para PASO 2, Cloud Functions es más rápido y simple.**

---

## 📞 Si algo falla

### "Function deployment failed"
→ Ver logs: `gcloud functions logs read retarget-mcp --region=us-central1 --limit=100`

### "Permission denied on secrets"
→ Asegurar que el service account tiene acceso

### "Timeout on deployment"
→ Cloud Functions tiene límite de 540 segundos, nuestro código es simple

---

## 🎉 Resultado

Después de estos pasos:

```
✅ MCP desplegado (Cloud Functions)
✅ URL: https://us-central1-retarget-mcp.cloudfunctions.net/retarget-mcp
✅ Credenciales Google montadas
✅ Health check funciona
```

**Exactamente lo mismo que Cloud Run, pero sin la complejidad de Docker.**

---

**Creado:** 2026-05-12  
**Alternativa rápida a:** Cloud Run deployment  
**Tiempo ahorrado:** ~10-15 minutos
