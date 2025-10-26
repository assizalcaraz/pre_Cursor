# Pre-Cursor: Generador de Proyectos Optimizado para Agentes de IA

**Pre-Cursor** es un sistema de scaffolding automatizado que genera proyectos siguiendo una metodología establecida, optimizado para trabajo con agentes de IA en Cursor IDE.

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- Git

### Estructura del Proyecto
```
pre-cursor/
├── README.md              # Documentación principal
├── init_project.py        # Generador principal
├── src/pre_cursor/        # Código fuente
├── templates/             # Plantillas de proyecto
├── docs/                  # Documentación técnica
├── docs/guides/           # Guías de usuario
├── config/                # Archivos de configuración
├── scripts/               # Scripts de desarrollo
├── tests/                 # Pruebas unitarias
└── examples/              # Ejemplos y demos
```

### Instalación y Uso
```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd pre_cursor

# Instalar en modo desarrollo
pip install -e ".[dev]"

# CLI mejorado (recomendado)
pre-cursor create MiNuevoProyecto
pre-cursor create mi-api --type "Python Web App (FastAPI)"
pre-cursor template --type "Python Library"
pre-cursor list-types

# CLI legacy (compatible)
python3 init_project.py MiNuevoProyecto
python3 init_project.py --config mi_config.json
```

## ✨ Características Principales

### 🎯 Generación Automática de Proyectos
- **Sistema de plantillas** completamente funcional con procesamiento híbrido de placeholders
- **11 tipos de proyecto** soportados (Python, C++, Node.js, TD_MCP, etc.)
- **Dependencias reales** y código Python funcional sin placeholders
- **Configuración flexible** con soporte para JSON y YAML

### 🤖 Supervisor Automático de Cursor
- **Detección automática** de problemas en la estructura del proyecto
- **Corrección automática** de archivos fuera de lugar y duplicados
- **Integración con Cursor IDE** para supervisión continua
- **Test Supervisor especializado** con validación LLM para tests
- **Sistema de triggers** para activación externa y monitoreo automático
- **AutoExecutor** para correcciones directas del sistema de archivos
- **Daemon en segundo plano** sin abrir IDE constantemente
- **Feedback loop completo** entre detección y corrección

## 🎯 ¿Qué hace Pre-Cursor?

Pre-Cursor es un **generador de proyectos automatizado** que:

1. **Crea proyectos completos** siguiendo una metodología establecida
2. **Genera documentación automática** (README, BITACORA, tutoriales)
3. **Configura estructura de directorios** optimizada para desarrollo
4. **Supervisa y corrige** problemas automáticamente con Cursor IDE
5. **Valida tests y documentación** usando inteligencia artificial

### ¿Cómo funciona?

```python
from init_project import ProjectGenerator

# Crear generador
generator = ProjectGenerator()

# Generar proyecto completo
generator.generate_project("MiProyecto")
```

---

## 🎯 CLI Mejorado

Pre-Cursor incluye una interfaz de línea de comandos moderna y profesional con las siguientes características:

### ✨ Características del CLI
- **Subcomandos especializados**: `create`, `template`, `generate`, `list-types`, `info`
- **Autocompletado**: Soporte completo para bash/zsh
- **Interfaz Rich**: Tablas, paneles y colores para mejor experiencia
- **Modo interactivo**: Configuración guiada paso a paso
- **Dry-run**: Simulación sin crear archivos
- **Configuración flexible**: Soporte para JSON y YAML

### 🚀 Comandos Principales

#### Gestión del Supervisor
```bash
# Verificar estado del supervisor
pre-cursor supervisor status /path/to/project
pre-cursor supervisor status -p  # Usar directorio actual

# Iniciar supervisión (verificación única)
pre-cursor supervisor start /path/to/project
pre-cursor supervisor start -p  # Usar directorio actual

# Iniciar supervisión continua (daemon)
pre-cursor supervisor start -p --daemon --interval 600

# Configurar supervisor
pre-cursor supervisor config -p --interval 300 --auto-fix true

# Corregir problemas detectados
pre-cursor supervisor fix -p --fix

# Ver logs del supervisor
pre-cursor supervisor logs -p

# Detener supervisión
pre-cursor supervisor stop -p

# Test Supervisor especializado
pre-cursor supervisor test-supervisor -p
pre-cursor supervisor test-supervisor -p --daemon --interval 180

# Validar tests con LLM
pre-cursor supervisor validate-tests -p
pre-cursor supervisor validate-tests -p --cleanup

# Sistema de triggers y monitoreo automático
pre-cursor supervisor trigger-monitor -p --daemon --interval 300
pre-cursor supervisor create-trigger -p
pre-cursor supervisor trigger-status -p

# Integración bidireccional completa
pre-cursor supervisor start-bidirectional -p
pre-cursor supervisor instructions -p
pre-cursor supervisor apply -p
pre-cursor supervisor metrics -p
```

#### Crear Proyectos
```bash
# Crear proyecto básico
pre-cursor create mi-proyecto

# Crear con tipo específico
pre-cursor create mi-api --type "Python Web App (FastAPI)"

# Modo interactivo
pre-cursor create mi-proyecto --interactive

# En ruta específica
pre-cursor create mi-proyecto --path /ruta/personalizada

# Crear proyecto openFrameworks
pre-cursor create-of mi-proyecto-of

# Crear proyecto openFrameworks con addons
pre-cursor create-of mi-proyecto-of -a ofxGui -a ofxOsc

# Modo interactivo para openFrameworks
pre-cursor create-of -i

# Listar addons disponibles
pre-cursor create-of --list-addons

# Especificar ruta de openFrameworks
pre-cursor create-of mi-proyecto-of --of-path /ruta/openframeworks
```

#### Plantillas y Configuración
```bash
# Crear plantilla
pre-cursor template --type "Python Library"

# Crear plantilla YAML
pre-cursor template --type "TD_MCP Project" --format yaml --output mi_config.yaml

# Generar desde configuración
pre-cursor generate mi_config.json

# Simular generación
pre-cursor generate config.yaml --dry-run
```

#### Información y Ayuda
```bash
# Listar tipos disponibles
pre-cursor list-types

# Información del proyecto
pre-cursor info --examples

# Ayuda general
pre-cursor --help

# Ayuda de comando específico
pre-cursor create --help
```

### 🔧 Configurar Autocompletado
```bash
# Activar autocompletado
source completion.sh

# Ahora puedes usar TAB para autocompletar
pre-cursor <TAB>  # Verá: create template generate list-types info
pre-cursor create <TAB>  # Verá opciones del comando create
```

---

## 📁 Estructura del Proyecto

```
pre_cursor/
├── README.md                    # Este archivo
├── BITACORA.md                 # Log de desarrollo
├── METODOLOGIA_DESARROLLO.md   # Metodología establecida
├── init_project.py             # Script principal
├── config.py                   # Configuración
├── pyproject.toml              # Configuración del proyecto
├── requirements-dev.txt        # Dependencias de desarrollo
├── templates/                   # Plantillas de archivos
│   ├── README.md.tpl
│   ├── README_td_mcp.md.tpl    # Plantilla específica TD_MCP
│   ├── BITACORA.md.tpl
│   ├── roadmap_v1.md.tpl
│   ├── requirements.txt.tpl
│   ├── requirements_td_mcp.txt.tpl
│   ├── TUTORIAL.md.tpl
│   ├── modulo_principal.py.tpl
│   ├── modulo_principal_td_mcp.py.tpl
│   ├── config_td_mcp.py.tpl
│   ├── config_td_mcp.json.tpl
│   └── [otras plantillas...]
├── src/                        # Código fuente del generador
│   ├── config_loader.py        # Cargador de configuraciones
│   └── validator.py            # Validador de parámetros
├── tests/                      # Pruebas
│   ├── README.md
│   ├── test_config_loader.py
│   ├── test_init_project.py
│   ├── test_integration.py
│   └── test_validator.py
├── docs/                       # Documentación
├── examples/                   # Ejemplos de configuración
│   ├── config_fastapi.yaml
│   └── config_python_library.json
└── structure/                  # Estructura base (vacío)
```

---

## 🎯 Características Principales

### ✅ Implementado
- **Sistema de Plantillas**: Plantillas personalizables con placeholders
- **Generación Automática**: Script completo de generación de proyectos
- **Inicialización Git**: Configuración automática de repositorio
- **Múltiples Tipos**: Soporte para diferentes tipos de proyecto
- **Documentación**: Sistema completo de documentación
- **Metodología**: Sigue la metodología establecida
- **Validación**: Validación robusta de parámetros de entrada
- **Configuración**: Soporte para archivos de configuración JSON/YAML
- **TD_MCP Integration**: Soporte específico para proyectos TD_MCP
- **openFrameworks Integration**: Integración con el ProjectGenerator oficial de openFrameworks
- **Supervisor Automático**: Detección y corrección automática de problemas
- **Test Supervisor**: Validación y limpieza de tests con LLM
- **Integración Bidireccional**: Sistema completo de supervisión continua
- **Daemon en Background**: Ejecución continua sin intervención del usuario
- **Sistema de Triggers**: Activación externa y monitoreo automático
- **AutoExecutor**: Correcciones directas del sistema de archivos
- **Cursor Agent CLI**: Ejecución de prompts inteligentes
- **Feedback Processor**: Procesamiento automático de resultados

### 🔄 En Desarrollo
- **Tests Automáticos**: Suite de tests para el generador
- **Plantillas Adicionales**: Más tipos de proyecto
- **Configuración Avanzada**: Más opciones de personalización

---

## 🧪 Testing

Seguir las instrucciones en `tests/README.md` para ejecutar las pruebas.

```bash
# Ejecutar tests
python3 -m pytest tests/

# Ejecutar con cobertura
python3 -m pytest tests/ --cov=src/

# Verificar generación
python3 init_project.py ProyectoTest
```

---

## 📚 Documentación

- [Metodología de Desarrollo](docs/METODOLOGIA_DESARROLLO.md)
- [Bitácora del Proyecto](BITACORA.md)
- [Instrucciones de Testing](tests/README.md)
- [Ejemplos de Configuración](examples/)
- [Guías de Usuario](docs/guides/)

---

## 🔧 Tipos de Proyecto Soportados

1. **Python Library**: Librerías Python estándar
2. **Python CLI Tool**: Herramientas de línea de comandos
3. **Python Web App (Flask)**: Aplicaciones web con Flask
4. **Python Web App (Django)**: Aplicaciones web con Django
5. **Python Web App (FastAPI)**: Aplicaciones web con FastAPI
6. **Python Data Science**: Proyectos de ciencia de datos
7. **Python ML/AI**: Proyectos de machine learning e IA
8. **C++ Project**: Proyectos en C++
9. **Node.js Project**: Proyectos en Node.js
10. **TD_MCP Project**: Proyectos MCP para TouchDesigner
11. **openFrameworks Project**: Proyectos multimedia interactivos con C++
12. **Otro**: Configuración personalizada

---

## 🚀 Metodología de Desarrollo Universal

Pre-Cursor implementa una **metodología de desarrollo estandarizada** que puede aplicarse a cualquier proyecto:

### 📋 Principios Fundamentales
1. **Documentación Continua**: BITACORA.md actualizada en tiempo real
2. **Testing Proactivo**: Evaluar tests existentes antes de crear nuevos
3. **Organización Modular**: Estructura clara de directorios
4. **Tutoriales Estructurados**: Formato consistente con fecha, lección y resumen

### 🎯 Beneficios para Desarrolladores
- **Consistencia Garantizada**: Cada proyecto sigue la misma metodología
- **Punto de Entrada Único**: Una sola instrucción para crear proyecto completo
- **Reducción de Ambigüedad**: Información estructurada y predecible
- **Contexto Automático**: Documentación generada automáticamente
- **Escalabilidad**: Estructura preparada para crecimiento

### 🤖 Uso para Agentes de IA
```
"Clona el repositorio pre_cursor y ejecuta 
python3 init_project.py para crear un nuevo proyecto llamado 
'MiNuevaApp' con la descripción 'Una aplicación para 
visualización de datos'."
```

---

## 📚 Documentación

### Estructura de Documentación
- **`docs/`** - Documentación técnica del proyecto
- **`docs/guides/`** - Guías de usuario paso a paso
- **`docs/CURSOR_SUPERVISOR.md`** - Guía completa del supervisor automático
- **`docs/INVESTIGACION_CURSOR_CLI.md`** - Investigación y desarrollo
- **`docs/METODOLOGIA_DESARROLLO.md`** - Metodología establecida

### Guías Disponibles
- **`docs/guides/QUICKSTART.md`** - Inicio rápido y uso básico
- **`docs/guides/GUIA_PASO_A_PASO.md`** - Guía detallada paso a paso

### Archivos de Configuración
- **`config/`** - Archivos de configuración del proyecto
- **`examples/`** - Ejemplos de uso y configuración
- **`scripts/`** - Scripts de instalación y desarrollo

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'WIP: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

**Assiz Alcaraz Baxter**
- Gemini 2.5 revisor, Cursor Pro IDE
- Basado en metodología establecida en proyectos anteriores

---

## 📞 Contacto

Para preguntas o sugerencias, crear un issue en el repositorio.

---

**Fecha de Creación**: 2024-12-19  
**Última Actualización**: 2024-12-19  
**Estado**: Fase 3 Completada - Test Supervisor e Integración Bidireccional Implementada
