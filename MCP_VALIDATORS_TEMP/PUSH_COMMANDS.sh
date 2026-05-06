#!/bin/bash
# Comandos para hacer push de los nuevos validadores al MCP
# Copiar y pegar en terminal

echo "🚀 Haciendo push de validadores al MCP..."

# 1. Ir al repo MCP (ajústalo según dónde lo tengas)
cd ~/projects/SistemasRetarget/MCP || cd /path/to/SistemasRetarget/MCP

# 2. Verificar que estamos en main
git checkout main

# 3. Copiar archivos de validadores
echo "📁 Copiando validadores..."
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/validators ./
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/routes ./

# 4. Actualizar requirements.txt
echo "📝 Agregando dependencias..."
if ! grep -q "requests" requirements.txt; then
    echo "requests>=2.28.0" >> requirements.txt
fi
if ! grep -q "beautifulsoup4" requirements.txt; then
    echo "beautifulsoup4>=4.11.0" >> requirements.txt
fi

# 5. Verificar cambios
echo "🔍 Verificando cambios..."
git status

# 6. Agregar al stage
git add validators/
git add routes/
git add requirements.txt

# 7. Commit
git commit -m "feat: Agregar validadores de sitios web

- Core Web Vitals (LCP, INP, CLS, TTFB, FCP)
- Google Ads Policies (HTTPS, privacidad, mobile-friendly)
- SEO Técnico (meta tags, schema, sitemap, robots)
- Mobile First (viewport, media queries, touch targets, responsive)

Integración completa para validación de sitios web de clientes
antes de deploy y campañas Google Ads."

# 8. Push
git push origin main

echo "✅ Push completado!"
echo ""
echo "⏳ Cloud Build redeployará automáticamente."
echo "📊 Ver estado en: https://console.cloud.google.com/cloud-build"
echo ""
echo "🌐 URL del servicio: https://cmsretargetv1-270024878418.europe-west1.run.app"
