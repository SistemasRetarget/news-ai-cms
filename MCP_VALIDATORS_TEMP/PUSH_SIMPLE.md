# Comandos para Push (Copiar y Pegar)

## Opción 1: Script Automático

```bash
# Copia esto y pégalo en terminal:
bash /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/PUSH_COMMANDS.sh
```

## Opción 2: Comandos Manuales

```bash
# Paso 1: Ir al repo MCP
cd /path/to/SistemasRetarget/MCP  # <-- AJUSTA ESTA RUTA

# Paso 2: Cambiar a main
git checkout main

# Paso 3: Copiar archivos
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/validators ./
cp -r /Users/spam11/Desktop/RETARGET-WORKSPACE/MCP_VALIDATORS_TEMP/routes ./

# Paso 4: Agregar dependencias
echo "requests>=2.28.0" >> requirements.txt
echo "beautifulsoup4>=4.11.0" >> requirements.txt

# Paso 5: Verificar
git status

# Paso 6: Commit
git add validators/ routes/ requirements.txt
git commit -m "Agregar validadores Core Web Vitals, Google Ads, SEO y Mobile First"

# Paso 7: PUSH
git push origin main
```

## Paso 8: Esperar Deploy

Después del push, Cloud Build automáticamente:
1. Construye la imagen Docker
2. Sube a Container Registry
3. Deploya a Cloud Run
4. Actualiza el servicio

**Ver progreso:** https://console.cloud.google.com/cloud-build

## Paso 9: Verificar

```bash
# Test endpoint
curl -X POST \
  https://cmsretargetv1-270024878418.europe-west1.run.app/api/v1/validate-website \
  -H "Content-Type: application/json" \
  -d '{"url": "https://puebloladehesa.cl"}'
```

## ¿Problemas?

### Si no tienes el repo clonado:
```bash
git clone https://github.com/SistemasRetarget/MCP.git
cd MCP
# Luego ejecutar pasos 3-7 arriba
```

### Si hay conflictos:
```bash
git pull origin main --rebase
# Resolver conflictos si los hay
# Luego: git push origin main
```

## 📁 Archivos que se agregan

```
validators/
├── core_web_vitals.py      ✅
├── google_ads_policies.py  ✅
├── seo_technical.py        ✅
└── mobile_first.py         ✅

routes/
└── website_validation.py   ✅ (actualizado)

requirements.txt            ✅ (actualizado)
```

**¿Listo para ejecutar?**
