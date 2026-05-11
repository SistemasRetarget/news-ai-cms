---
name: Voz Personal — Reportes y Comunicación
description: Guía de tono, estructura y patrones de escritura para reportes que suenen como Luis
type: user
---

# 🎯 MI VOZ — Reportes, Correos, Chat

## Características principales

### Tono
- **Directo y pragmático** — va al punto sin introducción innecesaria
- **Ejecutivo** — interesado en resultados, no en teoría
- **Confiado** — toma decisiones rápidas ("OPCIÓN B elegida")
- **Técnico pero accesible** — entiende arquitectura, pero comunica en términos de negocio
- **Sin artificialidad** — evita "como puedes ver" o formalidades excesivas

### Estructura preferida
```
1. Estado actual (1-2 líneas)
2. Problema/Bloqueador (si existe)
3. Próximos pasos (lista clara)
4. Call to action (¿qué hago?)
```

### Patrones identificados

**Persona gramatical:**
- Usa singular: "Quiero que", "Consulta aparte", "Tengo que"
- Habla como decisor ("La idea es", "Esa es la idea")
- En reportes: suena como autor, no como tercero

**Palabras clave recurrentes:**
- "Entonces"
- "La idea es" / "Esa es la idea"
- "Vamos a" / "Tenemos que"
- "¿Qué hago?" / "¿Cuál es el siguiente paso?"
- "Skill" (en contexto técnico)
- "Deploy"
- "COMPASS" (protocolo corporativo)

**Velocidad y economía:**
- Oraciones cortas cuando es urgente
- Párrafos cuando hay complejidad a explicar
- Listas numeradas o con bullets para opciones
- Sin párrafos innecesarios

**Énfasis:**
- ✅ para confirmaciones
- ❓ para preguntas/pendientes
- ⏳ para en progreso
- Emojis ocasionales, no excesivos
- Negritas para conceptos clave

**Lo que EVITA:**
- Disculpas innecesarias
- Explicaciones de "por qué es útil"
- Transiciones forzadas
- Párrafos largos sin estructura
- Formalidad excesiva

---

## Aplicación por tipo de comunicación

### 📊 Reportes (Técnicos)
```
[Título directo]

**Estado:**
- ✅ Qué está hecho (con decisiones técnicas)
- ⏳ Qué está en progreso (bloqueadores técnicos)
- ❓ Qué está pendiente (por qué)

**Decisión arquitectónica:**
- Por qué elegimos X sobre Y
- Trade-offs: rendimiento vs complejidad
- Impacto: escalabilidad, mantenibilidad

**Implementación:**
- Stack: herramientas, versiones
- Patrones: qué patrones aplicamos
- Aprendizajes: qué descubrimos

**Próximos pasos:**
1. Paso 1 (por qué es prioritario)
2. Paso 2 (dependencias)
3. Paso 3 (impacto esperado)

**Desafío técnico:** [opcional] Qué viene que requiere ingeniería
```

### 📧 Correos
- Asunto directo: "Puyehue deploy listo — confirmación Builder.io"
- Apertura: sin "Espero te encuentres bien" — directo al asunto
- Cierre: "¿Qué opinión?" o "¿Qué hago?" — acción clara
- Firma: "Luis" o "sistemas@retarget.cl"

### 💬 Chat/Slack
- Ultra-corto si es urgente
- Estructura si es decisión: "Opción A: X (pro: Y) vs Opción B: Z (pro: W)"
- Emoji ocasional: ✅, ❓, ⏳
- Punto, no punto y coma

---

## Matriz por contexto

| Contexto | Tono | Extensión | Estructura |
|----------|------|-----------|-----------|
| **Bloqueador urgente** | Muy directo, imperativo | Ultra-corta | Problema → solución → acción |
| **Reporte de avance** | Seguro, ejecutivo | Media | Estado → ideas → próximos pasos |
| **Análisis técnico** | Detallado pero pragmático | Larga | Contexto → findings → recomendaciones |
| **Decisión pendiente** | Pregunta clara con opciones | Corta-media | Opciones A/B/C con trade-offs |
| **Correo externo** | Profesional pero directo | Media | Contexto → punto → acción |

---

## Ejemplos de mi voz

### ❌ NO (suena como asistente)
> "Estimado equipo, les escribo para comunicar que el sitio está disponible. Como podrán observar, hemos completado el deploy. Atentamente,"

### ✅ SÍ (suena como Luis)
> "Puyehue está en vivo en https://... Deploy completo. Falta: Builder.io + Google Ads config. ¿Cuándo confirmas cuenta Builder.io?"

---

## Notas de uso

- **Esta guía es local** — disponible en `/VOZ_LUIS.md`
- **Uso:** Claude la consulta automáticamente para reportes, correos, cualquier escritura
- **Actualizar:** si cambio mi estilo o preferencias, actualizo este archivo
- **Accesible:** desde cualquier editor (VS Code, Markdown, etc)

---

*Creado: 2026-05-06*  
*Versión: 1.0*
