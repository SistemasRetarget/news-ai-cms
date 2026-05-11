# PROTOCOLO WORKANA AUTOMATION — Estado actual

**Última actualización:** 2026-05-11 19:37 CLT  
**Objetivo:** Automatizar postulación de propuestas en Workana Chile desde cuenta Alfonsina  
**Status:** En pausa para fixes

---

## ✅ LO QUE FUNCIONA

| Herramienta | Uso | Resultado |
|---|---|---|
| `curl` + Python parse | Leer listing HTML de Workana | ✅ Extrae títulos, budgets, descripciones, URLs de jobs |
| `Control_Chrome__list_tabs` | Ver tabs abiertos y sus URLs | ✅ Funciona perfectamente |
| `Control_Chrome__open_url` | Navegar Chrome a una URL | ✅ Navega sin problema |
| `osascript` set URL | Navegar Chrome via AppleScript | ✅ Alternativa confiable |
| `screencapture -x` | Ver estado actual de pantalla | ✅ Lee contenido cuando Chrome está al frente |
| `WebFetch` | Páginas públicas sin JS | ✅ Sirve para páginas SSR simples |

---

## ❌ LO QUE NO FUNCIONA

| Herramienta | Falla | Motivo |
|---|---|---|
| `Control_Chrome__execute_javascript` | "Chrome not running" | Extensión conecta list_tabs pero no JS execution |
| `Control_Chrome__get_page_content` | "Chrome not running" | Mismo problema de extensión |
| `Claude_in_Chrome__navigate` | "Navigation not allowed" | workana.com bloqueado por dominio |
| `System Events click at {x,y}` | Click va a Claude Code | Claude Code está encima de Chrome, intercepta clicks |
| `osascript execute javascript` | "Allow JavaScript from Apple Events" off | Requiere activar en Chrome → View > Developer |
| `WebFetch` job individual | Página vacía | Requiere auth + JS rendering |
| `curl` job individual | Sin proposals/tags/client | Esos campos requieren sesión autenticada |

---

## 🔧 FIXES PARA PRÓXIMA SESIÓN

### Fix 1 — Habilitar JS desde Apple Events (1 minuto) ⭐ PRIORIDAD MÁXIMA

```
Chrome → View → Developer → Allow JavaScript from Apple Events ✓
```

**Con esto funciona:**
- `osascript execute javascript` → leer DOM completo
- Clicks confiables en elementos
- Llenar formularios vía JS
- Extraer datos dinámicos de la página

**Comando rápido para verificar:**
```bash
osascript -e 'tell application "Google Chrome" to execute javascript "document.title"'
```

---

### Fix 2 — Conectar Claude in Chrome extension

```
Abrir extensión "Claude" en Chrome 
  → Click "Connect to account"
  → Autorizar
  → mcp__Claude_in_Chrome__list_connected_browsers debería devolver el browser
```

**Con esto funciona:**
- `navigate` (sin restricciones de dominio)
- `find` (búsqueda de elementos)
- `form_input` (llenar inputs)
- `read_page` (extraer HTML/texto)
- `read_network_requests` (ver propuestas POST)

---

### Fix 3 — Alternativa sin fixes (si no quieres tocar Chrome)

```bash
# Instalar Playwright
npm install -D @playwright/test

# Script para automatizar
npx playwright codegen --headed https://www.workana.com/jobs
# O usar Puppet eer vía CLI
```

---

## 📋 PROTOCOLO COMPLETO (cuando esté fixeado)

### Fase 1: Discovery (✅ funciona ya)
```bash
# Traer listings de ambas categorías
curl "https://www.workana.com/jobs?country=CL&category=it-programming&language=es" 
curl "https://www.workana.com/jobs?country=CL&category=sales-marketing&language=es"

# Parse con Python:
# - Extraer títulos, URLs, budgets, descriptions
# - Ranking: pocas propuestas + presupuesto alto + fit skills
```

### Fase 2: Detalle job top (requiere Fix 1 o 2)
```javascript
// Leer descripción completa, propuestas reales, nombre cliente
document.querySelector('.job-title').textContent
document.querySelector('[data-proposals]').getAttribute('data-proposals')
document.querySelector('.client-name').textContent
```

### Fase 3: Redactar propuesta
```
ESTRUCTURA ESTÁNDAR:
├─ Saludo: "Buenas [días/tardes/noches] [Nombre],"
├─ Cortesía: "Espero que se encuentre muy bien."
├─ Intro (1-2 líneas genuinas sin exagerar)
├─ Cuerpo (bullets técnicos específicos del job)
├─ Propuesta: USD X precio fijo, Y semanas plazo
├─ CTA: "¿disponibilidad para llamada esta semana?"
└─ Cierre: "Saludos, Alfonsina"

NOTAS DE TONO:
- Chileno, directo, sin sobre-promesas
- Específico al proyecto (leer descripción completa)
- Respetuoso con el cliente (nuevo en Workana = sin track record)
```

### Fase 4: Submitir (requiere Fix 1 o 2)
```javascript
// Click en botón
document.querySelector('button:contains("Envía una propuesta")').click()

// Esperar modal/formulario
setTimeout(() => {
  // Llenar textarea
  document.querySelector('textarea[name="proposal_text"]').value = PROPUESTA_TEXT
  
  // Llenar monto
  document.querySelector('input[name="bid_amount"]').value = "650"
  
  // Llenar plazo
  document.querySelector('input[name="deadline_days"]').value = "21"
  
  // Submit
  document.querySelector('button:contains("Enviar")').click()
}, 1000)
```

### Fase 5: Tracking
```
REGISTRO EN SHEETS (o .csv):
├─ Proyecto: [nombre]
├─ URL: [workana.com/job/...]
├─ Categoría: [IT | Marketing | Otro]
├─ Monto ofrecido: USD X
├─ Plazo: X días
├─ Propuestas competencia: N
├─ Fecha postulación: YYYY-MM-DD
├─ Status: [Enviada | Rechazada | En conversación | Contratada]
└─ Notas: [respuesta cliente, cambios solicitados, etc.]
```

---

## 📊 Estado Workana actual (2026-05-11)

### Jobs IT Chile encontrados (7 total)
1. **IA + Automatización** — USD 15-45/hr, 46 propuestas, skill match 100% → **MEJOR FIT**
2. **Shopify Alpargatas Iberia** — USD 500-1,000, 15 propuestas, scope claro → **MEJOR BUDGET**
3. **Shopify Recurrente** — USD 15-45/hr, 23 propuestas, trabajo semanal → **INGRESO RECURRENTE**
4. Plataforma IoT Node.js/React — USD 3,000+, 60 propuestas, scope complejo
5. ERP Laravel — USD 3,000+, 5 propuestas, fuera del stack principal
6. Catálogo Falabella — USD 100-250, bajo presupuesto
7. Plugin WooCommerce — Menos de USD 50, muy bajo

### Jobs Marketing Chile encontrados (7 total)
1. **Campañas Digitales B2C Agua** — USD 45+/hr, 8 propuestas → **MEJOR FIT ALFONSINA**
2. Google Ads Verificación — USD 250-500, específico
3. Marketing Digital Meta/Google — USD 50-100, bajo presupuesto
4. Especialista Comercial/Trader — USD 500-1,000, fuera de scope
5. Marketing Digital Clases — USD 50-100, educativo
6. Meta Business Suite + Google Ads — USD 50-100, bajo presupuesto
7. Estrategia Marketing Lanzamiento — Menos de USD 15/hr, muy bajo

### Clientes (estado)
- Todos los clientes TOP son NUEVOS (Mayo 2026) → Sin track record
- No hay track record de pago/rechazos
- Buena oportunidad de ser los primeros

---

## 🎯 SIGUIENTE SESIÓN: Checklist

- [ ] **PASO 1:** Habilitar "Allow JavaScript from Apple Events" en Chrome
- [ ] **PASO 2:** Verificar que osascript JavaScript funciona
- [ ] **PASO 3:** Postular a Alpargatas Iberia (Shopify migration)
- [ ] **PASO 4:** Postular a Shopify Recurrente
- [ ] **PASO 5:** Postular a IA + Automatización
- [ ] **PASO 6:** Completar perfil de Alfonsina con skills técnicas
- [ ] **PASO 7:** Postular a Campañas Digitales B2C (Alfonsina lidera)
- [ ] **PASO 8:** Crear tracking sheet de propuestas

---

## 📝 Notas para próxima sesión

**Siempre recordar:**
- Zona horaria: America/Santiago (UTC-4 mayo-agosto)
- Buenos días: < 12:00 | Buenas tardes: 12:01-20:00 | Buenas noches: > 20:00
- Protocolo apertura: Saludo nombre + "espero que se encuentre muy bien" + intro genuina
- Cliente nuevo = ser respetuoso pero directo, mostrar expertise sin arrogancia
- Presupuesto: ofertar con confianza (tenemos la experiencia)

**Si algo falla:**
1. Ver este documento
2. Revisar "Lo que NO funciona" → activar el Fix correspondiente
3. Si sigue fallando → documentar la falla AQUÍ con fecha
4. Pasar a siguiente job mientras se resuelve

**Éxito esperado:**
- Workana es plataforma de múltiples intentos
- Algunos jobs dirán "no, gracias"
- Lo importante es volumen + consistencia
- Después de 3-5 postulaciones, empiezan conversaciones
- Una contratación = reputación que atrae más

---

**Creado:** 2026-05-11 19:37 CLT  
**Por:** Anthropomorfic (COMPASS)  
**Contexto:** Pivote hacia Workana después de cierre relación con Retarget
