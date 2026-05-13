# 🤖 COMPASS Cloud Auto-Responder

Sistema automatizado que responde emails de Mauricio/Leig sin que Luis esté conectado.

## 🎯 Qué hace

```
Mauricio/Leig envía correo
       ↓
Cloud Scheduler (cada 5 min) ← corre EN GOOGLE CLOUD, sin tu PC
       ↓
Lee Gmail, encuentra correos sin responder
       ↓
COMPASS responde automáticamente:
  • Si es corrección → Template 2 "Corrección Recibida"
  • Si es reporte → Template 4 "Reporte Avance"
  • Si es aclaración → Template 5 "Pedido Aclaración"
       ↓
Adjunta stats vivos del Sheets (✅ completadas, ⏳ en progreso, etc)
       ↓
Registra T-XX en Sheets como "Pendiente Luis — Detalles"
       ↓
Marca email como procesado
       ↓
Siguiente ejecución en 5 min
```

**Resultado:** Luis se conecta después, ve T-XX nuevo en Sheets, completa detalles (solución, fechas, etc).

---

## 📁 Estructura

```
cloud/
├── compass-email-responder.py    ← Cloud Function principal
├── setup-gmail-oauth.py          ← Setup ONE TIME (obtener refresh token)
├── requirements.txt              ← Dependencias Python
├── .env.example                  ← Variables de config
├── DEPLOY.md                     ← Instrucciones step-by-step
└── README.md                     ← Este archivo
```

---

## ⚡ Quick Start

### 1️⃣ Autorizar Gmail (Una sola vez)

```bash
cd cloud
python3 setup-gmail-oauth.py
```

Esto:
- Abre navegador para que autorices
- Obtiene refresh token
- Lo guarda en Google Cloud Secret Manager

### 2️⃣ Deploy a Google Cloud

```bash
# Ver DEPLOY.md para pasos exactos
gcloud functions deploy compass-email-responder \
  --runtime python311 --trigger-http --allow-unauthenticated

gcloud scheduler jobs create http compass-responder-trigger \
  --schedule="*/5 * * * *"
```

### 3️⃣ Test

```bash
# Ver logs
gcloud functions logs read compass-email-responder --limit 20 --follow
```

---

## 🔄 Flujo completo

### Antes (Manual)

```
Mauricio envía email
Luis se conecta a leer
Luis responde manualmente
Luis registra en Sheets
Luis completa ticket
```

### Ahora (Automatizado)

```
Mauricio envía email
Cloud Function responde automáticamente (sin Luis)
Registra T-XX en Sheets (pendiente Luis para detalles)
Luis se conecta cuando quiera, ve T-XX, completa detalles
```

---

## 📊 Qué registra en Sheets

**Cuando llega correo nuevo:**

| Ticket | Negocio | Sitio | Origen | Problema | Solución | Estado | Responsable |
|--------|---------|-------|--------|----------|----------|--------|------------|
| T-23 | Correo Externo | Múltiple | mauricio@... | "Subject del email" | [Pendiente Luis - Detalles] | Pendiente Luis | COMPASS |

**Nota:** El estado dice "Pendiente Luis" porque la Cloud Function solo registra, no resuelve. Cuando Luis vea T-23, actualiza:
- Solución → qué se va a hacer
- Responsable → quién lo hace
- Fecha estimada
- etc.

---

## 🔐 Seguridad

✅ **Refresh token cifrado** en Google Cloud Secret Manager  
✅ **Service account** con permisos mínimos  
✅ **Logs auditables** en Cloud Logging  
✅ **Email responses** enviados desde COMPASS (ZORRITO)  

---

## 📈 Monitoreo

```bash
# Logs en tiempo real
gcloud functions logs read compass-email-responder --follow

# Estadísticas de ejecución
gcloud scheduler jobs describe compass-responder-trigger --location=us-central1

# Ejecutar manualmente (testing)
gcloud functions call compass-email-responder
```

---

## ❌ Troubleshooting

### "Permission denied"
→ Ver sección Troubleshooting en DEPLOY.md

### "Gmail API not enabled"
```bash
gcloud services enable gmail.googleapis.com sheets.googleapis.com
```

### "Secret not found"
```bash
# Verificar
gcloud secrets list
# Crear manualmente si falta
gcloud secrets create gmail-refresh-token --data-file=- <<< "TOKEN"
```

---

## 🎯 Próximos pasos

1. ✅ Setup OAuth
2. ✅ Deploy función
3. ✅ Crear scheduler
4. 📊 Monitorear
5. 🎨 Ajustar templates según feedback
6. 📈 Agregar más contactos/sitios

---

## 📝 Notas

- **Corre en Google Cloud** — funciona incluso con tu PC apagado
- **Event-driven** — solo actúa cuando hay email (no spam constante)
- **Discreto** — sin revelar procesos internos
- **Escalable** — mismo código para múltiples clientes/contactos

---

*COMPASS Auto-Responder | Retarget Agency | 2026-05-13*
