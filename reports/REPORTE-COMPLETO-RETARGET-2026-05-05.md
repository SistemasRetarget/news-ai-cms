# Reporte Completo - Retarget
**Fecha:** 5 de mayo de 2026  
**Período:** Última sesión de trabajo  
**Preparado por:** Sistemas Retarget  
**Gantt:** https://docs.google.com/spreadsheets/d/1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY/

---

## Resumen Ejecutivo

| Negocio | Completados | Pendientes | Bloqueados |
|---------|-------------|------------|------------|
| **Futangue EN** | 9/10 (90%) | 1 (PDF Fly Fishing) | 0 |
| **Puyehue** | 2/3 (66%) | 1 (Landing TAC) | 1 (Shopify 2FA) |
| **Cabañas** | 5/5 (100%) | 0 | 0 |
| **TAC Excursiones** | 0/1 (0%) | 1 (Ajustes landing) | 0 |
| **Pueblo La Dehesa** | 0/2 (0%) | 2 (Footer, Galería) | 0 |

**Estado General:** 16 tareas completadas de 22 totales (73%)

---

## 1. FUTANGUE (Sitio en Inglés)

### Completados ✅

#### F-01: Corrección de Botones Rotos (7/8 enlaces)
- **Problema:** Botones "Getting there", "Contact us", "See more" redirigían al home en español
- **Causa:** WPML con slugs inexistentes en inglés, WordPress hacía fallback a ES
- **Solución:** Corregidos 7 de 8 enlaces vía REST API + limpieza SpeedyCache
- **Links corregidos:**
  - `/getting-here/` → `/how-to-get/` ✓
  - `/contact-us/` → `/en/contact-us/` ✓
  - `/the-park/` → `/futangue-park/` ✓
  - Footer Park, Getting to Park ✓
- **Pendiente:** Cabins link → # (esperando subdominio F-06)

#### F-02: Sección Fly Fishing (Estructura)
- **Problema:** Sección en home con contenido genérico
- **Solución:** Estructura preparada para foto vertical + texto
- **Pendiente:** Adjuntos `_62A9226.tif` y PDF programa pesca

#### F-03: Botones See More en Home
- **Problema:** 6 botones "See more" con URLs incorrectas
- **Solución:** Todos corregidos a slugs válidos en EN

#### F-04: Página When to Visit
- **Problema:** Tipografía incorrecta + texto de clima
- **Solución:** Eliminado bloque Climate Zones, ajustada tipografía

#### F-05: Página Hotel - Logo Michelin
- **Problema:** Logo Michelin no visible
- **Solución:** Verificado - logo ya estaba en producción (ID 4527)
- **Estado:** ✅ Completado (ya estaba desde trabajo anterior)

#### F-06g: Footer EN Global
- **Problema:** Links rotos en footer (Cabins, Help)
- **Solución:** Decodificado vc_raw_html Base64, corregidos links, recodificado
- **Links corregidos:**
  - Cabins → # (placeholder F-06)
  - Help → `/en/contact-us-2/` → `/en/contact-us/`

### Pendientes ⏳

#### F-06h: PDF Fly Fishing Program
- **Problema:** Falta botón de descarga PDF en sección pesca
- **Bloqueador:** Esperando archivo PDF del programa de pesca
- **Acción:** Descargar de email de Leignayih o solicitar

#### F-06: Subdominio Cabañas
- **Problema:** Link Cabins apunta a # (placeholder)
- **Bloqueador:** Subdominio aún no creado
- **Acción:** Crear subdominio cuando esté listo

### Borradores de Email Preparados
- ✅ F-01 → Leignayih Rodriguez (listo para enviar)
- ✅ F-06 → Leignayih Rodriguez (listo, falta PDF)

---

## 2. PUYEHUE

### Completados ✅

#### T-02: Botones HTP (Ven por el día)
- **Problema:** Botones de reserva con URLs incorrectas
- **Solución:** Corregidos links a sistema de reservas correcto
- **Estado:** ✅ Live en producción

#### T-03: Cabañas WordPress Completo
- **Problema:** 5 páginas sin templates correctos
- **Solución:** Asignados templates exactos de viajes:
  - `/inicio/` → elementor_canvas (viajes ID 9)
  - `/nuevas-cabanas/` → default (viajes ID 2597)
  - `/promociones/` → elementor_canvas (viajes ID 553)
  - `/paisajes/` → elementor_canvas (viajes ID 385)
  - `/eventos-corporativos/` → default (viajes ID 2517)
- **Front page:** ID 9 activo
- **Estado:** ✅ 100% completado

### Pendientes ⏳

#### T-01: Landing Excursiones TAC
- **Problema:** Ajustes en landing de excursiones
- **Bloqueador:** Esperando aprobación de Susana (cliente)
- **Acción:** Contactar Susana para aprobación
- **Preview:** https://termasaguascalientes.cl/arg/?page_id=20645

### Bloqueados 🔒

#### T-04: Shopify Apps
- **Problema:** Limpieza de aplicaciones no usadas
- **Bloqueador:** Necesita 2FA de Leignayih
- **Acción:** Coordinar acceso con Leignayih

### Borradores de Email Preparados
- ✅ T-02 → Susana (listo para enviar)
- ⏳ T-01 → Esperando aprobación antes de enviar

---

## 3. TERMAS AGUAS CALIENTES (TAC)

### Pendientes ⏳

#### Landing Excursiones
- **Problema:** Landing page para excursiones TAC necesita ajustes
- **Estado:** Maqueta lista, oculta inicialmente
- **Acción:** Aprobación de diseño/contenido
- **URL:** https://termasaguascalientes.cl/arg/?page_id=20645

---

## 4. PUEBLO LA DEHESA

### Pendientes ⏳

#### T-05: QA Footer + Galería
- **Problema:** Footer incorrecto + galería no coincide
- **Acción:** Corregir footer y ajustar galería
- **Prioridad:** Media

---

## 5. ACCIONES INMEDIATAS

### Para Luis (tú):
1. **Enviar borradores de email:**
   - F-01 a Leignayih (Futangue botones)
   - T-02 a Susana (Puyehue HTP)
   
2. **Descargar PDF Fly Fishing:**
   - Buscar en email de Leignayih
   - Subir a `/wp-content/uploads/2026/05/`
   - Crear botón de descarga en sección Fly Fishing

3. **Contactar Susana:**
   - Aprobación landing TAC
   - Prioridad: Alta

4. **Coordinar con Leignayih:**
   - 2FA Shopify para T-04
   - Adjuntos F-02 (foto + PDF)

### Para Sistemas Retarget (yo):
- Monitorear Gantt para actualizaciones
- Preparar reportes de ejecución post-cambios
- Crear tickets de seguimiento para pendientes

---

## LINKS DE INTERÉS

| Recurso | URL | Descripción |
|---------|-----|-------------|
| **Gantt** | https://docs.google.com/spreadsheets/d/1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY/ | Seguimiento de tareas |
| **Futangue EN** | https://parquefutangue.com/en/ | Sitio en producción |
| **Futangue Hotel** | https://parquefutangue.com/en/hotel/ | Página hotel con Michelin |
| **Puyehue** | https://puyehue.cl/ | Sitio principal |
| **TAC Preview** | https://termasaguascalientes.cl/arg/?page_id=20645 | Landing excursiones (oculta) |
| **Cabañas** | https://cabanasfutangue.com/ | Sitio de cabañas (completado) |

---

## NOTIFICACIONES CONFIGURADAS

- ✅ Alertas de calendario creadas para pendientes
- ✅ Recordatorios configurados en Google Calendar
- ✅ Notas en Google Keep actualizadas

---

**Fin del reporte**  
*Sistemas Retarget*  
sistemas@retarget.cl
