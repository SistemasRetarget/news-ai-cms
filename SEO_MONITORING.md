# 🔍 SEO Monitoring para Campañas WordPress

**Objetivo:** Validar automáticamente SEO, velocidad y estructura de páginas de campaña (Futangue, Puyehue, TAC) post-deploy.

---

## 📊 Stack Instalado

| Component | Herramienta | Estado |
|-----------|------------|--------|
| **Velocidad** | Lighthouse CLI | ✅ Instalado |
| **On-Page SEO** | Custom validator script | ✅ Creado |
| **Alertas** | Slack webhook | ⚠️ Necesita setup |
| **Ranking** | Google Search Console API | ⏳ Futuro |

---

## 🚀 Uso Rápido

### 1️⃣ Validar URL manualmente

```bash
# SEO score + meta + schema + headings
python3 scripts/seo-validator.py https://puyehue.cl/hot-sale-25

# CTA analyzer: GA4 tracking + copy quality + strategy
python3 scripts/cta-analyzer.py https://puyehue.cl/hot-sale-25

# Salida JSON (ejemplo)
{
  "score": 85,
  "meta": {
    "title": "HOT SALE 25% - Puyehue",
    "description": "Disfruta de nuestro HOT SALE..."
  },
  "headings": {"h1_count": 1, "h2_count": 3},
  "schema": {"has_json_ld": true},
  "issues": ["✅ Meta title OK", "✅ H1 structure OK"]
}

# CTA Analyzer output
{
  "cta_count": 3,
  "tracking": {"ga4_tracked": 2, "total": 3, "coverage": 66.7},
  "score": 70,
  "issues": ["✅ CTA count OK (3)", "⚠️ Only 2/3 CTAs tracked"],
  "strategy": ["📢 Campaign Page Detected", "🔍 Add GA4 tracking to remaining CTA"]
}
```

### 2️⃣ Reporte completo (Lighthouse + SEO + CTA + Slack)

```bash
# Sin Slack (solo reportes locales)
bash scripts/post-deploy-seo-report.sh https://puyehue.cl/hot-sale-25

# Con Slack (requiere setup abajo)
export SLACK_WEBHOOK_URL="<tu-webhook-url>"
bash scripts/post-deploy-seo-report.sh https://puyehue.cl/hot-sale-25

# Salida incluye:
# - Lighthouse: Performance, Accessibility, SEO, Best Practices
# - SEO Validator: Meta tags, headings, schema, alt text
# - CTA Analyzer: GA4 tracking, copy quality, conversion strategy
```

---

## 🔧 Setup Slack (Necesario para notificaciones)

### Paso 1: Crear webhook en Slack

1. Ve a https://api.slack.com/apps
2. Crea una app nueva (o usa una existente)
3. Activa "Incoming Webhooks"
4. "Add New Webhook to Workspace"
5. Selecciona canal (ej: #compass-seo-reports)
6. Copia el webhook URL que te entrega Slack

### Paso 2: Guardar en env

```bash
# Opción A: En ~/.zshrc o ~/.bashrc
export SLACK_WEBHOOK_URL="<tu-webhook-url>"

# Opción B: En .env del workspace
echo "SLACK_WEBHOOK_URL=<tu-webhook-url>" >> /Users/spam11/Desktop/RETARGET-WORKSPACE/.env

# Opción C: Cloud Secret Manager (Google Cloud)
gcloud secrets create SLACK_WEBHOOK_URL --data-file=- <<< "<tu-webhook-url>"
```

---

## 📈 Métricas que Mide

### Lighthouse (rendimiento)
- ⚡ Performance score
- ♿ Accessibility
- 🔍 SEO
- ✅ Best Practices
- Core Web Vitals (LCP, CLS, FID)

### SEO Validator (on-page)
- ✅ Meta title (max 60 chars)
- ✅ Meta description (max 160 chars)
- ✅ H1 (debe haber exactamente 1)
- ✅ H2+ (estructura jerárquica)
- ✅ Schema.org markup (JSON-LD)
- ✅ Alt text en imágenes (> 80% coverage)

**Score:** 0-100 basado en issues encontrados

### CTA Analyzer (conversión)
- 🎯 CTA detection (buttons, links con class cta/btn/action)
- 📊 GA4 tracking coverage (% de CTAs tracked)
- 📝 Copy quality (largo < 30 chars, action verbs, urgency)
- 🔄 Conversion strategy (detecta campaign pages, sugiere A/B tests)
- 💰 Strategic recommendations (urgency testing, secondary CTAs)

**Tracking patterns validados:**
- `data-event` attributes
- `gtag()` calls en onclick
- `ga-*` CSS classes

**Score:** 0-100 basado en tracking coverage + copy quality

---

## 🔄 Integración en Flujo Post-Deploy

### Para Cloud Run (Google Cloud Build)

Agrega a `cloudbuild.yaml`:

```yaml
- name: 'gcr.io/cloud-builders/gke-deploy'
  args:
    - run
    - --on-deploy-seo-check
  env:
    - 'SLACK_WEBHOOK_URL=${_SLACK_WEBHOOK_URL}'
    - 'DEPLOY_URL=${_DEPLOY_URL}'

# Después del deploy, ejecuta:
- name: 'gcr.io/cloud-builders/kubectl'
  entrypoint: 'bash'
  args:
    - '-c'
    - |
      curl -sS ${_DEPLOY_URL}/health > /dev/null
      bash scripts/post-deploy-seo-report.sh ${_DEPLOY_URL}
```

### Para local (desarrollo)

```bash
# Deploy
git push origin feature/hot-sale-25
# Esperar a que Cloud Build compile...

# Luego, manualmente:
export SLACK_WEBHOOK_URL="..."
bash scripts/post-deploy-seo-report.sh https://tu-url-deployada.run.app
```

---

## 📋 Checklist para Campañas

Antes de publicar una campaña:

- [ ] URL amigable (ej: `/hot-sale-25/` no `/?p=123`)
- [ ] Meta title único y < 60 chars
- [ ] Meta description < 160 chars
- [ ] H1 presente y único
- [ ] Schema.org markup (mínimo Product o Event)
- [ ] Imágenes con alt text
- [ ] Lighthouse Performance > 80
- [ ] Lighthouse SEO > 90
- [ ] Links internos correctos
- [ ] Mobile-friendly
- [ ] **CTAs con GA4 tracking (data-event o gtag)**
- [ ] **CTA copy con action verbs (Comprar, Reservar, etc)**
- [ ] **Urgency language en campaign pages (Ahora, Hoy, Limitado)**

**Script — Validación completa:**
```bash
bash scripts/post-deploy-seo-report.sh https://puyehue.cl/hot-sale-25
# Genera reportes: Lighthouse + SEO Validator + CTA Analyzer
# Si SEO score > 80 + CTA score > 70 + Lighthouse Perf > 75 → ✅ Publicar
# Si alguno < umbral → ⚠️ Revisar issues antes de publicar
```

---

## 🔮 Próximas Mejoras

- [ ] **Google Search Console API** — trending queries, ranking position
- [ ] **Backlink monitor** — detectar nuevos enlaces
- [ ] **Scheduled SEO audit** — cada lunes, auditoría completa
- [ ] **Competitive analysis** — ranking vs competencia
- [ ] **Core Web Vitals tracking** — histórico de scores

---

## 📞 Troubleshooting

### "lighthouse: command not found"
```bash
npm install -g lighthouse
```

### "SLACK_WEBHOOK_URL not set"
```bash
export SLACK_WEBHOOK_URL="<tu-webhook-url>"
```

### "seo-validator.py: Permission denied"
```bash
chmod +x scripts/seo-validator.py
```

### Script lento (Lighthouse tarda)
Lighthouse demora ~1-2 min por URL (toma screenshot, mide métricas).  
Normal. Usa `--quiet` para menos output.

---

*Última actualización: 2026-05-14*  
*Creado por: COMPASS SEO Monitoring*
