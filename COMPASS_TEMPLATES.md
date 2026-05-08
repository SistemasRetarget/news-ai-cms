# 📨 COMPASS Templates — Plantillas oficiales de comunicación

> **Regla inmutable:** Misma estructura SIEMPRE. Diferente adaptación. Footer COMPASS obligatorio.

## Identidad visual fija

- **Naranja COMPASS:** `#FF6B35` → `#F7931E` (gradiente)
- **Brújula SVG:** SMIL animation, rota cada 6-8s
- **Tipografía:** `-apple-system, Segoe UI, Roboto`
- **Logo arriba** → correo INTERNO
- **Logo abajo** → correo a CLIENTE

---

## Componentes reutilizables

### Brújula animada SVG

```html
<svg width="56" height="56" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6B35"/>
      <stop offset="100%" stop-color="#F7931E"/>
    </linearGradient>
  </defs>
  <circle cx="50" cy="50" r="46" fill="none" stroke="url(#g)" stroke-width="3"/>
  <polygon points="50,12 56,50 50,55 44,50" fill="url(#g)">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="6s" repeatCount="indefinite"/>
  </polygon>
  <polygon points="50,88 44,50 50,45 56,50" fill="#202124" opacity="0.3">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="6s" repeatCount="indefinite"/>
  </polygon>
  <circle cx="50" cy="50" r="5" fill="#FF6B35"/>
</svg>
```

### Header INTERNO (logo arriba centrado)

```html
<tr><td align="center" style="padding:16px 0 24px 0; border-bottom:1px solid #e8eaed;">
  [BRÚJULA SVG]
  <div style="font-size:14px; font-weight:bold; color:#FF6B35; letter-spacing:3px; margin-top:8px;">COMPASS</div>
  <div style="font-size:12px; color:#5f6368; margin-top:4px; letter-spacing:1px;">SISTEMAS · RETARGET</div>
  <div style="font-size:11px; color:#FF6B35; font-weight:bold; letter-spacing:2px; margin-top:12px;">[TAG] · [CONTEXTO]</div>
</td></tr>
```

### Footer CLIENTE (logo abajo centrado)

```html
<tr><td align="center" style="padding:32px 0 24px 0; border-top:1px solid #e8eaed;">
  [BRÚJULA SVG]
  <div style="font-size:14px; font-weight:bold; color:#FF6B35; letter-spacing:3px; margin-top:8px;">COMPASS</div>
  <div style="font-size:12px; color:#5f6368; margin-top:4px; letter-spacing:1px;">SISTEMAS · RETARGET</div>
  <div style="font-size:12px; color:#5f6368; margin-top:8px;">✉ sistemas@retarget.cl</div>
  <div style="font-size:12px; color:#5f6368;">🌐 retarget.cl</div>
</td></tr>
```

### Auto-generado (siempre al final)

```html
<tr><td align="center" style="padding-top:8px;">
  <div style="font-size:11px; color:#9aa0a6; font-style:italic;">Generado automáticamente por COMPASS · [FECHA]</div>
</td></tr>
```

---

## 📋 Las 5 plantillas oficiales

### 1. [REPORTE] · Avance de proyecto (INTERNO)

**Audiencia:** Mauricio, Leig (interno)  
**Tag:** `[REPORTE] · [Proyecto]`  
**Logo:** Arriba  
**Estructura:**
- Header con logo + tag
- 📊 Avance del proyecto (texto)
- Stats coloridos (completados / pendientes / bloqueados)
- ✅ Completados esta semana (lista códigos)
- ⏳ Pendientes (lista códigos)
- Link Tracking Master
- Auto-generado

### 2. [ALERTA] · REQ entrante (INTERNO)

**Audiencia:** Equipo interno (#sistemas-compass-alerts)  
**Tag:** `🚨 [ALERTA] · REQ ENTRANTE`  
**Logo:** Arriba  
**Estructura:**
- Header con logo + tag rojo
- 🚨 REQ-XXX detectado (texto)
- Bloque rojo con detalles (Cliente / Solicitante / Asunto / Estado / Recibido)
- 📋 Descripción
- 👉 Acción siguiente
- Link Tracking Master
- Auto-generado

### 3. Re: REQ-XXX · Aclarado (CLIENTE)

**Audiencia:** Cliente (CC: Mauricio)  
**Tag:** `[REQ-XXX] · [Proyecto]` (header pequeño)  
**Logo:** Abajo  
**Estructura:**
- Tag pequeño arriba (sin logo)
- ✅ REQ aclarado (saludo)
- Bloque verde con detalles (Cliente / Estado / Deadline)
- 📋 Scope confirmado (lista)
- ✅ Añadido al Tracking Master
- Despedida
- Footer COMPASS grande
- Auto-generado

### 4. [ENTREGA] · Listo para revisión (CLIENTE)

**Audiencia:** Cliente (CC: Mauricio)  
**Tag:** `[ENTREGA] · REQ-XXX`  
**Logo:** Abajo  
**Estructura:**
- Tag pequeño arriba (sin logo)
- 📦 Proyecto X — Lista (saludo)
- Bloque verde (Estado / URL Preview / Deadline)
- ✅ Implementado (lista)
- 👉 Próximo paso
- Despedida
- Footer COMPASS grande
- Auto-generado

### 5. [INCIDENCIA] · Reporte (CLIENTE)

**Audiencia:** Cliente (CC: Mauricio)  
**Tag:** `⚠ [INCIDENCIA] · [Sitio]`  
**Logo:** Abajo  
**Estructura:**
- Tag pequeño arriba (sin logo)
- ⚠ Reporte de incidencia (saludo)
- Bloque rojo (Sitio / Detectado / Resuelto / Estado / Impacto)
- 🔍 Causa
- 🛠 Acciones tomadas (lista)
- 🛡 Prevención
- Despedida
- Footer COMPASS grande
- Auto-generado

---

## Paleta de bloques destacados

| Tipo | Color borde | Background | Uso |
|------|-------------|-----------|-----|
| Info / Stats | `#FF6B35` (naranja) | `#FFF8F3` | Resúmenes, números |
| Éxito / Aclarado | `#34a853` (verde) | `#F0F9F4` | REQ aclarado, entrega lista |
| Alerta / Error | `#ea4335` (rojo) | `#FFF1F0` | Alertas, incidencias |

---

## Reglas críticas

1. **Footer COMPASS obligatorio** en TODO correo
2. **Brújula animada** siempre presente (arriba o abajo)
3. **"Generado automáticamente por COMPASS"** al final, siempre
4. **No alterar la estructura** — adaptar solo contenido
5. **Internos:** logo arriba · **Clientes:** logo abajo

---

*Versión: 1.0 — 2026-05-07*
