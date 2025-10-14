# Guía de Inicio Rápido - Pre-Cursor

Esta guía te ayudará a usar Pre-Cursor para generar proyectos nuevos de manera rápida y eficiente.

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd pre_cursor
```

### 2. Verificar Requisitos
```bash
# Verificar Python
python3 --version  # Debe ser 3.8+

# Verificar Git
git --version
```

## 📝 Uso Básico

### Modo Interactivo (Recomendado para principiantes)
```bash
python3 init_project.py
```
Sigue las instrucciones en pantalla para configurar tu proyecto.

### Modo Directo
```bash
python3 init_project.py MiNuevoProyecto
```

### Modo con Configuración
```bash
# Crear plantilla de configuración
python3 init_project.py --create-template "Python Library" -o mi_config.json

# Editar la configuración
nano mi_config.json

# Generar proyecto
python3 init_project.py --config mi_config.json
```

## 🎯 Tipos de Proyecto Disponibles

| Tipo | Descripción | Uso Recomendado |
|------|-------------|-----------------|
| **Python Library** | Librerías Python estándar | APIs, utilidades |
| **Python CLI Tool** | Herramientas de línea de comandos | Scripts, herramientas |
| **Python Web App (Flask)** | Aplicaciones web con Flask | Prototipos rápidos |
| **Python Web App (Django)** | Aplicaciones web con Django | Aplicaciones complejas |
| **Python Web App (FastAPI)** | Aplicaciones web con FastAPI | APIs modernas |
| **Python Data Science** | Proyectos de ciencia de datos | Análisis, ML |
| **Python ML/AI** | Proyectos de machine learning | IA, algoritmos |
| **C++ Project** | Proyectos en C++ | Rendimiento crítico |
| **Node.js Project** | Proyectos en Node.js | JavaScript/TypeScript |
| **TD_MCP Project** | Proyectos MCP para TouchDesigner | Integración TD |
| **Otro** | Configuración personalizada | Casos especiales |

## 📋 Ejemplos Prácticos

### Ejemplo 1: Crear una Librería Python
```bash
python3 init_project.py mi_libreria
# Seleccionar: 1 (Python Library)
# Completar información solicitada
```

### Ejemplo 2: Crear una API con FastAPI
```bash
python3 init_project.py mi_api
# Seleccionar: 5 (Python Web App FastAPI)
# Completar información solicitada
```

### Ejemplo 3: Crear un Proyecto TD_MCP
```bash
python3 init_project.py mi_td_project
# Seleccionar: 10 (TD_MCP Project)
# Completar información solicitada
```

## 🔧 Configuración Avanzada

### Crear Plantilla Personalizada
```bash
# Crear plantilla para FastAPI
python3 init_project.py --create-template "Python Web App (FastAPI)" -o fastapi_template.json

# Editar plantilla
nano fastapi_template.json

# Usar plantilla
python3 init_project.py --config fastapi_template.json
```

### Estructura de Archivo de Configuración
```json
{
    "project_name": "mi_proyecto",
    "description": "Descripción del proyecto",
    "detailed_description": "Descripción detallada",
    "project_type": "Python Library",
    "author": "Tu Nombre",
    "email": "tu@email.com",
    "github_user": "tu_usuario",
    "repository_url": "https://github.com/tu_usuario/mi_proyecto",
    "python_version_min": "3.8",
    "license": "MIT",
    "objective": "Objetivo del proyecto",
    "main_functionality": "Funcionalidad principal",
    "dependencies": {
        "main": ["requests>=2.28.0"],
        "development": ["pytest>=7.0.0", "black>=22.0.0"],
        "testing": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
        "optional": ["numpy>=1.21.0"]
    },
    "features": [
        "Funcionalidad principal",
        "Sistema de logging",
        "Manejo de errores"
    ]
}
```

## 📁 Estructura Generada

Cada proyecto generado incluye:

```
mi_proyecto/
├── README.md                    # Documentación principal
├── BITACORA.md                 # Log de desarrollo
├── roadmap_v1.md               # Plan de desarrollo
├── requirements.txt             # Dependencias
├── METODOLOGIA_DESARROLLO.md   # Metodología establecida
├── CONTEXTO.md                 # Información del proyecto
├── src/                        # Código fuente
│   └── mi_proyecto.py
├── tests/                      # Pruebas
│   └── README.md
├── docs/                       # Documentación
│   └── TUTORIAL.md
├── examples/                   # Ejemplos
└── logs/                       # Logs
```

## 🚀 Próximos Pasos

Después de generar tu proyecto:

1. **Navegar al proyecto**:
   ```bash
   cd mi_proyecto
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Revisar documentación**:
   ```bash
   cat CONTEXTO.md
   cat docs/TUTORIAL.md
   ```

4. **Iniciar desarrollo**:
   ```bash
   # Seguir las instrucciones en TUTORIAL.md
   ```

## 🆘 Solución de Problemas

### Error: "python3: command not found"
```bash
# Instalar Python 3.8+
# macOS con Homebrew:
brew install python@3.8

# Ubuntu/Debian:
sudo apt update
sudo apt install python3.8
```

### Error: "Permission denied"
```bash
# Dar permisos de ejecución
chmod +x init_project.py
```

### Error: "Module not found"
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

## 📞 Soporte

- **Documentación**: Revisa `METODOLOGIA_DESARROLLO.md`
- **Issues**: Crea un issue en el repositorio
- **Ejemplos**: Revisa la carpeta `examples/`

---

**¡Listo para empezar!** 🎉

Sigue esta guía y tendrás tu proyecto generado en minutos.
