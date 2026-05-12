# PASO 2 (OPCIÓN B) — Checklist de Ejecución

**Objetivo:** Desplegar Cloud Run MCP centralizado para que usuarios se conecten sin instalar nada  
**Timeline:** Hoy (2026-05-11)  
**Responsables:** Luis (deploy del MCP) + Usuario Test (verificación)  
**Versión:** 2.0 (Cloud Run MCP)

---

## 🎯 PASO 2.1 — Desplegar MCP en Cloud Run (Luis)

**Tiempo:** 10-15 minutos  
**Responsable:** Luis

### Opción A: Usar script automatizado (RECOMENDADO ⭐)

```bash
# 1. Clonar repo (si aún no lo tienes)
git clone https://github.com/SistemasRetarget/retarget-mcp-new.git
cd retarget-mcp-new

# 2. Ejecutar script de deploy
./deploy-cloud-run.sh retarget-mcp

# Espera ~5 minutos mientras Cloud Build construye la imagen
```

El script automáticamente:
- ✅ Habilita APIs necesarias (Cloud Run, Artifact Registry, Cloud Build)
- ✅ Crea Artifact Registry si no existe
- ✅ Construye imagen Docker
- ✅ Despliega a Cloud Run
- ✅ Testea health check
- ✅ Imprime URL del servicio

**Resultado:** URL del MCP en Cloud Run (ej: `https://retarget-mcp-xxx.run.app`)

- [ ] Script ejecutado exitosamente
- [ ] Obtuve la URL del MCP
- [ ] Health check responde ✅

### Opción B: Despliegue manual paso a paso

Si prefieres hacerlo manualmente o el script falla:

```bash
# 1. Configurar proyecto
gcloud config set project retarget-mcp

# 2. Habilitar APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# 3. Desplegar desde GitHub (Cloud Run detecta Dockerfile automáticamente)
gcloud run deploy retarget-mcp \
  --source=https://github.com/SistemasRetarget/retarget-mcp-new.git#main \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=100

# 4. Obtener URL
gcloud run services describe retarget-mcp --region=us-central1 --format='value(status.url)'
```

**Verificación:**
```bash
curl https://retarget-mcp-xxxx.run.app/health
# Debe responder: {"status":"healthy"}
```

**URL del MCP desplegado:** `https://retarget-mcp-xxxx.run.app/`

**Status:** [ ] MCP desplegado en Cloud Run

---

## 🎯 PASO 2.2 — Conectar Service Account al MCP (Luis)

**Tiempo:** 10 minutos  
**Responsable:** Luis

- [ ] Abrí Google Secret Manager en Cloud Console
- [ ] Creé secreto: `retarget-mcp-credentials` con contenido de `retarget-mcp-2d37bb49c600.json`
- [ ] Ejecuté comandos:
  ```bash
  PROJECT_ID="retarget-mcp"
  gcloud secrets create retarget-mcp-credentials \
    --data-file=~/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json \
    --project=$PROJECT_ID
  
  gcloud secrets add-iam-policy-binding retarget-mcp-credentials \
    --member=serviceAccount:retarget-mcp@retarget-mcp.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor \
    --project=$PROJECT_ID
  ```
- [ ] En Cloud Run, edité el servicio `retarget-mcp`
- [ ] Añadí variable de entorno: `GOOGLE_APPLICATION_CREDENTIALS=/secrets/retarget-mcp-credentials.json`
- [ ] Monté el secreto en ruta: `/secrets/retarget-mcp-credentials.json`
- [ ] Hice clic en **"Implementar"** y esperé 5 minutos

**Verificación:**
```bash
curl -H "X-Request-Summary: Test" https://retarget-mcp-xxxx.run.app/api/v1/context/1
# Debería conectarse a Google (puede fallar si usuario no existe, es normal)
```

**Status:** [ ] Service Account conectado al MCP

---

## 🎯 PASO 2.3 — Setup de Usuario Nuevo (Otro usuario)

**Tiempo:** 10 minutos  
**Responsable:** Otro usuario (Juan en otra máquina)

### Fase 1: Preparación (2 min)

- [ ] Recibí de Luis:
  - [ ] URL del MCP (ej: `https://retarget-mcp-xxxx.run.app`)
  - [ ] Mi USER_ID en la DB (ej: 2)
- [ ] Instalé Claude Code en mi máquina

### Fase 2: Clonar COMPASS (3 min)

```bash
git clone https://github.com/SistemasRetarget/news-ai-cms.git
cd news-ai-cms/COMPASS
ls -la  # Debe mostrar: CONTEXTO/, TOOLS/, TEMPLATES/, README.md
```

- [ ] Cloné COMPASS correctamente
- [ ] Verifiqué estructura de carpetas

### Fase 3: Crear configuración (3 min)

```bash
# Crear directorio de configuración
mkdir -p ~/.compass

# Crear archivo config.json
cat > ~/.compass/config.json << 'EOF'
{
  "mcp_url": "https://retarget-mcp-xxxx.run.app",
  "user_id": 2,
  "ai_tool": "claude-code"
}
EOF

# Reemplaza:
# - retarget-mcp-xxxx → URL real del MCP (que te da Luis)
# - 2 → Tu USER_ID (que te da Luis)

# Verificar que se creó correctamente
cat ~/.compass/config.json
```

- [ ] Archivo `~/.compass/config.json` creado
- [ ] URL del MCP es correcta
- [ ] Mi USER_ID es correcto

### Fase 4: Activar COMPASS MODE (2 min)

En Claude Code, escribe:

```
COMPASS MODE
```

Debería responder algo como:
```
✅ COMPASS activado para [Tu nombre]

Contexto cargado desde Cloud Run MCP:
├─ Tareas activas: 5
├─ Emails recientes: 12
├─ Proyectos: 3
└─ Listo para operar
```

- [ ] COMPASS MODE funciona
- [ ] Se conecta al Cloud Run MCP

---

## ✅ PASO 2.4 — Verificación (Tests)

**Tiempo:** 5 minutos  
**Responsable:** Otro usuario

### Test 1: Conexión al MCP

En Claude Chat, escribe:
```
COMPASS MODE

¿Cuál es mi USER_ID en el MCP?
```

Debería responder:
```
Tu USER_ID en el MCP es 2
```

- [ ] Test 1 pasado ✅

### Test 2: Obtener contexto del servidor

Escribe:
```
COMPASS MODE

Muéstrame mi contexto actual (tareas, proyectos, emails)
```

Debería mostrar información desde el Cloud Run MCP.

- [ ] Test 2 pasado ✅

### Test 3: Acceder a archivos locales

Escribe:
```
COMPASS MODE

Lee CONTEXTO/PUNTO_CERO.md
```

Debería mostrar contenido del archivo local.

- [ ] Test 3 pasado ✅

### Test 4: Health check del MCP

En terminal:
```bash
curl https://retarget-mcp-xxxx.run.app/health
# Debería responder: {"status":"healthy"}
```

- [ ] Test 4 pasado ✅

### Test 5: Enviar feedback

Escribe:
```
COMPASS MODE

Registra feedback: "COMPASS está funcionando bien"
```

El MCP debería registrarlo en su base de datos.

- [ ] Test 5 pasado ✅

---

## 📝 Documentos a Leer (Otro usuario)

**Después de que funcione, lee (orden):**

1. [ ] CONTEXTO/PUNTO_CERO.md (5 min) — Qué es COMPASS
2. [ ] CONTEXTO/VOZ_LUIS.md (3 min) — Cómo escribimos
3. [ ] PASO_2_CLOUD_RUN_MCP.md (10 min) — Cómo funciona Cloud Run MCP
4. [ ] TOOLS/CLOUD_RUN_SETUP.md (5 min) — Setup simplificado
5. [ ] PROTOCOLO_WORKANA_AUTOMATION.md (15 min) — Protocolo principal

---

## 🎯 Resultado Final

Cuando TODO esté hecho:

```
✅ Luis configuró delegación en Google Workspace
✅ Luis compartió credenciales seguramente
✅ Otro usuario cloné COMPASS
✅ Otro usuario instalé MCPs
✅ Otro usuario ejecuté COMPASS MODE
✅ Otro usuario pude leer emails automáticamente
✅ Otro usuario pude escribir en Sheets automáticamente
✅ Otro usuario leí documentación COMPASS

RESULTADO: COMPASS es multi-usuario. Cualquiera
en su máquina puede automatizar tareas usando
credenciales centralizadas + contexto compartido.
```

---

## 🚨 Si algo falla

**Para Luis:**
- Si Google Admin no muestra opciones: busca "domain delegation" directamente
- Si el error dice "invalid scope": copia exactamente los scopes (sin espacios)
- Si after 30 min sigue sin funcionar: verifica ID del client (113501103455996498798)

**Para otro usuario:**
- Si "MCP not found": reinstala con `npm install -g @anthropic-ai/mcp-server-gmail`
- Si "GOOGLE_APPLICATION_CREDENTIALS not found": verifica la ruta exacta (con tu usuario)
- Si "Permission denied in Sheets": comparte la sheet con `compass-sheets-bot@retarget-mcp.iam.gserviceaccount.com` como "Editor"
- Si Files MCP no funciona: verifica que `/Users/[TU_USUARIO]/Desktop/RETARGET-WORKSPACE/COMPASS/` existe

---

## 📞 Contacto

Si algo sigue sin funcionar:
- Guarda el error exacto
- Escribe a: luis@retarget.cl
- Incluye: qué intentaste + error exacto + comandos ejecutados

---

## ✅ Checklist Final

**Luis:**
- [ ] Google Workspace delegación configurada
- [ ] Scopes autorizados completamente
- [ ] Esperé 15 minutos para propagación
- [ ] Compartí credenciales con otro usuario

**Otro usuario:**
- [ ] Recibí credenciales de Luis
- [ ] Cloné COMPASS desde git
- [ ] Instalé 3 MCPs en Claude Code
- [ ] Pasé los 5 tests de verificación
- [ ] Leí documentación COMPASS
- [ ] Entiendo cómo usar COMPASS MODE

**Si todo está checkado:**

# 🎉 PASO 2 COMPLETADO

COMPASS está listo para multi-usuario.

---

**Creado:** 2026-05-11  
**Por:** Anthropomorfic (COMPASS)  
**Status:** 🚀 Listo para ejecutar
