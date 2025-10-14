# 🚀 Pre-Cursor: Instalación Súper Fácil

## 🎯 Para Principiantes Absolutos

### ⚡ Instalación en 1 Comando
```bash
curl -fsSL https://raw.githubusercontent.com/assizalcaraz/pre_Cursor/master/install.sh | bash
```

**¡Eso es todo!** El script hace todo automáticamente.

---

## 📱 Instalación Manual (Si Prefieres)

### 1. Abrir Terminal
- **Mac**: `Cmd + Espacio` → "Terminal" → Enter
- **Windows**: `Win + R` → "cmd" → Enter  
- **Linux**: `Ctrl + Alt + T`

### 2. Copiar y Pegar
```bash
git clone https://github.com/assizalcaraz/pre_Cursor.git
cd pre_Cursor
pip3 install -e ".[dev]"
```

### 3. Probar
```bash
pre-cursor --help
```

---

## 🎨 Crear tu Primer Proyecto

### Opción 1: Súper Fácil
```bash
pre-cursor create mi_proyecto
```

### Opción 2: Con Tipo Específico
```bash
# Página web
pre-cursor create mi_pagina --type "Python Web App (FastAPI)"

# Librería Python
pre-cursor create mi_libreria --type "Python Library"

# Ciencia de datos
pre-cursor create mi_analisis --type "Python Data Science"
```

### Opción 3: Modo Interactivo
```bash
pre-cursor create mi_proyecto --interactive
```

---

## 🔍 Verificar que Funcionó

```bash
# Ver tu proyecto
ls -la

# Entrar al proyecto
cd mi_proyecto

# Ver contenido
ls -la

# Leer instrucciones
cat README.md
```

---

## 🆘 Si Algo Sale Mal

### ❌ "command not found"
```bash
python3 cli.py --help
```

### ❌ "Permission denied"
```bash
pip3 install --user -e ".[dev]"
```

### ❌ "No module named"
```bash
pip3 install click rich pyyaml
```

---

## 📚 Más Información

- **Guía súper simple**: `cat GUIA_SUPER_SIMPLE.md`
- **Guía detallada**: `cat GUIA_PASO_A_PASO.md`
- **Guía rápida**: `cat QUICKSTART.md`
- **Ejemplos**: `python3 demo_cli.py`

---

## 🎉 ¡Listo para Programar!

```bash
# Ver tipos disponibles
pre-cursor list-types

# Ver información
pre-cursor info --examples

# Crear plantilla
pre-cursor template --type "Python Library"
```

**¡Disfruta creando proyectos!** 🚀✨
