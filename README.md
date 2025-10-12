# Pre-Cursor: Generador de Proyectos Optimizado para Agentes de IA

**Pre-Cursor** es un sistema de scaffolding automatizado que genera proyectos siguiendo una metodología establecida, optimizado para trabajo con agentes de IA en Cursor IDE.

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- Git

### Instalación y Uso
```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd pre_cursor

# Modo interactivo
python3 init_project.py

# Modo directo
python3 init_project.py MiNuevoProyecto

# Usar archivo de configuración
python3 init_project.py --config mi_config.json
```

### Uso Básico
```python
from init_project import ProjectGenerator

# Crear generador
generator = ProjectGenerator()

# Generar proyecto
generator.generate_project("MiProyecto")
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

- [Metodología de Desarrollo](METODOLOGIA_DESARROLLO.md)
- [Bitácora del Proyecto](BITACORA.md)
- [Instrucciones de Testing](tests/README.md)
- [Ejemplos de Configuración](examples/)

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
11. **Otro**: Configuración personalizada

---

## 🚀 Uso para Agentes de IA

### Instrucción Simple para Agentes
```
"Clona el repositorio pre_cursor y ejecuta 
python3 init_project.py para crear un nuevo proyecto llamado 
'MiNuevaApp' con la descripción 'Una aplicación para 
visualización de datos'."
```

### Beneficios para Agentes
- **Punto de Entrada Único**: Una sola instrucción para crear proyecto completo
- **Reducción de Ambigüedad**: Información estructurada y predecible
- **Consistencia Garantizada**: Cada proyecto sigue la metodología al 100%
- **Contexto Automático**: Archivo CONTEXTO.md generado automáticamente
- **Soporte TD_MCP**: Generación específica para proyectos TouchDesigner MCP

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

**Sistema de Generación Automática**
- Basado en metodología establecida en proyectos anteriores

---

## 📞 Contacto

Para preguntas o sugerencias, crear un issue en el repositorio.

---

**Fecha de Creación**: 2024-12-19  
**Última Actualización**: 2024-12-19  
**Estado**: Fase 2 Completada - Integración TD_MCP Implementada
