"""
Tests unitarios para el script principal init_project.py.

Este módulo contiene tests para el generador de proyectos principal,
incluyendo tests de integración y funcionalidad completa.
"""

import pytest
import tempfile
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import json
import shutil

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Importar el módulo principal
sys.path.insert(0, str(Path(__file__).parent.parent))
from init_project import ProjectGenerator


class TestProjectGenerator:
    """Tests para la clase ProjectGenerator."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.generator = ProjectGenerator(verbose=False)
    
    def test_init(self):
        """Test de inicialización del generador."""
        assert self.generator.template_dir.exists()
        assert self.generator.structure_dir.exists()
        assert self.generator.project_data == {}
        assert self.generator.verbose is False
    
    def test_init_verbose(self):
        """Test de inicialización con modo verbose."""
        generator = ProjectGenerator(verbose=True)
        assert generator.verbose is True
    
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
            result = self.generator._to_pascal_case(input_text)
            assert result == expected, f"'{input_text}' -> '{result}', esperado '{expected}'"
    
    def test_get_dependencies_for_type(self):
        """Test de obtención de dependencias por tipo."""
        test_cases = [
            ("Python Library", "# Dependencias principales"),
            ("Python CLI Tool", "click>=8.0.0"),
            ("Python Web App (Flask)", "flask>=2.0.0"),
            ("Python Web App (Django)", "django>=4.0.0"),
            ("Python Web App (FastAPI)", "fastapi>=0.100.0"),
            ("Python Data Science", "pandas>=1.5.0"),
            ("Python ML/AI", "torch>=1.12.0"),
            ("C++ Project", "# CMake>=3.16"),
            ("Node.js Project", "# express>=4.18.0"),
            ("Otro", "# Añadir según necesidades")
        ]
        
        for project_type, expected_content in test_cases:
            deps = self.generator._get_dependencies_for_type(project_type)
            assert expected_content in deps, f"Tipo '{project_type}' debería contener '{expected_content}'"
    
    def test_get_destination_path_python(self):
        """Test de determinación de ruta de destino para Python."""
        self.generator.project_data = {
            'MODULO_PRINCIPAL': 'test_module',
            'TIPO_PROYECTO': 'Python Library'
        }
        
        project_path = Path("/tmp/test_project")
        
        # Test plantilla Python
        dest_path = self.generator._get_destination_path(
            "modulo_principal.py.tpl", project_path, "Python Library"
        )
        assert dest_path == project_path / "src" / "test_module.py"
        
        # Test plantilla README
        dest_path = self.generator._get_destination_path(
            "README.md.tpl", project_path, "Python Library"
        )
        assert dest_path == project_path / "README.md"
    
    def test_get_destination_path_cpp(self):
        """Test de determinación de ruta de destino para C++."""
        self.generator.project_data = {
            'MODULO_PRINCIPAL': 'test_module',
            'TIPO_PROYECTO': 'C++ Project'
        }
        
        project_path = Path("/tmp/test_project")
        
        # Test plantilla C++ .cpp
        dest_path = self.generator._get_destination_path(
            "modulo_principal_cpp.cpp.tpl", project_path, "C++ Project"
        )
        assert dest_path == project_path / "src" / "test_module.cpp"
        
        # Test plantilla C++ .hpp
        dest_path = self.generator._get_destination_path(
            "modulo_principal_cpp.hpp.tpl", project_path, "C++ Project"
        )
        assert dest_path == project_path / "src" / "test_module.hpp"
        
        # Test CMakeLists.txt
        dest_path = self.generator._get_destination_path(
            "CMakeLists.txt.tpl", project_path, "C++ Project"
        )
        assert dest_path == project_path / "CMakeLists.txt"
    
    def test_get_destination_path_nodejs(self):
        """Test de determinación de ruta de destino para Node.js."""
        self.generator.project_data = {
            'MODULO_PRINCIPAL': 'test_module',
            'TIPO_PROYECTO': 'Node.js Project'
        }
        
        project_path = Path("/tmp/test_project")
        
        # Test plantilla Node.js .js
        dest_path = self.generator._get_destination_path(
            "modulo_principal_nodejs.js.tpl", project_path, "Node.js Project"
        )
        assert dest_path == project_path / "src" / "test_module.js"
        
        # Test package.json
        dest_path = self.generator._get_destination_path(
            "package.json.tpl", project_path, "Node.js Project"
        )
        assert dest_path == project_path / "package.json"
    
    def test_create_project_structure(self):
        """Test de creación de estructura de proyecto."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            
            self.generator.create_project_structure(project_path)
            
            # Verificar que se crearon los directorios
            assert (project_path / "src").exists()
            assert (project_path / "tests").exists()
            assert (project_path / "docs").exists()
            assert (project_path / "examples").exists()
            assert (project_path / "logs").exists()
    
    def test_copy_static_files(self):
        """Test de copia de archivos estáticos."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            project_path.mkdir()
            
            # Crear directorios necesarios
            (project_path / "tests").mkdir()
            
            self.generator.copy_static_files(project_path)
            
            # Verificar que se copiaron los archivos
            assert (project_path / ".gitignore").exists()
            assert (project_path / "tests" / "README.md").exists()
            assert (project_path / "METODOLOGIA_DESARROLLO.md").exists()
    
    def test_process_template(self):
        """Test de procesamiento de plantilla."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            project_path.mkdir()
            (project_path / "src").mkdir()
            
            # Configurar datos del proyecto
            self.generator.project_data = {
                'NOMBRE_PROYECTO': 'TestProject',
                'DESCRIPCION_PROYECTO': 'Proyecto de prueba',
                'MODULO_PRINCIPAL': 'test_module',
                'TIPO_PROYECTO': 'Python Library'
            }
            
            # Crear plantilla de prueba
            template_content = "Proyecto: {{NOMBRE_PROYECTO}}\nDescripción: {{DESCRIPCION_PROYECTO}}"
            template_path = self.generator.template_dir / "test_template.tpl"
            
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            try:
                # Procesar plantilla
                self.generator._process_template(template_path, project_path)
                
                # Verificar que se creó el archivo procesado
                output_file = project_path / "test_template"
                assert output_file.exists()
                
                # Verificar contenido procesado
                with open(output_file, 'r') as f:
                    content = f.read()
                
                assert "Proyecto: TestProject" in content
                assert "Descripción: Proyecto de prueba" in content
                
            finally:
                # Limpiar plantilla de prueba
                if template_path.exists():
                    template_path.unlink()
    
    def test_create_context_file(self):
        """Test de creación de archivo de contexto."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            project_path.mkdir()
            
            # Configurar datos del proyecto
            self.generator.project_data = {
                'NOMBRE_PROYECTO': 'TestProject',
                'DESCRIPCION_PROYECTO': 'Proyecto de prueba',
                'TIPO_PROYECTO': 'Python Library',
                'AUTOR': 'Test Author',
                'FECHA_CREACION': '2024-12-19'
            }
            
            self.generator.create_context_file(project_path)
            
            # Verificar que se creó el archivo
            context_file = project_path / "CONTEXTO.md"
            assert context_file.exists()
            
            # Verificar contenido
            with open(context_file, 'r') as f:
                content = f.read()
            
            assert "TestProject" in content
            assert "Proyecto de prueba" in content
            assert "Python Library" in content
            assert "Test Author" in content
    
    @patch('subprocess.run')
    def test_initialize_git(self, mock_run):
        """Test de inicialización de Git."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            project_path.mkdir()
            
            # Configurar mock para subprocess
            mock_run.return_value = MagicMock(returncode=0)
            
            self.generator.initialize_git(project_path)
            
            # Verificar que se llamaron los comandos Git
            assert mock_run.call_count >= 3  # git init, git add, git commit
            
            # Verificar comandos específicos
            calls = [call[0][0] for call in mock_run.call_args_list]
            assert ['git', 'init'] in calls
            assert ['git', 'add', '.'] in calls
            # Verificar que git commit fue llamado (puede tener argumentos adicionales)
            commit_calls = [call[0][0] for call in mock_run.call_args_list if call[0][0][:2] == ['git', 'commit']]
            assert len(commit_calls) > 0


class TestProjectGeneratorIntegration:
    """Tests de integración para ProjectGenerator."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.generator = ProjectGenerator(verbose=False)
    
    @patch('builtins.input')
    def test_collect_project_info_interactive(self, mock_input):
        """Test de recolección de información interactiva."""
        # Configurar respuestas simuladas
        mock_input.side_effect = [
            "test-project",  # nombre del proyecto
            "Proyecto de prueba",  # descripción corta
            "Descripción detallada del proyecto",  # descripción detallada
            "1",  # tipo de proyecto (Python Library)
            "Test Author",  # autor
            "test@example.com",  # email
            "testuser",  # github user
            "",  # repositorio URL
            "3.8",  # python version
            "MIT",  # licencia
            "Objetivo del proyecto",  # objetivo
            "Funcionalidad principal"  # funcionalidad
        ]
        
        project_data = self.generator.collect_project_info()
        
        # Verificar datos recopilados
        assert project_data['NOMBRE_PROYECTO'] == "test-project"
        assert project_data['DESCRIPCION_PROYECTO'] == "Proyecto de prueba"
        assert project_data['DESCRIPCION_DETALLADA'] == "Descripción detallada del proyecto"
        assert project_data['TIPO_PROYECTO'] == "Python Library"
        assert project_data['AUTOR'] == "Test Author"
        assert project_data['EMAIL_CONTACTO'] == "test@example.com"
        assert project_data['GITHUB_USER'] == "testuser"
        assert project_data['PYTHON_VERSION_MIN'] == "3.8"
        assert project_data['LICENCIA'] == "MIT"
        assert project_data['OBJETIVO_PROYECTO'] == "Objetivo del proyecto"
        assert project_data['FUNCIONALIDAD_PRINCIPAL'] == "Funcionalidad principal"
        
        # Verificar campos generados automáticamente
        assert project_data['MODULO_PRINCIPAL'] == "test_project"
        assert project_data['CLASE_PRINCIPAL'] == "TestProject"
        assert project_data['REPOSITORIO_URL'] == "https://github.com/testuser/test-project"
    
    def test_generate_project_from_config(self):
        """Test de generación de proyecto desde configuración."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Crear archivo de configuración
            config_data = {
                "project_name": "config-test",
                "description": "Proyecto desde configuración",
                "project_type": "Python Library",
                "author": "Config Test Author",
                "email": "config@example.com",
                "github_user": "configuser",
                "python_version_min": "3.8",
                "license": "MIT",
                "objective": "Objetivo desde configuración",
                "main_functionality": "Funcionalidad desde configuración"
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            project_path = Path(temp_dir) / "generated_project"
            
            # Generar proyecto desde configuración
            self.generator.generate_project_from_config(config_path, project_path)
            
            # Verificar que se creó el proyecto
            assert project_path.exists()
            assert (project_path / "src").exists()
            assert (project_path / "tests").exists()
            assert (project_path / "docs").exists()
            assert (project_path / "README.md").exists()
            assert (project_path / "requirements.txt").exists()
            assert (project_path / "CONTEXTO.md").exists()
            
            # Verificar contenido del README
            with open(project_path / "README.md", 'r') as f:
                readme_content = f.read()
            
            assert "config-test" in readme_content
            assert "Proyecto desde configuración" in readme_content
            assert "Config Test Author" in readme_content


class TestProjectGeneratorErrorHandling:
    """Tests de manejo de errores para ProjectGenerator."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.generator = ProjectGenerator(verbose=False)
    
    def test_generate_project_validation_error(self):
        """Test de manejo de errores de validación."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "invalid_project"
            
            # Configurar datos inválidos
            self.generator.project_data = {
                'NOMBRE_PROYECTO': '',  # Inválido
                'DESCRIPCION_PROYECTO': '',  # Inválido
                'TIPO_PROYECTO': 'Invalid Type'  # Inválido
            }
            
            with pytest.raises(SystemExit):
                self.generator.generate_project("invalid_project", project_path)
    
    def test_generate_project_file_exists_error(self):
        """Test de manejo de error cuando el proyecto ya existe."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "existing_project"
            project_path.mkdir()  # Crear directorio existente
            
            # Configurar datos válidos
            self.generator.project_data = {
                'NOMBRE_PROYECTO': 'existing-project',
                'DESCRIPCION_PROYECTO': 'Proyecto existente',
                'TIPO_PROYECTO': 'Python Library',
                'EMAIL_CONTACTO': 'test@example.com',
                'GITHUB_USER': 'testuser',
                'PYTHON_VERSION_MIN': '3.8',
                'LICENCIA': 'MIT'
            }
            
            with pytest.raises(SystemExit):
                self.generator.generate_project("existing_project", project_path)
    
    @patch('subprocess.run')
    def test_initialize_git_error(self, mock_run):
        """Test de manejo de errores en inicialización de Git."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"
            project_path.mkdir()
            
            # Configurar mock para fallar
            mock_run.side_effect = subprocess.CalledProcessError(1, "git")
            
            # No debería lanzar excepción, solo mostrar advertencia
            self.generator.initialize_git(project_path)
            
            # Verificar que se intentó ejecutar git
            assert mock_run.called


class TestProjectGeneratorTemplateProcessing:
    """Tests específicos para procesamiento de plantillas."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.generator = ProjectGenerator(verbose=False)
        self.generator.project_data = {
            'NOMBRE_PROYECTO': 'TemplateTest',
            'DESCRIPCION_PROYECTO': 'Proyecto de prueba de plantillas',
            'TIPO_PROYECTO': 'Python Library',
            'MODULO_PRINCIPAL': 'template_test',
            'CLASE_PRINCIPAL': 'TemplateTest',
            'AUTOR': 'Template Author',
            'EMAIL_CONTACTO': 'template@example.com',
            'GITHUB_USER': 'templateuser',
            'REPOSITORIO_URL': 'https://github.com/templateuser/TemplateTest',
            'PYTHON_VERSION_MIN': '3.8',
            'LICENCIA': 'MIT',
            'FECHA_CREACION': '2024-12-19',
            'FECHA_ACTUALIZACION': '2024-12-19',
            'ESTADO_INICIAL': 'Fase inicial - Configuración',
            'PRIMER_PASO': 'Implementar funcionalidades core',
            'SEGUNDO_PASO': 'Crear tests unitarios',
            'TERCER_PASO': 'Documentar API',
            'SIGUIENTE_PASO': 'Implementar primera funcionalidad',
            'EJEMPLO_USO': '# Crear instancia\ninstancia = TemplateTest()\n# Usar funcionalidad\nresultado = instancia.procesar()',
            'CONFIGURACION_EJEMPLO': '# Configuración para TemplateTest\nDEBUG = True\nLOG_LEVEL = \'INFO\'',
            'DEPENDENCIAS_PRINCIPALES': '# Dependencias principales\n# requests>=2.28.0',
            'DEPENDENCIAS_DESARROLLO': 'pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0',
            'DEPENDENCIAS_TESTING': 'pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0',
            'DEPENDENCIAS_OPCIONALES': '# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0'
        }
    
    def test_process_templates_python(self):
        """Test de procesamiento de plantillas para Python."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "python_project"
            project_path.mkdir()
            (project_path / "src").mkdir()
            (project_path / "docs").mkdir()
            
            self.generator.process_templates(project_path)
            
            # Verificar archivos generados
            assert (project_path / "README.md").exists()
            assert (project_path / "requirements.txt").exists()
            assert (project_path / "src" / "template_test.py").exists()
            assert (project_path / "docs" / "TUTORIAL.md").exists()
            assert (project_path / "BITACORA.md").exists()
            assert (project_path / "roadmap_v1.md").exists()
    
    def test_process_templates_cpp(self):
        """Test de procesamiento de plantillas para C++."""
        self.generator.project_data['TIPO_PROYECTO'] = 'C++ Project'
        
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "cpp_project"
            project_path.mkdir()
            (project_path / "src").mkdir()
            (project_path / "docs").mkdir()
            
            self.generator.process_templates(project_path)
            
            # Verificar archivos generados
            assert (project_path / "README.md").exists()
            assert (project_path / "CMakeLists.txt").exists()
            assert (project_path / "src" / "template_test.cpp").exists()
            assert (project_path / "src" / "template_test.hpp").exists()
            assert (project_path / "docs" / "TUTORIAL.md").exists()
    
    def test_process_templates_nodejs(self):
        """Test de procesamiento de plantillas para Node.js."""
        self.generator.project_data['TIPO_PROYECTO'] = 'Node.js Project'
        
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "nodejs_project"
            project_path.mkdir()
            (project_path / "src").mkdir()
            (project_path / "docs").mkdir()
            
            self.generator.process_templates(project_path)
            
            # Verificar archivos generados
            assert (project_path / "README.md").exists()
            assert (project_path / "package.json").exists()
            assert (project_path / "src" / "template_test.js").exists()
            assert (project_path / "docs" / "TUTORIAL.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
