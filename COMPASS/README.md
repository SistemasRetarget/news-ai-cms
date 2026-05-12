# COMPASS — Sistema Centralizado de Automatización

**Bienvenida a COMPASS.** Este repositorio contiene TODO lo necesario para que cualquiera (Luis, empleados, contractors) pueda acceder a las herramientas de automatización: lectura de correos, generación de respuestas, drafts, integración con Sheets, etc.

---

## 🎯 ¿Qué es COMPASS?

COMPASS es un **sistema de automatización inteligente** que permite:

- ✅ **Leer correos** de proyectos automáticamente
- ✅ **Generar respuestas** inteligentes (propuestas Workana, cotizaciones, etc.)
- ✅ **Crear drafts** para Sheets, Google Docs
- ✅ **Escribir resultados** en archivos centralizados
- ✅ **Acceder desde cualquier máquina** (no solo de Luis)

**Especialmente diseñado para:**
- 📧 Automatización de respuestas Workana
- 📊 Integración Sheets (proyectos, propuestas, tracking)
- 🔧 Integración con sistemas (APIs, webhooks)
- 👥 Acceso multi-usuario (equipos, contractors)

---

## 📂 Estructura

```
COMPASS/
├─ CONTEXTO/              ← Documentación base (LEE ESTO PRIMERO)
│  ├─ PUNTO_CERO.md      ← Fundamento absoluto
│  ├─ VOZ_LUIS.md        ← Cómo escribimos/hablamos
│  ├─ rules_compass_core.md  ← 5 reglas inmutables
│  └─ PROTOCOLO_*.md     ← Protocolos específicos (Workana, etc.)
│
├─ TOOLS/                 ← Configuración de herramientas
│  ├─ MCP_SETUP.md       ← Instalar MCPs (Gmail, Sheets, etc.)
│  ├─ GMAIL_AUTOMATION.md ← Leer/responder correos
│  ├─ SHEETS_INTEGRATION.md ← Escribir resultados en Sheets
│  └─ SCHEDULED_TASKS.md ← Automatización recurrente
│
├─ TEMPLATES/             ← Plantillas reutilizables
│  ├─ PROPOSAL_TEMPLATE.md    ← Propuestas Workana
│  ├─ EMAIL_RESPONSE.md       ← Respuestas automáticas
│  └─ SHEETS_DRAFT.md         ← Formato de datos Sheets
│
├─ secrets/               ← Credenciales (NUNCA en Git)
│  ├─ .gitignore          ← google-sa.json, credenciales
│  └─ [credenciales locales]
│
├─ MCP_CONFIGS/           ← Archivos de configuración MCP
│  ├─ gmail-config.json
│  └─ sheets-config.json
│
├─ README.md              ← Este archivo
└─ SETUP.md               ← Instrucciones para nuevo usuario
```

---

## 🚀 Primeros pasos

### Para Luis (administrador del sistema):
1. Lee `/CONTEXTO/PUNTO_CERO.md` — Qué es COMPASS
2. Lee **`PASO_2_CLOUD_RUN_SUMMARY.md`** — Resumen ejecutivo (5 min)
3. Despliega MCP en Cloud Run (40 min total)
   - Sigue: `PASO_2_CLOUD_RUN_MCP.md`
   - Checklist: `PASO_2_CHECKLIST.md`

### Para otro usuario (Juan en otra máquina):
1. **Lee `TOOLS/CLOUD_RUN_SETUP.md`** — Setup simplificado (5 min)
2. Clona este repo: `git clone [URL]`
3. Crea `~/.compass/config.json` con:
   - URL del MCP (que te da Luis)
   - Tu USER_ID (que Luis crea en DB)
4. **Escribe "COMPASS MODE"** en Claude → conecta a Cloud Run MCP
5. ¡Listo! Estás operacional sin instalar nada

---

## 📖 Documentación por tema

| Necesito | Archivo | Tiempo |
|---|---|---|
| Entender qué es COMPASS | CONTEXTO/PUNTO_CERO.md | 5 min |
| Cómo hablamos/escribimos | CONTEXTO/VOZ_LUIS.md | 3 min |
| Reglas inmutables | CONTEXTO/rules_compass_core.md | 2 min |
| Postular en Workana | CONTEXTO/PROTOCOLO_WORKANA_AUTOMATION.md | 10 min |
| Instalar herramientas | TOOLS/MCP_SETUP.md | 20 min |
| Leer/responder emails | TOOLS/GMAIL_AUTOMATION.md | 10 min |
| Escribir en Sheets | TOOLS/SHEETS_INTEGRATION.md | 10 min |
| Plantilla propuesta | TEMPLATES/PROPOSAL_TEMPLATE.md | 2 min |

---

## 🔐 Seguridad

**Credenciales:**
- `secrets/google-sa.json` ← **NUNCA en Git**
- `secrets/.env` ← **NUNCA en Git**
- `.gitignore` lo protege automáticamente

**Acceso:**
- Whitelist de usuarios (qué emails pueden acceder)
- Service account de Google (central, no personal)
- Auditoría en Sheets (quién hizo qué, cuándo)

---

## 💬 Cómo usar COMPASS

### En Claude Chat:
```
Escribe en cualquier sesión de Claude:

"COMPASS MODE"

↓ Sistema automático (Opción B — Cloud Run):
- Lee tu config.json (~/.compass/config.json)
- Se conecta al Cloud Run MCP centralizado
- Obtiene tu contexto desde el servidor
- Carga /CONTEXTO/* localmente
- Responde: "✅ COMPASS activado para [tu nombre]"

↓ Ahora puedes:
- Usar protocolos específicos
- Leer/responder correos (vía MCP)
- Escribir en Sheets (vía MCP)
- Ver reportes y métricas
- TODO con contexto COMPASS completo + infraestructura en la nube
```

**Nota:** COMPASS usa un MCP centralizado en **Google Cloud Run**, no MCPs locales. Esto significa:
- ✅ Sin instalar MCPs complejos
- ✅ Un único punto centralizado
- ✅ Credenciales seguras en servidor
- ✅ Auditoría automática

### En Slack (futuro):
```
#compass-prompts: "COMPASS MODE - Postular a [proyecto]"
@compass-bot: procesa automáticamente
```

---

## 📞 Contacto & Soporte

**Problemas?**
1. Revisa `SETUP.md`
2. Verifica credenciales en `secrets/`
3. Lee `/TOOLS/` para la herramienta específica
4. Escribe a: luis@retarget.cl con error específico

---

## 🚀 PASO 2 — Cloud Run MCP Centralizado (LISTO PARA EJECUTAR ✅)

Para desplegar MCP a Cloud Run y configurar acceso multi-usuario:

**🎯 Empezar aquí:**
- **[PASO_2_INICIO.md](../PASO_2_INICIO.md)** ← PUNTO DE ENTRADA (Leo esto primero)
- **[PASO_2_EJECUTAR_AHORA.md](../PASO_2_EJECUTAR_AHORA.md)** — Ejecución rápida en 3 fases (30-40 min)

**📚 Documentación detallada:**
- **[PASO_2_1_DESPLEGAR_CLOUD_RUN.md](../PASO_2_1_DESPLEGAR_CLOUD_RUN.md)** — Deploy del MCP (15 min)
- **[PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md](../PASO_2_2_CONECTAR_SERVICE_ACCOUNT.md)** — Credenciales Google (10 min)
- **[PASO_2_CLOUD_RUN_MCP.md](../PASO_2_CLOUD_RUN_MCP.md)** — Especificación técnica completa
- **[PASO_2_CLOUD_RUN_SUMMARY.md](../PASO_2_CLOUD_RUN_SUMMARY.md)** — Resumen ejecutivo

**Para otro usuario (después de PASO 2):**
- **[TOOLS/CLOUD_RUN_SETUP.md](./TOOLS/CLOUD_RUN_SETUP.md)** — Setup en 5 minutos (sin instalar nada)

---

**Última actualización:** 2026-05-11  
**Versión:** 1.0 (PASO 1 completado, PASO 2 en progreso)  
**Status:** 🔧 PASO 2 — Service Account Centralizado iniciado
