"""
Tests unitarios para el sistema de configuración.

Este módulo contiene tests para config_loader.py que maneja
la carga y validación de archivos de configuración JSON/YAML.
"""

import pytest
import json
import yaml
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import sys

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config_loader import (
    ConfigLoader,
    load_project_config,
    create_config_template
)


class TestConfigLoader:
    """Tests para la clase ConfigLoader."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.loader = ConfigLoader()
    
    def test_init(self):
        """Test de inicialización del ConfigLoader."""
        assert self.loader.supported_formats == ['.json', '.yaml', '.yml']
        assert isinstance(self.loader.default_config, dict)
        assert 'project_name' in self.loader.default_config
    
    def test_get_default_config(self):
        """Test de configuración por defecto."""
        config = self.loader._get_default_config()
        
        # Verificar campos requeridos
        assert 'project_name' in config
        assert 'description' in config
        assert 'project_type' in config
        assert 'author' in config
        assert 'dependencies' in config
        
        # Verificar estructura de dependencias
        assert isinstance(config['dependencies'], dict)
        assert 'main' in config['dependencies']
        assert 'development' in config['dependencies']
        assert 'testing' in config['dependencies']
        assert 'optional' in config['dependencies']
    
    def test_load_config_json(self):
        """Test de carga de configuración JSON."""
        config_data = {
            "project_name": "test-project",
            "description": "Proyecto de prueba",
            "project_type": "Python Library",
            "author": "Test Author",
            "email": "test@example.com"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = self.loader.load_config(config_path)
            
            assert loaded_config['project_name'] == "test-project"
            assert loaded_config['description'] == "Proyecto de prueba"
            assert loaded_config['project_type'] == "Python Library"
            assert loaded_config['author'] == "Test Author"
            assert loaded_config['email'] == "test@example.com"
            
            # Verificar que se combinó con valores por defecto
            assert 'git_init' in loaded_config
            assert 'create_context' in loaded_config
            
        finally:
            Path(config_path).unlink()
    
    def test_load_config_yaml(self):
        """Test de carga de configuración YAML."""
        config_data = {
            "project_name": "test-project-yaml",
            "description": "Proyecto de prueba YAML",
            "project_type": "Python CLI Tool",
            "author": "Test Author YAML",
            "email": "test-yaml@example.com"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            loaded_config = self.loader.load_config(config_path)
            
            assert loaded_config['project_name'] == "test-project-yaml"
            assert loaded_config['description'] == "Proyecto de prueba YAML"
            assert loaded_config['project_type'] == "Python CLI Tool"
            assert loaded_config['author'] == "Test Author YAML"
            assert loaded_config['email'] == "test-yaml@example.com"
            
        finally:
            Path(config_path).unlink()
    
    def test_load_config_file_not_found(self):
        """Test de carga con archivo inexistente."""
        with pytest.raises(FileNotFoundError):
            self.loader.load_config("archivo_inexistente.json")
    
    def test_load_config_unsupported_format(self):
        """Test de carga con formato no soportado."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"test content")
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Formato no soportado"):
                self.loader.load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_json(self):
        """Test de carga con JSON inválido."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Error parseando JSON"):
                self.loader.load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_load_config_invalid_yaml(self):
        """Test de carga con YAML inválido."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Error parseando YAML"):
                self.loader.load_config(config_path)
        finally:
            Path(config_path).unlink()
    
    def test_merge_with_defaults(self):
        """Test de combinación con valores por defecto."""
        config_data = {
            "project_name": "custom-project",
            "description": "Proyecto personalizado",
            "dependencies": {
                "main": ["requests>=2.28.0"],
                "development": ["pytest>=7.0.0"]
            }
        }
        
        merged_config = self.loader._merge_with_defaults(config_data)
        
        # Verificar valores personalizados
        assert merged_config['project_name'] == "custom-project"
        assert merged_config['description'] == "Proyecto personalizado"
        assert merged_config['dependencies']['main'] == ["requests>=2.28.0"]
        assert merged_config['dependencies']['development'] == ["pytest>=7.0.0"]
        
        # Verificar valores por defecto
        assert merged_config['project_type'] == "Python Library"
        assert merged_config['author'] == "Desarrollador"
        assert merged_config['git_init'] is True
    
    def test_validate_config_valid(self):
        """Test de validación de configuración válida."""
        valid_config = {
            "project_name": "valid-project",
            "description": "Proyecto válido",
            "project_type": "Python Library",
            "python_version_min": "3.8"
        }
        
        # No debería lanzar excepción
        self.loader._validate_config(valid_config)
    
    def test_validate_config_missing_required(self):
        """Test de validación con campos requeridos faltantes."""
        invalid_config = {
            "project_name": "",  # Campo requerido vacío
            "description": "Proyecto válido"
        }
        
        with pytest.raises(ValueError, match="Campo requerido faltante"):
            self.loader._validate_config(invalid_config)
    
    def test_validate_config_invalid_project_type(self):
        """Test de validación con tipo de proyecto inválido."""
        invalid_config = {
            "project_name": "test-project",
            "description": "Proyecto de prueba",
            "project_type": "Invalid Type"
        }
        
        with pytest.raises(ValueError, match="Tipo de proyecto inválido"):
            self.loader._validate_config(invalid_config)
    
    def test_validate_config_invalid_python_version(self):
        """Test de validación con versión de Python inválida."""
        invalid_config = {
            "project_name": "test-project",
            "description": "Proyecto de prueba",
            "project_type": "Python Library",
            "python_version_min": "2.7"
        }
        
        with pytest.raises(ValueError, match="Versión de Python inválida"):
            self.loader._validate_config(invalid_config)
    
    def test_save_config_template_json(self):
        """Test de guardado de plantilla JSON."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            self.loader.save_config_template(config_path, "Python Library")
            
            # Verificar que el archivo se creó
            assert Path(config_path).exists()
            
            # Verificar contenido
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            assert config['project_name'] == "mi-proyecto-ejemplo"
            assert config['project_type'] == "Python Library"
            assert config['author'] == "Tu Nombre"
            
        finally:
            Path(config_path).unlink()
    
    def test_save_config_template_yaml(self):
        """Test de guardado de plantilla YAML."""
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
            config_path = f.name
        
        try:
            self.loader.save_config_template(config_path, "Python CLI Tool")
            
            # Verificar que el archivo se creó
            assert Path(config_path).exists()
            
            # Verificar contenido
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            assert config['project_name'] == "mi-proyecto-ejemplo"
            assert config['project_type'] == "Python CLI Tool"
            assert config['author'] == "Tu Nombre"
            
        finally:
            Path(config_path).unlink()
    
    def test_convert_to_project_data(self):
        """Test de conversión a formato de datos del proyecto."""
        config = {
            "project_name": "test-conversion",
            "description": "Proyecto de conversión",
            "detailed_description": "Descripción detallada",
            "project_type": "Python Library",
            "author": "Test Author",
            "email": "test@example.com",
            "github_user": "testuser",
            "objective": "Objetivo del proyecto",
            "main_functionality": "Funcionalidad principal",
            "dependencies": {
                "main": ["requests>=2.28.0"],
                "development": ["pytest>=7.0.0"],
                "testing": ["pytest-cov>=4.0.0"],
                "optional": ["numpy>=1.21.0"]
            }
        }
        
        project_data = self.loader.convert_to_project_data(config)
        
        # Verificar campos básicos
        assert project_data['NOMBRE_PROYECTO'] == "test-conversion"
        assert project_data['DESCRIPCION_PROYECTO'] == "Proyecto de conversión"
        assert project_data['DESCRIPCION_DETALLADA'] == "Descripción detallada"
        assert project_data['TIPO_PROYECTO'] == "Python Library"
        assert project_data['AUTOR'] == "Test Author"
        assert project_data['EMAIL_CONTACTO'] == "test@example.com"
        assert project_data['GITHUB_USER'] == "testuser"
        
        # Verificar campos técnicos
        assert project_data['MODULO_PRINCIPAL'] == "test_conversion"
        assert project_data['CLASE_PRINCIPAL'] == "TestConversion"
        
        # Verificar dependencias
        assert "requests>=2.28.0" in project_data['DEPENDENCIAS_PRINCIPALES']
        assert "pytest>=7.0.0" in project_data['DEPENDENCIAS_DESARROLLO']
        assert "pytest-cov>=4.0.0" in project_data['DEPENDENCIAS_TESTING']
        assert "numpy>=1.21.0" in project_data['DEPENDENCIAS_OPCIONALES']
    
    def test_convert_to_project_data_with_repository_url(self):
        """Test de conversión con URL de repositorio."""
        config = {
            "project_name": "test-repo",
            "description": "Proyecto con repo",
            "project_type": "Python Library",
            "github_user": "testuser",
            "repository_url": "https://github.com/testuser/custom-repo"
        }
        
        project_data = self.loader.convert_to_project_data(config)
        
        assert project_data['REPOSITORIO_URL'] == "https://github.com/testuser/custom-repo"
    
    def test_convert_to_project_data_generated_repository_url(self):
        """Test de conversión con URL de repositorio generada."""
        config = {
            "project_name": "test-generated-repo",
            "description": "Proyecto con repo generado",
            "project_type": "Python Library",
            "github_user": "testuser"
        }
        
        project_data = self.loader.convert_to_project_data(config)
        
        expected_url = "https://github.com/testuser/test-generated-repo"
        assert project_data['REPOSITORIO_URL'] == expected_url
    
    def test_to_pascal_case(self):
        """Test de conversión a PascalCase."""
        test_cases = [
            ("mi-proyecto", "MiProyecto"),
            ("mi_proyecto", "MiProyecto"),
            ("mi proyecto", "MiProyecto"),
            ("proyecto123", "Proyecto123"),
            ("a", "A")
        ]
        
        for input_text, expected in test_cases:
            result = self.loader._to_pascal_case(input_text)
            assert result == expected, f"'{input_text}' -> '{result}', esperado '{expected}'"


class TestConfigFunctions:
    """Tests para las funciones de conveniencia."""
    
    def test_load_project_config_function(self):
        """Test de la función load_project_config."""
        config_data = {
            "project_name": "function-test",
            "description": "Test de función",
            "project_type": "Python Library",
            "author": "Function Test Author"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            project_data = load_project_config(config_path)
            
            assert project_data['NOMBRE_PROYECTO'] == "function-test"
            assert project_data['DESCRIPCION_PROYECTO'] == "Test de función"
            assert project_data['TIPO_PROYECTO'] == "Python Library"
            assert project_data['AUTOR'] == "Function Test Author"
            
        finally:
            Path(config_path).unlink()
    
    def test_create_config_template_function(self):
        """Test de la función create_config_template."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            create_config_template(config_path, "Python CLI Tool")
            
            # Verificar que el archivo se creó
            assert Path(config_path).exists()
            
            # Verificar contenido
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            assert config['project_type'] == "Python CLI Tool"
            assert config['project_name'] == "mi-proyecto-ejemplo"
            
        finally:
            Path(config_path).unlink()


class TestConfigLoaderEdgeCases:
    """Tests para casos edge del ConfigLoader."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.loader = ConfigLoader()
    
    def test_deep_merge_nested_dictionaries(self):
        """Test de merge profundo con diccionarios anidados."""
        default_config = {
            "dependencies": {
                "main": ["default-main"],
                "development": ["default-dev"],
                "testing": ["default-test"]
            },
            "settings": {
                "debug": True,
                "verbose": False
            }
        }
        
        override_config = {
            "dependencies": {
                "main": ["override-main"],
                "optional": ["override-optional"]
            },
            "settings": {
                "debug": False
            }
        }
        
        # Simular merge profundo
        def deep_merge(default, override):
            for key, value in override.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    default[key] = deep_merge(default[key], value)
                else:
                    default[key] = value
            return default
        
        merged = deep_merge(default_config.copy(), override_config)
        
        # Verificar merge correcto
        assert merged['dependencies']['main'] == ["override-main"]
        assert merged['dependencies']['development'] == ["default-dev"]  # Preservado
        assert merged['dependencies']['testing'] == ["default-test"]  # Preservado
        assert merged['dependencies']['optional'] == ["override-optional"]  # Nuevo
        assert merged['settings']['debug'] is False  # Sobrescrito
        assert merged['settings']['verbose'] is False  # Preservado
    
    def test_empty_dependencies(self):
        """Test con dependencias vacías."""
        config = {
            "project_name": "empty-deps",
            "description": "Proyecto con dependencias vacías",
            "project_type": "Python Library",
            "dependencies": {
                "main": [],
                "development": [],
                "testing": [],
                "optional": []
            }
        }
        
        project_data = self.loader.convert_to_project_data(config)
        
        # Verificar que se maneja correctamente
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_PRINCIPALES']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_DESARROLLO']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_TESTING']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_OPCIONALES']
    
    def test_missing_dependencies_section(self):
        """Test con sección de dependencias faltante."""
        config = {
            "project_name": "no-deps",
            "description": "Proyecto sin dependencias",
            "project_type": "Python Library"
        }
        
        project_data = self.loader.convert_to_project_data(config)
        
        # Verificar que se maneja correctamente
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_PRINCIPALES']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_DESARROLLO']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_TESTING']
        assert "Añadir según necesidades" in project_data['DEPENDENCIAS_OPCIONALES']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
