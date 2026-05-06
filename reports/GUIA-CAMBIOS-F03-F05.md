# Guía de Cambios - Futangue F-03 a F-05

## F-03: Botones "See More" en Home y Private Reserve (Inglés)

### Problema
Botones "See more" apuntan a URLs incorrectas que redirigen al home en español.

### Cambios necesarios

#### 1. Home Inglés (/en/)
**Ubicación:** Páginas → Home → Editar con WPBakery (versión inglés)

**Botón 1:** Sección Hotel - "See more"
- **Estado actual:** href="/hotel" (sin /en/, redirige a español)
- **Corrección:** href="/en/hotel"

**Botón 2:** Sección Park - "See more"  
- **Estado actual:** href="/en/park/" (slug inexistente)
- **Corrección:** href="/en/futangue-park/"

**Botón 3:** Sección Excursions - "See more"
- **Estado actual:** href="/en/excursions/" (puede estar OK, verificar)
- **Verificar que apunte a:** /en/excursions-2/ (si es el slug correcto)

**Botón 4:** Sección Gastronomy - "See more"
- **Estado actual:** href="/en/gastronomy/"
- **Verificar que exista esta página en inglés**

**Botón 5:** Sección Cafeteria - "See more"
- **Estado actual:** href="/en/cafeteria/"
- **Verificar que exista esta página en inglés**

**Botón 6:** Sección Getting Here - "See more"
- **Estado actual:** href="/en/getting-here/" (slug inexistente)
- **Corrección:** href="/en/how-to-get/"

#### 2. Private Reserve Inglés (/en/private-reserve/)
**Ubicación:** Páginas → Private Reserve → Editar con WPBakery (versión inglés)

**Botón 1:** "See more" de Conservation
- **Estado actual:** href="/en/conservation/"
- **Verificar:** Si la página existe en inglés o redirige

---

## F-04: Página "When to Visit" - Tipografía y eliminar texto de clima

### Problema
- Tipografía no coincide con diseño
- Texto de clima debe eliminarse

### Cambios necesarios
**Ubicación:** Páginas → When to Visit → Editar con WPBakery

1. **Eliminar sección de texto sobre clima**
   - Buscar y remover el texto sobre condiciones climáticas

2. **Ajustar tipografía**
   - Verificar que use las fuentes correctas del tema
   - Revisar tamaños de headings (h1, h2, h3)

---

## F-05: Página Hotel - Logo Michelin y botón descarga PDF pesca

### Cambios necesarios
**Ubicación:** Páginas → Hotel → Editar con WPBakery

1. **Agregar logo Michelin**
   - Ubicar sección de awards/distinciones
   - Agregar imagen del logo Michelin

2. **Agregar botón de descarga PDF programa de pesca**
   - Crear botón "Download Fly Fishing Program" o similar
   - Enlazar al PDF del programa de pesca (esperando archivo)

---

## Post-cambios: Limpiar caché

Después de cada modificación:
1. **Guardar página** en WPBakery
2. **Actualizar** la página
3. **Limpiar caché SpeedyCache:**
   - En admin: SpeedyCache → Limpiar caché
   - O acceder directamente al archivo del plugin

---

## Verificación final

Para cada cambio, verificar en el sitio en vivo:
```
https://parquefutangue.com/en/
https://parquefutangue.com/en/private-reserve/
```

Hacer clic en cada botón "See more" corregido y confirmar que:
1. Va a la página correcta en inglés
2. No redirige al home en español
3. URL final es la correcta

---

**Documento preparado por:** Sistemas Retarget
**Fecha:** 5 de mayo de 2026
**Ticket:** RT-RT-202602 (F-03), F-04, F-05
