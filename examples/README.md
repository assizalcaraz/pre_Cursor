# Ejemplos de Configuración - Pre-Cursor

Esta carpeta contiene ejemplos de archivos de configuración para diferentes tipos de proyectos que puedes generar con Pre-Cursor.

## 📁 Archivos Disponibles

### `ejemplo_python_library.json`
Configuración para crear una librería Python estándar con dependencias para procesamiento de datos.

**Uso:**
```bash
python3 init_project.py --config examples/ejemplo_python_library.json
```

**Características:**
- Pandas, NumPy, Matplotlib, Seaborn
- Tests con pytest
- Formateo con Black y Flake8
- Documentación automática

### `ejemplo_fastapi.json`
Configuración para crear una API REST moderna con FastAPI.

**Uso:**
```bash
python3 init_project.py --config examples/ejemplo_fastapi.json
```

**Características:**
- FastAPI con documentación automática
- Autenticación JWT
- SQLAlchemy + Alembic
- Tests asíncronos
- Validación con Pydantic

### `ejemplo_td_mcp.json`
Configuración para crear un proyecto TD_MCP (TouchDesigner MCP).

**Uso:**
```bash
python3 init_project.py --config examples/ejemplo_td_mcp.json
```

**Características:**
- Servidor MCP para TouchDesigner
- WebSocket para comunicación en tiempo real
- Integración con TouchEngine SDK
- Manejo de archivos TOX

## 🚀 Cómo Usar los Ejemplos

### Método 1: Usar Configuración Directa
```bash
# Copiar y editar un ejemplo
cp examples/ejemplo_python_library.json mi_config.json
nano mi_config.json  # Editar con tus datos

# Generar proyecto
python3 init_project.py --config mi_config.json
```

### Método 2: Crear Plantilla Personalizada
```bash
# Crear plantilla basada en un tipo existente
python3 init_project.py --create-template "Python Library" -o mi_plantilla.json

# Editar la plantilla
nano mi_plantilla.json

# Usar la plantilla
python3 init_project.py --config mi_plantilla.json
```

### Método 3: Ejecutar Ejemplos Automáticamente
```bash
# Ejecutar script de ejemplos
python3 ejemplos_uso.py
```

## 📝 Personalizar Configuraciones

### Campos Principales
- `project_name`: Nombre del proyecto (sin espacios)
- `description`: Descripción breve
- `detailed_description`: Descripción detallada
- `project_type`: Tipo de proyecto (ver tipos disponibles)
- `author`: Tu nombre
- `email`: Tu email
- `github_user`: Tu usuario de GitHub

### Dependencias
```json
"dependencies": {
    "main": ["paquete>=version"],           // Dependencias principales
    "development": ["paquete>=version"],   // Desarrollo
    "testing": ["paquete>=version"],       // Testing
    "optional": ["paquete>=version"]       // Opcionales
}
```

### Características
```json
"features": [
    "Característica 1",
    "Característica 2",
    "Característica 3"
]
```

## 🔧 Tipos de Proyecto Disponibles

1. **Python Library** - Librerías Python estándar
2. **Python CLI Tool** - Herramientas de línea de comandos
3. **Python Web App (Flask)** - Aplicaciones web con Flask
4. **Python Web App (Django)** - Aplicaciones web con Django
5. **Python Web App (FastAPI)** - Aplicaciones web con FastAPI
6. **Python Data Science** - Proyectos de ciencia de datos
7. **Python ML/AI** - Proyectos de machine learning
8. **C++ Project** - Proyectos en C++
9. **Node.js Project** - Proyectos en Node.js
10. **TD_MCP Project** - Proyectos MCP para TouchDesigner
11. **Otro** - Configuración personalizada

## 💡 Consejos

- **Nombres de proyecto**: Usa solo letras minúsculas, números y guiones bajos
- **Versiones de Python**: Especifica la versión mínima requerida
- **Dependencias**: Incluye siempre las versiones mínimas
- **Licencias**: MIT, Apache-2.0, GPL-3.0 son opciones comunes
- **Keywords**: Separa con comas, usa minúsculas

## 🆘 Solución de Problemas

### Error: "Invalid project type"
Verifica que el tipo de proyecto esté en la lista de tipos válidos.

### Error: "Missing required field"
Asegúrate de que todos los campos requeridos estén presentes.

### Error: "Invalid email format"
Usa un formato de email válido (ejemplo@dominio.com).

## 📚 Más Información

- [Guía de Inicio Rápido](../QUICKSTART.md)
- [README Principal](../README.md)
- [Metodología de Desarrollo](../METODOLOGIA_DESARROLLO.md)

---

**¡Experimenta y crea tus propias configuraciones!** 🎉
