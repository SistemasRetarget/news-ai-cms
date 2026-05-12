# ⚡ PASO 2 — EJECUCIÓN RÁPIDA

**Para:** Luis (administrador COMPASS)  
**Tiempo total:** 30-40 minutos  
**Estado:** ✅ Listo para ejecutar  
**Resultado:** MCP centralizado en Cloud Run + acceso multi-usuario

---

## 🎯 Lo que haremos (en 3 fases)

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1: Desplegar MCP a Cloud Run (15 min)                  │
│  - Clonar repo con código Rails                             │
│  - Ejecutar script de deploy                                │
│  - Obtener URL del MCP                                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2: Conectar credenciales Google (10 min)               │
│  - Crear secreto en Secret Manager                          │
│  - Montar secreto en Cloud Run                              │
│  - Verificar acceso a Gmail/Sheets/Drive                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 3: Crear usuario de test (5 min)                       │
│  - Conectarse a PostgreSQL                                  │
│  - Insertar usuario                                         │
│  - Guardar USER_ID para próximos usuarios                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 FASE 1: Desplegar MCP a Cloud Run

**Documentación completa:** [PASO_2_1_DESPLEGAR_CLOUD_RUN.md](PASO_2_1_DESPLEGAR_CLOUD_RUN.md)

### En 3 comandos:

```bash
# 1. Clonar repo
cd /Users/spam11/Desktop/RETARGET-WORKSPACE
git clone https://github.com/SistemasRetarget/retarget-mcp-new.git
cd retarget-mcp-new

# 2. Ejecutar deploy (automatizado)
./deploy-cloud-run.sh retarget-mcp

# 3. Esperar ~10 minutos y copiar URL del resultado
# Verás algo como: https://retarget-mcp-xxxxx.run.app
```

**✅ Checklist FASE 1:**
- [ ] Script ejecutado exitosamente
- [ ] Health check responde (`curl https://retarget-mcp-xxxxx.run.app/health`)
- [ ] **Guardé la URL del MCP** (necesaria para FASE 2 y usuarios)

---

## 🔐 FASE 2: Conectar Service Account

**Documentación completa:** [PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md](PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md)

### En 2 pasos principales:

```bash
# PASO A: Crear secreto con credenciales Google
PROJECT_ID="retarget-mcp"

gcloud secrets create retarget-mcp-credentials \
  --data-file=/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json \
  --replication-policy="automatic"

# Dar acceso a Cloud Run
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CLOUD_RUN_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding retarget-mcp-credentials \
  --member=serviceAccount:$CLOUD_RUN_SA \
  --role=roles/secretmanager.secretAccessor

# PASO B: Montar secreto en Cloud Run
gcloud run services update retarget-mcp \
  --region=us-central1 \
  --update-secrets="/var/secrets/cloud.google.com/service_account/key.json=retarget-mcp-credentials:latest" \
  --update-env-vars="GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/cloud.google.com/service_account/key.json,RAILS_ENV=production" \
  --quiet
```

**✅ Checklist FASE 2:**
- [ ] Secreto creado en Secret Manager
- [ ] Permisos asignados a Cloud Run
- [ ] Servicio actualizado con secreto montado
- [ ] Verificación: `curl https://retarget-mcp-xxxxx.run.app/health` responde ✅

---

## 🗄️ FASE 3: Crear usuario de test

**Para crear un usuario en la base de datos:**

```bash
# Conectarse a Cloud SQL PostgreSQL
gcloud sql connect retarget-mcp-db \
  --user=postgres \
  --project=retarget-mcp

# En psql (cuando abra el prompt):
INSERT INTO users (
  name, 
  email, 
  role, 
  ai_tool, 
  created_at, 
  updated_at
) VALUES (
  'Juan Test',
  'juan@retarget.cl',
  'user',
  'claude-code',
  NOW(),
  NOW()
);

-- Copiar el ID que genera (ej: 1, 2, 3...)
SELECT id FROM users WHERE email = 'juan@retarget.cl';

-- Salir de psql
\q
```

**✅ Checklist FASE 3:**
- [ ] Conectado a PostgreSQL
- [ ] Usuario creado
- [ ] Obtuve el USER_ID (ej: 1, 2, 3)
- [ ] **Guardé el USER_ID para dárselo al usuario**

---

## 📊 Resultado Final

Cuando PASO 2 esté completado:

```
✅ MCP corriendo en Cloud Run (URL pública)
✅ Credenciales Google montadas (acceso a Gmail/Sheets/Drive)
✅ Database PostgreSQL con usuarios registrados
✅ Auditoría automática de todas las acciones
✅ Ready para múltiples usuarios simultáneamente
```

Tienes:
- **URL del MCP:** Ej: `https://retarget-mcp-xxxxx.run.app`
- **USER_ID:** Ej: `1`

---

## 👥 Siguiente: Onboarding para otro usuario

Cuando PASO 2 esté listo, otros usuarios solo necesitan:

```bash
# 1. Clonar COMPASS (es documentación + contexto)
git clone https://github.com/SistemasRetarget/news-ai-cms.git
cd news-ai-cms/COMPASS

# 2. Crear config (reemplazar con tu URL y USER_ID de Luis)
mkdir -p ~/.compass
cat > ~/.compass/config.json << 'EOF'
{
  "mcp_url": "https://retarget-mcp-xxxxx.run.app",
  "user_id": 1,
  "ai_tool": "claude-code"
}
EOF

# 3. En Claude Code
COMPASS MODE

# ✅ Funciona - conectado al MCP
```

---

## 🆘 Troubleshooting Rápido

| Error | Solución |
|---|---|
| "Dockerfile not found" | `cd /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-new && ls Dockerfile` |
| "Permission denied" en script | `chmod +x deploy-cloud-run.sh` |
| "Secret not found" | `gcloud secrets list \| grep credentials` |
| Build falla | Ver logs: `gcloud builds log --limit=100` |
| "Connection refused" a MCP | Esperar 5 min más o verificar URL |

---

## 📋 Documentación Completa

Cada FASE tiene un documento detallado si necesitas más ayuda:

1. **[PASO_2_1_DESPLEGAR_CLOUD_RUN.md](PASO_2_1_DESPLEGAR_CLOUD_RUN.md)** — Deploy paso a paso
2. **[PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md](PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md)** — Secretos y credenciales
3. **[PASO_2_CHECKLIST.md](PASO_2_CHECKLIST.md)** — Checklist completo con verificaciones

---

## ⏱️ Timeline

```
Hora 0:00 — Ejecutar script deploy (./deploy-cloud-run.sh)
Hora 0:10 — Esperar mientras Cloud Build construye (tomar café ☕)
Hora 0:10 — Mientras esperas, empezar FASE 2 (crear secreto)
Hora 0:15 — MCP desplegado ✅
Hora 0:20 — Montar secreto en Cloud Run
Hora 0:25 — Servicio actualizado ✅
Hora 0:30 — Crear usuario en PostgreSQL
Hora 0:35 — Todo listo ✅
```

**Total:** 35-40 minutos

---

## 🎉 Cuando esté listo

Tendrás:
- ✅ MCP en la nube (no local)
- ✅ Credenciales centralizadas y seguras
- ✅ Auditoría automática
- ✅ Ready para multi-usuario
- ✅ Infraestructura empresarial

**PASO 2 == Punto de inflexión donde COMPASS pasa de experimento personal a sistema empresarial.**

---

**Creado:** 2026-05-11  
**Versión:** 1.0 (FINAL)  
**Status:** ✅ Listo para ejecutar
