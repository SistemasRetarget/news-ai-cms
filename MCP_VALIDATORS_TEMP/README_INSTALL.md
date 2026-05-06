# Instrucciones de Instalación
## Validadores de Website para MCP

### Archivos Creados

```
MCP_VALIDATORS_TEMP/
├── validators/
│   ├── core_web_vitals.py      # Valida Core Web Vitals
│   ├── google_ads_policies.py  # Valida políticas Google Ads
│   ├── seo_technical.py        # Valida SEO técnico
│   └── mobile_first.py         # Valida Mobile First & Responsive
├── routes/
│   └── website_validation.py   # Endpoints API
└── README_INSTALL.md           # Este archivo
```

---

## Pasos de Instalación

### 1. Copiar archivos al repo MCP

```bash
# Ir al repo MCP
cd /path/to/SistemasRetarget/MCP

# Copiar carpetas
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/validators ./
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/routes ./
```

### 2. Agregar dependencias a requirements.txt

```bash
echo "requests>=2.28.0" >> requirements.txt
echo "beautifulsoup4>=4.11.0" >> requirements.txt
```

O agregar manualmente:
```
requests>=2.28.0
beautifulsoup4>=4.11.0
```

### 3. Registrar el blueprint en app.py (o main.py)

```python
# Agregar al inicio
from routes.website_validation import website_validation_bp

# Agregar antes de app.run()
app.register_blueprint(website_validation_bp)
```

### 4. Commit y Push

```bash
git add .
git commit -m "Agregar validadores Core Web Vitals, Google Ads y SEO técnico"
git push origin main
```

### 5. Cloud Build redeploya automáticamente

Ver en Google Cloud Console:
- Cloud Build → History
- Esperar que termine el build

---

## Uso de la API

### Endpoint: Validación Completa

```bash
POST /api/v1/validate-website
Content-Type: application/json

{
  "url": "https://example.com/landing",
  "strategy": "mobile"
}
```

### Ejemplo con curl:

```bash
curl -X POST \
  https://cmsretargetv1-270024878418.europe-west1.run.app/api/v1/validate-website \
  -H "Content-Type: application/json" \
  -d '{"url": "https://puebloladehesa.cl"}'
```

### Respuesta:

```json
{
  "url": "https://puebladehesa.cl",
  "passed": true,
  "overall_score": 85,
  "core_web_vitals": {
    "overall_score": 92,
    "metrics": {
      "LCP": {"value": 2.1, "status": "good"},
      "INP": {"value": 150, "status": "good"},
      "CLS": {"value": 0.05, "status": "good"}
    },
    "passed": true
  },
  "google_ads_policies": {
    "passed": true,
    "checks": {
      "https": {"passed": true},
      "privacy_policy": {"passed": true},
      "mobile_friendly": {"passed": true}
    }
  },
  "seo_technical": {
    "score": 80,
    "checks": {
      "meta_title": {"passed": true},
      "meta_description": {"passed": true},
      "canonical": {"passed": true}
    },
    "passed": true
  },
  "mobile_first": {
    "passed": true,
    "score": 88,
    "mobile_first_compliant": true,
    "checks": {
      "viewport": {"passed": true},
      "media_queries": {"passed": true},
      "touch_targets": {"passed": true}
    }
  },
  "mobile_first_compliant": true,
  "issues": [],
  "recommendations": ["Agregar Schema.org markup"]
}
```

### Endpoint: Validación Rápida

```bash
GET /api/v1/validate-website/quick?url=https://example.com
```

---

## Variables de Entorno Opcionales

```bash
# Para evitar límites de PageSpeed Insights API
PAGESPEED_API_KEY=tu_api_key_de_google_cloud
```

---

## Integración con el Workflow

Ahora el MCP puede validar automáticamente:

1. **Antes de aprobar un sitio web** → Validar Core Web Vitals + Mobile First
2. **Antes de lanzar campaña Google Ads** → Validar políticas
3. **Antes de entregar al cliente** → Validar SEO técnico + Mobile First Compliance

### Ejemplo de uso en código:

```python
from validators.core_web_vitals import validate_core_web_vitals
from validators.google_ads_policies import validate_google_ads_policies
from validators.mobile_first import validate_mobile_first

# Validar antes de aprobar
cwv = validate_core_web_vitals("https://cliente.com/landing")
ads = validate_google_ads_policies("https://cliente.com/landing")
mobile = validate_mobile_first("https://cliente.com/landing")

if cwv['passed'] and ads['passed'] and mobile['mobile_first_compliant']:
    print("✅ Aprobado para deploy - Cumple estándares Google Mobile First")
else:
    print("❌ Corregir issues antes de deploy")
    if not mobile['mobile_first_compliant']:
        print(f"   Mobile First Score: {mobile['score']}/100")
        print(f"   Issues: {mobile['issues']}")
```

---

## Validaciones Incluidas

### Core Web Vitals
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1
- TTFB < 600ms
- FCP < 1.8s

### Google Ads Policies
- HTTPS obligatorio
- Política de privacidad visible
- Mobile-friendly
- No pop-ups intrusivos
- No contenido engañoso
- Contacto claro

### SEO Técnico
- Meta title (30-60 chars)
- Meta description (120-160 chars)
- Canonical URL
- Estructura H1/H2 correcta
- Alt text en imágenes
- Schema.org markup
- sitemap.xml accesible
- robots.txt accesible

### Mobile First & Responsive Design
- Viewport correctamente configurado (width=device-width, initial-scale=1)
- Media queries mobile-first (min-width, no max-width sin mobile)
- Touch targets >= 48x48px
- Responsive images (srcset, sizes)
- Font sizes legibles (16px base mínimo)
- No horizontal scroll (overflow-x)
- CSS Flexbox/Grid (no floats)
- Inputs con font-size >= 16px (evita zoom iOS)
- Tap targets no overlap

---

## Mobile First Compliance

Un sitio es **Mobile First Compliant** cuando:
- Score >= 80%
- Viewport configurado correctamente
- No usa floats para layout
- Font sizes legibles
- Touch targets adecuados

Esto garantiza cumplimiento con estándares de desarrollo Google para mobile-first.

---

## Soporte

¿Problemas? Revisar:
1. Cloud Build logs en Google Cloud Console
2. Cloud Run logs para errores
3. Verificar que las dependencias estén instaladas
