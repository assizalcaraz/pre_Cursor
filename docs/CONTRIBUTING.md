# Contributing to Pre-Cursor

¡Gracias por tu interés en contribuir a Pre-Cursor! Este documento te guiará a través del proceso de contribución.

## 🚀 Cómo Contribuir

### 1. Fork y Clone
```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/tu-usuario/pre_Cursor.git
cd pre_Cursor
```

### 2. Configurar Entorno de Desarrollo
```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Instalar pre-commit hooks (opcional pero recomendado)
pre-commit install
```

### 3. Crear una Rama
```bash
git checkout -b feature/tu-nueva-funcionalidad
# o
git checkout -b fix/correccion-de-bug
```

### 4. Hacer Cambios
- Sigue la [Metodología de Desarrollo](METODOLOGIA_DESARROLLO.md)
- Mantén el código limpio y bien documentado
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 5. Ejecutar Tests
```bash
# Ejecutar todos los tests
pytest

# Ejecutar con cobertura
pytest --cov=src --cov=init_project

# Ejecutar linting
black .
flake8 .
mypy .
```

### 6. Commit y Push
```bash
git add .
git commit -m "feat: Agregar nueva funcionalidad X"
git push origin feature/tu-nueva-funcionalidad
```

### 7. Crear Pull Request
- Ve a GitHub y crea un Pull Request
- Describe claramente qué cambios hiciste y por qué
- Asegúrate de que todos los tests pasen

## 📋 Tipos de Contribuciones

### 🐛 Reportar Bugs
- Usa el template de issue para bugs
- Incluye pasos para reproducir el problema
- Especifica tu sistema operativo y versión de Python

### ✨ Sugerir Nuevas Funcionalidades
- Usa el template de issue para feature requests
- Explica el caso de uso y beneficio
- Considera si es algo que otros usuarios necesitarían

### 📚 Mejorar Documentación
- Corregir errores tipográficos
- Mejorar claridad de instrucciones
- Agregar ejemplos adicionales
- Traducir a otros idiomas

### 🔧 Mejorar Código
- Optimizar rendimiento
- Refactorizar código existente
- Agregar nuevos tipos de proyecto
- Mejorar manejo de errores

## 🎯 Tipos de Proyecto Soportados

Actualmente soportamos:
- Python Library
- Python CLI Tool
- Python Web App (Flask/Django/FastAPI)
- Python Data Science
- Python ML/AI
- C++ Project
- Node.js Project
- TD_MCP Project
- Otro (personalizado)

¿Tienes una idea para un nuevo tipo de proyecto? ¡Nos encantaría escucharla!

## 🧪 Testing

### Ejecutar Tests Específicos
```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Tests específicos
pytest tests/test_validator.py::TestProjectValidator::test_validate_project_name_valid
```

### Cobertura de Código
- Mantenemos un mínimo de 80% de cobertura
- Los nuevos tests deben cubrir el código nuevo
- Usa `pytest --cov-report=html` para ver el reporte detallado

## 📝 Estándares de Código

### Formato
- Usamos **Black** para formateo automático
- Línea máxima: 88 caracteres
- Usa **Flake8** para linting

### Tipos
- Usamos **MyPy** para verificación de tipos
- Agrega type hints a funciones nuevas
- Mantén compatibilidad con Python 3.8+

### Commits
- Usa mensajes descriptivos
- Formato: `tipo: descripción breve`
- Tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🚀 Proceso de Release

1. **Desarrollo**: Trabajo en rama `develop`
2. **Testing**: Tests automáticos con GitHub Actions
3. **Review**: Code review por maintainers
4. **Merge**: Merge a `master`
5. **Release**: Tag de versión automático
6. **PyPI**: Publicación automática

## 📞 Contacto

- **Issues**: Usa GitHub Issues para bugs y feature requests
- **Discussions**: Usa GitHub Discussions para preguntas generales
- **Email**: contact@pre-cursor.dev (para temas privados)

## 🙏 Reconocimientos

Todos los contribuidores son reconocidos en:
- README.md (sección Contributors)
- CHANGELOG.md (por release)
- GitHub Contributors page

## 📄 Licencia

Al contribuir, aceptas que tu código será licenciado bajo la [MIT License](LICENSE).

---

**¡Gracias por hacer Pre-Cursor mejor!** 🎉
