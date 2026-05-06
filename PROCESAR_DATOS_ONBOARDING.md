# Procesar Datos del Onboarding
## Organizar Respuestas del Equipo

**Fecha:** 2026-04-28  
**Objetivo:** Procesar datos recopilados y crear configuración personalizada para cada agente  
**Tiempo estimado:** 2-3 horas

---

## PASO 1: Recopilar Respuestas

### Dónde están los datos:
```
□ Formulario Google Forms (si lo usaste)
□ Email con respuestas
□ Documento compartido
□ Spreadsheet
□ Otro: _______________
```

**¿Dónde están los datos? Comparte el link o archivo.**

---

## PASO 2: Crear Spreadsheet de Consolidación

### Estructura recomendada:

```
SPREADSHEET: "MCP_Onboarding_Respuestas"

Columnas:
├─ Nombre
├─ Email
├─ Rol
├─ IA Tool
├─ Información más importante
├─ Tarea que toma más tiempo
├─ Datos que faltan
├─ Cómo IA podría ayudar
├─ Proyectos principales
├─ Clientes principales
├─ Herramientas que usa
├─ Personas que reportan/supervisan
├─ Notas adicionales
└─ Prioridad de implementación
```

---

## PASO 3: PLANTILLA PARA PROCESAR DATOS

### Usuario: MAURICIO (CEO)

```
INFORMACIÓN RECOPILADA:
═══════════════════════════════════════════════════════════════

Rol: CEO
Email: mauricio@retarget.cl
IA Tool: ChatGPT
Prioridad: ALTA

NECESIDADES PRINCIPALES:
├─ Información más importante: _______________
├─ Tarea que toma más tiempo: _______________
├─ Datos que faltan: _______________
└─ Cómo IA podría ayudar: _______________

CONTEXTO PERSONALIZADO:
├─ Clientes principales: _______________
├─ Proyectos activos: _______________
├─ KPIs que monitorea: _______________
└─ Equipo directo: _______________

INTEGRACIONES NECESARIAS:
├─ Google Workspace: _______________
├─ Herramientas externas: _______________
└─ APIs: _______________

CONFIGURACIÓN DEL AGENTE:
├─ Nombre: "Agente Estratega"
├─ Rol: CEO
├─ Contexto: [Resumen de necesidades]
├─ Integraciones: [Lista de APIs]
├─ Frecuencia de actualización: Diaria
├─ Alertas críticas: [Qué alertar]
└─ Reportes automáticos: [Qué reportar]

PRÓXIMOS PASOS:
├─ Crear usuario en MCP
├─ Configurar integraciones
├─ Testear contexto
└─ Capacitar a usuario
```

---

## PASO 4: CREAR USUARIOS EN MCP

Una vez procesados los datos, crear usuarios en Cloud SQL:

```bash
# Conectarse a Cloud SQL
gcloud sql connect retarget-mcp-db --user=rails

# Insertar usuarios (reemplaza con datos reales)
INSERT INTO users (email, name, role, ai_tool, is_ai_user, active, created_at, updated_at) VALUES
('mauricio@retarget.cl', 'Mauricio', 0, 2, true, true, NOW(), NOW()),
('barbana@retarget.cl', 'Barbana', 1, 1, true, true, NOW(), NOW()),
('luis@retarget.cl', 'Luis', 2, 0, true, true, NOW(), NOW()),
('daniel@retarget.cl', 'Daniel', 6, 1, true, true, NOW(), NOW()),
('alejandra@retarget.cl', 'Alejandra', 3, 0, true, true, NOW(), NOW()),
('leig@retarget.cl', 'Leig', 2, 1, true, true, NOW(), NOW()),
('andrea@retarget.cl', 'Andrea', 4, 1, true, true, NOW(), NOW()),
('cota@retarget.cl', 'Cota', 7, 0, true, true, NOW(), NOW());

# Verificar
SELECT * FROM users;

# Salir
\q
```

---

## PASO 5: CREAR CONFIGURACIÓN PERSONALIZADA

Para cada usuario, crear documento con:

### Documento: AGENTE_MAURICIO_CEO.md

```markdown
# Agente Estratega — Mauricio (CEO)

## Información del Usuario
- Email: mauricio@retarget.cl
- Rol: CEO
- IA Tool: ChatGPT
- User ID: 1

## Necesidades Principales
1. [Necesidad 1]
2. [Necesidad 2]
3. [Necesidad 3]

## Contexto Personalizado
- Clientes principales: [Lista]
- Proyectos activos: [Lista]
- KPIs: [Lista]
- Equipo directo: [Lista]

## Integraciones
- Google Workspace: Gmail, Calendar, Chat
- Herramientas externas: [Lista]
- APIs: [Lista]

## Configuración del Agente
- Nombre: Agente Estratega
- Descripción: Asistente estratégico para CEO
- Contexto: [Resumen de necesidades]
- Frecuencia: Diaria
- Alertas: [Qué alertar]
- Reportes: [Qué reportar]

## Ejemplos de Uso
1. "¿Cuál es el estado de mis clientes hoy?"
2. "¿Hay algún problema crítico?"
3. "¿Cuál es mi proyección de ingresos?"

## Métricas de Éxito
- Adopción: ¿Lo usa diariamente?
- Utilidad: ¿Toma decisiones basadas en contexto?
- Impacto: ¿Mejora su productividad?
```

---

## PASO 6: CREAR TABLA DE CONSOLIDACIÓN

### Resumen Ejecutivo

```
CONSOLIDACIÓN DE DATOS ONBOARDING
═══════════════════════════════════════════════════════════════

USUARIO          | ROL       | IA TOOL | PRIORIDAD | STATUS
─────────────────┼───────────┼─────────┼───────────┼─────────
Mauricio         | CEO       | ChatGPT | ALTA      | ✅
Barbana          | COO       | Gemini  | ALTA      | ✅
Luis             | Dev       | Claude  | ALTA      | ✅
Daniel           | SEO       | Gemini  | MEDIA     | ✅
Alejandra        | Diseño    | Claude  | MEDIA     | ✅
Leig             | CM        | ?       | MEDIA     | ✅
Andrea           | Media     | ?       | MEDIA     | ✅
Cota             | Journalist| ?       | BAJA      | ✅

TOTAL USUARIOS: 8
USUARIOS ACTIVOS: 8
ADOPCIÓN ESPERADA: 100%

NECESIDADES MÁS COMUNES:
1. Información en tiempo real (6/8 usuarios)
2. Automatización de tareas (7/8 usuarios)
3. Análisis de datos (5/8 usuarios)
4. Reportes automáticos (6/8 usuarios)
5. Alertas de problemas (5/8 usuarios)

INTEGRACIONES MÁS SOLICITADAS:
1. Google Workspace (8/8 usuarios)
2. Google Analytics (3/8 usuarios)
3. Meta Ads (2/8 usuarios)
4. GitHub (1/8 usuarios)
5. Figma (1/8 usuarios)

PRÓXIMOS PASOS:
├─ Crear usuarios en MCP (HECHO)
├─ Configurar integraciones Google Workspace
├─ Crear agentes personalizados
├─ Testear con usuarios piloto
├─ Capacitar al equipo
└─ Monitoreo semanal
```

---

## PASO 7: CREAR AGENTES PERSONALIZADOS

Para cada usuario, crear archivo de configuración:

### Archivo: config/agentes/mauricio.yml

```yaml
# Agente Estratega - Mauricio (CEO)
agent:
  name: "Agente Estratega"
  user_id: 1
  email: "mauricio@retarget.cl"
  role: "ceo"
  ai_tool: "chatgpt"

context:
  refresh_frequency: "daily"
  data_sources:
    - type: "google_workspace"
      services:
        - gmail
        - calendar
        - chat
    - type: "internal_api"
      endpoints:
        - /api/v1/clients
        - /api/v1/projects
        - /api/v1/metrics

personalizations:
  greeting: "Buenos días Mauricio, aquí está tu resumen estratégico"
  focus_areas:
    - client_health
    - revenue_metrics
    - team_performance
    - strategic_decisions
  
  alerts:
    - type: "critical"
      condition: "client_at_risk"
      action: "notify_immediately"
    - type: "warning"
      condition: "project_delay"
      action: "notify_daily"
    - type: "info"
      condition: "new_opportunity"
      action: "include_in_summary"

reports:
  daily_summary:
    enabled: true
    time: "08:00"
    format: "email"
    content:
      - client_status
      - revenue_forecast
      - team_metrics
      - decisions_pending
  
  weekly_report:
    enabled: true
    time: "monday_09:00"
    format: "dashboard"
    content:
      - weekly_performance
      - roi_analysis
      - strategic_recommendations

integrations:
  gmail:
    enabled: true
    read_emails: true
    extract_context: true
  
  calendar:
    enabled: true
    read_events: true
    extract_context: true
  
  chat:
    enabled: true
    read_messages: true
    extract_context: true
```

---

## PASO 8: CREAR PROMPTS PERSONALIZADOS

Para cada agente, crear prompts específicos:

### Archivo: prompts/mauricio.md

```markdown
# Prompts Personalizados - Mauricio (CEO)

## Contexto del Usuario
- Rol: CEO de Retarget
- Responsabilidades: Estrategia, clientes, equipo
- Herramienta IA: ChatGPT
- Frecuencia de uso: Diaria

## Prompts Sugeridos

### 1. Resumen Diario
"Basándote en mi contexto de CEO, dame un resumen ejecutivo de:
- Estado de clientes (activos, en riesgo, nuevos)
- Métricas de ingresos
- Problemas críticos que necesito resolver
- Decisiones pendientes
Formato: Bullet points, máximo 5 minutos de lectura"

### 2. Análisis de Cliente
"Analiza el estado del cliente [NOMBRE]:
- Rentabilidad
- Satisfacción
- Riesgos
- Oportunidades de crecimiento
- Recomendaciones"

### 3. Proyecciones
"¿Cuál es mi proyección de ingresos para los próximos 3 meses?
- Por cliente
- Por vertical de negocio
- Escenarios (optimista, realista, pesimista)"

### 4. Decisiones Estratégicas
"Necesito tomar una decisión sobre [TEMA].
Basándote en datos:
- Pros y contras
- Impacto esperado
- Recomendación
- Riesgos"

### 5. Alertas Críticas
"¿Hay algo crítico que deba saber ahora?
- Clientes en riesgo
- Proyectos en peligro
- Oportunidades urgentes
- Problemas del equipo"
```

---

## PASO 9: TESTEAR CON USUARIOS PILOTO

### Seleccionar 2-3 usuarios piloto

```
PILOTOS RECOMENDADOS:
├─ Mauricio (CEO) — Impacto máximo
├─ Luis (Dev) — Feedback técnico
└─ Barbana (COO) — Coordinación
```

### Plan de Testing

```
SEMANA 1: Testing Intensivo
├─ Día 1-2: Capacitación
├─ Día 3-5: Uso diario
├─ Día 6-7: Feedback y ajustes

SEMANA 2: Validación
├─ Monitoreo de adopción
├─ Recolección de feedback
├─ Ajustes basados en uso real
└─ Preparación para rollout general

SEMANA 3: Rollout General
├─ Capacitar al resto del equipo
├─ Monitoreo diario
├─ Soporte activo
└─ Iteraciones rápidas
```

---

## PASO 10: CREAR DOCUMENTO FINAL

### Documento: AGENTES_CONFIGURACION_FINAL.md

```markdown
# Configuración Final de Agentes MCP
## Retarget — Sistema de Agentes Claude

### Resumen Ejecutivo
- Total de usuarios: 8
- Usuarios activos: 8
- Adopción esperada: 100%
- Timeline: 3 semanas

### Agentes Configurados

#### 1. Agente Estratega (Mauricio - CEO)
- Status: ✅ Configurado
- Prioridad: ALTA
- Integraciones: Google Workspace
- Frecuencia: Diaria
- Reportes: Daily summary, Weekly report

#### 2. Agente Orchestrator (Barbana - COO)
- Status: ✅ Configurado
- Prioridad: ALTA
- Integraciones: Google Workspace, Chat
- Frecuencia: Diaria
- Reportes: Task status, Blocker alerts

#### 3. Agente Builder (Luis - Dev)
- Status: ✅ Configurado
- Prioridad: ALTA
- Integraciones: Google Workspace, GitHub
- Frecuencia: Por tarea
- Reportes: Task context, Code review

#### 4. Agente Optimizer (Daniel - SEO)
- Status: ✅ Configurado
- Prioridad: MEDIA
- Integraciones: Google Workspace, Google Analytics
- Frecuencia: Diaria
- Reportes: SEO metrics, Opportunities

#### 5. Agente Visual (Alejandra - Diseño)
- Status: ✅ Configurado
- Prioridad: MEDIA
- Integraciones: Google Workspace, Figma
- Frecuencia: Por proyecto
- Reportes: Design feedback, Brand consistency

#### 6. Agente Social (Leig - CM)
- Status: ✅ Configurado
- Prioridad: MEDIA
- Integraciones: Google Workspace, Social APIs
- Frecuencia: Diaria
- Reportes: Engagement metrics, Sentiment analysis

#### 7. Agente Media (Andrea - Media Buyer)
- Status: ✅ Configurado
- Prioridad: MEDIA
- Integraciones: Google Workspace, Meta Ads, Google Ads
- Frecuencia: Diaria
- Reportes: Campaign performance, ROAS analysis

#### 8. Agente Editor (Cota - Journalist)
- Status: ✅ Configurado
- Prioridad: BAJA
- Integraciones: Google Workspace, Analytics
- Frecuencia: Por artículo
- Reportes: Content performance, SEO optimization

### Próximos Pasos
1. Crear usuarios en MCP ✅
2. Configurar integraciones Google Workspace
3. Testear con usuarios piloto
4. Capacitar al equipo
5. Monitoreo semanal
6. Iteraciones basadas en feedback
```

---

## CHECKLIST: PROCESAR DATOS

```
RECOPILACIÓN:
□ Obtener respuestas del formulario
□ Consolidar en spreadsheet
□ Verificar que todos respondieron
□ Identificar datos faltantes

PROCESAMIENTO:
□ Crear tabla de consolidación
□ Identificar necesidades comunes
□ Identificar integraciones necesarias
□ Priorizar usuarios

CONFIGURACIÓN:
□ Crear usuarios en MCP
□ Crear archivos de configuración
□ Crear prompts personalizados
□ Crear documentación

TESTING:
□ Seleccionar usuarios piloto
□ Capacitar pilotos
□ Monitorear uso
□ Recolectar feedback

ROLLOUT:
□ Ajustar basado en feedback
□ Capacitar al resto del equipo
□ Monitoreo diario
□ Soporte activo
```

---

## PRÓXIMOS PASOS INMEDIATOS

1. **Comparte los datos del formulario**
   - Link a Google Forms
   - Spreadsheet
   - Email con respuestas
   - Otro formato

2. **Yo procesaré los datos y crearé:**
   - Tabla de consolidación
   - Configuración de agentes
   - Prompts personalizados
   - Documentación

3. **Luego:**
   - Crear usuarios en MCP
   - Testear con pilotos
   - Capacitar al equipo
   - Monitoreo semanal

---

**¿Dónde están los datos del formulario? Comparte el link o archivo.**
