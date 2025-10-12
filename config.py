# Configuración del Generador de Proyectos

## Configuración por Defecto

```python
# config.py
DEFAULT_CONFIG = {
    "python_version_min": "3.8",
    "licencia": "MIT",
    "autor": "Desarrollador",
    "email_contacto": "",
    "github_user": "",
    "repositorio_url": "",
    "tipo_proyecto": "Python Library",
    "dependencias_principales": {
        "Python Library": "# Dependencias principales\n# requests>=2.28.0",
        "Python CLI Tool": "# Dependencias principales\nclick>=8.0.0\nrich>=12.0.0",
        "Python Web App (Flask)": "# Dependencias principales\nflask>=2.0.0\nflask-cors>=3.0.0",
        "Python Web App (Django)": "# Dependencias principales\ndjango>=4.0.0\ndjangorestframework>=3.14.0",
        "Python Data Science": "# Dependencias principales\npandas>=1.5.0\nnumpy>=1.21.0\nmatplotlib>=3.5.0",
        "Python ML/AI": "# Dependencias principales\ntorch>=1.12.0\ntensorflow>=2.10.0\nscikit-learn>=1.1.0",
        "Otro": "# Dependencias principales\n# Añadir según necesidades"
    },
    "dependencias_desarrollo": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
    "dependencias_testing": "pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0",
    "dependencias_opcionales": "# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0"
}
```

## Personalización

Puedes personalizar la configuración modificando el archivo `config.py` o pasando parámetros directamente al script.

## Variables de Entorno

```bash
export PROJECT_GENERATOR_AUTHOR="Tu Nombre"
export PROJECT_GENERATOR_EMAIL="tu@email.com"
export PROJECT_GENERATOR_GITHUB="tu_usuario"
export PROJECT_GENERATOR_LICENSE="MIT"
```

## Configuración Avanzada

Para proyectos específicos, puedes crear un archivo `project_config.json`:

```json
{
    "nombre_proyecto": "MiProyecto",
    "descripcion_proyecto": "Descripción del proyecto",
    "tipo_proyecto": "Python Library",
    "autor": "Tu Nombre",
    "email_contacto": "tu@email.com",
    "github_user": "tu_usuario",
    "python_version_min": "3.8",
    "licencia": "MIT",
    "dependencias_custom": [
        "requests>=2.28.0",
        "click>=8.0.0"
    ]
}
```

Y usar el script con:

```bash
python init_project.py --config project_config.json
```
