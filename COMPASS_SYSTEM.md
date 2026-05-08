# COMPASS — Sistema Operativo Integral

**Tu agente para desarrollar sitios perfectos, rápido, con auditoría completa.**

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│            COMPASS CONTEXT LOADER v1.0           │
│        (Carga paralela, óptimo, veloz)          │
└──────────────┬──────────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
   ┌────────┐    ┌─────────┐
   │ LOCAL  │    │ MEMORIA │
   └────────┘    └─────────┘
       │             │
       │ 9 files    │ 7 files
       │             │
       ▼             ▼
   ┌──────────────────────────┐
   │   VALIDAR INTEGRIDAD     │
   │  (paralelo, < 500ms)     │
   └──────────┬───────────────┘
              │
              ▼
       ┌────────────┐
       │ DRIVE MCP  │
       │ 6 protoc.  │
       └────────────┘
              │
              ▼
        ┌──────────┐
        │ LISTO 🎯 │
        └──────────┘
```

---

## 📊 Flujo Diario

```
EMAIL CLIENTE
     │
     ▼
PROTOCOLO: Toma de Requerimientos
(validar URL, descripción, validador)
     │
     ▼
SHEETS: Registrar REQ-XXX
(Gantt — tracking master)
     │
     ▼
EJECUTAR (según protocolo)
├─ WordPress REST API
├─ Modificar landing
├─ Tomar screenshot antes/después
└─ Documentar en Drive
     │
     ▼
PROTOCOLO: Flujo Completo REQ
(solicitar validación → aprobación → cierre)
     │
     ▼
SHEETS: Marcar COMPLETADO
(auditoría + fecha cierre)
     │
     ▼
DRIVE: Guardar evidencia
(REQ-XXX/antes.png + después.png + log)
```

---

## 🚀 Cómo usar

### Iniciar sesión

```bash
/compass
```

**Resultado (< 500ms):**
```
✅ COMPASS v1.0 LISTO

Contexto cargado:
  Local Files:     9/9 ✅
  Memory Files:    7/7 ✅
  Drive Protocols: 6/6 ✅

Tu Gantt actual:
| Ticket | Estado | Prioridad |
|--------|--------|-----------|
| F-06h  | ⏳     | 🔴       |
| T-01   | ⏳     | 🔴       |
| T-04   | 🔴     | 🟡       |

Protocolos disponibles:
• Flujo Completo REQ
• Toma de Requerimientos
• Monitoreo de Correos
• WordPress REST API

¿Qué necesitas?
```

---

## 📚 Qué carga `/compass`

| Tipo | Cantidad | Qué es | Dónde |
|------|----------|--------|-------|
| **Local Files** | 9 | Contexto operativo | `/RETARGET-WORKSPACE/` |
| **Memory** | 7 | Configuración personal | `.claude/projects/.../memory/` |
| **Drive Sheets** | 1 | Tu Gantt (trabajo real) | Google Sheets |
| **Drive Protocolos** | 5 | Flujos aprobados | Google Drive |
| **Total** | **22** | Sistema completo | Paralelo en <500ms |

---

## 🎯 Los 5 Protocolos (Drive)

Cargan automáticamente en compass. Úsalos según necesidad:

### 1. Flujo Completo REQ
**Cuándo:** Nuevo REQ o aclaración desbloqueada  
**Qué hace:** Etapas 1-6 (recepción → ejecución → validación → cierre)  
**Output:** REQ completado, auditoría en Drive

### 2. Toma de Requerimientos
**Cuándo:** Llega nuevo email  
**Qué hace:** 6 reglas críticas + checklist mínimo (URL, descripción, validador, deadline)  
**Output:** REQ aclarado o petición de info faltante

### 3. Monitoreo de Correos
**Cuándo:** Cada 10 minutos (7am-8pm)  
**Qué hace:** Detectar respuestas nuevas, desbloquear REQs, ejecutar aprobaciones  
**Output:** Estado actualizado en Sheets

### 4. WordPress REST API
**Cuándo:** Editar Puyehue, TAC, Futangue  
**Qué hace:** Auth + lectura/actualización Elementor + validación visual  
**Output:** Cambio en vivo, antes/después documentado

### 5. Script REQs
**Cuándo:** Referencia  
**Qué hace:** Estructura de datos para sincronización automática  
**Output:** Integración futura con Google Apps Script

---

## 💾 Auditoría Completa

Cada acción queda registrada en:

| Lugar | Qué se guarda | Acceso |
|-------|---------------|--------|
| **Sheets** | REQ-XXX + estado + fecha cierre | Gantt master (tiempo real) |
| **Drive/REQ-XXX/** | before.png + after.png + log | Evidencia visual |
| **Git** | Commits de cambios | Historial + versioning |
| **Memory** | Lecciones aprendidas | Contexto para próximas sesiones |

---

## 🔑 Diferencia con otros agentes

| Aspecto | Antes | COMPASS |
|--------|-------|---------|
| **Contexto** | Manual, incompleto | Automático, paralelo, 22 fuentes |
| **Velocidad** | Preguntar qué hacer | <500ms, listo para ejecutar |
| **Procedimientos** | En la cabeza | 5 protocolos en Drive, vivos |
| **Auditoría** | Ninguna | Sheets + Drive + Git + Memory |
| **Flujos aprobados** | Ad-hoc | Validados, repetibles, escalables |

---

## 🛠️ Stack

```
Frontend: Next.js, Tailwind, Elementor
Backend: Node.js, Python (scripts)
CMS: WordPress, Payload CMS
Automatización: Google Apps Script
Auditoría: Sheets + Drive + Git
Monitoreo: COMPASS Context Loader
```

---

## 🎓 Próximos pasos

### Fase 1 (Hecha)
✅ Sistema de carga paralela  
✅ Validación de contexto  
✅ Protocolos en Drive  
✅ Auditoría (Sheets + Drive + Git)

### Fase 2 (Próxima)
- [ ] Auto-sincronizar Sheets → Tracking Master
- [ ] Monitoreo de correos automático (cron)
- [ ] Generador de auditoría semanal
- [ ] Dashboard de estado de proyectos

### Fase 3
- [ ] A/B testing automático para landings
- [ ] Optimización de Core Web Vitals (automática)
- [ ] Recomendaciones de mejora (IA)

---

## 📞 Comandos disponibles

```bash
/compass                  # Cargar contexto
/req-parse                # Analizar nuevo email
/wp-connect               # Conectar a WordPress
/site-qa                  # Validación visual
/compass-report          # Generar reporte auditoría
```

---

## 🎖️ Estado Actual

**Versión:** 1.0  
**Status:** PRODUCCIÓN  
**Última actualización:** 2026-05-07  
**Tiempo de carga:** <500ms  
**Disponibilidad:** 24/7  

---

**COMPASS = Tu arquitecto + desarrollador + auditor, funcionando en paralelo.**

*Creado para trabajar rápido, bien y con registro de todo.*
