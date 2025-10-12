"""
Tests de integración para el generador de proyectos.

Este módulo contiene tests que ejecutan init_project.py completo
y verifican la integridad de la estructura y archivos resultantes.
"""

import pytest
import tempfile
import subprocess
import sys
import json
import yaml
from pathlib import Path
from unittest.mock import patch
import shutil

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestProjectGeneratorIntegration:
    """Tests de integración para el generador completo."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.project_root = Path(__file__).parent.parent
    
    def test_generate_python_library_project(self):
        """Test de generación completa de proyecto Python Library."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test_python_lib"
            project_path = Path(temp_dir) / project_name
            
            # Crear configuración para proyecto Python
            config_data = {
                "project_name": project_name,
                "description": "Librería Python de prueba",
                "detailed_description": "Una librería Python completa para testing",
                "project_type": "Python Library",
                "author": "Test Author",
                "email": "test@example.com",
                "github_user": "testuser",
                "python_version_min": "3.8",
                "license": "MIT",
                "objective": "Demostrar generación de librería Python",
                "main_functionality": "Procesamiento de datos",
                "dependencies": {
                    "main": ["requests>=2.28.0", "numpy>=1.21.0"],
                    "development": ["pytest>=7.0.0", "black>=22.0.0"],
                    "testing": ["pytest-cov>=4.0.0", "pytest-asyncio>=0.21.0"],
                    "optional": ["pandas>=1.5.0"]
                }
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Ejecutar generador
            init_script = Path(__file__).parent.parent / "init_project.py"
            result = subprocess.run([
                sys.executable, str(init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            # Verificar éxito
            assert result.returncode == 0, f"Error: {result.stderr}"
            
            # Verificar estructura del proyecto
            assert project_path.exists()
            assert (project_path / "src").exists()
            assert (project_path / "tests").exists()
            assert (project_path / "docs").exists()
            assert (project_path / "examples").exists()
            assert (project_path / "logs").exists()
            
            # Verificar archivos principales
            assert (project_path / "README.md").exists()
            assert (project_path / "requirements.txt").exists()
            assert (project_path / "BITACORA.md").exists()
            assert (project_path / "roadmap_v1.md").exists()
            assert (project_path / "CONTEXTO.md").exists()
            assert (project_path / "METODOLOGIA_DESARROLLO.md").exists()
            
            # Verificar archivos específicos de Python
            assert (project_path / "src" / f"{project_name}.py").exists()
            assert (project_path / "tests" / "README.md").exists()
            assert (project_path / "docs" / "TUTORIAL.md").exists()
            
            # Verificar contenido del README
            with open(project_path / "README.md", 'r') as f:
                readme_content = f.read()
            
            assert project_name in readme_content
            assert "Librería Python de prueba" in readme_content
            assert "Test Author" in readme_content
            assert "MIT" in readme_content
            
            # Verificar contenido de requirements.txt
            with open(project_path / "requirements.txt", 'r') as f:
                requirements_content = f.read()
            
            assert "requests>=2.28.0" in requirements_content
            assert "numpy>=1.21.0" in requirements_content
            
            # Verificar contenido del módulo principal
            module_file = project_path / "src" / f"{project_name}.py"
            with open(module_file, 'r') as f:
                module_content = f.read()
            
            assert f"class {project_name.title().replace('_', '')}" in module_content
            assert "Test Author" in module_content
    
    def test_generate_cpp_project(self):
        """Test de generación completa de proyecto C++."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test_cpp_project"
            project_path = Path(temp_dir) / project_name
            
            # Crear configuración para proyecto C++
            config_data = {
                "project_name": project_name,
                "description": "Proyecto C++ de prueba",
                "detailed_description": "Un proyecto C++ completo con CMake",
                "project_type": "C++ Project",
                "author": "C++ Test Author",
                "email": "cpp@example.com",
                "github_user": "cppuser",
                "python_version_min": "3.8",  # No aplica pero necesario
                "license": "MIT",
                "objective": "Demostrar generación de proyecto C++",
                "main_functionality": "Procesamiento de datos C++"
            }
            
            config_path = Path(temp_dir) / "config.yaml"
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f)
            
            # Ejecutar generador
            init_script = Path(__file__).parent.parent / "init_project.py"
            result = subprocess.run([
                sys.executable, str(init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            # Verificar éxito
            assert result.returncode == 0, f"Error: {result.stderr}"
            
            # Verificar estructura del proyecto
            assert project_path.exists()
            assert (project_path / "src").exists()
            assert (project_path / "tests").exists()
            assert (project_path / "docs").exists()
            
            # Verificar archivos específicos de C++
            assert (project_path / "CMakeLists.txt").exists()
            assert (project_path / "src" / f"{project_name}.cpp").exists()
            assert (project_path / "src" / f"{project_name}.hpp").exists()
            
            # Verificar contenido del CMakeLists.txt
            with open(project_path / "CMakeLists.txt", 'r') as f:
                cmake_content = f.read()
            
            assert "cmake_minimum_required(VERSION 3.16)" in cmake_content
            assert f"project({project_name}" in cmake_content
            assert "CMAKE_CXX_STANDARD 17" in cmake_content
            
            # Verificar contenido del header
            header_file = project_path / "src" / f"{project_name}.hpp"
            with open(header_file, 'r') as f:
                header_content = f.read()
            
            assert f"class {project_name.title().replace('_', '')}" in header_content
            assert "#ifndef" in header_content
            assert "#define" in header_content
            assert "#endif" in header_content
    
    def test_generate_nodejs_project(self):
        """Test de generación completa de proyecto Node.js."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "test-nodejs-project"
            project_path = Path(temp_dir) / project_name
            
            # Crear configuración para proyecto Node.js
            config_data = {
                "project_name": project_name,
                "description": "Proyecto Node.js de prueba",
                "detailed_description": "Un proyecto Node.js completo con package.json",
                "project_type": "Node.js Project",
                "author": "Node.js Test Author",
                "email": "nodejs@example.com",
                "github_user": "nodejsuser",
                "python_version_min": "3.8",  # No aplica pero necesario
                "license": "MIT",
                "objective": "Demostrar generación de proyecto Node.js",
                "main_functionality": "API REST con Express",
                "dependencies": {
                    "main": ["express>=4.18.0", "cors>=2.8.5"],
                    "development": ["nodemon>=2.0.0", "jest>=29.0.0"],
                    "testing": ["supertest>=6.0.0"],
                    "optional": ["mongoose>=6.0.0"]
                }
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Ejecutar generador
            init_script = Path(__file__).parent.parent / "init_project.py"
            result = subprocess.run([
                sys.executable, str(init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            # Verificar éxito
            assert result.returncode == 0, f"Error: {result.stderr}"
            
            # Verificar estructura del proyecto
            assert project_path.exists()
            assert (project_path / "src").exists()
            assert (project_path / "tests").exists()
            assert (project_path / "docs").exists()
            
            # Verificar archivos específicos de Node.js
            assert (project_path / "package.json").exists()
            # Para Node.js, el módulo principal mantiene guiones
            assert (project_path / "src" / f"{project_name}.js").exists()
            
            # Verificar contenido del package.json
            with open(project_path / "package.json", 'r') as f:
                package_content = json.load(f)
            
            assert package_content["name"] == project_name
            assert package_content["description"] == "Proyecto Node.js de prueba"
            assert package_content["author"] == "Node.js Test Author"
            assert package_content["license"] == "MIT"
            assert "express" in package_content["dependencies"]
            assert "nodemon" in package_content["devDependencies"]
            
            # Verificar contenido del módulo principal
            module_file = project_path / "src" / f"{project_name}.js"
            with open(module_file, 'r') as f:
                module_content = f.read()
            
            assert f"class {project_name.title().replace('-', '')}" in module_content
            assert "Node.js Test Author" in module_content
    
    def test_generate_project_with_invalid_config(self):
        """Test de manejo de configuración inválida."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Crear configuración inválida
            invalid_config = {
                "project_name": "",  # Inválido
                "description": "",  # Inválido
                "project_type": "Invalid Type"  # Inválido
            }
            
            config_path = Path(temp_dir) / "invalid_config.json"
            with open(config_path, 'w') as f:
                json.dump(invalid_config, f)
            
            # Ejecutar generador
            init_script = Path(__file__).parent.parent / "init_project.py"
            result = subprocess.run([
                sys.executable, str(init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            # Verificar que falló
            assert result.returncode != 0
            assert "Error" in result.stderr or "Error" in result.stdout
    
    def test_create_config_template(self):
        """Test de creación de plantillas de configuración."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = Path(temp_dir) / "template.json"
            
            # Crear plantilla
            result = subprocess.run([
                sys.executable, str(self.init_script),
                "--create-template", "Python Library",
                "--template-output", str(template_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            # Verificar éxito
            assert result.returncode == 0, f"Error: {result.stderr}"
            
            # Verificar que se creó la plantilla
            assert template_path.exists()
            
            # Verificar contenido
            with open(template_path, 'r') as f:
                template_content = json.load(f)
            
            assert template_content["project_type"] == "Python Library"
            assert template_content["project_name"] == "mi-proyecto-ejemplo"
            assert "dependencies" in template_content
            assert "features" in template_content
    
    def test_generate_project_interactive_mode(self):
        """Test de modo interactivo (simulado)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "interactive_test"
            
            # Simular entrada interactiva
            input_responses = [
                project_name,  # nombre del proyecto
                "Proyecto interactivo",  # descripción corta
                "Descripción detallada",  # descripción detallada
                "1",  # tipo de proyecto (Python Library)
                "Interactive Author",  # autor
                "interactive@example.com",  # email
                "interactiveuser",  # github user
                "",  # repositorio URL
                "3.8",  # python version
                "MIT",  # licencia
                "Objetivo interactivo",  # objetivo
                "Funcionalidad interactiva"  # funcionalidad
            ]
            
            # Ejecutar con entrada simulada
            process = subprocess.Popen([
                sys.executable, str(self.init_script)
            ], cwd=temp_dir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
               stderr=subprocess.PIPE, text=True)
            
            # Enviar respuestas
            input_data = "\n".join(input_responses) + "\n"
            stdout, stderr = process.communicate(input=input_data)
            
            # Verificar éxito
            assert process.returncode == 0, f"Error: {stderr}"
            
            # Verificar que se creó el proyecto
            project_path = Path(temp_dir) / project_name
            assert project_path.exists()
            assert (project_path / "README.md").exists()
            assert (project_path / "src").exists()


class TestProjectValidation:
    """Tests de validación de proyectos generados."""
    
    def setup_method(self):
        """Configurar antes de cada test."""
        self.project_root = Path(__file__).parent.parent
    
    def test_python_project_compilation(self):
        """Test de que el proyecto Python generado es válido."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "compilation_test"
            
            # Generar proyecto Python
            config_data = {
                "project_name": project_name,
                "description": "Proyecto para test de compilación",
                "project_type": "Python Library",
                "author": "Compilation Test",
                "email": "compilation@example.com",
                "github_user": "compilationuser",
                "python_version_min": "3.8",
                "license": "MIT"
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Generar proyecto
            result = subprocess.run([
                sys.executable, str(self.init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            assert result.returncode == 0
            
            project_path = Path(temp_dir) / project_name
            
            # Verificar que el módulo Python es válido
            module_file = project_path / "src" / f"{project_name}.py"
            assert module_file.exists()
            
            # Intentar importar el módulo (verificar sintaxis)
            import sys
            sys.path.insert(0, str(project_path / "src"))
            
            try:
                module = __import__(project_name)
                assert hasattr(module, project_name.title().replace('_', ''))
            except ImportError as e:
                pytest.fail(f"No se pudo importar el módulo: {e}")
    
    def test_cpp_project_cmake_configuration(self):
        """Test de que el proyecto C++ tiene configuración CMake válida."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "cmake_test"
            
            # Generar proyecto C++
            config_data = {
                "project_name": project_name,
                "description": "Proyecto C++ para test de CMake",
                "project_type": "C++ Project",
                "author": "CMake Test",
                "email": "cmake@example.com",
                "github_user": "cmakeuser",
                "python_version_min": "3.8",
                "license": "MIT"
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Generar proyecto
            result = subprocess.run([
                sys.executable, str(self.init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            assert result.returncode == 0
            
            project_path = Path(temp_dir) / project_name
            
            # Verificar archivos C++
            cpp_file = project_path / "src" / f"{project_name}.cpp"
            hpp_file = project_path / "src" / f"{project_name}.hpp"
            cmake_file = project_path / "CMakeLists.txt"
            
            assert cpp_file.exists()
            assert hpp_file.exists()
            assert cmake_file.exists()
            
            # Verificar que CMakeLists.txt es válido
            with open(cmake_file, 'r') as f:
                cmake_content = f.read()
            
            # Verificar elementos básicos de CMake
            assert "cmake_minimum_required" in cmake_content
            assert "project(" in cmake_content
            assert "CMAKE_CXX_STANDARD" in cmake_content
            assert "add_library" in cmake_content or "add_executable" in cmake_content
    
    def test_nodejs_project_package_json_validity(self):
        """Test de que el proyecto Node.js tiene package.json válido."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_name = "nodejs_test"
            
            # Generar proyecto Node.js
            config_data = {
                "project_name": project_name,
                "description": "Proyecto Node.js para test",
                "project_type": "Node.js Project",
                "author": "Node.js Test",
                "email": "nodejs@example.com",
                "github_user": "nodejsuser",
                "python_version_min": "3.8",
                "license": "MIT",
                "dependencies": {
                    "main": ["express>=4.18.0"],
                    "development": ["nodemon>=2.0.0"]
                }
            }
            
            config_path = Path(temp_dir) / "config.json"
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Generar proyecto
            result = subprocess.run([
                sys.executable, str(self.init_script),
                "--config", str(config_path)
            ], cwd=temp_dir, capture_output=True, text=True)
            
            assert result.returncode == 0
            
            project_path = Path(temp_dir) / project_name
            
            # Verificar package.json
            package_file = project_path / "package.json"
            assert package_file.exists()
            
            # Verificar que es JSON válido
            with open(package_file, 'r') as f:
                package_data = json.load(f)
            
            # Verificar campos requeridos
            assert "name" in package_data
            assert "version" in package_data
            assert "description" in package_data
            assert "main" in package_data
            assert "scripts" in package_data
            assert "dependencies" in package_data
            assert "devDependencies" in package_data
            
            # Verificar valores específicos
            assert package_data["name"] == project_name
            assert package_data["description"] == "Proyecto Node.js para test"
            assert package_data["author"] == "Node.js Test"
            assert package_data["license"] == "MIT"
    
    def test_project_structure_completeness(self):
        """Test de que todos los proyectos tienen estructura completa."""
        project_types = ["Python Library", "C++ Project", "Node.js Project"]
        
        for project_type in project_types:
            with tempfile.TemporaryDirectory() as temp_dir:
                project_name = f"structure_test_{project_type.lower().replace(' ', '_')}"
                
                # Generar proyecto
                config_data = {
                    "project_name": project_name,
                    "description": f"Proyecto {project_type} para test de estructura",
                    "project_type": project_type,
                    "author": "Structure Test",
                    "email": "structure@example.com",
                    "github_user": "structureuser",
                    "python_version_min": "3.8",
                    "license": "MIT"
                }
                
                config_path = Path(temp_dir) / "config.json"
                with open(config_path, 'w') as f:
                    json.dump(config_data, f)
                
                # Generar proyecto
                result = subprocess.run([
                    sys.executable, str(self.init_script),
                    "--config", str(config_path)
                ], cwd=temp_dir, capture_output=True, text=True)
                
                assert result.returncode == 0, f"Error generando {project_type}: {result.stderr}"
                
                project_path = Path(temp_dir) / project_name
                
                # Verificar estructura común
                common_files = [
                    "README.md",
                    "BITACORA.md", 
                    "roadmap_v1.md",
                    "CONTEXTO.md",
                    "METODOLOGIA_DESARROLLO.md",
                    ".gitignore"
                ]
                
                for file_name in common_files:
                    assert (project_path / file_name).exists(), f"Falta {file_name} en {project_type}"
                
                # Verificar directorios comunes
                common_dirs = ["src", "tests", "docs", "examples", "logs"]
                
                for dir_name in common_dirs:
                    assert (project_path / dir_name).exists(), f"Falta directorio {dir_name} en {project_type}"
                
                # Verificar archivos específicos por tipo
                if project_type == "Python Library":
                    assert (project_path / "requirements.txt").exists()
                    assert (project_path / "src" / f"{project_name}.py").exists()
                elif project_type == "C++ Project":
                    assert (project_path / "CMakeLists.txt").exists()
                    assert (project_path / "src" / f"{project_name}.cpp").exists()
                    assert (project_path / "src" / f"{project_name}.hpp").exists()
                elif project_type == "Node.js Project":
                    assert (project_path / "package.json").exists()
                    assert (project_path / "src" / f"{project_name}.js").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
