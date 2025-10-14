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
from string import Template
import concurrent.futures
from functools import lru_cache

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
        
        # Configurar logging básico
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Añadir handler de archivo solo si no estamos en modo test
        if not hasattr(self, '_test_mode'):
            try:
                file_handler = logging.FileHandler('project_generator.log', mode='a')
                logging.getLogger().addHandler(file_handler)
            except (OSError, PermissionError):
                # Si no se puede crear el archivo de log, continuar sin él
                pass
        
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
            "MODULO_PRINCIPAL": self._get_module_name(nombre_proyecto, tipo_proyecto),
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
            "DEPENDENCIAS_DESARROLLO": self._get_dev_dependencies_for_type(tipo_proyecto),
            "DEPENDENCIAS_TESTING": "pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0",
            "DEPENDENCIAS_OPCIONALES": "# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0",
            
            # Campos adicionales para Node.js
            "PALABRAS_CLAVE": "python, library, api",
            "NODE_VERSION": "18.0.0",
            
            # Variables adicionales para completar placeholders
            "TIPOS_IMPORTADOS": "List, Dict, Optional, Union",
            "TIPO_RETORNO": "Any",
            "TIPO_RETORNO_SECUNDARIO": "bool",
            "TIPO_RETORNO_FUNCION": "str",
            "METODO_PRINCIPAL": "procesar",
            "METODO_SECUNDARIO": "validar",
            "FUNCION_UTILITARIA": "utilidad",
            "PARAMETROS_INIT": "config=None",
            "PARAMETROS_METODO": "datos",
            "PARAMETROS_METODO_SECUNDARIO": "valor",
            "PARAMETROS_FUNCION": "entrada",
            "IMPLEMENTACION_METODO": "pass  # Implementar lógica aquí",
            "IMPLEMENTACION_METODO_SECUNDARIO": "return True",
            "IMPLEMENTACION_FUNCION": 'return "resultado"',
            "RETORNO_METODO": "None",
            "RETORNO_METODO_SECUNDARIO": "True",
            "RETORNO_FUNCION": '"resultado"',
            "DESCRIPCION_CLASE_PRINCIPAL": "Clase principal del proyecto",
            "DESCRIPCION_METODO_PRINCIPAL": "Método principal de procesamiento",
            "DESCRIPCION_METODO_SECUNDARIO": "Método secundario de validación",
            "DESCRIPCION_FUNCION_UTILITARIA": "Función utilitaria",
            "DESCRIPCION_RETORNO": "Resultado del procesamiento",
            "DESCRIPCION_RETORNO_SECUNDARIO": "Estado de la validación",
            
            # Variables específicas para CURSOR_GUIDE.md
            "DESCRIPCION_TIPO_PROYECTO": self._get_project_type_description(tipo_proyecto),
            "CARACTERISTICA_1": self._get_characteristic_1(tipo_proyecto),
            "CARACTERISTICA_2": self._get_characteristic_2(tipo_proyecto),
            "CARACTERISTICA_3": self._get_characteristic_3(tipo_proyecto),
            "CASO_USO_1": self._get_use_case_1(tipo_proyecto),
            "CASO_USO_2": self._get_use_case_2(tipo_proyecto),
            "CASO_USO_3": self._get_use_case_3(tipo_proyecto),
            "VERSION_PROYECTO": "1.0.0",
            "DESCRIPCION_RETORNO_FUNCION": "Resultado de la función",
            "DOCSTRING_PARAMETROS": "config: Configuración opcional",
            "DOCSTRING_PARAMETROS_METODO": "datos: Datos a procesar",
            "DOCSTRING_PARAMETROS_METODO_SECUNDARIO": "valor: Valor a validar",
            "DOCSTRING_PARAMETROS_FUNCION": "entrada: Entrada a procesar",
            "EXCEPCIONES": "ValueError",
            "DESCRIPCION_EXCEPCIONES": "Si los datos son inválidos",
            "ATRIBUTO_1": "config",
            "ATRIBUTO_2": "datos",
            "OBJETIVO_DETALLADO": "Crear una solución robusta y escalable",
            "FUNCIONALIDAD_CORE_1": "Procesamiento de datos",
            "FUNCIONALIDAD_CORE_2": "Validación de entrada",
            "FUNCIONALIDAD_CORE_3": "Manejo de errores",
            "FEATURE_1": "API REST",
            "FEATURE_2": "Base de datos",
            "FEATURE_3": "Autenticación",
            "DESCRIPCION_FEATURE_1": "API REST para comunicación",
            "DESCRIPCION_FEATURE_2": "Integración con base de datos",
            "DESCRIPCION_FEATURE_3": "Sistema de autenticación seguro",
            "FEATURE_ADICIONAL_1": "Logging",
            "FEATURE_ADICIONAL_2": "Testing",
            "DESCRIPCION_FEATURE_ADICIONAL_1": "Sistema de logging completo",
            "DESCRIPCION_FEATURE_ADICIONAL_2": "Suite de tests automatizados",
            "TIEMPO_RESPUESTA": "100",
            "CRITERIO_USABILIDAD": "Interfaz intuitiva",
            "PASO_INMEDIATO": "Configurar entorno de desarrollo",
            "PASO_CORTO_PLAZO": "Implementar funcionalidades básicas",
            "PASO_MEDIANO_PLAZO": "Añadir características avanzadas",
            "BENEFICIO_1": "Fácil de usar",
            "BENEFICIO_2": "Altamente configurable",
            "BENEFICIO_3": "Bien documentado",
            "OTRO_REQUISITO": "Git instalado",
            "EJEMPLO_1_TITULO": "Uso básico",
            "EJEMPLO_1_DESCRIPCION": "Ejemplo de uso básico del proyecto",
            "EJEMPLO_1_CODIGO": f"from {self._get_module_name(nombre_proyecto, tipo_proyecto)} import {self._to_pascal_case(nombre_proyecto)}\ninstancia = {self._to_pascal_case(nombre_proyecto)}()\nresultado = instancia.procesar()",
            "EJEMPLO_2_TITULO": "Configuración avanzada",
            "EJEMPLO_2_DESCRIPCION": "Ejemplo de configuración avanzada",
            "EJEMPLO_2_CODIGO": f"config = {{'debug': True}}\ninstancia = {self._to_pascal_case(nombre_proyecto)}(config)\nresultado = instancia.procesar()",
            "VARIABLE_1": "DEBUG",
            "VALOR_1": "true",
            "VARIABLE_2": "LOG_LEVEL",
            "VALOR_2": "INFO",
            "PROBLEMA_1": "Error de importación",
            "SINTOMAS_1": "ModuleNotFoundError",
            "SOLUCION_1": "Verificar que las dependencias estén instaladas",
            "PROBLEMA_2": "Error de configuración",
            "SINTOMAS_2": "ConfigurationError",
            "SOLUCION_2": "Verificar archivo de configuración",
            "DISCORD_SERVER": "https://discord.gg/tu-servidor",
            "OTRA_DEPENDENCIA": "requests",
            "VERSION_MINIMA": "2.28.0",
            "MODULO_PRINCIPAL_UPPER": self._get_module_name(nombre_proyecto, tipo_proyecto).upper(),
            "METODO_SECUNDARIO_RETORNO": "bool",
            "PARAMETROS_METODO_SECUNDARIO_DOC": "valor Valor a validar",
            "DESCRIPCION_RETORNO_METODO_SECUNDARIO": "Estado de la validación",
            "IMPLEMENTACION_METODO_PRINCIPAL": "// Implementar lógica aquí",
            "IMPLEMENTACION_METODO_SECUNDARIO": "return true;",
            "RETORNO_METODO_SECUNDARIO": "True",
            "TIPO_RETORNO_METODO_SECUNDARIO": "Promise<boolean>",
            "IMPLEMENTACION_METODO_PRINCIPAL": "// Implementar lógica aquí",
            "IMPLEMENTACION_METODO_SECUNDARIO": "return True",
            "RETORNO_METODO_SECUNDARIO": "True",
            "EJEMPLO_USO_MAIN": f"# Crear instancia\ninstancia = {self._to_pascal_case(nombre_proyecto)}()\n# Usar funcionalidad\nresultado = instancia.procesar()",
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
        print("10. TD_MCP Project")
        print("11. Otro")
        
        while True:
            choice = input("Selecciona (1-11): ").strip()
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
                "10": "TD_MCP Project",
                "11": "Otro"
            }
            if choice in types:
                self.logger.info(f"Tipo de proyecto seleccionado: {types[choice]}")
                return types[choice]
            print("❌ Opción inválida. Intenta de nuevo.")
    
    def _get_dev_dependencies_for_type(self, project_type: str) -> str:
        """Obtener dependencias de desarrollo según el tipo de proyecto."""
        dev_dependencies = {
            "Python Library": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python CLI Tool": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python Web App (Flask)": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python Web App (Django)": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python Web App (FastAPI)": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python Data Science": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "Python ML/AI": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
            "TD_MCP Project": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0\npytest-asyncio>=0.21.0",
            "C++ Project": "# Dependencias de desarrollo\n# gtest>=1.11.0\n# clang-format",
            "Node.js Project": '"nodemon": "^2.0.0",\n    "jest": "^29.0.0",\n    "eslint": "^8.0.0",\n    "prettier": "^2.8.0"',
            "Otro": "# Dependencias de desarrollo\n# Añadir según necesidades"
        }
        return dev_dependencies.get(project_type, dev_dependencies["Otro"])
    
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
            "TD_MCP Project": "# Dependencias principales\nmcp>=1.0.0\nasyncio-mqtt>=0.13.0\nwebsockets>=11.0.0\npydantic>=2.0.0",
            "C++ Project": "# Dependencias principales\n# CMake>=3.16\n# gtest>=1.11.0",
            "Node.js Project": '"express": "^4.18.0",\n    "cors": "^2.8.5"',
            "Otro": "# Dependencias principales\n# Añadir según necesidades"
        }
        return dependencies.get(project_type, dependencies["Otro"])
    
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
    
    def create_project_structure(self, project_path: Path) -> None:
        """
        Crear estructura de directorios del proyecto de manera optimizada.
        
        Args:
            project_path: Ruta donde crear el proyecto
        """
        print(f"📁 Creando estructura en {project_path}")
        
        # Crear directorios principales en lote
        directories = [
            "src",
            "tests", 
            "docs",
            "examples",
            "logs"
        ]
        
        # Crear todos los directorios de una vez para mejor rendimiento
        self._create_directories_batch(project_path, directories)
    
    def _create_directories_batch(self, project_path: Path, directories: list) -> None:
        """
        Crear múltiples directorios de manera eficiente.
        
        Args:
            project_path: Ruta base del proyecto
            directories: Lista de directorios a crear
        """
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
        Procesar plantillas y crear archivos del proyecto de manera optimizada.
        
        Args:
            project_path: Ruta del proyecto
        """
        print("🔧 Procesando plantillas...")
        
        project_type = self.project_data.get('TIPO_PROYECTO', 'Python Library')
        
        # Obtener lista de plantillas a procesar
        template_files = self._get_template_files(project_type)
        
        # Filtrar plantillas existentes
        existing_templates = []
        for template_file in template_files:
            template_path = self.template_dir / template_file
            if template_path.exists():
                existing_templates.append(template_path)
            else:
                print(f"  ⚠️ Plantilla no encontrada: {template_file}")
        
        # Procesar plantillas en paralelo para mejor rendimiento
        if len(existing_templates) > 3:  # Solo usar paralelismo si hay suficientes plantillas
            self._process_templates_parallel(existing_templates, project_path)
        else:
            # Procesamiento secuencial para pocas plantillas
            for template_path in existing_templates:
                self._process_template(template_path, project_path)
    
    @lru_cache(maxsize=32)
    def _get_template_files(self, project_type: str) -> tuple:
        """
        Obtener lista de plantillas basada en el tipo de proyecto (con cache).
        
        Args:
            project_type: Tipo de proyecto
            
        Returns:
            tuple: Lista de archivos de plantilla
        """
        # Plantillas base comunes
        base_templates = [
            "BITACORA.md.tpl", 
            "roadmap_v1.md.tpl",
            "TUTORIAL.md.tpl",
            "CURSOR_GUIDE.md.tpl"  # Guía específica para Cursor AI
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
        elif project_type == "TD_MCP Project":
            specific_templates = [
                "README_td_mcp.md.tpl",
                "requirements_td_mcp.txt.tpl",
                "modulo_principal_td_mcp.py.tpl",
                "config_td_mcp.py.tpl",
                "config_td_mcp.json.tpl"
            ]
        else:  # Proyectos Python
            specific_templates = [
                "README.md.tpl",
                "requirements.txt.tpl",
                "modulo_principal.py.tpl"
            ]
        
        return tuple(base_templates + specific_templates)
    
    def _process_templates_parallel(self, template_paths: list, project_path: Path) -> None:
        """
        Procesar plantillas en paralelo para mejor rendimiento.
        
        Args:
            template_paths: Lista de rutas de plantillas
            project_path: Ruta del proyecto
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # Crear tareas para procesamiento paralelo
            futures = [
                executor.submit(self._process_template, template_path, project_path)
                for template_path in template_paths
            ]
            
            # Esperar a que todas las tareas terminen
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"  ❌ Error en procesamiento paralelo: {e}")
    
    def _process_template(self, template_path: Path, project_path: Path) -> None:
        """
        Procesar una plantilla individual de manera optimizada.
        Maneja ambos formatos de placeholders: $VARIABLE y {{VARIABLE}}.
        
        Args:
            template_path: Ruta de la plantilla
            project_path: Ruta del proyecto
        """
        try:
            # Leer plantilla una sola vez
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Preparar datos de reemplazo con valores seguros
            safe_data = {}
            for key, value in self.project_data.items():
                # Escapar caracteres especiales para Template
                safe_value = str(value).replace('$', '$$')
                safe_data[key] = safe_value
            
            # Procesar formato $VARIABLE usando Template
            try:
                template = Template(content)
                content = template.safe_substitute(safe_data)
                self.logger.debug(f"Procesado formato $VARIABLE en {template_path.name}")
            except KeyError as e:
                self.logger.warning(f"Error con Template en {template_path.name}: {e}")
            except Exception as e:
                self.logger.warning(f"Error procesando $VARIABLE en {template_path.name}: {e}")
            
            # Procesar formato {{VARIABLE}} usando str.replace
            for key, value in safe_data.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in content:
                    content = content.replace(placeholder, value)
                    self.logger.debug(f"Reemplazado {placeholder} en {template_path.name}")
            
            # Verificar placeholders no procesados
            unprocessed_placeholders = self._find_unprocessed_placeholders(content)
            if unprocessed_placeholders:
                self.logger.warning(f"Placeholders no procesados en {template_path.name}: {unprocessed_placeholders}")
                # Intentar reemplazar con valores por defecto
                content = self._replace_with_defaults(content, unprocessed_placeholders)
            
            # Determinar archivo de destino
            template_name = template_path.name
            project_type = self.project_data.get('TIPO_PROYECTO', 'Python Library')
            modulo_principal = self.project_data.get('MODULO_PRINCIPAL', 'main')
            dest_path = self._get_destination_path(template_name, str(project_path), project_type, modulo_principal)
            
            # Crear directorio padre si no existe
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo procesado
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {dest_path.name}")
            
        except Exception as e:
            print(f"  ❌ Error procesando {template_path.name}: {e}")
            self.logger.error(f"Error procesando plantilla {template_path.name}: {e}")
    
    def _find_unprocessed_placeholders(self, content: str) -> list:
        """
        Encontrar placeholders no procesados en el contenido.
        
        Args:
            content: Contenido a verificar
            
        Returns:
            list: Lista de placeholders no procesados
        """
        import re
        
        # Buscar formato {{VARIABLE}}
        curly_placeholders = re.findall(r'\{\{([^}]+)\}\}', content)
        
        # Buscar formato $VARIABLE (que no hayan sido procesados)
        dollar_placeholders = re.findall(r'\$([A-Z_]+)', content)
        
        return curly_placeholders + dollar_placeholders
    
    def _replace_with_defaults(self, content: str, unprocessed_placeholders: list) -> str:
        """
        Reemplazar placeholders no procesados con valores por defecto.
        
        Args:
            content: Contenido a procesar
            unprocessed_placeholders: Lista de placeholders no procesados
            
        Returns:
            str: Contenido con placeholders reemplazados por defectos
        """
        # Valores por defecto para placeholders comunes
        default_values = {
            # Variables de tipos
            'TIPOS_IMPORTADOS': 'List, Dict, Optional, Union',
            'TIPO_RETORNO': 'Any',
            'TIPO_RETORNO_SECUNDARIO': 'bool',
            'TIPO_RETORNO_FUNCION': 'str',
            
            # Variables de métodos
            'METODO_PRINCIPAL': 'procesar',
            'METODO_SECUNDARIO': 'validar',
            'FUNCION_UTILITARIA': 'utilidad',
            'PARAMETROS_INIT': 'config=None',
            'PARAMETROS_METODO': 'datos',
            'PARAMETROS_METODO_SECUNDARIO': 'valor',
            'PARAMETROS_FUNCION': 'entrada',
            
            # Variables de implementación
            'IMPLEMENTACION_METODO': 'pass  # Implementar lógica aquí',
            'IMPLEMENTACION_METODO_SECUNDARIO': 'return True',
            'IMPLEMENTACION_FUNCION': 'return "resultado"',
            'RETORNO_METODO': 'None',
            'RETORNO_METODO_SECUNDARIO': 'True',
            'RETORNO_FUNCION': '"resultado"',
            
            # Variables de documentación
            'DESCRIPCION_CLASE_PRINCIPAL': 'Clase principal del proyecto',
            'DESCRIPCION_METODO_PRINCIPAL': 'Método principal de procesamiento',
            'DESCRIPCION_METODO_SECUNDARIO': 'Método secundario de validación',
            'DESCRIPCION_FUNCION_UTILITARIA': 'Función utilitaria',
            'DESCRIPCION_RETORNO': 'Resultado del procesamiento',
            'DESCRIPCION_RETORNO_SECUNDARIO': 'Estado de la validación',
            'DESCRIPCION_RETORNO_FUNCION': 'Resultado de la función',
            'DOCSTRING_PARAMETROS': 'config: Configuración opcional',
            'DOCSTRING_PARAMETROS_METODO': 'datos: Datos a procesar',
            'DOCSTRING_PARAMETROS_METODO_SECUNDARIO': 'valor: Valor a validar',
            'DOCSTRING_PARAMETROS_FUNCION': 'entrada: Entrada a procesar',
            'EXCEPCIONES': 'ValueError',
            'DESCRIPCION_EXCEPCIONES': 'Si los datos son inválidos',
            
            # Variables de atributos
            'ATRIBUTO_1': 'config',
            'ATRIBUTO_2': 'datos',
            
            # Variables de roadmap
            'OBJETIVO_DETALLADO': 'Crear una solución robusta y escalable',
            'FUNCIONALIDAD_CORE_1': 'Procesamiento de datos',
            'FUNCIONALIDAD_CORE_2': 'Validación de entrada',
            'FUNCIONALIDAD_CORE_3': 'Manejo de errores',
            'FEATURE_1': 'API REST',
            'FEATURE_2': 'Base de datos',
            'FEATURE_3': 'Autenticación',
            'DESCRIPCION_FEATURE_1': 'API REST para comunicación',
            'DESCRIPCION_FEATURE_2': 'Integración con base de datos',
            'DESCRIPCION_FEATURE_3': 'Sistema de autenticación seguro',
            'FEATURE_ADICIONAL_1': 'Logging',
            'FEATURE_ADICIONAL_2': 'Testing',
            'DESCRIPCION_FEATURE_ADICIONAL_1': 'Sistema de logging completo',
            'DESCRIPCION_FEATURE_ADICIONAL_2': 'Suite de tests automatizados',
            'TIEMPO_RESPUESTA': '100',
            'CRITERIO_USABILIDAD': 'Interfaz intuitiva',
            'PASO_INMEDIATO': 'Configurar entorno de desarrollo',
            'PASO_CORTO_PLAZO': 'Implementar funcionalidades básicas',
            'PASO_MEDIANO_PLAZO': 'Añadir características avanzadas',
            
            # Variables de tutorial
            'BENEFICIO_1': 'Fácil de usar',
            'BENEFICIO_2': 'Altamente configurable',
            'BENEFICIO_3': 'Bien documentado',
            'OTRO_REQUISITO': 'Git instalado',
            'EJEMPLO_1_TITULO': 'Uso básico',
            'EJEMPLO_1_DESCRIPCION': 'Ejemplo de uso básico del proyecto',
            'EJEMPLO_1_CODIGO': 'from proyecto import ClasePrincipal\ninstancia = ClasePrincipal()\nresultado = instancia.procesar()',
            'EJEMPLO_2_TITULO': 'Configuración avanzada',
            'EJEMPLO_2_DESCRIPCION': 'Ejemplo de configuración avanzada',
            'EJEMPLO_2_CODIGO': 'config = {"debug": True}\ninstancia = ClasePrincipal(config)\nresultado = instancia.procesar()',
            'EJEMPLO_USO_MAIN': '# Crear instancia\ninstancia = ClasePrincipal()\n# Usar funcionalidad\nresultado = instancia.procesar()',
            'VARIABLE_1': 'DEBUG',
            'VALOR_1': 'true',
            'VARIABLE_2': 'LOG_LEVEL',
            'VALOR_2': 'INFO',
            'PROBLEMA_1': 'Error de importación',
            'SINTOMAS_1': 'ModuleNotFoundError',
            'SOLUCION_1': 'Verificar que las dependencias estén instaladas',
            'PROBLEMA_2': 'Error de configuración',
            'SINTOMAS_2': 'ConfigurationError',
            'SOLUCION_2': 'Verificar archivo de configuración',
            'DISCORD_SERVER': 'https://discord.gg/tu-servidor',
            
            # Variables de dependencias
            'OTRA_DEPENDENCIA': 'requests',
            'VERSION_MINIMA': '2.28.0',
            
            # Variables de C++
            'MODULO_PRINCIPAL_UPPER': self.project_data.get('MODULO_PRINCIPAL', 'main').upper(),
            'METODO_SECUNDARIO_RETORNO': 'bool',
            'PARAMETROS_METODO_SECUNDARIO_DOC': 'valor Valor a validar',
            'DESCRIPCION_RETORNO_METODO_SECUNDARIO': 'Estado de la validación',
            'IMPLEMENTACION_METODO_PRINCIPAL': '// Implementar lógica aquí',
            'IMPLEMENTACION_METODO_SECUNDARIO': 'return true;',
            'RETORNO_METODO_SECUNDARIO': 'true',
            
            # Variables de Node.js
            'PARAMETROS_METODO_SECUNDARIO_DOC': 'valor Valor a validar',
            'TIPO_RETORNO_METODO_SECUNDARIO': 'Promise<boolean>',
            'IMPLEMENTACION_METODO_PRINCIPAL': '// Implementar lógica aquí',
            'IMPLEMENTACION_METODO_SECUNDARIO': 'return true;',
            'RETORNO_METODO_SECUNDARIO': 'true',
        }
        
        # Reemplazar placeholders con valores por defecto
        for placeholder in unprocessed_placeholders:
            if placeholder in default_values:
                # Reemplazar formato {{VARIABLE}}
                content = content.replace(f"{{{{{placeholder}}}}}", default_values[placeholder])
                # Reemplazar formato $VARIABLE
                content = content.replace(f"${placeholder}", default_values[placeholder])
                self.logger.info(f"Reemplazado {placeholder} con valor por defecto: {default_values[placeholder]}")
            else:
                self.logger.warning(f"Placeholder sin valor por defecto: {placeholder}")
        
        return content
    
    @lru_cache(maxsize=128)
    def _get_destination_path(self, template_name: str, project_path_str: str, project_type: str, modulo_principal: str) -> Path:
        """
        Determinar la ruta de destino basada en el tipo de proyecto (con cache).
        
        Args:
            template_name: Nombre de la plantilla
            project_path_str: Ruta del proyecto como string (para cache)
            project_type: Tipo de proyecto
            modulo_principal: Nombre del módulo principal
            
        Returns:
            Path: Ruta de destino del archivo
        """
        project_path = Path(project_path_str)
        
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
        
        elif project_type == "TD_MCP Project":
            if template_name == "README_td_mcp.md.tpl":
                return project_path / "README.md"
            elif template_name == "requirements_td_mcp.txt.tpl":
                return project_path / "requirements.txt"
            elif template_name == "modulo_principal_td_mcp.py.tpl":
                return project_path / "src" / f"{modulo_principal}.py"
            elif template_name == "config_td_mcp.py.tpl":
                return project_path / "config.py"
            elif template_name == "config_td_mcp.json.tpl":
                return project_path / "config.json"
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
            project_name = self.project_data.get('NOMBRE_PROYECTO', 'proyecto')
            commit_message = f"WIP: Proyecto {project_name} inicializado"
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

        # Obtener nombre del módulo principal
        module_name = self.project_data.get('MODULO_PRINCIPAL', 'main')
        
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
│   └── {module_name}.py
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


    def _get_project_type_description(self, project_type: str) -> str:
        """Obtener descripción del tipo de proyecto para la guía de Cursor."""
        descriptions = {
            "Python Library": "Librería Python estándar con funcionalidades reutilizables",
            "Python CLI Tool": "Herramienta de línea de comandos para automatización",
            "Python Web App (Flask)": "Aplicación web moderna con framework Flask",
            "Python Web App (Django)": "Aplicación web robusta con framework Django",
            "Python Web App (FastAPI)": "API REST moderna y rápida con FastAPI",
            "Python Data Science": "Proyecto de análisis y visualización de datos",
            "Python ML/AI": "Proyecto de machine learning e inteligencia artificial",
            "C++ Project": "Proyecto en C++ con CMake y testing",
            "Node.js Project": "Aplicación Node.js con npm y testing",
            "TD_MCP Project": "Proyecto MCP para integración con TouchDesigner",
            "Otro": "Proyecto personalizado con configuración flexible"
        }
        return descriptions.get(project_type, "Proyecto personalizado")
    
    def _get_characteristic_1(self, project_type: str) -> str:
        """Obtener primera característica del proyecto."""
        characteristics = {
            "Python Library": "Código modular y reutilizable",
            "Python CLI Tool": "Interfaz de línea de comandos intuitiva",
            "Python Web App (Flask)": "Arquitectura web escalable",
            "Python Web App (Django)": "Framework web completo y robusto",
            "Python Web App (FastAPI)": "API REST de alto rendimiento",
            "Python Data Science": "Análisis de datos con pandas y numpy",
            "Python ML/AI": "Modelos de machine learning entrenables",
            "C++ Project": "Código C++ optimizado y eficiente",
            "Node.js Project": "Aplicación JavaScript del lado servidor",
            "TD_MCP Project": "Integración nativa con TouchDesigner",
            "Otro": "Configuración personalizable"
        }
        return characteristics.get(project_type, "Funcionalidad personalizada")
    
    def _get_characteristic_2(self, project_type: str) -> str:
        """Obtener segunda característica del proyecto."""
        characteristics = {
            "Python Library": "Documentación completa y ejemplos",
            "Python CLI Tool": "Configuración flexible y opciones avanzadas",
            "Python Web App (Flask)": "Templates y rutas organizadas",
            "Python Web App (Django)": "Sistema de administración incluido",
            "Python Web App (FastAPI)": "Documentación automática con Swagger",
            "Python Data Science": "Visualizaciones con matplotlib/seaborn",
            "Python ML/AI": "Pipeline de entrenamiento y evaluación",
            "C++ Project": "Sistema de build con CMake",
            "Node.js Project": "Gestión de dependencias con npm",
            "TD_MCP Project": "Protocolo MCP para comunicación",
            "Otro": "Estructura de proyecto profesional"
        }
        return characteristics.get(project_type, "Arquitectura bien definida")
    
    def _get_characteristic_3(self, project_type: str) -> str:
        """Obtener tercera característica del proyecto."""
        characteristics = {
            "Python Library": "Testing completo con pytest",
            "Python CLI Tool": "Logging y manejo de errores robusto",
            "Python Web App (Flask)": "Base de datos integrada",
            "Python Web App (Django)": "ORM potente y migraciones",
            "Python Web App (FastAPI)": "Validación automática de datos",
            "Python Data Science": "Jupyter notebooks incluidos",
            "Python ML/AI": "Modelos exportables y versionados",
            "C++ Project": "Testing con Google Test",
            "Node.js Project": "Testing con Jest",
            "TD_MCP Project": "Configuración JSON flexible",
            "Otro": "Testing y documentación completos"
        }
        return characteristics.get(project_type, "Testing y validación incluidos")
    
    def _get_use_case_1(self, project_type: str) -> str:
        """Obtener primer caso de uso del proyecto."""
        use_cases = {
            "Python Library": "Importar y usar en otros proyectos Python",
            "Python CLI Tool": "Automatizar tareas desde terminal",
            "Python Web App (Flask)": "Desplegar aplicación web en servidor",
            "Python Web App (Django)": "Crear sistema web completo con admin",
            "Python Web App (FastAPI)": "Exponer API REST para frontend/móvil",
            "Python Data Science": "Analizar datasets y generar reportes",
            "Python ML/AI": "Entrenar y desplegar modelos de IA",
            "C++ Project": "Compilar y ejecutar aplicación nativa",
            "Node.js Project": "Ejecutar servidor web o API",
            "TD_MCP Project": "Conectar con TouchDesigner via MCP",
            "Otro": "Implementar funcionalidad específica"
        }
        return use_cases.get(project_type, "Resolver problema específico")
    
    def _get_use_case_2(self, project_type: str) -> str:
        """Obtener segundo caso de uso del proyecto."""
        use_cases = {
            "Python Library": "Distribuir via PyPI o pip",
            "Python CLI Tool": "Integrar en scripts de automatización",
            "Python Web App (Flask)": "Desarrollar API REST simple",
            "Python Web App (Django)": "Crear CMS o sistema de gestión",
            "Python Web App (FastAPI)": "Construir microservicios escalables",
            "Python Data Science": "Crear dashboards interactivos",
            "Python ML/AI": "Integrar en aplicaciones de producción",
            "C++ Project": "Crear bibliotecas de alto rendimiento",
            "Node.js Project": "Desarrollar aplicaciones full-stack",
            "TD_MCP Project": "Crear herramientas para artistas digitales",
            "Otro": "Personalizar según necesidades específicas"
        }
        return use_cases.get(project_type, "Adaptar a requerimientos únicos")
    
    def _get_use_case_3(self, project_type: str) -> str:
        """Obtener tercer caso de uso del proyecto."""
        use_cases = {
            "Python Library": "Contribuir a ecosistema Python",
            "Python CLI Tool": "Crear herramientas de DevOps",
            "Python Web App (Flask)": "Prototipar aplicaciones rápidamente",
            "Python Web App (Django)": "Desarrollar aplicaciones empresariales",
            "Python Web App (FastAPI)": "Construir APIs para IoT o móviles",
            "Python Data Science": "Realizar investigación científica",
            "Python ML/AI": "Crear sistemas de recomendación",
            "C++ Project": "Desarrollar software de sistemas",
            "Node.js Project": "Crear aplicaciones en tiempo real",
            "TD_MCP Project": "Desarrollar instalaciones interactivas",
            "Otro": "Experimentar con nuevas tecnologías"
        }
        return use_cases.get(project_type, "Explorar posibilidades creativas")


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
