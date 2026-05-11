# SETUP — Guía para nuevo usuario COMPASS

**Tiempo estimado:** 20-30 minutos  
**Requisito:** Tener cuenta en @retarget.cl (o autorizado por Luis)

---

## 🎯 Objetivo final

Al terminar este setup, podrás:
- ✅ Clonar COMPASS en tu máquina
- ✅ Instalar herramientas (MCPs)
- ✅ Acceder a correos del proyecto automáticamente
- ✅ Generar propuestas, drafts, respuestas
- ✅ Escribir resultados en Sheets compartidas
- ✅ **TODO desde tu propia máquina**

---

## 📋 Prerequisitos

- [ ] Acceso a @retarget.cl (email corporativo)
- [ ] Git instalado (`git --version`)
- [ ] Claude Code instalado ([descargar aquí](https://claude.com/claude-code))
- [ ] Acceso a Google Workspace (para credenciales compartidas)
- [ ] Una taza de café ☕

---

## PASO 1: Clonar el repositorio

```bash
# En tu terminal
git clone https://github.com/SistemasRetarget/news-ai-cms.git
cd news-ai-cms
cd COMPASS

# Verificar estructura
ls -la
# Deberías ver: CONTEXTO/, TOOLS/, TEMPLATES/, secrets/, README.md, SETUP.md
```

---

## PASO 2: Leer documentación base (15 minutos)

**Orden de lectura (CRÍTICO):**

1. **`CONTEXTO/PUNTO_CERO.md`** (5 min)
   - Qué es COMPASS, por qué existe, visión

2. **`CONTEXTO/VOZ_LUIS.md`** (3 min)
   - Cómo escribimos, tono, registro

3. **`README.md`** (3 min)
   - Este archivo, estructura general

4. **Uno de estos según tu rol:**
   - `CONTEXTO/PROTOCOLO_WORKANA_AUTOMATION.md` si vas a postular a Workana
   - `TOOLS/GMAIL_AUTOMATION.md` si vas a leer correos
   - `TOOLS/SHEETS_INTEGRATION.md` si vas a escribir datos

---

## PASO 3: Obtener credenciales (2 minutos)

**Escribe a Luis:**
```
Asunto: COMPASS Setup — credenciales service account

Hola Luis,
Estoy haciendo setup de COMPASS en mi máquina.
Necesito las credenciales de Google service account.
¿Me pasas el archivo google-sa.json compartido?

Gracias,
[Tu nombre]
```

**Luis responderá con:**
- Archivo `google-sa.json` (via email seguro, NO Git)
- Instrucciones de dónde ponerlo

---

## PASO 4: Configurar credenciales (3 minutos)

```bash
# En tu terminal, dentro de COMPASS/
cd secrets

# Luis te envía google-sa.json
# Cópialo acá (NO lo subes a Git)
# El .gitignore lo protege automáticamente

# Verificar que está oculto de Git:
cd ..
git status
# NO debe mostrar secrets/google-sa.json
```

**Ubicación final:**
```
COMPASS/
└─ secrets/
   └─ google-sa.json  ← ACÁ
```

---

## PASO 5: Instalar MCPs en Claude Code (10 minutos)

Abre Claude Code y ve a:
```
Settings → MCP Servers → Add Server
```

**Instala estos MCPs:**

1. **Gmail MCP**
   - Comando: `npm install @anthropic-ai/mcp-server-gmail`
   - Config: usa `secrets/google-sa.json`
   - Permite: leer/responder emails

2. **Google Sheets MCP**
   - Comando: `npm install @anthropic-ai/mcp-server-sheets`
   - Config: usa `secrets/google-sa.json`
   - Permite: escribir/leer datos en Sheets

3. **Files MCP** (opcional, ya viene)
   - Lee archivos locales
   - Permite: acceder a `/CONTEXTO/`, `/TEMPLATES/`

[Ver instrucciones detalladas en `TOOLS/MCP_SETUP.md`]

---

## PASO 6: Verificar que funciona (2 minutos)

En Claude Code, escribe:

```
COMPASS MODE
```

**Deberías ver:**
```
✅ COMPASS activado para [Tu nombre]
Contexto cargado:
├─ PUNTO_CERO.md
├─ VOZ_LUIS.md
├─ PROTOCOLO_WORKANA_AUTOMATION.md
├─ MCP Servers: Gmail, Sheets, Files
└─ Memoria: [tu nombre]

Listo para operar.
```

---

## PASO 7: Primer test — Lee un email

En Claude Code, escribe:

```
Lee los últimos 5 emails de la bandeja COMPASS.
Muéstrame los asuntos y remitentes.
```

**Debería responder algo como:**
```
Últimos emails:
1. De: cliente@example.com | Asunto: Propuesta Shopify
2. De: contractor@retarget.cl | Asunto: Status proyecto
3. ...
```

Si funciona, **¡setup completo!** ✅

---

## 🎮 Próximos pasos — Usa COMPASS

Ahora puedes usar los protocolos:

### 1️⃣ Leer correos y responder:
```
Busca propuestas de Workana en los últimos 3 días.
Genera respuestas automáticas siguiendo VOZ_LUIS.md.
Muéstramelas para revisar antes de enviar.
```

### 2️⃣ Postular a proyectos:
```
Busca 5 proyectos en Workana Chile (categoría IT + Marketing).
Genera propuestas siguiendo PROTOCOLO_WORKANA_AUTOMATION.md.
Estoy listo para postular.
```

### 3️⃣ Escribir en Sheets:
```
Registra propuesta de Workana en: [nombre Sheets]
Campos: Proyecto, Budget, Plazo, Fecha, Status
```

---

## 🆘 Si algo falla

| Problema | Solución |
|---|---|
| "MCP not found" | Reinstala MCPs, verifica Google auth |
| "Can't read secrets/google-sa.json" | Verifica ruta: debe estar en COMPASS/secrets/ |
| "COMPASS MODE no reconoce comandos" | Lee CONTEXTO/PUNTO_CERO.md de nuevo |
| "No puedo escribir en Sheets" | Verifica que service account tiene acceso (Luis lo configura) |
| Otro error | Escribe a Luis con error exacto |

---

## ✅ Checklist final

- [ ] Cloné COMPASS
- [ ] Leí PUNTO_CERO.md
- [ ] Obtuve google-sa.json de Luis
- [ ] Instalé MCPs (Gmail + Sheets)
- [ ] Escribí "COMPASS MODE" y funcionó
- [ ] Leí al menos un email automáticamente
- [ ] Entiendo cómo generar propuestas
- [ ] Sé dónde escribir resultados en Sheets

**Si todo está checkado: ¡Estás listo para usar COMPASS!** 🎉

---

## 📞 Support

**Preguntas específicas:**
- MCP: ve a `/TOOLS/MCP_SETUP.md`
- Workana: ve a `/CONTEXTO/PROTOCOLO_WORKANA_AUTOMATION.md`
- General: Lee `/CONTEXTO/PUNTO_CERO.md` de nuevo
- Todavía confundido: escribe a luis@retarget.cl

---

**Creado:** 2026-05-11  
**Versión:** 1.0  
**Última actualización:** PASO 1 setup
