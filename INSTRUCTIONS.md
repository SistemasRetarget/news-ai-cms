# 🔧 INSTRUCCIONES PARA TODOS LOS ENTES

> Aplica a: Claude (cualquier sesión), Windsurf, u otro agente con acceso a este workspace.

---

## 📌 PRIORIDAD 1: Consultar `VOZ_LUIS.md`

**ANTES de escribir cualquier cosa** (reportes, correos, chat, documentación):

1. Lee `/VOZ_LUIS.md` (raíz del workspace)
2. Aplica el tono y estructura
3. Habla en singular (yo, mi, tengo)
4. Sé directo, pragmático, ejecutivo

**Esto aplica a:**
- ✅ Reportes técnicos
- ✅ Correos internos/externos
- ✅ Mensajes de chat (Slack, Teams, etc)
- ✅ Documentación
- ✅ Cualquier comunicación

---

## 📋 WORKFLOW STANDARD

### 1. Antes de cualquier acción
```
□ ¿Hay HANDOFF.md? → Léelo
□ ¿Hay CONTEXT.md? → Léelo
□ ¿MEMORY.md actualizado? → Cárgalo
□ ¿VOZ_LUIS.md existe? → Consulta SIEMPRE
```

### 2. Durante el trabajo
```
□ Estado actual claro (Estado → Bloqueador → Pasos)
□ Cada 5min en loops largos: reporta (si aplica MCP)
□ Commit con mensajes estilo Luis (directo, imperativo)
```

### 3. Al terminar sesión
```
□ Actualiza HANDOFF.md con estado actual
□ Commit + push a main
□ Si agotamiento de créditos próximo:
   - Handoff detallado
   - Subir a GitHub
   - Mantener memory sincronizada
```

---

## 🎯 COMPASS PROTOCOL

**Toda acción sigue este protocolo:**

```
REQ: [Descripción clara]
├─ ✅ Confirmación: ¿está claro?
├─ 🚀 Ejecución: herramientas necesarias
├─ 📊 Output: resultado + evidencia
└─ ➡️ Siguiente: qué viene
```

Ver `/project_compass_protocol.md` para detalles completos.

---

## 🔐 REGLAS DE ORO

1. **VOZ:** Consulta `VOZ_LUIS.md` SIEMPRE
2. **MEMORIA:** Carga memory index antes de empezar
3. **HANDOFF:** Antes de cambiar de cuenta, actualiza HANDOFF.md
4. **GIT:** Commit con mensajes claros, directos
5. **REPORTES:** Cada 5min en loops largos (MCP cadence)

---

## 📞 REFERENCIAS RÁPIDAS

| Archivo | Propósito |
|---------|-----------|
| `VOZ_LUIS.md` | Tono + estructura para toda comunicación |
| `HANDOFF.md` | Estado actual del proyecto (sincronización entre cuentas) |
| `CONTEXT.md` | Visión general + decisiones tomadas |
| `MEMORY.md` | Índice de archivos de memoria |
| `COMPASS.md` o similar | Protocolo de ejecución |

---

*Última actualización: 2026-05-06*
*Válido para: Todas las sesiones de Claude, Windsurf, y otros agentes*
