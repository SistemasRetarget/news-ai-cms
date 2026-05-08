# TOOLS & SKILLS — Retarget Agency

Referencia rápida de qué usar y cuándo.

---

## SKILLS (invocar con `/nombre`)

| Skill | Cuándo usar |
|---|---|
| `/compass` | Activar modo COMPASS — carga todo el contexto automáticamente |
| `/req-parse` | Analizar email de cliente y extraer REQ sin preguntas adicionales |
| `/clone-section` | Replicar sección/página de sitio original a Next.js + Tailwind con visual diff automático |
| `/site-parity` | Verificar paridad entre sitio original (PROD) y replicación (QA) antes de trabajar |
| `/site-qa` | QA visual completo — screenshots lado a lado, reporte de páginas que pasan/fallan |
| `/wp-connect` | Conectar a cualquier WordPress para investigar o editar (REST API o Playwright) |
| `/wp-maintain` | Ejecutar cambio en WordPress con validación visual antes/después |
| `/elementor-edit` | Editar páginas WordPress con Elementor via Playwright (cuando REST API está bloqueada) |

---

## MCP TOOLS (disponibles en Claude)

### Navegación & Browser
| Tool | Cuándo usar |
|---|---|
| `Claude in Chrome` | Controlar browser para tareas que requieren autenticación visual, Elementor, admin WP |
| `Control Chrome` | Navegación headless, ejecutar JS, inspeccionar páginas |

### Google Workspace
| Tool | Cuándo usar |
|---|---|
| `Gmail MCP` | Leer/procesar emails de clientes, detectar REQs entrantes |
| `Calendar MCP` | Agendar, revisar disponibilidad, crear eventos |
| `Google Drive MCP` | Leer/escribir documentos, compartir archivos con clientes |

### Productividad
| Tool | Cuándo usar |
|---|---|
| `Apple Notes` | Notas rápidas, borradores internos |
| `Word (Anthropic)` | Crear/editar documentos .docx para clientes |

### Archivos
| Tool | Cuándo usar |
|---|---|
| `Read/Write/Edit` | Editar código, archivos de configuración, markdown |
| `Bash` | Comandos: git, npm, gcloud, curl, deploy |
| `PDF Viewer` | Revisar briefings, propuestas o contratos en PDF |

---

## CUÁNDO USAR QUÉ

### REQ de cliente llega por email
```
1. /req-parse → extraer qué quiere el cliente
2. Evaluar: ¿es WordPress o Next.js?
3. WordPress → /wp-maintain o /elementor-edit
4. Next.js → desarrollar + /site-qa para validar
```

### Proyecto nuevo de replicación
```
1. /site-parity → ver estado actual
2. /clone-section → replicar sección a sección
3. /site-qa → validación final
4. Deploy → gcloud run deploy (ver REGISTRY.json)
```

### Edición WordPress urgente
```
1. /wp-connect → conectar al sitio
2. REST API disponible → editar via API
3. REST API bloqueada → /elementor-edit via Playwright
4. Validar visualmente con screenshot antes/después
```

---

## REGLAS DE USO

- **Nunca presentar URLs sin verificar** — `curl -I [url]` primero
- **Elementor** — siempre usar `/elementor-edit`, la REST API está bloqueada en esos sitios
- **Deploy** — revisar `REGISTRY.json` para la URL y región correcta de cada cliente
- **Credenciales** — en `credentials_encrypted.md` (memory). Pedir passphrase antes de descifrar.

---

*Agregar nuevas skills o tools cuando se incorporen al stack.*
