"""
Sistema de Configuración para el Generador de Proyectos

Este módulo maneja la carga y validación de archivos de configuración
JSON/YAML para automatizar completamente la creación de proyectos.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Cargador de configuraciones desde archivos JSON/YAML."""
    
    def __init__(self):
        self.supported_formats = ['.json', '.yaml', '.yml']
        self.default_config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Obtener configuración por defecto."""
        return {
            "project_name": "",
            "description": "",
            "detailed_description": "",
            "project_type": "Python Library",
            "author": "Desarrollador",
            "email": "",
            "github_user": "",
            "repository_url": "",
            "python_version_min": "3.8",
            "license": "MIT",
            "objective": "",
            "main_functionality": "",
            "dependencies": {
                "main": [],
                "development": [],
                "testing": [],
                "optional": []
            },
            "features": [],
            "custom_templates": {},
            "git_init": True,
            "create_context": True,
            "verbose": False
        }
    
    def load_config(self, config_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Cargar configuración desde archivo.
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Dict con la configuración cargada
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado o hay errores de parsing
        """
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
        
        if config_path.suffix not in self.supported_formats:
            raise ValueError(
                f"Formato no soportado: {config_path.suffix}. "
                f"Formatos soportados: {', '.join(self.supported_formats)}"
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix == '.json':
                    config_data = json.load(f)
                else:  # .yaml o .yml
                    config_data = yaml.safe_load(f)
            
            logger.info(f"Configuración cargada desde: {config_path}")
            return self._merge_with_defaults(config_data)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parseando JSON: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parseando YAML: {e}")
        except Exception as e:
            raise ValueError(f"Error cargando configuración: {e}")
    
    def _merge_with_defaults(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combinar configuración cargada con valores por defecto.
        
        Args:
            config_data: Configuración cargada del archivo
            
        Returns:
            Dict con configuración combinada
        """
        merged_config = self.default_config.copy()
        
        # Merge recursivo para diccionarios anidados
        def deep_merge(default: Dict, override: Dict) -> Dict:
            for key, value in override.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    default[key] = deep_merge(default[key], value)
                else:
                    default[key] = value
            return default
        
        merged_config = deep_merge(merged_config, config_data)
        
        # Validar campos requeridos
        self._validate_config(merged_config)
        
        return merged_config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validar configuración cargada.
        
        Args:
            config: Configuración a validar
            
        Raises:
            ValueError: Si la configuración es inválida
        """
        required_fields = ["project_name", "description"]
        
        for field in required_fields:
            if not config.get(field):
                raise ValueError(f"Campo requerido faltante: {field}")
        
        # Validar tipo de proyecto
        valid_types = [
            "Python Library", "Python CLI Tool", "Python Web App (Flask)",
            "Python Web App (Django)", "Python Web App (FastAPI)",
            "Python Data Science", "Python ML/AI", "C++ Project",
            "Node.js Project", "TD_MCP Project", "Otro"
        ]
        
        if config.get("project_type") not in valid_types:
            raise ValueError(
                f"Tipo de proyecto inválido: {config.get('project_type')}. "
                f"Tipos válidos: {', '.join(valid_types)}"
            )
        
        # Validar versión de Python
        python_version = config.get("python_version_min", "3.8")
        if not python_version.startswith("3.") or len(python_version.split(".")) != 2:
            raise ValueError(f"Versión de Python inválida: {python_version}")
        
        logger.info("Configuración validada exitosamente")
    
    def save_config_template(self, output_path: Union[str, Path], project_type: str = "Python Library") -> None:
        """
        Guardar plantilla de configuración.
        
        Args:
            output_path: Ruta donde guardar la plantilla
            project_type: Tipo de proyecto para la plantilla
        """
        output_path = Path(output_path)
        
        # Crear configuración de ejemplo
        template_config = self.default_config.copy()
        template_config.update({
            "project_name": "mi-proyecto-ejemplo",
            "description": "Un proyecto de ejemplo generado automáticamente",
            "detailed_description": "Este es un proyecto de ejemplo que demuestra las capacidades del generador de proyectos.",
            "project_type": project_type,
            "author": "Tu Nombre",
            "email": "tu@email.com",
            "github_user": "tu_usuario",
            "objective": "Demostrar la generación automática de proyectos",
            "main_functionality": "Procesamiento de datos",
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
        })
        
        # Determinar formato basado en extensión
        if output_path.suffix == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template_config, f, indent=2, ensure_ascii=False)
        else:  # .yaml o .yml
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(template_config, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Plantilla de configuración guardada en: {output_path}")
    
    def convert_to_project_data(self, config: Dict[str, Any]) -> Dict[str, str]:
        """
        Convertir configuración a formato de datos del proyecto.
        
        Args:
            config: Configuración cargada
            
        Returns:
            Dict en formato de datos del proyecto
        """
        from datetime import datetime
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        project_name = config["project_name"]
        
        # Generar URL del repositorio si no está especificada
        repository_url = config.get("repository_url", "")
        if not repository_url and config.get("github_user") and project_name:
            repository_url = f"https://github.com/{config['github_user']}/{project_name}"
        
        # Procesar dependencias
        dependencies = config.get("dependencies", {})
        main_deps = dependencies.get("main", [])
        dev_deps = dependencies.get("development", [])
        test_deps = dependencies.get("testing", [])
        opt_deps = dependencies.get("optional", [])
        
        project_type = config.get("project_type", "Python Library")
        
        def format_dependencies(deps: list, project_type: str = "Python Library") -> str:
            if not deps:
                if project_type == "Node.js Project":
                    return '"express": "^4.18.0"'
                return "# Dependencias principales\n# Añadir según necesidades"
            
            if project_type == "Node.js Project":
                # Formatear como JSON válido para Node.js
                formatted_deps = []
                for dep in deps:
                    if ">=" in dep:
                        name, version = dep.split(">=")
                        formatted_deps.append(f'    "{name.strip()}": "^{version.strip()}"')
                    else:
                        formatted_deps.append(f'    "{dep.strip()}": "^1.0.0"')
                return ",\n".join(formatted_deps)
            else:
                # Formatear como comentarios para Python
                return "# Dependencias principales\n" + "\n".join(deps)
        
        return {
            # Información básica
            "NOMBRE_PROYECTO": project_name,
            "DESCRIPCION_PROYECTO": config["description"],
            "DESCRIPCION_DETALLADA": config.get("detailed_description", config["description"]),
            "OBJETIVO_PROYECTO": config.get("objective", ""),
            "FUNCIONALIDAD_PRINCIPAL": config.get("main_functionality", ""),
            
            # Información técnica
            "TIPO_PROYECTO": config["project_type"],
            "AUTOR": config.get("author", "Desarrollador"),
            "EMAIL_CONTACTO": config.get("email", ""),
            "GITHUB_USER": config.get("github_user", ""),
            "REPOSITORIO_URL": repository_url,
            "PYTHON_VERSION_MIN": config.get("python_version_min", "3.8"),
            "LICENCIA": config.get("license", "MIT"),
            
            # Fechas
            "FECHA_CREACION": fecha_actual,
            "FECHA_ACTUALIZACION": fecha_actual,
            
            # Información técnica específica
            "MODULO_PRINCIPAL": self._get_module_name(project_name, config.get("project_type", "Python Library")),
            "CLASE_PRINCIPAL": self._to_pascal_case(project_name),
            "ESTADO_INICIAL": "Fase inicial - Configuración",
            
            # Placeholders adicionales
            "PRIMER_PASO": "Implementar funcionalidades core",
            "SEGUNDO_PASO": "Crear tests unitarios",
            "TERCER_PASO": "Documentar API",
            "SIGUIENTE_PASO": "Implementar primera funcionalidad",
            
            # Ejemplos y configuración
            "EJEMPLO_USO": f"# Crear instancia\ninstancia = {self._to_pascal_case(project_name)}()\n# Usar funcionalidad\nresultado = instancia.procesar()",
            "CONFIGURACION_EJEMPLO": f"# Configuración para {project_name}\nDEBUG = True\nLOG_LEVEL = 'INFO'",
            
            # Dependencias
            "DEPENDENCIAS_PRINCIPALES": format_dependencies(main_deps, project_type),
            "DEPENDENCIAS_DESARROLLO": format_dependencies(dev_deps, project_type),
            "DEPENDENCIAS_TESTING": format_dependencies(test_deps, project_type),
            "DEPENDENCIAS_OPCIONALES": format_dependencies(opt_deps, project_type),
            
            # Campos adicionales para Node.js
            "PALABRAS_CLAVE": config.get("keywords", "nodejs, javascript, api"),
            "NODE_VERSION": config.get("node_version", "18.0.0"),
        }
    
    def _get_module_name(self, project_name: str, project_type: str) -> str:
        """Obtener nombre del módulo según el tipo de proyecto."""
        if project_type == "Node.js Project":
            # Para Node.js mantener guiones
            return project_name.lower()
        else:
            # Para Python y C++ usar guiones bajos
            return project_name.lower().replace("-", "_").replace(" ", "_")
    
    def _to_pascal_case(self, text: str) -> str:
        """Convertir texto a PascalCase."""
        return ''.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())


def load_project_config(config_path: Union[str, Path]) -> Dict[str, str]:
    """
    Función de conveniencia para cargar configuración de proyecto.
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        Dict en formato de datos del proyecto
    """
    loader = ConfigLoader()
    config = loader.load_config(config_path)
    return loader.convert_to_project_data(config)


def create_config_template(output_path: Union[str, Path], project_type: str = "Python Library") -> None:
    """
    Función de conveniencia para crear plantilla de configuración.
    
    Args:
        output_path: Ruta donde guardar la plantilla
        project_type: Tipo de proyecto para la plantilla
    """
    loader = ConfigLoader()
    loader.save_config_template(output_path, project_type)


if __name__ == "__main__":
    # Ejemplo de uso
    loader = ConfigLoader()
    
    # Crear plantilla de ejemplo
    loader.save_config_template("config_template.json", "Python Library")
    loader.save_config_template("config_template.yaml", "Python CLI Tool")
    
    print("✅ Plantillas de configuración creadas:")
    print("   - config_template.json")
    print("   - config_template.yaml")
