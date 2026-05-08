---
name: compass
displayName: COMPASS Context Loader v1.0
trigger: /compass
description: Carga contexto completo en paralelo (Sheets + Drive + Memoria) óptimo y veloz. Valida TODO antes de responder. Listo para trabajar.
category: operations
---

# COMPASS Context Loader v1.0

**Comando:** `/compass` o "modo compass" o "activa compass"

## ¿Qué carga?

### 1. ARCHIVOS LOCALES (9)
- HANDOFF.md — tu trabajo actual
- METHODOLOGY.md — flujos de trabajo
- TOOLS.md — stack y herramientas
- VOZ_LUIS.md — cómo comunicas
- VOZ_CLAUDE.md — mi personalidad
- SECURITY.md — auditoría
- LESSONS_LEARNED.md — lo que funciona
- COMPASS_CONTEXT.md — índice maestro
- COMPASS_DRIVE_CONFIG.md — secuencia Drive

### 2. MEMORIA (7)
- project_gantt_current.md — tu Gantt actual
- project_compass_protocol.md — protocolo COMPASS
- drive_protocolos_operativos.md — referencias Drive
- feedback_compass_ux.md — UX rules
- claude_personality.md — personalidad
- MEMORY.md — índice completo

### 3. DRIVE PROTOCOLOS (6 vía MCP)
- Sheets: Gantt (tu trabajo real)
- Flujo Completo REQ
- Toma de Requerimientos
- Monitoreo de Correos
- WordPress REST API
- Script REQs

## Flujo de carga

```
/compass
  ↓
Carga en paralelo (< 500ms):
  ├─ 9 archivos locales
  ├─ 7 archivos memoria
  └─ 6 documentos Drive
  ↓
Valida integridad:
  ├─ Todos existen
  ├─ Memoria sincronizada
  └─ Drive accesible
  ↓
Reporta status:
  ✅ LISTO PARA TRABAJAR
  (o ❌ CONTEXTO INCOMPLETO)
```

## Respuesta esperada

```
✅ COMPASS v1.0 LISTO

Contexto cargado:
  Local Files:     9/9 ✅
  Memory Files:    7/7 ✅
  Drive Protocols: 6/6 ✅

Tu Gantt actual:
[tabla de pendientes]

Protocolos disponibles:
• Flujo Completo REQ
• Toma de Requerimientos
• Monitoreo de Correos
• WordPress REST API

¿Qué necesitas?
```

## Reglas

- NO mencionar archivos leídos
- NO listar carga — mostrar resumen
- Responder como si ya supiera todo
- Adoptar VOZ_CLAUDE desde inicio
- NO proceder si contexto incompleto
- Listar bloqueadores si existen
