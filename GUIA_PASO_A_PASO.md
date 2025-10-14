# 🚀 Guía Paso a Paso: Crear Proyecto con Pre-Cursor CLI


### 📋 Índice
1. [Verificar Requisitos](#1-verificar-requisitos)
2. [Instalar Pre-Cursor](#2-instalar-pre-cursor)
3. [Verificar Instalación](#3-verificar-instalación)
4. [Crear tu Primer Proyecto](#4-crear-tu-primer-proyecto)
5. [Verificar que Funcionó](#5-verificar-que-funcionó)
6. [Solución de Problemas](#6-solución-de-problemas)

---

## 1. Verificar Requisitos

### ✅ Paso 1.1: Verificar Python
Abre tu terminal y escribe:
```bash
python3 --version
```

**¿Qué deberías ver?**
- Algo como: `Python 3.8.10` o `Python 3.9.5` o superior
- Si ves un error, instala Python desde [python.org](https://python.org)

**❌ Si no funciona:**
```bash
# En macOS con Homebrew:
brew install python@3.8

# En Ubuntu/Debian:
sudo apt update
sudo apt install python3.8

# En Windows: Descarga desde python.org
```

### ✅ Paso 1.2: Verificar Git
```bash
git --version
```

**¿Qué deberías ver?**
- Algo como: `git version 2.34.1`
- Si ves un error, instala Git desde [git-scm.com](https://git-scm.com)

### ✅ Paso 1.3: Verificar pip
```bash
pip3 --version
```

**¿Qué deberías ver?**
- Algo como: `pip 21.3.1 from /usr/lib/python3/dist-packages/pip`
- Si no funciona: `python3 -m ensurepip --upgrade`

---

## 2. Instalar Pre-Cursor

### 📥 Paso 2.1: Clonar el Repositorio
```bash
# Ir a tu directorio de proyectos (o donde quieras)
cd ~/Desktop
# o
cd ~/Documents
# o donde prefieras trabajar

# Clonar Pre-Cursor
git clone https://github.com/assizalcaraz/pre_Cursor.git
```

**¿Qué deberías ver?**
- Mensajes de descarga de archivos
- Al final: `Resolving deltas: 100% (X/X), done.`

### 📦 Paso 2.2: Entrar al Directorio
```bash
cd pre_Cursor
```

**¿Qué deberías ver?**
- Tu prompt cambia a algo como: `usuario@computadora:~/Desktop/pre_Cursor$`

### 🔧 Paso 2.3: Instalar en Modo Desarrollo
```bash
pip3 install -e ".[dev]"
```

**¿Qué deberías ver?**
- Muchos mensajes de instalación de paquetes
- Al final: `Successfully installed pre-cursor-1.0.0`

**❌ Si da error de permisos:**
```bash
pip3 install --user -e ".[dev]"
```

**❌ Si da error de pip:**
```bash
python3 -m pip install -e ".[dev]"
```

---

## 3. Verificar Instalación

### ✅ Paso 3.1: Probar el Comando Principal
```bash
pre-cursor --help
```

**¿Qué deberías ver?**
```
Usage: pre-cursor [OPTIONS] COMMAND [ARGS]...

  🚀 Pre-Cursor: Generador de proyectos optimizado para agentes de IA

Options:
  --version          Show the version and exit.
  -v, --verbose      Activar modo verbose
  -c, --config PATH  Archivo de configuración
  --help             Show this message and exit.

Commands:
  create      🎯 Crear un nuevo proyecto
  generate    ⚡ Generar proyecto desde archivo de configuración
  info        ℹ️ Información sobre Pre-Cursor
  list-types  📋 Listar tipos de proyecto disponibles
  template    📝 Crear plantilla de configuración
```

**❌ Si ves "command not found":**
```bash
# Agregar al PATH (temporal)
export PATH="$HOME/.local/bin:$PATH"

# O usar directamente:
python3 cli.py --help
```

### ✅ Paso 3.2: Ver Tipos de Proyecto Disponibles
```bash
pre-cursor list-types
```

**¿Qué deberías ver?**
- Una tabla bonita con tipos de proyecto y sus descripciones

---

## 4. Crear tu Primer Proyecto

### 🎯 Paso 4.1: Elegir Nombre y Tipo
**Reglas para el nombre:**
- Solo letras minúsculas
- Números están bien
- Guiones bajos (_) están bien
- NO espacios
- NO mayúsculas
- NO caracteres especiales

**Ejemplos BUENOS:**
- `mi_primer_proyecto`
- `mi-api-web`
- `proyecto123`

**Ejemplos MALOS:**
- `Mi Proyecto` (espacios y mayúsculas)
- `mi-proyecto@2024` (caracteres especiales)

### 🚀 Paso 4.2: Crear Proyecto Básico
```bash
pre-cursor create mi_primer_proyecto
```

**¿Qué deberías ver?**
- Mensajes de progreso
- Al final: `🎉 Proyecto 'mi_primer_proyecto' creado exitosamente!`

### 🎨 Paso 4.3: Crear Proyecto con Tipo Específico
```bash
pre-cursor create mi_api --type "Python Web App (FastAPI)"
```

**Tipos disponibles:**
- `Python Library`
- `Python CLI Tool`
- `Python Web App (Flask)`
- `Python Web App (Django)`
- `Python Web App (FastAPI)`
- `Python Data Science`
- `Python ML/AI`
- `C++ Project`
- `Node.js Project`
- `TD_MCP Project`
- `Otro`

### 💬 Paso 4.4: Modo Interactivo (Opcional)
```bash
pre-cursor create mi_proyecto_interactivo --interactive
```

**¿Qué pasará?**
- Te preguntará paso a paso qué tipo de proyecto quieres
- Te pedirá descripción, autor, email, etc.
- Te mostrará un resumen antes de crear

---

## 5. Verificar que Funcionó

### ✅ Paso 5.1: Ver el Proyecto Creado
```bash
ls -la
```

**¿Qué deberías ver?**
- Tu nuevo proyecto listado como directorio
- Ejemplo: `drwxr-xr-x 10 usuario usuario 4096 Dec 19 10:30 mi_primer_proyecto`

### ✅ Paso 5.2: Entrar al Proyecto
```bash
cd mi_primer_proyecto
```

### ✅ Paso 5.3: Ver la Estructura
```bash
ls -la
```

**¿Qué deberías ver?**
```
README.md
requirements.txt
src/
tests/
docs/
examples/
```

### ✅ Paso 5.4: Leer el README
```bash
cat README.md
```

**¿Qué deberías ver?**
- Documentación completa del proyecto
- Instrucciones de instalación
- Ejemplos de uso

### ✅ Paso 5.5: Verificar que es un Repositorio Git
```bash
git status
```

**¿Qué deberías ver?**
- Información del repositorio Git
- Archivos listados como "untracked files"

---

## 6. Solución de Problemas

### ❌ Problema: "command not found: pre-cursor"

**Solución 1:**
```bash
export PATH="$HOME/.local/bin:$PATH"
pre-cursor --help
```

**Solución 2:**
```bash
python3 cli.py --help
```

**Solución 3:**
```bash
# Reinstalar
pip3 uninstall pre-cursor
pip3 install -e ".[dev]"
```

### ❌ Problema: "Permission denied"

**Solución:**
```bash
pip3 install --user -e ".[dev]"
```

### ❌ Problema: "No module named 'click'"

**Solución:**
```bash
pip3 install click rich pyyaml
```

### ❌ Problema: "Git not found"

**Solución:**
```bash
# En macOS:
brew install git

# En Ubuntu/Debian:
sudo apt install git

# En Windows: Descargar desde git-scm.com
```

### ❌ Problema: Proyecto no se crea

**Verificar:**
1. ¿El nombre tiene espacios o caracteres especiales?
2. ¿Ya existe un directorio con ese nombre?
3. ¿Tienes permisos de escritura en el directorio actual?

**Solución:**
```bash
# Usar nombre simple
pre-cursor create test123

# O crear en directorio específico
pre-cursor create mi_proyecto --path ~/Desktop
```

### ❌ Problema: Error de Python

**Verificar versión:**
```bash
python3 --version
```

**Si es menor a 3.8:**
```bash
# Instalar Python 3.8+
# En macOS:
brew install python@3.8

# En Ubuntu/Debian:
sudo apt install python3.8
```

---

## 🎉 ¡Felicitaciones!

Si llegaste hasta aquí, ya tienes Pre-Cursor funcionando. Ahora puedes:

### 🚀 Comandos Útiles Adicionales

```bash
# Ver información del proyecto
pre-cursor info --examples

# Crear plantilla de configuración
pre-cursor template --type "Python Library" --output mi_config.json

# Generar proyecto desde configuración
pre-cursor generate mi_config.json

# Simular creación (sin crear archivos)
pre-cursor create test --dry-run
```

### 📚 Próximos Pasos

1. **Explorar tu proyecto**: `cd mi_primer_proyecto && ls -la`
2. **Leer documentación**: `cat README.md`
3. **Instalar dependencias**: `pip install -r requirements.txt`
4. **Ejecutar tests**: `python -m pytest tests/`

### 🆘 Si Necesitas Ayuda

- **Documentación completa**: `cat QUICKSTART.md`
- **Ejemplos**: `python3 demo_cli.py`
- **Issues**: [GitHub Issues](https://github.com/assizalcaraz/pre_Cursor/issues)

---

**¡Disfruta creando proyectos con Pre-Cursor!** 🚀
