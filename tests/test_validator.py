"""
Tests unitarios para el sistema de validación.

Este módulo contiene tests para validator.py que validan
todos los parámetros de entrada del generador de proyectos.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validator import (
    ProjectValidator, 
    ValidationError, 
    validate_project_data, 
    print_validation_results
)


class TestProjectValidator:
    """Tests para la clase ProjectValidator."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.validator = ProjectValidator()
    
    def test_init(self):
        """Test de inicialización del validador."""
        assert self.validator.errors == []
        assert self.validator.warnings == []
    
    def test_validate_project_name_valid(self):
        """Test de validación de nombres de proyecto válidos."""
        valid_names = [
            "mi-proyecto",
            "MiProyecto123",
            "proyecto_test",
            "ab",  # Mínimo 2 caracteres
            "proyecto-con-guiones",
            "proyecto_con_guiones_bajos"
        ]
        
        for name in valid_names:
            validator = ProjectValidator()
            assert validator.validate_project_name(name), f"Nombre '{name}' debería ser válido"
            assert len(validator.errors) == 0
    
    def test_validate_project_name_invalid(self):
        """Test de validación de nombres de proyecto inválidos."""
        invalid_cases = [
            ("", "nombre vacío"),
            ("a", "nombre muy corto (1 carácter)"),
            ("123proyecto", "comienza con número"),
            ("proyecto@test", "contiene caracteres especiales"),
            ("proyecto test", "contiene espacios"),
            ("test", "palabra reservada"),
            ("src", "palabra reservada"),
            ("docs", "palabra reservada")
        ]
        
        for name, description in invalid_cases:
            validator = ProjectValidator()
            result = validator.validate_project_name(name)
            assert not result, f"Nombre '{name}' ({description}) debería ser inválido"
            assert len(validator.errors) > 0
    
    def test_validate_project_name_length(self):
        """Test de validación de longitud de nombres."""
        # Nombre muy largo
        long_name = "a" * 51
        validator = ProjectValidator()
        assert not validator.validate_project_name(long_name)
        assert any("50 caracteres" in error for error in validator.errors)
    
    def test_validate_description_valid(self):
        """Test de validación de descripciones válidas."""
        valid_descriptions = [
            "Una descripción válida de proyecto",
            "Proyecto para procesamiento de datos con machine learning",
            "A" * 500  # Longitud máxima
        ]
        
        for desc in valid_descriptions:
            validator = ProjectValidator()
            assert validator.validate_description(desc)
            assert len(validator.errors) == 0
    
    def test_validate_description_invalid(self):
        """Test de validación de descripciones inválidas."""
        invalid_cases = [
            ("", "descripción vacía"),
            ("Corta", "descripción muy corta"),
            ("A" * 501, "descripción muy larga")
        ]
        
        for desc, description in invalid_cases:
            validator = ProjectValidator()
            result = validator.validate_description(desc)
            assert not result, f"Descripción '{desc}' ({description}) debería ser inválida"
            assert len(validator.errors) > 0
    
    def test_validate_email_valid(self):
        """Test de validación de emails válidos."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com"
        ]
        
        for email in valid_emails:
            validator = ProjectValidator()
            assert validator.validate_email(email)
            assert len(validator.errors) == 0
    
    def test_validate_email_invalid(self):
        """Test de validación de emails inválidos."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test@.com"
        ]
        
        for email in invalid_emails:
            validator = ProjectValidator()
            result = validator.validate_email(email)
            assert not result, f"Email '{email}' debería ser inválido"
            assert len(validator.errors) > 0
    
    def test_validate_email_optional(self):
        """Test de validación de email opcional."""
        validator = ProjectValidator()
        assert validator.validate_email("")  # Email vacío es válido (opcional)
        assert len(validator.warnings) > 0  # Debería generar advertencia
    
    def test_validate_github_user_valid(self):
        """Test de validación de GitHub usernames válidos."""
        valid_usernames = [
            "testuser",
            "test-user",
            "test123",
            "a",  # Username mínimo
            "a" * 39  # Username máximo
        ]
        
        for username in valid_usernames:
            validator = ProjectValidator()
            assert validator.validate_github_user(username)
            assert len(validator.errors) == 0
    
    def test_validate_github_user_invalid(self):
        """Test de validación de GitHub usernames inválidos."""
        invalid_usernames = [
            "-testuser",  # Comienza con guión
            "testuser-",  # Termina con guión
            "test--user",  # Guiones consecutivos
            "a" * 40,  # Muy largo
            "test@user",  # Caracteres especiales
            "test user"  # Espacios
        ]
        
        for username in invalid_usernames:
            validator = ProjectValidator()
            result = validator.validate_github_user(username)
            assert not result, f"Username '{username}' debería ser inválido"
            assert len(validator.errors) > 0
    
    def test_validate_python_version_valid(self):
        """Test de validación de versiones de Python válidas."""
        valid_versions = [
            "3.8",
            "3.9",
            "3.10",
            "3.11",
            "3.12",
            "3.99"
        ]
        
        for version in valid_versions:
            validator = ProjectValidator()
            assert validator.validate_python_version(version)
            assert len(validator.errors) == 0
    
    def test_validate_python_version_invalid(self):
        """Test de validación de versiones de Python inválidas."""
        invalid_versions = [
            "2.7",  # Versión muy antigua
            "3.7",  # Versión muy antigua
            "3",  # Formato incorrecto
            "3.8.1",  # Formato incorrecto
            "python3.8",  # Formato incorrecto
            "4.0"  # Versión futura
        ]
        
        for version in invalid_versions:
            validator = ProjectValidator()
            result = validator.validate_python_version(version)
            assert not result, f"Versión '{version}' debería ser inválida"
            assert len(validator.errors) > 0
    
    def test_validate_project_type_valid(self):
        """Test de validación de tipos de proyecto válidos."""
        valid_types = ProjectValidator.VALID_PROJECT_TYPES
        
        for project_type in valid_types:
            validator = ProjectValidator()
            assert validator.validate_project_type(project_type)
            assert len(validator.errors) == 0
    
    def test_validate_project_type_invalid(self):
        """Test de validación de tipos de proyecto inválidos."""
        invalid_types = [
            "Invalid Type",
            "Python App",
            "JavaScript Project",
            ""
        ]
        
        for project_type in invalid_types:
            validator = ProjectValidator()
            result = validator.validate_project_type(project_type)
            assert not result, f"Tipo '{project_type}' debería ser inválido"
            assert len(validator.errors) > 0
    
    def test_validate_license_valid(self):
        """Test de validación de licencias válidas."""
        valid_licenses = ProjectValidator.VALID_LICENSES
        
        for license_name in valid_licenses:
            validator = ProjectValidator()
            assert validator.validate_license(license_name)
            assert len(validator.errors) == 0
    
    def test_validate_license_invalid(self):
        """Test de validación de licencias inválidas."""
        invalid_licenses = [
            "Invalid License",
            "Custom License",
            "GPL"
        ]
        
        for license_name in invalid_licenses:
            validator = ProjectValidator()
            result = validator.validate_license(license_name)
            assert not result, f"Licencia '{license_name}' debería ser inválida"
            assert len(validator.errors) > 0
    
    def test_validate_project_path_valid(self):
        """Test de validación de rutas de proyecto válidas."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_path = temp_path / "nuevo_proyecto"
            
            validator = ProjectValidator()
            assert validator.validate_project_path(project_path)
            assert len(validator.errors) == 0
    
    def test_validate_project_path_invalid(self):
        """Test de validación de rutas de proyecto inválidas."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Directorio padre no existe
            invalid_path = temp_path / "inexistente" / "proyecto"
            validator = ProjectValidator()
            assert not validator.validate_project_path(invalid_path)
            assert len(validator.errors) > 0
    
    def test_validate_project_path_exists(self):
        """Test de validación cuando el proyecto ya existe."""
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_path = Path(temp_dir) / "proyecto_existente"
            existing_path.mkdir()
            
            validator = ProjectValidator()
            assert not validator.validate_project_path(existing_path)
            assert len(validator.errors) > 0
            assert any("ya existe" in error for error in validator.errors)
    
    @patch('os.access')
    def test_validate_project_path_no_permission(self, mock_access):
        """Test de validación sin permisos de escritura."""
        mock_access.return_value = False
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_path = temp_path / "nuevo_proyecto"
            
            validator = ProjectValidator()
            assert not validator.validate_project_path(project_path)
            assert len(validator.errors) > 0
            assert any("permisos" in error for error in validator.errors)
    
    def test_validate_all_valid(self):
        """Test de validación completa con datos válidos."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_path = temp_path / "proyecto_valido"
            
            project_data = {
                "NOMBRE_PROYECTO": "proyecto-valido",
                "DESCRIPCION_PROYECTO": "Un proyecto de prueba válido",
                "TIPO_PROYECTO": "Python Library",
                "EMAIL_CONTACTO": "test@example.com",
                "GITHUB_USER": "testuser",
                "PYTHON_VERSION_MIN": "3.8",
                "LICENCIA": "MIT"
            }
            
            validator = ProjectValidator()
            is_valid, errors, warnings = validator.validate_all(project_data, project_path)
            
            assert is_valid
            assert len(errors) == 0
            # Puede haber advertencias para campos opcionales
    
    def test_validate_all_invalid(self):
        """Test de validación completa con datos inválidos."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_path = temp_path / "proyecto_invalido"
            
            project_data = {
                "NOMBRE_PROYECTO": "",  # Inválido
                "DESCRIPCION_PROYECTO": "",  # Inválido
                "TIPO_PROYECTO": "Invalid Type",  # Inválido
                "EMAIL_CONTACTO": "invalid-email",  # Inválido
                "GITHUB_USER": "-invalid-user",  # Inválido
                "PYTHON_VERSION_MIN": "2.7",  # Inválido
                "LICENCIA": "Invalid License"  # Inválido
            }
            
            validator = ProjectValidator()
            is_valid, errors, warnings = validator.validate_all(project_data, project_path)
            
            assert not is_valid
            assert len(errors) > 0


class TestValidationFunctions:
    """Tests para las funciones de conveniencia."""
    
    def test_validate_project_data_function(self):
        """Test de la función validate_project_data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_path = temp_path / "proyecto_test"
            
            project_data = {
                "NOMBRE_PROYECTO": "proyecto-test",
                "DESCRIPCION_PROYECTO": "Proyecto de prueba",
                "TIPO_PROYECTO": "Python Library",
                "EMAIL_CONTACTO": "test@example.com",
                "GITHUB_USER": "testuser",
                "PYTHON_VERSION_MIN": "3.8",
                "LICENCIA": "MIT"
            }
            
            is_valid, errors, warnings = validate_project_data(project_data, project_path)
            
            assert is_valid
            assert len(errors) == 0
    
    @patch('builtins.print')
    def test_print_validation_results(self, mock_print):
        """Test de la función print_validation_results."""
        errors = ["Error 1", "Error 2"]
        warnings = ["Warning 1"]
        
        print_validation_results(False, errors, warnings)
        
        # Verificar que se llamó print
        assert mock_print.called
        
        # Verificar contenido de las llamadas
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        print_content = " ".join(print_calls)
        
        assert "Errores de validación" in print_content
        assert "Error 1" in print_content
        assert "Error 2" in print_content
        assert "Advertencias" in print_content
        assert "Warning 1" in print_content


class TestValidationError:
    """Tests para la excepción ValidationError."""
    
    def test_validation_error_creation(self):
        """Test de creación de ValidationError."""
        error = ValidationError("Mensaje de error")
        assert str(error) == "Mensaje de error"
    
    def test_validation_error_inheritance(self):
        """Test de herencia de ValidationError."""
        error = ValidationError("Test error")
        assert isinstance(error, Exception)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
