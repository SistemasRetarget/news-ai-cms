# METODOLOGÍA — Retarget Agency

**Stack:** Next.js 15 + Payload CMS 3 + PostgreSQL + Google Cloud Run  
**Aplica a:** Todos los proyectos de rediseño/clonación de sitios para clientes

---

## FLUJO ESTÁNDAR: De REQ a Producción

```
1. RECONNAISSANCE  → Analizar sitio original (estructura, colores, tipografía, componentes)
2. CONTENT         → Extraer contenido real (textos, imágenes, datos)
3. BUILD           → Crear componentes React/Next.js según specs
4. STYLE           → Aplicar colores, tipografía, espaciado exactos (Tailwind)
5. QA              → Validar: visual diff < 2%, Lighthouse > 90, responsive
6. DEPLOY          → Cloud Build → Cloud Run (ver REGISTRY.json para URLs por proyecto)
7. DOC             → Actualizar LESSONS_LEARNED.md + HANDOFF.md
```

---

## CRITERIOS DE ACEPTACIÓN (todos los proyectos)

```
✅ Visual diff < 2% vs sitio original
✅ Lighthouse Performance > 90
✅ Lighthouse SEO > 95
✅ Core Web Vitals: LCP < 2.5s, CLS < 0.1
✅ Responsive: mobile / tablet / desktop
✅ Sin imágenes placeholder (Unsplash u otros CDN externos)
✅ Sin secrets hardcodeados
```

---

## SUBAGENTES (patrón multi-agente)

Para proyectos complejos, dividir en agentes paralelos:

| Agente | Responsabilidad | Output |
|---|---|---|
| Reconnaissance | Analizar sitio original | specs de estructura, colores, tipografía |
| Layout Builder | Componentes React | `.tsx` por sección |
| Content Loader | Contenido real | JSON + imágenes del cliente |
| Style Engineer | Estilos exactos | Tailwind config + CSS vars |
| QA Validator | Validación | visual diff + Lighthouse report |
| Deployment | Deploy a Cloud Run | URL producción verificada |
| Doc Reporter | Documentar | LESSONS_LEARNED + HANDOFF actualizados |

---

## REGLAS CRÍTICAS

1. **Nunca presentar URLs sin verificar** — siempre `curl -I [url]` antes de entregar
2. **LOCAL === QA** antes de deployar a PROD
3. **PROD puede ser WordPress** — no comparar con LOCAL/QA (stacks diferentes)
4. **`npm ci`** en QA/PROD, nunca `npm install`
5. **Variables de entorno** — verificar en Cloud Run antes de deploy
6. **Imágenes** — usar Next.js `<Image>` con `sizes` + WebP + lazy loading

---

## ERROR HANDLING

```
Si algo falla en cualquier fase:
1. Registrar error en LESSONS_LEARNED.md
2. Revertir a versión anterior (git)
3. Proponer fix con evidencia
4. Esperar aprobación antes de continuar
```

```
Si visual diff > 2%:
1. Identificar diferencias exactas
2. Lista de ajustes priorizada
3. Iterar hasta pasar umbral
```

---

## DOCUMENTACIÓN OBLIGATORIA (por fase)

- Qué se hizo
- Qué falló y cómo se fijó
- Lección aprendida (→ LESSONS_LEARNED.md)
- Estado actual (→ HANDOFF.md al cerrar sesión)

---

## REGISTRO DE PROYECTOS

Ver `REGISTRY.json` — fuente de verdad de clientes, URLs, stacks y estados.

| Cliente | Stack | Estado |
|---|---|---|
| Pueblo La Dehesa | Next.js 15 + Payload CMS 3 + PostgreSQL | En desarrollo |
| Puyehue | Next.js 15 + Payload CMS 3 | En desarrollo |
| News AI CMS | Next.js + Payload CMS | En desarrollo |
| CRM Comunitario | Next.js | Activo |

---

*Actualizar cuando cambie el flujo o se aprendan nuevas lecciones.*
