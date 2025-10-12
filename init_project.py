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
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import json


class ProjectGenerator:
    """Generador de proyectos siguiendo la metodología establecida."""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.structure_dir = Path(__file__).parent / "structure"
        self.project_data: Dict[str, Any] = {}
        
    def collect_project_info(self) -> Dict[str, Any]:
        """
        Recopilar información del proyecto de manera interactiva.
        
        Returns:
            Dict con la información del proyecto
        """
        print("🚀 Generador de Proyectos Optimizado para Agentes de IA")
        print("=" * 60)
        
        # Información básica
        nombre_proyecto = input("📝 Nombre del proyecto: ").strip()
        descripcion_corta = input("📋 Descripción corta: ").strip()
        descripcion_detallada = input("📖 Descripción detallada: ").strip()
        
        # Información técnica
        tipo_proyecto = self._select_project_type()
        autor = input("👨‍💻 Autor: ").strip() or "Desarrollador"
        email_contacto = input("📧 Email de contacto: ").strip()
        github_user = input("🐙 GitHub username: ").strip()
        
        # Información del repositorio
        repositorio_url = input("🔗 URL del repositorio (opcional): ").strip()
        if not repositorio_url and github_user and nombre_proyecto:
            repositorio_url = f"https://github.com/{github_user}/{nombre_proyecto}"
        
        # Información técnica específica
        python_version_min = input("🐍 Versión mínima de Python (default: 3.8): ").strip() or "3.8"
        licencia = input("📄 Licencia (default: MIT): ").strip() or "MIT"
        
        # Objetivo y funcionalidades
        objetivo_proyecto = input("🎯 Objetivo principal del proyecto: ").strip()
        funcionalidad_principal = input("⚡ Funcionalidad principal: ").strip()
        
        # Fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
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
    
    def _select_project_type(self) -> str:
        """Seleccionar tipo de proyecto."""
        print("\n🔧 Tipo de proyecto:")
        print("1. Python Library")
        print("2. Python CLI Tool")
        print("3. Python Web App (Flask)")
        print("4. Python Web App (Django)")
        print("5. Python Data Science")
        print("6. Python ML/AI")
        print("7. Otro")
        
        while True:
            choice = input("Selecciona (1-7): ").strip()
            types = {
                "1": "Python Library",
                "2": "Python CLI Tool", 
                "3": "Python Web App (Flask)",
                "4": "Python Web App (Django)",
                "5": "Python Data Science",
                "6": "Python ML/AI",
                "7": "Otro"
            }
            if choice in types:
                return types[choice]
            print("❌ Opción inválida. Intenta de nuevo.")
    
    def _get_dependencies_for_type(self, project_type: str) -> str:
        """Obtener dependencias según el tipo de proyecto."""
        dependencies = {
            "Python Library": "# Dependencias principales\n# requests>=2.28.0",
            "Python CLI Tool": "# Dependencias principales\nclick>=8.0.0\nrich>=12.0.0",
            "Python Web App (Flask)": "# Dependencias principales\nflask>=2.0.0\nflask-cors>=3.0.0",
            "Python Web App (Django)": "# Dependencias principales\ndjango>=4.0.0\ndjangorestframework>=3.14.0",
            "Python Data Science": "# Dependencias principales\npandas>=1.5.0\nnumpy>=1.21.0\nmatplotlib>=3.5.0",
            "Python ML/AI": "# Dependencias principales\ntorch>=1.12.0\ntensorflow>=2.10.0\nscikit-learn>=1.1.0",
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
        
        template_files = [
            "README.md.tpl",
            "BITACORA.md.tpl", 
            "roadmap_v1.md.tpl",
            "requirements.txt.tpl",
            "TUTORIAL.md.tpl",
            "modulo_principal.py.tpl"
        ]
        
        for template_file in template_files:
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
            
            # Determinar archivo de destino
            template_name = template_path.name
            if template_name == "modulo_principal.py.tpl":
                dest_name = f"{self.project_data['MODULO_PRINCIPAL']}.py"
                dest_path = project_path / "src" / dest_name
            elif template_name == "TUTORIAL.md.tpl":
                dest_path = project_path / "docs" / "TUTORIAL.md"
            elif template_name.endswith(".tpl"):
                dest_name = template_name[:-4]  # Remover .tpl
                dest_path = project_path / dest_name
            else:
                dest_path = project_path / template_name
            
            # Crear directorio padre si no existe
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo procesado
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {dest_path.name}")
            
        except Exception as e:
            print(f"  ❌ Error procesando {template_path.name}: {e}")
    
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
        Generar proyecto completo.
        
        Args:
            project_name: Nombre del proyecto
            project_path: Ruta donde crear el proyecto (opcional)
        """
        if project_path is None:
            project_path = Path.cwd() / project_name
        
        print(f"🚀 Generando proyecto: {project_name}")
        print(f"📂 Ubicación: {project_path}")
        print()
        
        # Recopilar información
        self.project_data = self.collect_project_info()
        
        # Crear directorio del proyecto
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


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Generador de Proyectos Optimizado para Agentes de IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python init_project.py                    # Modo interactivo
  python init_project.py MiProyecto         # Crear proyecto específico
  python init_project.py MiProyecto /ruta/  # Crear en ruta específica
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
    
    args = parser.parse_args()
    
    try:
        generator = ProjectGenerator()
        
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
