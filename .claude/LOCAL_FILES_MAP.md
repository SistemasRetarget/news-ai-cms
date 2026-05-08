---
name: Local Files Map
description: Mapeo de archivos grandes que NO están en GitHub (se leen localmente)
---

# LOCAL FILES MAP — Archivos Grandes (Locales)

Estos archivos son demasiado grandes para GitHub (>100MB). Están en tu máquina pero NO en el repositorio remoto.

## 📍 Ubicación

```
/Users/spam11/Desktop/RETARGET-WORKSPACE/
├─ PROJECTS/
│  └─ otros/
│     └─ claude-local-app/
│        └─ dist-electron/           ← AQUÍ (local, no en GitHub)
│           ├─ *.dmg (150MB+)
│           ├─ *.zip (143MB+)
│           └─ *.app/ (211MB+)
└─ .gitignore                         ← Excluye dist-electron/
```

## 🔍 Cuándo leerlos

Si necesitas acceder a `dist-electron`:

```javascript
// En compass-loader.js o scripts locales
const localPath = '/Users/spam11/Desktop/RETARGET-WORKSPACE/PROJECTS/otros/claude-local-app/dist-electron/';

// Leer archivos localmente
fs.readdirSync(localPath)
// No intentar acceder vía GitHub API
```

## 📋 Archivo Binario

```bash
# Si necesitas sincronizar estos archivos:
# OPCIÓN 1: Usar Git LFS (Large File Storage)
git lfs track "PROJECTS/otros/claude-local-app/dist-electron/*.dmg"
git lfs track "PROJECTS/otros/claude-local-app/dist-electron/*.zip"

# OPCIÓN 2: Excluir permanentemente (recomendado para binarios)
# Ya configurado en .gitignore
```

## 🛠️ Para COMPASS

Cuando `compass-loader.js` ejecute:

```javascript
const localFiles = {
  distElectron: '/Users/spam11/Desktop/RETARGET-WORKSPACE/PROJECTS/otros/claude-local-app/dist-electron/',
  status: 'available_locally_only'
};
```

## ✅ Verificación

```bash
# Ver qué está excluido
cat .gitignore | grep dist-electron

# Verificar archivos locales existen
ls -lah /Users/spam11/Desktop/RETARGET-WORKSPACE/PROJECTS/otros/claude-local-app/dist-electron/
```

## 🚀 Cuando clones en otra máquina

```bash
# Los archivos dist-electron NO descargará
git clone https://github.com/SistemasRetarget/news-ai-cms.git

# Necesitarás traer dist-electron manualmente
# (o usar rsync/Drive/external storage)
```

---

**TL;DR:** GitHub solo tiene código. Los binarios grandes están en tu máquina, mapeados aquí.
