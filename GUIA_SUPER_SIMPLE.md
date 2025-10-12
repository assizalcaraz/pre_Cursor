# 🚀 Pre-Cursor: Guía Súper Simple
## (Para principiantes absolutos)

### 🎯 ¿Qué es Pre-Cursor?
Pre-Cursor es una herramienta que crea proyectos de programación completos automáticamente.
Es como tener un asistente que prepara todo para que puedas empezar a programar inmediatamente.

---

## 📱 Instalación en 3 Pasos

### 1️⃣ Abrir Terminal
- **Mac**: Presiona `Cmd + Espacio`, escribe "Terminal", presiona Enter
- **Windows**: Presiona `Win + R`, escribe "cmd", presiona Enter
- **Linux**: Presiona `Ctrl + Alt + T`

### 2️⃣ Copiar y Pegar Estos Comandos
```bash
# Paso 1: Descargar Pre-Cursor
git clone https://github.com/assizalcaraz/pre_Cursor.git
cd pre_Cursor

# Paso 2: Instalar
pip3 install -e ".[dev]"

# Paso 3: Probar
pre-cursor --help
```

### 3️⃣ ¡Listo!
Si ves un mensaje de ayuda, ¡funcionó! 🎉

---

## 🎨 Crear tu Primer Proyecto

### Opción A: Súper Fácil (Recomendado)
```bash
pre-cursor create mi_proyecto
```
**¡Eso es todo!** Tu proyecto estará listo en segundos.

### Opción B: Con Tipo Específico
```bash
# Para una página web
pre-cursor create mi_pagina --type "Python Web App (FastAPI)"

# Para una librería Python
pre-cursor create mi_libreria --type "Python Library"

# Para ciencia de datos
pre-cursor create mi_analisis --type "Python Data Science"
```

### Opción C: Modo Interactivo (Paso a Paso)
```bash
pre-cursor create mi_proyecto --interactive
```
Te hará preguntas y te guiará paso a paso.

---

## 🔍 Verificar que Funcionó

### 1. Ver tu Proyecto
```bash
ls -la
```
Deberías ver tu proyecto listado.

### 2. Entrar al Proyecto
```bash
cd mi_proyecto
```

### 3. Ver qué Contiene
```bash
ls -la
```
Deberías ver archivos como `README.md`, `requirements.txt`, etc.

### 4. Leer las Instrucciones
```bash
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

### ❌ "Git not found"
- **Mac**: `brew install git`
- **Ubuntu**: `sudo apt install git`
- **Windows**: Descargar desde [git-scm.com](https://git-scm.com)

---

## 🎉 ¡Ya Sabes Usar Pre-Cursor!

### Comandos Útiles
```bash
# Ver tipos de proyecto disponibles
pre-cursor list-types

# Ver información del proyecto
pre-cursor info

# Crear plantilla de configuración
pre-cursor template --type "Python Library"
```

### Próximos Pasos
1. **Explorar**: `cd mi_proyecto && ls -la`
2. **Leer**: `cat README.md`
3. **Instalar**: `pip install -r requirements.txt`
4. **Programar**: ¡Empieza a codear!

---

## 📚 Más Información

- **Guía completa**: `cat GUIA_PASO_A_PASO.md`
- **Ejemplos**: `python3 demo_cli.py`
- **Documentación**: `cat QUICKSTART.md`

**¡Disfruta programando!** 🚀✨
