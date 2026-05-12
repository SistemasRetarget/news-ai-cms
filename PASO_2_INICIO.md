# PASO 2 — Punto de Entrada

**Para:** Luis  
**Lee:** ESTE archivo primero (3 minutos)  
**Luego:** Pasa a [PASO_2_EJECUTAR_AHORA.md](PASO_2_EJECUTAR_AHORA.md)

---

## 🎯 ¿Qué es PASO 2?

PASO 2 es la **transformación de COMPASS de personal a empresarial**.

**Antes (PASO 1):**
- Documentación centralizada ✅
- Solo Luis puede operar ❌
- MCPs instalados localmente (complicado) ❌

**Después (PASO 2):**
- Documentación centralizada ✅
- Cualquier usuario puede operar ✅
- MCP en la nube (centralizado y seguro) ✅
- Credenciales en servidor (no en máquina local) ✅
- Auditoría automática ✅

---

## 🏗️ Arquitectura

```
COMPASS = Sistema descentralizado pero coordinado

USUARIO 1 (su máquina)           USUARIO 2 (su máquina)
┌──────────────────┐              ┌──────────────────┐
│ Claude Code      │              │ Claude Code      │
│ ~/.compass/      │              │ ~/.compass/      │
│ config.json      │              │ config.json      │
└────────┬─────────┘              └────────┬─────────┘
         │                                  │
         └──────────────┬───────────────────┘
                        │ HTTP
                        ↓
         ┌─────────────────────────────┐
         │ Cloud Run MCP Centralizado  │
         │ (retarget-mcp.run.app)      │
         │                             │
         │ • Context builder           │
         │ • Gmail integration         │
         │ • Sheets integration        │
         │ • Feedback/Reports          │
         └────────────┬────────────────┘
                      │
        ┌─────────────┴────────────────┐
        │                              │
        ↓                              ↓
   ┌─────────┐               ┌──────────────┐
   │ Google  │               │ PostgreSQL   │
   │ Cloud   │               │ (auditoría)  │
   └─────────┘               └──────────────┘
```

---

## 📋 Documentos por orden

### Para ejecutar PASO 2 (Luis)

1. **[PASO_2_EJECUTAR_AHORA.md](PASO_2_EJECUTAR_AHORA.md)** ← **EMPIEZA AQUÍ**
   - Resumen ejecutivo con 3 fases
   - Comandos listos para copiar/pegar
   - Tiempo estimado: 30-40 minutos

2. **[PASO_2_1_DESPLEGAR_CLOUD_RUN.md](PASO_2_1_DESPLEGAR_CLOUD_RUN.md)**
   - Si necesitas más detalle en el deployment
   - Script automatizado vs manual
   - Troubleshooting específico

3. **[PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md](PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md)**
   - Conexión de credenciales Google
   - Secret Manager + Cloud Run
   - Verificación de acceso

4. **[PASO_2_CHECKLIST.md](PASO_2_CHECKLIST.md)**
   - Checklist completo (tipo de documento anterior)
   - Para verificación final y auditoría

### Para otros usuarios (después de PASO 2)

5. **[TOOLS/CLOUD_RUN_SETUP.md](TOOLS/CLOUD_RUN_SETUP.md)**
   - Setup simplificado para nuevo usuario
   - Solo 5 minutos
   - Sin instalar MCPs

---

## ⏱️ Timeline

```
Si empiezas ahora mismo (14:00):

14:00 — Lees PASO_2_EJECUTAR_AHORA.md (3 min)
14:03 — Ejecutas ./deploy-cloud-run.sh (mientras tanto, empieza secreto)
14:10 — Esperando a que Cloud Build construya (tomar café)
14:15 — Cloud Build termina, obtuviste URL
14:20 — Secreto creado en Secret Manager
14:25 — Servicio actualizado con secreto
14:30 — PostgreSQL usuario creado
14:35 — ✅ PASO 2 COMPLETADO

Total: 35 minutos
```

---

## ✅ Requisitos

Antes de empezar:

- [ ] Acceso a `gcloud` CLI (google-cloud-sdk instalado)
- [ ] Proyecto GCP `retarget-mcp` creado
- [ ] Archivo `/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json` (credenciales)
- [ ] Git instalado
- [ ] Acceso a GitHub como SistemasRetarget

Verificar:
```bash
gcloud auth list  # Debe mostrar tu cuenta activa
gcloud config get-value project  # Debe mostrar retarget-mcp
```

---

## 🎯 Objetivo Final

Después de PASO 2:

```bash
# Otro usuario (cualquiera, en su máquina):
git clone https://github.com/SistemasRetarget/news-ai-cms.git
cd news-ai-cms/COMPASS

mkdir -p ~/.compass
cat > ~/.compass/config.json << 'EOF'
{
  "mcp_url": "https://retarget-mcp-xxxxx.run.app",  # URL del MCP (lo conseguiste en PASO 2)
  "user_id": 1                                       # USER_ID (lo conseguiste en PASO 2.3)
}
EOF

# En Claude Code:
# COMPASS MODE

# ✅ Conectado y listo para trabajar
# Sin instalar nada. Sin credenciales locales. Solo config.json.
```

---

## 🚀 ¿Listo?

### Opción A: Ejecución Rápida
→ Ir a **[PASO_2_EJECUTAR_AHORA.md](PASO_2_EJECUTAR_AHORA.md)**

### Opción B: Lectura completa
→ Leer [PASO_2_CLOUD_RUN_SUMMARY.md](PASO_2_CLOUD_RUN_SUMMARY.md) (resumen técnico)

### Opción C: Entender arquitectura
→ Leer [PASO_2_CLOUD_RUN_MCP.md](PASO_2_CLOUD_RUN_MCP.md) (especificación técnica completa)

---

## 📞 Si algo falla

1. Lee el troubleshooting en [PASO_2_EJECUTAR_AHORA.md](PASO_2_EJECUTAR_AHORA.md)
2. Si persiste, ve a [PASO_2_1_DESPLEGAR_CLOUD_RUN.md](PASO_2_1_DESPLEGAR_CLOUD_RUN.md) sección "Si algo falla"
3. Si aún no resuelve, contacta a Anthropomorfic

---

## 🎉 Bienvenida a la Era Empresarial de COMPASS

PASO 2 es donde COMPASS deja de ser un experimento y se convierte en infraestructura seria.

**Después de hoy:**
- ✅ Infraestructura en la nube
- ✅ Multi-usuario simultáneamente
- ✅ Credenciales centralizadas
- ✅ Auditoría automática
- ✅ Escalable y confiable

---

**Creado:** 2026-05-11  
**Para:** Luis (administrador COMPASS)  
**Status:** ✅ Listo para ejecutar  
**Tiempo estimado:** 40 minutos

→ **[Empezar PASO 2 AHORA](PASO_2_EJECUTAR_AHORA.md)**
