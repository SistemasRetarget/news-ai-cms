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

### Para Luis (admin del sistema):
1. Lee `/CONTEXTO/PUNTO_CERO.md` — Qué es COMPASS y por qué existe
2. Configura credenciales en `secrets/` (NO en Git)
3. Documenta nuevos protocolos en `CONTEXTO/`

### Para otro usuario (Juan en otra máquina):
1. **Lee `SETUP.md`** — Instrucciones paso a paso
2. Clona este repo
3. Instala MCPs (Gmail, Sheets)
4. Carga credenciales (compartidas y seguras)
5. **Escribe "COMPASS MODE"** en Claude → contexto listo
6. **Usa las herramientas normalmente**

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

↓ Sistema automático:
- Carga /CONTEXTO/* en tu sesión
- Carga tu memoria personal
- Activa herramientas (Gmail, Sheets)
- Responde: "✅ COMPASS activado para [tu nombre]"

↓ Ahora puedes:
- Usar protocolos específicos
- Leer/responder correos
- Escribir en Sheets
- TODO con contexto COMPASS completo
```

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

**Última actualización:** 2026-05-11  
**Versión:** 1.0 (PASO 1 — Estructura centralizada)  
**Status:** 🔧 En desarrollo — Próximo: PASO 2 (Service Account Google)
