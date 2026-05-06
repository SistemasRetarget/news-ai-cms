# Guía de Cambios - Puyehue P-01 a P-03

## P-01: Landing Excursiones TAC - Maqueta Oculta

### Estado
**BLOQUEADO POR CLIENTE** - Esperando aprobación de Susana (cliente)

### Descripción
Maqueta de landing page para excursiones TAC (Termas, Aventura, Cultura) que debe estar oculta inicialmente.

### Cuándo proceder
- Después de que Susana apruebe el diseño/contenido
- Ticket en espera - NO proceder hasta nuevo aviso

---

## P-02: "Ven por el día" - Correcciones Botones (Parcial)

### Estado
Parcialmente completado - faltan ajustes finales

### Cambios pendientes
**Ubicación:** Página "Ven por el día" en sitio Puyehue

1. **Verificar botones de reserva**
   - Confirmar que apuntan al sistema de reservas correcto
   - URLs deben incluir parámetros de idioma si es necesario

2. **Botones de "Más información"**
   - Verificar que enlazan a las excursiones correctas
   - Corregir slugs si es necesario

---

## P-03: Limpieza Apps Shopify

### Descripción
Eliminar aplicaciones no utilizadas en la tienda Shopify de Puyehue para mejorar performance.

### Lista de apps a revisar (verificar cuáles están instaladas)

**Apps comúnmente candidatas a eliminación:**
1. Apps de email marketing no usadas
2. Apps de popups/chat inactivos
3. Apps de analytics duplicadas
4. Apps de shipping/logística no usadas
5. Apps de reviews/social proof no configuradas

### Procedimiento

1. **Acceder a Shopify Admin:**
   - URL: https://admin.shopify.com/store/[nombre-tienda]/apps

2. **Revisar cada app instalada:**
   - ¿Está activa?
   - ¿Se usa actualmente?
   - ¿Tiene costo mensual?

3. **Apps a eliminar (confirmar con equipo):**
   - [ ] App 1: ________________
   - [ ] App 2: ________________
   - [ ] App 3: ________________

4. **Documentar antes de eliminar:**
   - Nombre de la app
   - Función que cumplía
   - Razón de eliminación
   - Fecha de eliminación

---

## Resumen de Prioridades

| Código | Proyecto | Prioridad | Estado | Bloqueador |
|--------|----------|-----------|--------|------------|
| F-03 | Futangue - Botones See More | Media | Pendiente | Acceso WordPress |
| F-04 | Futangue - When to Visit | Media | Pendiente | Acceso WordPress |
| F-05 | Futangue - Hotel Michelin | Media | Pendiente | Acceso WordPress |
| P-01 | Puyehue - Landing TAC | Alta | Bloqueado | Cliente Susana |
| P-02 | Puyehue - Ven por el día | Alta | Parcial | Acceso Shopify |
| P-03 | Puyehue - Limpieza Apps | Baja | Pendiente | Acceso Shopify |

---

## Próximos Pasos

1. **Para F-03, F-04, F-05:**
   - Requiere acceso a wp-admin de Futangue
   - Usar guía detallada en GUIA-CAMBIOS-F03-F05.md

2. **Para P-01:**
   - Contactar a Susana para aprobación
   - Preparar maqueta en staging

3. **Para P-02, P-03:**
   - Requiere acceso a Shopify Admin de Puyehue
   - Hacer lista de apps instaladas

---

**Documento preparado por:** Sistemas Retarget  
**Fecha:** 5 de mayo de 2026  
**Tickets:** RT-RT-202602 y siguientes
