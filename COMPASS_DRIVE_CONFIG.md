---
name: COMPASS Drive Config
description: Secuencia automática de lectura - Sheets + Drive Protocolos
type: config
---

# COMPASS — Secuencia Automática de Lectura

## 🎯 Orden de carga (cuando activas "modo compass")

### 1. TU TRABAJO REAL (SHEETS)
- **URL:** https://docs.google.com/spreadsheets/d/1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY/edit#gid=854866235
- **Contenido:** Gantt completo (tickets T-xx, F-xx actualizados en tiempo real)
- **Acción:** LEE PRIMERO

### 2. PROTOCOLOS OPERATIVOS (Drive)
Carpeta: COMPASS_System/Protocolos

| # | Protocolo | Documento | File ID | Cuándo leer |
|---|-----------|-----------|---------|------------|
| 1 | Flujo Completo REQ | PROTOCOLO - Flujo Completo REQ | 1YblHjN2FF94h3UPLqyjLZI18qYQNnzKExVxknrKdyrI | Antes de procesar nuevo REQ |
| 2 | Toma de Requerimientos | PROTOCOLO - Toma de Requerimientos | 18pElm2tWwXutQwh_b-YOwwymDtcVgY6g5YuM15obhrc | Al recibir email nuevo |
| 3 | Monitoreo de Correos | PROTOCOLO - Monitoreo de Correos | 1Ce9ye9kNHck8GUHaDZaOZNBnGBakbaxrXuGYngf61aY | Ciclo cada 10 min (horario 7am-8pm) |
| 4 | WordPress REST API | PROTOCOLO - WordPress REST API | 1HgNcKjFQl4-rqpPYegjzPCKUG0apxHmOuOz2bBTjnig | Para editar WordPress |
| 5 | Script REQs | SCRIPT - Sincronizar REQs a Tracking Master | 1huA5LVkU-uekwHRDZDDk6Y-ymz43SyAPeqjQ0qNVZM0 | Referencia para automatización |

### 3. CONTEXTO PERSONAL (memoria)
- VOZ_LUIS.md — Cómo escribir/comunicar
- VOZ_CLAUDE.md — Mi personalidad
- Credenciales (cifradas)

---

## 🔗 Cómo funciona

### Al activar "modo compass":

```
1. Carga SHEETS → lee Gantt actual
2. Muestra resumen de pendientes
3. Carga PROTOCOLOS del Drive → disponibles para referencia
4. Carga contexto personal
5. LISTO — responde como si ya supiera todo
```

### Durante la sesión:

- **Nuevo REQ llega** → abre PROTOCOLO - Toma de Requerimientos
- **Flujo completo** → abre PROTOCOLO - Flujo Completo REQ
- **Editar WordPress** → abre PROTOCOLO - WordPress REST API
- **Duda operativa** → abre el protocolo correspondiente del Drive

---

## 📥 Lectura de Drive (via MCP)

Los protocolos se leen automáticamente usando:

```
mcp__8640bf08-fb09-4c65-bc08-69382bc0a6ab__read_file_content
con fileId para cada documento
```

Esto permite:
- Leer el contenido actual del Drive sin descargar
- Mantener protocolos actualizados en Drive (no en git)
- Cambiar protocolos sin tocar código

---

## 🎛️ Configuración

- **Sheets:** fuente de verdad única (tareas)
- **Drive/Protocolos:** documentación viva (procedimientos)
- **Memory:** contexto personal (voz, credenciales)

Todo "enchufado" a compass para activación automática.

---

*Actualizar Drive cuando cambien procedimientos*  
*Actualizar Sheets cuando cierres tickets o recibas nuevos REQs*
