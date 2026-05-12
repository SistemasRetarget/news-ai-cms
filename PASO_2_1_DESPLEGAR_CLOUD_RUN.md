# PASO 2.1 — Desplegar MCP a Cloud Run

**Para:** Luis (administrador COMPASS)  
**Tiempo:** 10-15 minutos  
**Objetivo:** Tener el MCP corriendo en Google Cloud Run

---

## ✅ Verificaciones previas

Antes de empezar, asegúrate que tienes:

- [ ] Acceso a Google Cloud Console (`console.cloud.google.com`)
- [ ] Proyecto `retarget-mcp` creado
- [ ] `gcloud` CLI instalado y configurado
- [ ] Git instalado

Verificar:
```bash
gcloud auth list
# Debe mostrar tu cuenta @retarget.cl como ACTIVE

gcloud config get-value project
# Debe mostrar: retarget-mcp
```

---

## 🚀 OPCIÓN A: Script Automatizado (RECOMENDADO)

### Paso 1: Clonar repositorio

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE
git clone https://github.com/SistemasRetarget/retarget-mcp-new.git
cd retarget-mcp-new
```

### Paso 2: Ejecutar script de deploy

```bash
./deploy-cloud-run.sh retarget-mcp
```

El script hará:
1. ✅ Habilitar APIs necesarias (Cloud Run, Artifact Registry, Cloud Build)
2. ✅ Crear repositorio Artifact Registry
3. ✅ Construir imagen Docker
4. ✅ Desplegar a Cloud Run
5. ✅ Testear health check
6. ✅ Imprimir URL del servicio

### Paso 3: Esperar a que termine

Mientras ejecuta, verás algo como:
```
1️⃣ Configurando proyecto GCP...
2️⃣ Habilitando APIs...
3️⃣ Verificando Artifact Registry...
...
✅ Despliegue completado!
📍 URL del servicio:
   https://retarget-mcp-xxxxx.run.app
```

**Guarda la URL — la necesitarás para el siguiente paso.**

---

## 🚀 OPCIÓN B: Despliegue Manual

Si el script falla o prefieres hacerlo manualmente:

### Paso 1: Configurar proyecto

```bash
gcloud config set project retarget-mcp
gcloud services enable cloudbuild.googleapis.com run.googleapis.com artifactregistry.googleapis.com
```

### Paso 2: Desplegar desde GitHub

```bash
gcloud run deploy retarget-mcp \
  --source=https://github.com/SistemasRetarget/retarget-mcp-new.git#main \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=2Gi \
  --cpu=2 \
  --max-instances=100 \
  --quiet
```

Esto tardará ~5-10 minutos mientras Cloud Build construye la imagen.

### Paso 3: Obtener la URL

```bash
gcloud run services describe retarget-mcp \
  --region=us-central1 \
  --format='value(status.url)'
```

Copia la URL resultante (ej: `https://retarget-mcp-xxxxx.run.app`)

---

## ✔️ Verificación

Prueba que el MCP está funcionando:

```bash
# Reemplaza con tu URL real
curl https://retarget-mcp-xxxxx.run.app/health

# Debe responder algo como:
# {"status":"healthy"}
```

---

## 📋 Próximos Pasos

Cuando el MCP esté desplegado:

1. **PASO 2.2:** Conectar Service Account (10 min)
   - Crear secreto en Secret Manager con credenciales Google
   - Montar secreto en Cloud Run

2. **PASO 2.3:** Crear usuario en Database (5 min)
   - Conectarse a PostgreSQL
   - Insertar usuario de test

3. **PASO 2.4:** Verificar acceso para otro usuario (10 min)
   - Usuario crea `~/.compass/config.json`
   - Usuario ejecuta `COMPASS MODE` en Claude
   - Verifica que funciona

---

## 🆘 Si algo falla

### Error: "Dockerfile not found"
**Solución:** El Dockerfile está en el repo. Asegúrate de estar en el directorio correcto:
```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-new
ls Dockerfile  # Debe existir
```

### Error: "Permission denied" en script
**Solución:** Dale permisos de ejecución:
```bash
chmod +x deploy-cloud-run.sh
./deploy-cloud-run.sh retarget-mcp
```

### Error: "Project not found"
**Solución:** Asegúrate que el proyecto existe:
```bash
gcloud projects list | grep retarget-mcp
gcloud config set project retarget-mcp
```

### Error: "API not enabled"
**Solución:** El script lo hace automáticamente. Si falla:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Build tarda muy time o falla
**Solución:** Ver logs de Cloud Build:
```bash
gcloud builds log --region=us-central1 --limit=100
```

---

## 📊 Checklist Final para PASO 2.1

- [ ] Verifiqué acceso a GCP y proyecto `retarget-mcp`
- [ ] Cloné repositorio `retarget-mcp-new`
- [ ] Ejecuté `./deploy-cloud-run.sh retarget-mcp`
- [ ] El despliegue terminó exitosamente
- [ ] Obtuve URL del MCP (ej: `https://retarget-mcp-xxxxx.run.app`)
- [ ] Probé `/health` y responde ✅
- [ ] **Guardé la URL — la necesito para PASO 2.2**

**Si todo está checkado:** ✅ **PASO 2.1 COMPLETADO**

Próximo: PASO 2.2 — Conectar Service Account

---

**Creado:** 2026-05-11  
**Versión:** 1.0  
**Para:** Luis (COMPASS Admin)
