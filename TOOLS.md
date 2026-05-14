# TOOLS.md — Herramientas disponibles en Claude Code

Referencia de capacidades MCP y plugins activos en el workspace Retarget.  
Consultar antes de improvisar soluciones manuales — muchas de estas cosas se pueden hacer directo.

---

## 🎨 Adobe Creative (plugin activo)

Plugin MCP que conecta con Photoshop API, Lightroom API, Adobe Express, Premiere y Firefly.  
**Requiere llamar `adobe_mandatory_init` antes de cualquier tool Adobe.**

### Imágenes — Photoshop / Lightroom

| Qué hacer | Tool |
|---|---|
| Quitar fondo → PNG transparente | `image_remove_background` |
| Extender foto con IA (outpainting) | `image_generative_expand` ← única gen-AI disponible |
| Crop inteligente con detección de sujeto | `image_crop_and_resize` |
| Crop manual por coordenadas | `image_crop_to_bounds` |
| Auto corrección de tonos | `image_apply_auto_tone` |
| Brillo / contraste | `image_adjust_brightness_and_contrast` |
| Exposición | `image_adjust_exposure` |
| Highlights / sombras | `image_adjust_highlights` / `image_adjust_dark_portions` |
| Temperatura de color | `image_adjust_color_temperature` |
| Saturación / vibrance | `image_adjust_vibrance_and_saturation` |
| HSL (matiz, saturación, luminosidad) | `image_adjust_hsl` |
| Aplicar preset Lightroom | `image_apply_preset` (usar `image_list_presets` primero) |
| Vectorizar imagen a SVG | `image_vectorize` |
| Seleccionar sujeto principal | `image_select_subject` |
| Seleccionar área por prompt | `image_select_by_prompt` |
| Invertir selección/máscara | `image_invert_selection` |
| Rellenar área con color sólido | `image_fill_area` |
| Blur gaussiano | `image_apply_gaussian_blur` |
| Blur de lente (bokeh) | `image_apply_lens_blur` |
| Efecto glitch | `image_apply_glitch_effect` |
| Efecto halftone | `image_apply_halftone` |
| Tinte monocromático | `image_apply_monochromatic_tint` |
| Color overlay | `image_apply_color_overlay` |
| Enderezar automático | `image_auto_straighten` |
| Grain / ruido | `image_add_grain` / `image_add_noise` |
| Preview inline (verificar resultado) | `asset_inline_preview` |
| Mostrar resultado al usuario | `asset_preview_file` |

### Adobe Stock

| Qué hacer | Tool |
|---|---|
| Buscar fotos/videos stock | `asset_search` con `entityScope: "StockAsset"` |
| Licenciar + descargar stock | `asset_license_and_download_stock` |
| Buscar assets en Creative Cloud | `asset_search` con `entityScope: "CCAsset"` |
| Buscar generaciones Firefly | `asset_search` con `entityScope: "GenAIAsset"` |

> ⚠️ Las URLs de thumbnail de Stock son baja resolución. Siempre licenciar antes de usar en edición.

### Adobe Express (diseño / templates)

| Qué hacer | Tool |
|---|---|
| Buscar plantillas (flyers, posts IG, stories, posters) | `search_design` |
| Cambiar color de fondo | `change_background_color` |
| Actualizar texto en diseño | `fill_text` |
| Animar diseño | `animate_design` |
| Crear mood board con assets | `create_firefly_board` |
| Recomendar fuentes | `font_recommend` |

### Video & Audio — Premiere

> ⚠️ Video tools son **asíncronos** — cuando retornan `status: "working"`, esperar widget, NO llamar polling manual.  
> Requieren `assetId` (no URL) — obtener via `asset_add_file` o `asset_finalize_file_upload`.

| Qué hacer | Tool |
|---|---|
| Crear highlight reel automático | `video_create_quick_cut` |
| Redimensionar video | `video_resize` |
| Limpiar audio / enhance speech | `media_enhance_speech` |
| Resumir video/audio | `media_summarize` |

### Documentos — InDesign / Illustrator

| Qué hacer | Tool |
|---|---|
| Convertir PDF a InDesign | `document_convert_pdf` |
| Exportar InDesign a PDF/JPEG/PNG | `document_render_layout` |
| Data merge desde CSV (layout) | `document_merge_data_layout` |
| Exportar Illustrator a PNG/PDF/SVG | `document_render_vector` |
| Data merge desde CSV (vector) | `document_merge_data_vector` |

### Archivos — Upload / Download

- Archivos locales: usar `asset_add_file` (abre file picker)
- Archivos en servidor (`/mnt/...`): upload programático vía `asset_initialize_file_upload` → chunks PUT → `asset_finalize_file_upload`
- URLs públicas: pasar directamente a las tools de imagen

### ❌ Lo que NO está disponible aquí

- Generación de imagen desde texto (text-to-image) — usar Firefly web
- Generative fill por prompt — usar Photoshop / Firefly
- Reemplazo de fondo con prompt de IA
- Eliminación de objetos con IA
- Compositing (pegar persona en otra foto)
- Conversión de formato de video (MOV→MP4, etc.)
- OCR / extracción de texto de imagen
- Upscaling / super-resolución

---

## 🖥️ Browser / Chrome MCP

Control de Chrome para automatización web.

| Capacidad | Notas |
|---|---|
| Navegar URLs | Sólo dominios con permiso en la extensión |
| Leer DOM / texto de página | |
| Ejecutar JavaScript | |
| Tomar screenshots | |
| Hacer clicks, fill forms | Requiere permiso explícito del usuario para acciones sensibles |

> ⚠️ `parquefutangue.com` no tiene permiso en la extensión Chrome — usar WP REST API directo.

---

## 📊 Google Sheets API (service account)

Credenciales en `/Users/spam11/Desktop/RETARGET-WORKSPACE/retarget-mcp-2d37bb49c600.json`

| Capacidad | Notas |
|---|---|
| Leer Gantt | `spreadsheets().values().get()` |
| Actualizar estado de tarea | `batchUpdate` con `USER_ENTERED` |
| Agregar fila nueva | `spreadsheets().values().append()` |

Sheet ID: `1murmG-pdc5GkJ1CYc4_1UISRTcipMxPYv2jiH_-7ZIY`

---

## 🔌 WordPress REST API

Acceso a sitios WP vía cookies de sesión + nonce.

| Sitio | Cookies |
|---|---|
| parquefutangue.com | `/tmp/futangue_cookies2.txt` |
| termasaguascalientes.cl | `/tmp/tac_cookies2.txt` |

Nonce: `GET /wp-admin/admin-ajax.php?action=rest-nonce`  
SpeedyCache purge: `POST admin-post.php?action=speedycache_delete_cache&_wpnonce={nonce}`  
Elementor cache: `DELETE /wp-json/elementor/v1/cache`

---

## ☁️ Google Drive MCP

| Capacidad | Notas |
|---|---|
| Leer archivos | `mcp__d7a6ac9f...` tools |
| Buscar archivos | `search_files` |
| Descargar contenido | `download_file_content` |

---

## 📧 Gmail MCP

| Capacidad | Notas |
|---|---|
| Buscar threads | `search_threads` |
| Leer thread | `get_thread` |
| Crear draft | `create_draft` |

---

## ⚙️ Quality Gate MCP (Activo — servidor local)

Orquestación de proyectos, QA visual, validación y documentación de lecciones.

**Configurado en:** `/Users/spam11/Documents/workspace-mcp-global/servers/quality-gate/`

| Capacidad | Tool | Notas |
|---|---|---|
| Listar proyectos | `list-projects` | Descubre todos los proyectos bajo RETARGET-WORKSPACE |
| Screenshots | `screenshot` | Captura URL con Playwright, salva en evidence store |
| Validar código | `validate` | Typecheck + lint + build (detiene en primer error) |
| Validar visualmente | `visual-diff` | Compara screenshot actual vs reference, tolerance % |
| Establecer referencia | `reference-set` | Archiva imagen como "so debe verse" para un view |
| Buscar lecciones | `lessons-search` | Query KB de patrones aprendidos (síntomas + fixes) |
| Registrar lección | `lessons-log` | Append lección: categoría + síntoma + fix |
| Railway logs | `railway-logs` | Tail de deploy logs para proyecto |
| Esperar deploy | `wait-for-deploy` | Poll URL hasta HTTP 200 (con content_match opcional) |
| Iterar sección | `iterate-section` | FAT: autonomía loop screenshot → diff → fix → commit → push |
| Reporte sesión | `session_report` | Estado actual del proyecto |
| Carga sesión | `session_start` | FAT: carga contract + QA state + lecciones + antipatterns |

**Credenciales:** Variables de entorno WP_PUYEHUE_PASS, WP_TAC_PASS, WP_FUTANGUE_PASS (en workspace)

**Uso típico:**
```bash
# Validar proyecto antes de push
mcp__quality-gate__validate --project puebloladehesa

# Capturar estado visual actual
mcp__quality-gate__screenshot --url https://... --project X --view home

# Comparar contra referencia
mcp__quality-gate__visual-diff --project X --view home --tolerance 2.0

# Buscar si ya resolvimos esto antes
mcp__quality-gate__lessons-search --query "Elementor grid width"

# Autonomía: iterar sobre sección hasta convergencia
mcp__quality-gate__iterate-section --project puebloladehesa --section casas-grid --deploy-url https://... --tolerance 2.0
```

---

*Última actualización: 2026-05-14*
