# Generador de Proyectos Optimizado para Agentes de IA

**Fecha**: 2024-12-19  
**Objetivo**: Crear un sistema de scaffolding automatizado que genere proyectos siguiendo la metodología establecida, optimizado para trabajo con agentes de IA en Cursor IDE

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
python init_project.py

# Modo directo
python init_project.py MiNuevoProyecto

# Script de inicio rápido
./iniciar.sh MiNuevoProyecto
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
├── iniciar.sh                  # Script de inicio rápido
├── config.py                   # Configuración
├── ejemplos_basicos.py         # Ejemplos de uso
├── templates/                   # Plantillas de archivos
│   ├── README.md.tpl
│   ├── BITACORA.md.tpl
│   ├── roadmap_v1.md.tpl
│   ├── requirements.txt.tpl
│   ├── TUTORIAL.md.tpl
│   └── modulo_principal.py.tpl
├── tests/                      # Pruebas
│   └── README.md
├── docs/                       # Documentación
├── examples/                   # Ejemplos
└── structure/                  # Estructura base
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

### 🔄 En Desarrollo
- **Tests Automáticos**: Suite de tests para el generador
- **Configuración Avanzada**: Archivos de configuración JSON
- **Plantillas Adicionales**: Más tipos de proyecto
- **Validación**: Validación de parámetros de entrada

---

## 🧪 Testing

Seguir las instrucciones en `tests/README.md` para ejecutar las pruebas.

```bash
# Ejecutar ejemplos
python ejemplos_basicos.py

# Verificar generación
python init_project.py ProyectoTest
```

---

## 📚 Documentación

- [Metodología de Desarrollo](METODOLOGIA_DESARROLLO.md)
- [Bitácora del Proyecto](BITACORA.md)
- [Instrucciones de Testing](tests/README.md)
- [Ejemplos de Uso](ejemplos_basicos.py)

---

## 🔧 Tipos de Proyecto Soportados

1. **Python Library**: Librerías Python estándar
2. **Python CLI Tool**: Herramientas de línea de comandos
3. **Python Web App (Flask)**: Aplicaciones web con Flask
4. **Python Web App (Django)**: Aplicaciones web con Django
5. **Python Data Science**: Proyectos de ciencia de datos
6. **Python ML/AI**: Proyectos de machine learning e IA
7. **Otro**: Configuración personalizada

---

## 🚀 Uso para Agentes de IA

### Instrucción Simple para Agentes
```
"Clona el repositorio project-template-generator y ejecuta 
python init_project.py para crear un nuevo proyecto llamado 
'MiNuevaApp' con la descripción 'Una aplicación para 
visualización de datos'."
```

### Beneficios para Agentes
- **Punto de Entrada Único**: Una sola instrucción para crear proyecto completo
- **Reducción de Ambigüedad**: Información estructurada y predecible
- **Consistencia Garantizada**: Cada proyecto sigue la metodología al 100%
- **Contexto Automático**: Archivo CONTEXTO.md generado automáticamente

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
**Estado**: Fase 1 Completada - Estructura Base Implementada
