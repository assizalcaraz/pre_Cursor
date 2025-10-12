"""
Sistema de Validación para el Generador de Proyectos

Este módulo contiene todas las funciones de validación para parámetros
de entrada del generador de proyectos.
"""

import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    pass


class ProjectValidator:
    """Validador de parámetros para proyectos."""
    
    # Patrones de validación
    VALID_PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]*$')
    VALID_EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    VALID_GITHUB_USER_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$')
    VALID_PYTHON_VERSION_PATTERN = re.compile(r'^3\.([8-9]|[1-9][0-9])$')
    
    # Tipos de proyecto válidos
    VALID_PROJECT_TYPES = [
        "Python Library",
        "Python CLI Tool", 
        "Python Web App (Flask)",
        "Python Web App (Django)",
        "Python Web App (FastAPI)",
        "Python Data Science",
        "Python ML/AI",
        "C++ Project",
        "Node.js Project",
        "TD_MCP Project",
        "Otro"
    ]
    
    # Licencias válidas
    VALID_LICENSES = [
        "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", 
        "ISC", "LGPL-3.0", "MPL-2.0", "Unlicense"
    ]
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_project_name(self, name: str) -> bool:
        """
        Validar nombre del proyecto.
        
        Args:
            name: Nombre del proyecto a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not name or not name.strip():
            self.errors.append("El nombre del proyecto es requerido")
            return False
        
        name = name.strip()
        
        # Verificar longitud
        if len(name) < 2:
            self.errors.append("El nombre del proyecto debe tener al menos 2 caracteres")
            return False
        
        if len(name) > 50:
            self.errors.append("El nombre del proyecto no puede exceder 50 caracteres")
            return False
        
        # Verificar patrón
        if not self.VALID_PROJECT_NAME_PATTERN.match(name):
            self.errors.append(
                "El nombre del proyecto debe comenzar con una letra y contener solo "
                "letras, números, guiones y guiones bajos"
            )
            return False
        
        # Verificar palabras reservadas
        reserved_words = [
            "test", "tests", "src", "docs", "examples", "build", "dist",
            "node_modules", ".git", ".github", "venv", "env", "python"
        ]
        
        if name.lower() in reserved_words:
            self.errors.append(f"'{name}' es una palabra reservada y no puede usarse como nombre de proyecto")
            return False
        
        logger.info(f"Nombre del proyecto '{name}' validado correctamente")
        return True
    
    def validate_description(self, description: str) -> bool:
        """
        Validar descripción del proyecto.
        
        Args:
            description: Descripción a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not description or not description.strip():
            self.errors.append("La descripción del proyecto es requerida")
            return False
        
        description = description.strip()
        
        # Verificar longitud mínima
        if len(description) < 10:
            self.errors.append("La descripción debe tener al menos 10 caracteres")
            return False
        
        # Verificar longitud máxima
        if len(description) > 500:
            self.errors.append("La descripción no puede exceder 500 caracteres")
            return False
        
        logger.info("Descripción del proyecto validada correctamente")
        return True
    
    def validate_email(self, email: str) -> bool:
        """
        Validar dirección de email.
        
        Args:
            email: Email a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not email:
            self.warnings.append("Email no proporcionado (opcional)")
            return True
        
        email = email.strip()
        
        if not self.VALID_EMAIL_PATTERN.match(email):
            self.errors.append("Formato de email inválido")
            return False
        
        logger.info(f"Email '{email}' validado correctamente")
        return True
    
    def validate_github_user(self, username: str) -> bool:
        """
        Validar nombre de usuario de GitHub.
        
        Args:
            username: Username de GitHub a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not username:
            self.warnings.append("GitHub username no proporcionado (opcional)")
            return True
        
        username = username.strip()
        
        if not self.VALID_GITHUB_USER_PATTERN.match(username):
            self.errors.append(
                "Username de GitHub inválido. Debe contener solo letras, números "
                "y guiones, comenzar con letra o número, y tener máximo 39 caracteres"
            )
            return False
        
        logger.info(f"GitHub username '{username}' validado correctamente")
        return True
    
    def validate_python_version(self, version: str) -> bool:
        """
        Validar versión de Python.
        
        Args:
            version: Versión de Python a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not version:
            self.warnings.append("Versión de Python no especificada, usando 3.8 por defecto")
            return True
        
        version = version.strip()
        
        if not self.VALID_PYTHON_VERSION_PATTERN.match(version):
            self.errors.append(
                "Versión de Python inválida. Debe ser 3.8 o superior "
                "(formato: 3.x donde x >= 8)"
            )
            return False
        
        logger.info(f"Versión de Python '{version}' validada correctamente")
        return True
    
    def validate_project_type(self, project_type: str) -> bool:
        """
        Validar tipo de proyecto.
        
        Args:
            project_type: Tipo de proyecto a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not project_type:
            self.errors.append("El tipo de proyecto es requerido")
            return False
        
        if project_type not in self.VALID_PROJECT_TYPES:
            self.errors.append(
                f"Tipo de proyecto inválido. Opciones válidas: {', '.join(self.VALID_PROJECT_TYPES)}"
            )
            return False
        
        logger.info(f"Tipo de proyecto '{project_type}' validado correctamente")
        return True
    
    def validate_license(self, license_name: str) -> bool:
        """
        Validar licencia.
        
        Args:
            license_name: Licencia a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not license_name:
            self.warnings.append("Licencia no especificada, usando MIT por defecto")
            return True
        
        if license_name not in self.VALID_LICENSES:
            self.errors.append(
                f"Licencia inválida. Opciones válidas: {', '.join(self.VALID_LICENSES)}"
            )
            return False
        
        logger.info(f"Licencia '{license_name}' validada correctamente")
        return True
    
    def validate_project_path(self, project_path: Path) -> bool:
        """
        Validar ruta del proyecto.
        
        Args:
            project_path: Ruta donde crear el proyecto
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        try:
            # Verificar si el directorio padre existe y es escribible
            parent_dir = project_path.parent
            if not parent_dir.exists():
                self.errors.append(f"El directorio padre '{parent_dir}' no existe")
                return False
            
            if not os.access(parent_dir, os.W_OK):
                self.errors.append(f"Sin permisos de escritura en '{parent_dir}'")
                return False
            
            # Verificar si el proyecto ya existe
            if project_path.exists():
                self.errors.append(f"El directorio '{project_path}' ya existe")
                return False
            
            logger.info(f"Ruta del proyecto '{project_path}' validada correctamente")
            return True
            
        except Exception as e:
            self.errors.append(f"Error validando ruta del proyecto: {e}")
            return False
    
    def validate_all(self, project_data: Dict[str, str], project_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validar todos los parámetros del proyecto.
        
        Args:
            project_data: Diccionario con datos del proyecto
            project_path: Ruta donde crear el proyecto
            
        Returns:
            Tuple[bool, List[str], List[str]]: (es_válido, errores, advertencias)
        """
        self.errors.clear()
        self.warnings.clear()
        
        logger.info("Iniciando validación completa de parámetros del proyecto")
        
        # Validar parámetros básicos
        self.validate_project_name(project_data.get("NOMBRE_PROYECTO", ""))
        self.validate_description(project_data.get("DESCRIPCION_PROYECTO", ""))
        self.validate_project_type(project_data.get("TIPO_PROYECTO", ""))
        
        # Validar parámetros opcionales
        self.validate_email(project_data.get("EMAIL_CONTACTO", ""))
        self.validate_github_user(project_data.get("GITHUB_USER", ""))
        self.validate_python_version(project_data.get("PYTHON_VERSION_MIN", ""))
        self.validate_license(project_data.get("LICENCIA", ""))
        
        # Validar ruta del proyecto
        self.validate_project_path(project_path)
        
        is_valid = len(self.errors) == 0
        
        if is_valid:
            logger.info("Validación completada exitosamente")
        else:
            logger.error(f"Validación fallida con {len(self.errors)} errores")
        
        return is_valid, self.errors.copy(), self.warnings.copy()


def validate_project_data(project_data: Dict[str, str], project_path: Path) -> Tuple[bool, List[str], List[str]]:
    """
    Función de conveniencia para validar datos del proyecto.
    
    Args:
        project_data: Diccionario con datos del proyecto
        project_path: Ruta donde crear el proyecto
        
    Returns:
        Tuple[bool, List[str], List[str]]: (es_válido, errores, advertencias)
    """
    validator = ProjectValidator()
    return validator.validate_all(project_data, project_path)


def print_validation_results(is_valid: bool, errors: List[str], warnings: List[str]) -> None:
    """
    Imprimir resultados de validación de forma legible.
    
    Args:
        is_valid: Si la validación fue exitosa
        errors: Lista de errores
        warnings: Lista de advertencias
    """
    if warnings:
        print("\n⚠️  Advertencias:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if errors:
        print("\n❌ Errores de validación:")
        for error in errors:
            print(f"   • {error}")
        print("\n🔧 Por favor corrige los errores antes de continuar.")
    elif is_valid:
        print("\n✅ Validación exitosa - Todos los parámetros son válidos")


if __name__ == "__main__":
    # Ejemplo de uso
    test_data = {
        "NOMBRE_PROYECTO": "mi-proyecto-test",
        "DESCRIPCION_PROYECTO": "Un proyecto de prueba para validación",
        "TIPO_PROYECTO": "Python Library",
        "EMAIL_CONTACTO": "test@example.com",
        "GITHUB_USER": "testuser",
        "PYTHON_VERSION_MIN": "3.8",
        "LICENCIA": "MIT"
    }
    
    test_path = Path.cwd() / "test_project"
    
    is_valid, errors, warnings = validate_project_data(test_data, test_path)
    print_validation_results(is_valid, errors, warnings)
