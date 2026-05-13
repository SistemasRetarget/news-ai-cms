---
date: 2026-05-13
status: LISTO PARA DESPLEGAR
---

# ⚡ COMPASS Auto-Responder — Próximos Pasos

Sistema **100% automatizado** en Google Cloud que responde emails de Mauricio/Leig sin intervención.

---

## 🎯 Lo que hace

```
Email de Mauricio/Leig
       ↓
Cloud Function (Google Cloud)
  • Lee Gmail
  • Responde con template + stats vivos
  • Registra T-XX en Sheets ("Pendiente Luis")
  • Marca como procesado
       ↓
Luis se conecta después, ve T-XX, completa detalles
```

**Costo:** ~$0.5/mes (corre sin tu PC)  
**Velocidad:** Responde en <5 minutos  
**Confiabilidad:** 100% cloud-managed  

---

## 📋 Checklist de Implementación

### ✅ YA HECHO (por mí)

- ✅ Cloud Function principal (`compass-email-responder.py`)
- ✅ OAuth setup script (`setup-gmail-oauth.py`)
- ✅ Deployment automatizado (`deploy.sh`)
- ✅ Documentación completa

### 👤 FALTA (por ti)

```
1. [ ] Instalar Google Cloud CLI
2. [ ] Autorizar Gmail (OAuth setup) — 2 min
3. [ ] Ejecutar deploy script — 1 min
4. [ ] Verificar logs — Opcional, verificación
5. [ ] Opcionalmente: ajustar templates según feedback
```

---

## 🚀 Instrucciones Paso a Paso

### 1️⃣ Instalar Google Cloud CLI (5 min)

```bash
# macOS
brew install google-cloud-sdk
gcloud init
gcloud auth login
```

### 2️⃣ Autorizar Gmail (2 min)

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/cloud
python3 setup-gmail-oauth.py
```

**Qué pasa:**
- Script abre navegador
- Autorizas acceso a Gmail
- Se guarda refresh token en Secret Manager

### 3️⃣ Desplegar (1 min)

```bash
bash deploy.sh
```

**Qué pasa:**
- Instala Cloud Function en Google Cloud
- Crea Cloud Scheduler (cada 5 min)
- Muestra URL de la función

### 4️⃣ Verificar (Opcional)

```bash
# Ver logs en vivo
gcloud functions logs read compass-email-responder --follow

# Ejecutar manualmente para testing
gcloud functions call compass-email-responder
```

---

## 📊 Resultado esperado

### Antes

```
📧 Mauricio/Leig envía → Luis se conecta → Responde manual
   ❌ Requiere que Luis esté conectado
   ❌ Delay potencial
   ❌ Tedioso registrar en Sheets
```

### Ahora

```
📧 Mauricio/Leig envía → COMPASS responde automático → Registra en Sheets
   ✅ Corre sin que Luis esté conectado
   ✅ Respuesta en <5 min
   ✅ T-XX ya en Sheets, Luis solo completa detalles
```

---

## 📝 Respuestas automáticas

### Tipo 1: Corrección reportada

**Ejemplo email:** "La página está rota, botones desalineados"

**Respuesta automática:**
```
Hola,

Anotado. Revisamos el punto reportado.

Corrección tomada. Lo resolvemos y confirmamos cuando esté live.

⚡ Zorrito — RETARGET
sistemas@retarget.cl · retarget.cl
```

### Tipo 2: Reporte/Status

**Ejemplo email:** "¿Qué hay de nuevo? ¿Cómo va el avance?"

**Respuesta automática:**
```
Hola,

Aquí el estado de las iniciativas:

📊 Resumen:
✅ 5 completadas hoy
⏳ 3 en progreso
⏲️ 2 pendientes
📈 Total: 23 tickets

Estamos ejecutando en orden de prioridad. Reportamos cambios cuando hay movimiento.

⚡ Zorrito — RETARGET
sistemas@retarget.cl · retarget.cl
```

---

## 🔐 Seguridad

✅ Gmail token en **Secret Manager** (Google Cloud encrypts)  
✅ Service account con **permisos mínimos**  
✅ Logs **auditables** (para tracking)  
✅ **CORS disabled** (no publicly accessible)  

---

## 💾 Archivos creados

```
/cloud/
├── compass-email-responder.py    ← Cloud Function
├── setup-gmail-oauth.py          ← OAuth setup (ejecutar una sola vez)
├── deploy.sh                     ← Deployment (ejecutar una sola vez)
├── requirements.txt              ← Dependencias Python
├── .env.example                  ← Variables de config
├── DEPLOY.md                     ← Instrucciones detalladas
└── README.md                     ← Documentación general
```

---

## ⏱️ Timeline

| Paso | Tiempo | Descripción |
|------|--------|------------|
| 1. Instalar gcloud | 5 min | One-time setup |
| 2. OAuth authorize | 2 min | Browser click |
| 3. Deploy | 1 min | Un script |
| 4. Verify (opcional) | 2 min | Check logs |
| **Total** | **~10 min** | **100% automatizado después** |

---

## 📈 Próximos pasos después de deploy

1. **Monitoreo primeras 48h**
   - Ver si llegan emails de Mauricio/Leig
   - Verificar que se responden correctamente
   - Ajustar templates si es necesario

2. **Agregar más contactos**
   - Modificar ALLOWED_FROM en función
   - Re-deploy

3. **Escalar a otros sitios**
   - Mismo código, diferentes Sheets
   - Crear nuevas Cloud Functions si es necesario

---

## ❓ FAQ

**P: ¿Funciona si mi PC está apagado?**  
R: Sí. Corre en Google Cloud, completamente independiente.

**P: ¿Cuánto cuesta?**  
R: ~$0.50/mes. Cloud Functions gratuito (primera 1M de invocaciones/mes), Scheduler $0.4/mes aprox.

**P: ¿Qué pasa si hay error?**  
R: Cloud Function lo registra en logs. Puedo debuggear y corregir. No afecta operación (se reintenta).

**P: ¿Puedo cambiar templates?**  
R: Sí. Actualizar en `compass-email-responder.py` y re-ejecutar deploy.

**P: ¿Qué pasa con los T-XX que registra?**  
R: Son "Pendiente Luis - Detalles". Tú los completas cuando te conectes (solución, fechas, responsable).

---

## ⚠️ Limitaciones conocidas

- No integra con WP API (solo lee/responde emails + Sheets)
- No ejecuta las soluciones automáticamente (solo reporta)
- Respuestas son templates fijos (no IA generada, es discreto así)

---

## 🎯 Resumen en una línea

**Luis no tiene que estar conectado para responder a Mauricio/Leig. COMPASS lo hace automáticamente cada 5 minutos.**

---

**Listo para desplegar cuando des OK:**

```bash
cd /Users/spam11/Desktop/RETARGET-WORKSPACE/cloud

# 1. OAuth
python3 setup-gmail-oauth.py

# 2. Deploy
bash deploy.sh

# 3. Listo ✅
```

---

*COMPASS Cloud Auto-Responder | 2026-05-13 | Ready to Deploy*
