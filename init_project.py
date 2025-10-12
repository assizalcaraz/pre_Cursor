#!/usr/bin/env python3
"""
Generador de Proyectos Optimizado para Agentes de IA

Este script genera proyectos siguiendo la metodología establecida,
optimizado para trabajo con agentes de IA en Cursor IDE.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import sys
import shutil
import subprocess
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json

# Importar sistemas de validación y configuración
sys.path.append(str(Path(__file__).parent / "src"))
from validator import validate_project_data, print_validation_results, ValidationError
from config_loader import load_project_config, create_config_template


class ProjectGenerator:
    """Generador de proyectos siguiendo la metodología establecida."""
    
    def __init__(self, verbose: bool = False):
        self.template_dir = Path(__file__).parent / "templates"
        self.structure_dir = Path(__file__).parent / "structure"
        self.project_data: Dict[str, Any] = {}
        self.verbose = verbose
        
        # Configurar logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Configurar sistema de logging."""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('project_generator.log', mode='a')
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Sistema de logging configurado")
        
    def collect_project_info(self) -> Dict[str, Any]:
        """
        Recopilar información del proyecto de manera interactiva con validación.
        
        Returns:
            Dict con la información del proyecto
        """
        print("🚀 Generador de Proyectos Optimizado para Agentes de IA")
        print("=" * 60)
        
        self.logger.info("Iniciando recolección interactiva de información del proyecto")
        
        # Información básica con validación
        nombre_proyecto = self._get_validated_input(
            "📝 Nombre del proyecto", 
            self._validate_project_name_input
        )
        
        descripcion_corta = self._get_validated_input(
            "📋 Descripción corta", 
            self._validate_description_input
        )
        
        descripcion_detallada = self._get_validated_input(
            "📖 Descripción detallada", 
            self._validate_description_input
        )
        
        # Información técnica con validación
        tipo_proyecto = self._select_project_type()
        autor = input("👨‍💻 Autor: ").strip() or "Desarrollador"
        
        email_contacto = self._get_validated_input(
            "📧 Email de contacto (opcional)", 
            self._validate_email_input,
            optional=True
        )
        
        github_user = self._get_validated_input(
            "🐙 GitHub username (opcional)", 
            self._validate_github_user_input,
            optional=True
        )
        
        # Información del repositorio
        repositorio_url = input("🔗 URL del repositorio (opcional): ").strip()
        if not repositorio_url and github_user and nombre_proyecto:
            repositorio_url = f"https://github.com/{github_user}/{nombre_proyecto}"
        
        # Información técnica específica con validación
        python_version_min = self._get_validated_input(
            "🐍 Versión mínima de Python (default: 3.8)", 
            self._validate_python_version_input,
            default="3.8"
        )
        
        licencia = self._get_validated_input(
            "📄 Licencia (default: MIT)", 
            self._validate_license_input,
            default="MIT"
        )
        
        # Objetivo y funcionalidades
        objetivo_proyecto = input("🎯 Objetivo principal del proyecto: ").strip()
        funcionalidad_principal = input("⚡ Funcionalidad principal: ").strip()
        
        # Fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        self.logger.info("Información del proyecto recopilada exitosamente")
        
        return {
            # Información básica
            "NOMBRE_PROYECTO": nombre_proyecto,
            "DESCRIPCION_PROYECTO": descripcion_corta,
            "DESCRIPCION_DETALLADA": descripcion_detallada,
            "OBJETIVO_PROYECTO": objetivo_proyecto,
            "FUNCIONALIDAD_PRINCIPAL": funcionalidad_principal,
            
            # Información técnica
            "TIPO_PROYECTO": tipo_proyecto,
            "AUTOR": autor,
            "EMAIL_CONTACTO": email_contacto,
            "GITHUB_USER": github_user,
            "REPOSITORIO_URL": repositorio_url,
            "PYTHON_VERSION_MIN": python_version_min,
            "LICENCIA": licencia,
            
            # Fechas
            "FECHA_CREACION": fecha_actual,
            "FECHA_ACTUALIZACION": fecha_actual,
            
            # Información técnica específica
            "MODULO_PRINCIPAL": nombre_proyecto.lower().replace("-", "_").replace(" ", "_"),
            "CLASE_PRINCIPAL": self._to_pascal_case(nombre_proyecto),
            "ESTADO_INICIAL": "Fase inicial - Configuración",
            
            # Placeholders adicionales
            "PRIMER_PASO": "Implementar funcionalidades core",
            "SEGUNDO_PASO": "Crear tests unitarios",
            "TERCER_PASO": "Documentar API",
            "SIGUIENTE_PASO": "Implementar primera funcionalidad",
            
            # Ejemplos y configuración
            "EJEMPLO_USO": f"# Crear instancia\ninstancia = {self._to_pascal_case(nombre_proyecto)}()\n# Usar funcionalidad\nresultado = instancia.procesar()",
            "CONFIGURACION_EJEMPLO": f"# Configuración para {nombre_proyecto}\nDEBUG = True\nLOG_LEVEL = 'INFO'",
            
            # Dependencias
            "DEPENDENCIAS_PRINCIPALES": self._get_dependencies_for_type(tipo_proyecto),
            "DEPENDENCIAS_DESARROLLO": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "DEPENDENCIAS_TESTING": "pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0",
            "DEPENDENCIAS_OPCIONALES": "# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0",
        }
    
    def _get_validated_input(self, prompt: str, validator_func, optional: bool = False, default: str = "") -> str:
        """
        Obtener entrada del usuario con validación en tiempo real.
        
        Args:
            prompt: Mensaje para el usuario
            validator_func: Función de validación
            optional: Si el campo es opcional
            default: Valor por defecto
            
        Returns:
            str: Valor validado
        """
        while True:
            try:
                if default:
                    user_input = input(f"{prompt}: ").strip() or default
                else:
                    user_input = input(f"{prompt}: ").strip()
                
                if not user_input and optional:
                    return ""
                
                if validator_func(user_input):
                    return user_input
                else:
                    print("❌ Valor inválido. Intenta de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n❌ Operación cancelada por el usuario")
                sys.exit(1)
            except Exception as e:
                self.logger.error(f"Error en entrada validada: {e}")
                print(f"❌ Error: {e}")
    
    def _validate_project_name_input(self, name: str) -> bool:
        """Validar nombre del proyecto."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_project_name(name)
    
    def _validate_description_input(self, description: str) -> bool:
        """Validar descripción."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_description(description)
    
    def _validate_email_input(self, email: str) -> bool:
        """Validar email."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_email(email)
    
    def _validate_github_user_input(self, username: str) -> bool:
        """Validar GitHub username."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_github_user(username)
    
    def _validate_python_version_input(self, version: str) -> bool:
        """Validar versión de Python."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_python_version(version)
    
    def _validate_license_input(self, license_name: str) -> bool:
        """Validar licencia."""
        from validator import ProjectValidator
        validator = ProjectValidator()
        return validator.validate_license(license_name)
    
    def _select_project_type(self) -> str:
        """Seleccionar tipo de proyecto."""
        print("\n🔧 Tipo de proyecto:")
        print("1. Python Library")
        print("2. Python CLI Tool")
        print("3. Python Web App (Flask)")
        print("4. Python Web App (Django)")
        print("5. Python Web App (FastAPI)")
        print("6. Python Data Science")
        print("7. Python ML/AI")
        print("8. C++ Project")
        print("9. Node.js Project")
        print("10. Otro")
        
        while True:
            choice = input("Selecciona (1-10): ").strip()
            types = {
                "1": "Python Library",
                "2": "Python CLI Tool", 
                "3": "Python Web App (Flask)",
                "4": "Python Web App (Django)",
                "5": "Python Web App (FastAPI)",
                "6": "Python Data Science",
                "7": "Python ML/AI",
                "8": "C++ Project",
                "9": "Node.js Project",
                "10": "Otro"
            }
            if choice in types:
                self.logger.info(f"Tipo de proyecto seleccionado: {types[choice]}")
                return types[choice]
            print("❌ Opción inválida. Intenta de nuevo.")
    
    def _get_dependencies_for_type(self, project_type: str) -> str:
        """Obtener dependencias según el tipo de proyecto."""
        dependencies = {
            "Python Library": "# Dependencias principales\n# requests>=2.28.0",
            "Python CLI Tool": "# Dependencias principales\nclick>=8.0.0\nrich>=12.0.0",
            "Python Web App (Flask)": "# Dependencias principales\nflask>=2.0.0\nflask-cors>=3.0.0",
            "Python Web App (Django)": "# Dependencias principales\ndjango>=4.0.0\ndjangorestframework>=3.14.0",
            "Python Web App (FastAPI)": "# Dependencias principales\nfastapi>=0.100.0\nuvicorn>=0.23.0\npydantic>=2.0.0",
            "Python Data Science": "# Dependencias principales\npandas>=1.5.0\nnumpy>=1.21.0\nmatplotlib>=3.5.0",
            "Python ML/AI": "# Dependencias principales\ntorch>=1.12.0\ntensorflow>=2.10.0\nscikit-learn>=1.1.0",
            "C++ Project": "# Dependencias principales\n# CMake>=3.16\n# gtest>=1.11.0",
            "Node.js Project": "# Dependencias principales\n# express>=4.18.0\n# nodemon>=2.0.0",
            "Otro": "# Dependencias principales\n# Añadir según necesidades"
        }
        return dependencies.get(project_type, dependencies["Otro"])
    
    def _to_pascal_case(self, text: str) -> str:
        """Convertir texto a PascalCase."""
        return ''.join(word.capitalize() for word in text.replace('-', ' ').replace('_', ' ').split())
    
    def create_project_structure(self, project_path: Path) -> None:
        """
        Crear estructura de directorios del proyecto.
        
        Args:
            project_path: Ruta donde crear el proyecto
        """
        print(f"📁 Creando estructura en {project_path}")
        
        # Crear directorios principales
        directories = [
            "src",
            "tests", 
            "docs",
            "examples",
            "logs"
        ]
        
        for directory in directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory}/")
    
    def copy_static_files(self, project_path: Path) -> None:
        """
        Copiar archivos estáticos (sin plantillas).
        
        Args:
            project_path: Ruta del proyecto
        """
        print("📋 Copiando archivos estáticos...")
        
        # Copiar .gitignore
        gitignore_src = Path(__file__).parent / ".gitignore"
        gitignore_dst = project_path / ".gitignore"
        shutil.copy2(gitignore_src, gitignore_dst)
        print("  ✅ .gitignore")
        
        # Copiar tests/README.md
        tests_readme_src = Path(__file__).parent / "tests" / "README.md"
        tests_readme_dst = project_path / "tests" / "README.md"
        shutil.copy2(tests_readme_src, tests_readme_dst)
        print("  ✅ tests/README.md")
        
        # Copiar METODOLOGIA_DESARROLLO.md
        metodologia_src = Path(__file__).parent / "METODOLOGIA_DESARROLLO.md"
        metodologia_dst = project_path / "METODOLOGIA_DESARROLLO.md"
        shutil.copy2(metodologia_src, metodologia_dst)
        print("  ✅ METODOLOGIA_DESARROLLO.md")
    
    def process_templates(self, project_path: Path) -> None:
        """
        Procesar plantillas y crear archivos del proyecto.
        
        Args:
            project_path: Ruta del proyecto
        """
        print("🔧 Procesando plantillas...")
        
        project_type = self.project_data.get('TIPO_PROYECTO', 'Python Library')
        
        # Plantillas base comunes
        base_templates = [
            "BITACORA.md.tpl", 
            "roadmap_v1.md.tpl",
            "TUTORIAL.md.tpl"
        ]
        
        # Plantillas específicas por tipo de proyecto
        if project_type == "C++ Project":
            specific_templates = [
                "README_cpp.md.tpl",
                "CMakeLists.txt.tpl",
                "modulo_principal_cpp.cpp.tpl",
                "modulo_principal_cpp.hpp.tpl"
            ]
        elif project_type == "Node.js Project":
            specific_templates = [
                "README_nodejs.md.tpl",
                "package.json.tpl",
                "modulo_principal_nodejs.js.tpl"
            ]
        else:  # Proyectos Python
            specific_templates = [
                "README.md.tpl",
                "requirements.txt.tpl",
                "modulo_principal.py.tpl"
            ]
        
        # Combinar todas las plantillas
        all_templates = base_templates + specific_templates
        
        for template_file in all_templates:
            template_path = self.template_dir / template_file
            if template_path.exists():
                self._process_template(template_path, project_path)
            else:
                print(f"  ⚠️ Plantilla no encontrada: {template_file}")
    
    def _process_template(self, template_path: Path, project_path: Path) -> None:
        """
        Procesar una plantilla individual.
        
        Args:
            template_path: Ruta de la plantilla
            project_path: Ruta del proyecto
        """
        try:
            # Leer plantilla
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar placeholders
            for key, value in self.project_data.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))
            
            # Determinar archivo de destino basado en tipo de proyecto
            template_name = template_path.name
            project_type = self.project_data.get('TIPO_PROYECTO', 'Python Library')
            
            dest_path = self._get_destination_path(template_name, project_path, project_type)
            
            # Crear directorio padre si no existe
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo procesado
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {dest_path.name}")
            
        except Exception as e:
            print(f"  ❌ Error procesando {template_path.name}: {e}")
    
    def _get_destination_path(self, template_name: str, project_path: Path, project_type: str) -> Path:
        """
        Determinar la ruta de destino basada en el tipo de proyecto.
        
        Args:
            template_name: Nombre de la plantilla
            project_path: Ruta del proyecto
            project_type: Tipo de proyecto
            
        Returns:
            Path: Ruta de destino del archivo
        """
        modulo_principal = self.project_data['MODULO_PRINCIPAL']
        
        # Mapeo de plantillas a archivos de destino por tipo de proyecto
        if project_type == "C++ Project":
            if template_name == "README_cpp.md.tpl":
                return project_path / "README.md"
            elif template_name == "CMakeLists.txt.tpl":
                return project_path / "CMakeLists.txt"
            elif template_name == "modulo_principal_cpp.cpp.tpl":
                return project_path / "src" / f"{modulo_principal}.cpp"
            elif template_name == "modulo_principal_cpp.hpp.tpl":
                return project_path / "src" / f"{modulo_principal}.hpp"
            elif template_name == "TUTORIAL.md.tpl":
                return project_path / "docs" / "TUTORIAL.md"
            elif template_name.endswith(".tpl"):
                dest_name = template_name[:-4]
                return project_path / dest_name
            else:
                return project_path / template_name
        
        elif project_type == "Node.js Project":
            if template_name == "README_nodejs.md.tpl":
                return project_path / "README.md"
            elif template_name == "package.json.tpl":
                return project_path / "package.json"
            elif template_name == "modulo_principal_nodejs.js.tpl":
                return project_path / "src" / f"{modulo_principal}.js"
            elif template_name == "TUTORIAL.md.tpl":
                return project_path / "docs" / "TUTORIAL.md"
            elif template_name.endswith(".tpl"):
                dest_name = template_name[:-4]
                return project_path / dest_name
            else:
                return project_path / template_name
        
        else:  # Proyectos Python
            if template_name == "modulo_principal.py.tpl":
                return project_path / "src" / f"{modulo_principal}.py"
            elif template_name == "TUTORIAL.md.tpl":
                return project_path / "docs" / "TUTORIAL.md"
            elif template_name.endswith(".tpl"):
                dest_name = template_name[:-4]
                return project_path / dest_name
            else:
                return project_path / template_name
    
    def initialize_git(self, project_path: Path) -> None:
        """
        Inicializar repositorio Git.
        
        Args:
            project_path: Ruta del proyecto
        """
        print("🔧 Inicializando repositorio Git...")
        
        try:
            # Cambiar al directorio del proyecto
            original_cwd = os.getcwd()
            os.chdir(project_path)
            
            # Inicializar Git
            subprocess.run(["git", "init"], check=True, capture_output=True)
            print("  ✅ git init")
            
            # Añadir archivos
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            print("  ✅ git add .")
            
            # Commit inicial
            commit_message = f"WIP: Proyecto {self.project_data['NOMBRE_PROYECTO']} inicializado"
            subprocess.run(["git", "commit", "-m", commit_message], check=True, capture_output=True)
            print("  ✅ Commit inicial")
            
            # Restaurar directorio original
            os.chdir(original_cwd)
            
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️ Error con Git: {e}")
        except Exception as e:
            print(f"  ❌ Error inicializando Git: {e}")
    
    def create_context_file(self, project_path: Path) -> None:
        """
        Crear archivo CONTEXTO.md con información del proyecto.
        
        Args:
            project_path: Ruta del proyecto
        """
        print("📄 Creando archivo de contexto...")
        
        context_content = f"""# CONTEXTO - {self.project_data['NOMBRE_PROYECTO']}

## Información del Proyecto

- **Nombre**: {self.project_data['NOMBRE_PROYECTO']}
- **Descripción**: {self.project_data['DESCRIPCION_PROYECTO']}
- **Tipo**: {self.project_data['TIPO_PROYECTO']}
- **Autor**: {self.project_data['AUTOR']}
- **Fecha de Creación**: {self.project_data['FECHA_CREACION']}

## Estructura Generada

```
{self.project_data['NOMBRE_PROYECTO']}/
├── README.md                    # Documentación principal
├── BITACORA.md                 # Log de desarrollo
├── roadmap_v1.md               # Plan de desarrollo
├── requirements.txt            # Dependencias
├── METODOLOGIA_DESARROLLO.md   # Metodología establecida
├── CONTEXTO.md                 # Este archivo
├── src/                        # Código fuente
│   └── {self.project_data['MODULO_PRINCIPAL']}.py
├── tests/                      # Pruebas
│   └── README.md
├── docs/                       # Documentación
│   └── TUTORIAL.md
├── examples/                   # Ejemplos
└── logs/                       # Logs
```

## Próximos Pasos

1. Revisar y ajustar archivos generados
2. Implementar funcionalidades core
3. Crear tests unitarios
4. Seguir metodología en METODOLOGIA_DESARROLLO.md

## Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest

# Actualizar bitácora
echo "### $(date +%Y-%m-%d)" >> BITACORA.md
```

---
**Generado automáticamente**: {self.project_data['FECHA_CREACION']}
"""
        
        context_path = project_path / "CONTEXTO.md"
        with open(context_path, 'w', encoding='utf-8') as f:
            f.write(context_content)
        
        print("  ✅ CONTEXTO.md")
    
    def generate_project(self, project_name: str, project_path: Optional[Path] = None) -> None:
        """
        Generar proyecto completo con validación robusta.
        
        Args:
            project_name: Nombre del proyecto
            project_path: Ruta donde crear el proyecto (opcional)
        """
        try:
            if project_path is None:
                project_path = Path.cwd() / project_name
            
            self.logger.info(f"Iniciando generación de proyecto: {project_name}")
            self.logger.info(f"Ubicación: {project_path}")
            
            print(f"🚀 Generando proyecto: {project_name}")
            print(f"📂 Ubicación: {project_path}")
            print()
            
            # Recopilar información
            self.project_data = self.collect_project_info()
            
            # Validación completa antes de proceder
            print("🔍 Validando parámetros del proyecto...")
            is_valid, errors, warnings = validate_project_data(self.project_data, project_path)
            
            if warnings:
                print("\n⚠️  Advertencias:")
                for warning in warnings:
                    print(f"   • {warning}")
            
            if not is_valid:
                print("\n❌ Errores de validación:")
                for error in errors:
                    print(f"   • {error}")
                print("\n🔧 Por favor corrige los errores antes de continuar.")
                raise ValidationError("Validación fallida")
            
            print("✅ Validación exitosa - Todos los parámetros son válidos")
            
            # Crear directorio del proyecto
            self.logger.info("Creando directorio del proyecto")
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Crear estructura
            self.create_project_structure(project_path)
            
            # Copiar archivos estáticos
            self.copy_static_files(project_path)
            
            # Procesar plantillas
            self.process_templates(project_path)
            
            # Crear archivo de contexto
            self.create_context_file(project_path)
            
            # Inicializar Git
            self.initialize_git(project_path)
            
            self.logger.info("Proyecto generado exitosamente")
            
            print()
            print("🎉 ¡Proyecto generado exitosamente!")
            print(f"📂 Ubicación: {project_path}")
            print()
            print("📋 Próximos pasos:")
            print(f"  1. cd {project_name}")
            print("  2. pip install -r requirements.txt")
            print("  3. Revisar CONTEXTO.md")
            print("  4. Seguir TUTORIAL.md")
            print("  5. Actualizar BITACORA.md")
            
        except ValidationError as e:
            self.logger.error(f"Error de validación: {e}")
            print(f"\n❌ Error de validación: {e}")
            sys.exit(1)
        except FileExistsError as e:
            self.logger.error(f"Error de archivo existente: {e}")
            print(f"\n❌ Error: El directorio '{project_path}' ya existe")
            print("💡 Sugerencia: Usa un nombre diferente o elimina el directorio existente")
            sys.exit(1)
        except PermissionError as e:
            self.logger.error(f"Error de permisos: {e}")
            print(f"\n❌ Error de permisos: {e}")
            print("💡 Sugerencia: Verifica que tienes permisos de escritura en el directorio")
            sys.exit(1)
        except KeyboardInterrupt:
            self.logger.info("Operación cancelada por el usuario")
            print("\n❌ Operación cancelada por el usuario")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            print(f"\n❌ Error inesperado: {e}")
            print("💡 Sugerencia: Revisa los logs en 'project_generator.log' para más detalles")
            sys.exit(1)
    
    def generate_project_from_config(self, config_path: Path, project_path: Optional[Path] = None) -> None:
        """
        Generar proyecto desde archivo de configuración.
        
        Args:
            config_path: Ruta al archivo de configuración
            project_path: Ruta donde crear el proyecto (opcional)
        """
        try:
            self.logger.info(f"Cargando configuración desde: {config_path}")
            
            # Cargar configuración
            self.project_data = load_project_config(config_path)
            project_name = self.project_data["NOMBRE_PROYECTO"]
            
            if project_path is None:
                project_path = Path.cwd() / project_name
            
            self.logger.info(f"Iniciando generación de proyecto desde configuración: {project_name}")
            self.logger.info(f"Ubicación: {project_path}")
            
            print(f"🚀 Generando proyecto desde configuración: {project_name}")
            print(f"📂 Ubicación: {project_path}")
            print(f"📋 Configuración: {config_path}")
            print()
            
            # Validación completa antes de proceder
            print("🔍 Validando parámetros del proyecto...")
            is_valid, errors, warnings = validate_project_data(self.project_data, project_path)
            
            if warnings:
                print("\n⚠️  Advertencias:")
                for warning in warnings:
                    print(f"   • {warning}")
            
            if not is_valid:
                print("\n❌ Errores de validación:")
                for error in errors:
                    print(f"   • {error}")
                print("\n🔧 Por favor corrige los errores en el archivo de configuración.")
                raise ValidationError("Validación fallida")
            
            print("✅ Validación exitosa - Todos los parámetros son válidos")
            
            # Crear directorio del proyecto
            self.logger.info("Creando directorio del proyecto")
            project_path.mkdir(parents=True, exist_ok=True)
            
            # Crear estructura
            self.create_project_structure(project_path)
            
            # Copiar archivos estáticos
            self.copy_static_files(project_path)
            
            # Procesar plantillas
            self.process_templates(project_path)
            
            # Crear archivo de contexto
            self.create_context_file(project_path)
            
            # Inicializar Git
            self.initialize_git(project_path)
            
            self.logger.info("Proyecto generado exitosamente desde configuración")
            
            print()
            print("🎉 ¡Proyecto generado exitosamente desde configuración!")
            print(f"📂 Ubicación: {project_path}")
            print()
            print("📋 Próximos pasos:")
            print(f"  1. cd {project_name}")
            print("  2. pip install -r requirements.txt")
            print("  3. Revisar CONTEXTO.md")
            print("  4. Seguir TUTORIAL.md")
            print("  5. Actualizar BITACORA.md")
            
        except ValidationError as e:
            self.logger.error(f"Error de validación: {e}")
            print(f"\n❌ Error de validación: {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            self.logger.error(f"Archivo de configuración no encontrado: {e}")
            print(f"\n❌ Error: Archivo de configuración no encontrado: {config_path}")
            sys.exit(1)
        except ValueError as e:
            self.logger.error(f"Error en configuración: {e}")
            print(f"\n❌ Error en configuración: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            print(f"\n❌ Error inesperado: {e}")
            print("💡 Sugerencia: Revisa los logs en 'project_generator.log' para más detalles")
            sys.exit(1)


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Generador de Proyectos Optimizado para Agentes de IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python init_project.py                                    # Modo interactivo
  python init_project.py MiProyecto                         # Crear proyecto específico
  python init_project.py MiProyecto /ruta/                  # Crear en ruta específica
  python init_project.py --verbose                          # Modo verbose con logging detallado
  python init_project.py --config config.json               # Usar archivo de configuración
  python init_project.py --create-template "Python Library"  # Crear plantilla de configuración
  python init_project.py -t "FastAPI" -o mi_config.yaml    # Crear plantilla YAML específica
        """
    )
    
    parser.add_argument(
        "project_name",
        nargs="?",
        help="Nombre del proyecto a crear"
    )
    
    parser.add_argument(
        "project_path",
        nargs="?",
        help="Ruta donde crear el proyecto"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Activar modo verbose con logging detallado"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Archivo de configuración JSON/YAML"
    )
    
    parser.add_argument(
        "--create-template", "-t",
        type=str,
        help="Crear plantilla de configuración (especificar tipo de proyecto)"
    )
    
    parser.add_argument(
        "--template-output", "-o",
        type=str,
        help="Ruta de salida para plantilla de configuración"
    )
    
    args = parser.parse_args()
    
    try:
        generator = ProjectGenerator(verbose=args.verbose)
        
        # Crear plantilla de configuración
        if args.create_template:
            project_type = args.create_template
            output_path = args.template_output or f"config_template_{project_type.lower().replace(' ', '_')}.json"
            
            print(f"📝 Creando plantilla de configuración para: {project_type}")
            print(f"📂 Archivo de salida: {output_path}")
            
            create_config_template(output_path, project_type)
            print(f"✅ Plantilla creada exitosamente: {output_path}")
            print("💡 Edita el archivo y úsalo con: python init_project.py --config <archivo>")
            return
        
        # Generar proyecto desde configuración
        if args.config:
            config_path = Path(args.config)
            if not config_path.exists():
                print(f"❌ Archivo de configuración no encontrado: {config_path}")
                sys.exit(1)
            
            generator.generate_project_from_config(config_path)
            return
        
        if args.project_name:
            project_path = Path(args.project_path) if args.project_path else None
            generator.generate_project(args.project_name, project_path)
        else:
            # Modo interactivo completo
            project_name = input("📝 Nombre del proyecto: ").strip()
            if not project_name:
                print("❌ El nombre del proyecto es requerido")
                sys.exit(1)
            
            generator.generate_project(project_name)
            
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
