#!/usr/bin/env python3
"""
Pre-Cursor CLI - Interfaz de línea de comandos mejorada
======================================================

Interfaz moderna y profesional para Pre-Cursor usando Click.
Proporciona subcomandos, autocompletado y mejor experiencia de usuario.
"""

import click
import json
import yaml
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import print as rprint

# Importar el generador principal
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from init_project import ProjectGenerator

console = Console()

@click.group()
@click.version_option(version="1.0.1", prog_name="pre-cursor")
@click.option('--verbose', '-v', is_flag=True, help='Activar modo verbose')
@click.option('--config', '-c', type=click.Path(exists=True), help='Archivo de configuración')
@click.pass_context
def cli(ctx, verbose, config):
    """
    🚀 Pre-Cursor: Generador de proyectos optimizado para agentes de IA
    
    Genera estructuras de proyecto completas con metodología establecida.
    Soporta Python, FastAPI, TD_MCP, C++, Node.js y más.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config
    
    if verbose:
        console.print("🔧 Modo verbose activado", style="blue")

@cli.command()
@click.argument('project_name')
@click.option('--description', '-d', help='Descripción del proyecto')
@click.option('--path', '-p', type=click.Path(), help='Ruta donde crear el proyecto (deprecated, usar --output-dir)')
@click.option('--output-dir', '-o', type=str, help='Directorio de salida para el proyecto')
@click.option('--type', '-t', 'project_type', 
              type=click.Choice([
                  'Python Library', 'Python CLI Tool', 'Python Web App (Flask)',
                  'Python Web App (Django)', 'Python Web App (FastAPI)',
                  'Python Data Science', 'Python ML/AI', 'C++ Project',
                  'Node.js Project', 'TD_MCP Project', 'Otro'
              ]),
              help='Tipo de proyecto')
@click.option('--interactive', '-i', is_flag=True, help='Modo interactivo')
@click.option('--open-cursor', is_flag=True, help='Abrir proyecto en Cursor al finalizar')
@click.option('--force', '-f', is_flag=True, help='Forzar creación aunque el directorio ya exista')
@click.pass_context
def create(ctx, project_name, description, path, output_dir, project_type, interactive, open_cursor, force):
    """
    🎯 Crear un nuevo proyecto
    
    Ejemplos:
    pre-cursor create mi-proyecto
    pre-cursor create mi-api --type "Python Web App (FastAPI)" --description "API REST moderna"
    pre-cursor create mi-lib --output-dir ~/Desktop --open-cursor
    pre-cursor create mi-app --interactive --force
    pre-cursor create mi-tool -d "Herramienta CLI" -t "Python CLI Tool" -o ~/Projects
    """
    import os
    console.print(f"\n🚀 Creando proyecto: [bold blue]{project_name}[/bold blue]")
    
    # Validar nombre del proyecto
    if not _validate_project_name(project_name):
        console.print("❌ Error: El nombre del proyecto debe contener solo letras minúsculas, números y guiones bajos", style="red")
        sys.exit(1)
    
    # Determinar ruta de salida (priorizar --output-dir sobre --path)
    if output_dir:
        output_path = os.path.join(output_dir, project_name)
    elif path:
        output_path = os.path.join(path, project_name) if not path.endswith(project_name) else path
    else:
        output_path = None
    
    if interactive:
        # Modo interactivo mejorado
        project_path = _interactive_create(project_name, output_path, force)
    else:
        # Modo directo mejorado
        project_path = _direct_create(project_name, description, output_path, project_type, force)
    
    # Abrir en Cursor si se solicita
    if open_cursor:
        _open_in_cursor(project_path)
    else:
        # Preguntar si quiere abrir en Cursor
        if Confirm.ask("\n¿Abrir proyecto en Cursor?"):
            _open_in_cursor(project_path)

@cli.command()
@click.option('--type', '-t', 'project_type',
              type=click.Choice([
                  'Python Library', 'Python CLI Tool', 'Python Web App (Flask)',
                  'Python Web App (Django)', 'Python Web App (FastAPI)',
                  'Python Data Science', 'Python ML/AI', 'C++ Project',
                  'Node.js Project', 'TD_MCP Project', 'Otro'
              ]),
              help='Tipo de proyecto')
@click.option('--output', '-o', type=click.Path(), default='config.json',
              help='Archivo de salida')
@click.option('--format', 'output_format', 
              type=click.Choice(['json', 'yaml']), default='json',
              help='Formato de salida')
def template(project_type, output, output_format):
    """
    📝 Crear plantilla de configuración
    
    Genera un archivo de configuración template para personalizar.
    
    Ejemplos:
    pre-cursor template --type "Python Library"
    pre-cursor template --type "FastAPI" --format yaml --output mi_config.yaml
    """
    console.print(f"\n📝 Generando plantilla para: [bold blue]{project_type}[/bold blue]")
    
    generator = ProjectGenerator()
    template_data = generator._create_config_template(project_type)
    
    if output_format == 'yaml':
        content = yaml.dump(template_data, default_flow_style=False, sort_keys=False)
    else:
        content = json.dumps(template_data, indent=2, ensure_ascii=False)
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)
    
    console.print(f"✅ Plantilla creada: [bold green]{output}[/bold green]")

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Simular sin crear archivos')
def generate(config_file, dry_run):
    """
    ⚡ Generar proyecto desde archivo de configuración
    
    Ejemplos:
    pre-cursor generate mi_config.json
    pre-cursor generate config.yaml --dry-run
    """
    console.print(f"\n⚡ Generando desde: [bold blue]{config_file}[/bold blue]")
    
    if dry_run:
        console.print("🔍 Modo dry-run: simulando generación...", style="yellow")
    
    generator = ProjectGenerator()
    
    try:
        if config_file.endswith('.yaml') or config_file.endswith('.yml'):
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        else:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        
        if dry_run:
            _show_config_preview(config_data)
        else:
            generator.generate_project_from_config(config_data)
            console.print("✅ Proyecto generado exitosamente!", style="green")
            
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)

@cli.command()
def list_types():
    """
    📋 Listar tipos de proyecto disponibles
    """
    console.print("\n📋 Tipos de proyecto disponibles:")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Tipo", style="cyan")
    table.add_column("Descripción", style="white")
    table.add_column("Tecnologías", style="green")
    
    types_info = {
        "Python Library": ("Librerías Python estándar", "Python, pytest, black"),
        "Python CLI Tool": ("Herramientas de línea de comandos", "Python, Click, argparse"),
        "Python Web App (Flask)": ("Aplicaciones web con Flask", "Python, Flask, SQLAlchemy"),
        "Python Web App (Django)": ("Aplicaciones web con Django", "Python, Django, PostgreSQL"),
        "Python Web App (FastAPI)": ("Aplicaciones web con FastAPI", "Python, FastAPI, Pydantic"),
        "Python Data Science": ("Proyectos de ciencia de datos", "Python, pandas, numpy, matplotlib"),
        "Python ML/AI": ("Proyectos de machine learning", "Python, scikit-learn, tensorflow"),
        "C++ Project": ("Proyectos en C++", "C++, CMake, Google Test"),
        "Node.js Project": ("Proyectos en Node.js", "Node.js, npm, Jest"),
        "TD_MCP Project": ("Proyectos MCP para TouchDesigner", "Python, MCP, TouchEngine SDK"),
        "Otro": ("Configuración personalizada", "Personalizable")
    }
    
    for project_type, (description, technologies) in types_info.items():
        table.add_row(project_type, description, technologies)
    
    console.print(table)

@cli.command()
@click.option('--examples', is_flag=True, help='Mostrar ejemplos de uso')
def info(examples):
    """
    ℹ️ Información sobre Pre-Cursor
    """
    console.print(Panel.fit(
        "[bold blue]🚀 Pre-Cursor v1.0.1[/bold blue]\n\n"
        "Generador de proyectos optimizado para agentes de IA\n"
        "Crea estructuras completas con metodología establecida\n\n"
        "[bold green]Características:[/bold green]\n"
        "• Soporte para múltiples lenguajes y frameworks\n"
        "• Plantillas profesionales y documentación completa\n"
        "• Integración con Git y herramientas de desarrollo\n"
        "• Optimizado para trabajo con agentes de IA\n\n"
        "[bold yellow]Autor:[/bold yellow] Assiz Alcaraz Baxter\n"
        "[bold yellow]Licencia:[/bold yellow] MIT",
        title="Información del Proyecto"
    ))
    
    if examples:
        console.print("\n📚 Ejemplos de uso:")
        console.print("• pre-cursor create mi-proyecto")
        console.print("• pre-cursor create mi-api --type 'Python Web App (FastAPI)'")
        console.print("• pre-cursor template --type 'Python Library'")
        console.print("• pre-cursor generate mi_config.json")

def _validate_project_name(name):
    """Validar nombre del proyecto."""
    import re
    return bool(re.match(r'^[a-z0-9_]+$', name))

def _get_default_project_path(project_name):
    """Obtener ruta por defecto para el proyecto."""
    import os
    home = os.path.expanduser("~")
    current_dir = os.getcwd()
    
    # Priorizar el directorio actual como primera opción
    if os.access(current_dir, os.W_OK):
        return os.path.join(current_dir, project_name)
    
    # Si estamos en el directorio pre_Cursor, usar directorio padre
    if current_dir.endswith('pre_Cursor') or current_dir.endswith('pre-cursor'):
        parent_dir = os.path.dirname(current_dir)
        if os.access(parent_dir, os.W_OK):
            return os.path.join(parent_dir, project_name)
    
    # Intentar directorios comunes de proyectos
    possible_paths = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Documents", "Projects"),
        os.path.join(home, "Projects"),
        os.path.join(home, "Developer"),
        os.path.join(home, "Documents")
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.access(path, os.W_OK):
            return os.path.join(path, project_name)
    
    # Fallback al directorio actual
    return os.path.join(current_dir, project_name)

def _open_in_cursor(project_path):
    """Abrir proyecto en Cursor con verificación robusta."""
    import subprocess
    import os
    import shutil
    
    if not os.path.exists(project_path):
        console.print(f"❌ Error: Directorio {project_path} no existe", style="red")
        return
    
    console.print(f"\n🖥️ Abriendo proyecto en Cursor...")
    
    # Verificar si cursor está disponible
    if shutil.which("cursor"):
        try:
            subprocess.run(["cursor", project_path], check=True)
            console.print("✅ Proyecto abierto en Cursor", style="green")
            return
        except subprocess.CalledProcessError as e:
            console.print(f"⚠️ Error al abrir con Cursor: {e}", style="yellow")
    
    # Fallback a VS Code
    if shutil.which("code"):
        try:
            subprocess.run(["code", project_path], check=True)
            console.print("✅ Proyecto abierto en VS Code", style="green")
            return
        except subprocess.CalledProcessError as e:
            console.print(f"⚠️ Error al abrir con VS Code: {e}", style="yellow")
    
    # Fallback a abrir directorio en explorador
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["explorer", project_path], check=True)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["open", project_path], check=True)
        console.print("✅ Directorio abierto en el explorador", style="green")
        return
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        console.print(f"⚠️ Error al abrir explorador: {e}", style="yellow")
    
    # Si todo falla, mostrar instrucciones manuales
    console.print("⚠️ No se pudo abrir automáticamente. Abre manualmente:", style="yellow")
    console.print(f"   cd {project_path}")
    if shutil.which("cursor"):
        console.print("   cursor .")
    elif shutil.which("code"):
        console.print("   code .")
    else:
        console.print("   # Instala Cursor o VS Code para abrir automáticamente")

def _interactive_create(project_name, path, force=False):
    """Modo interactivo mejorado con Rich."""
    import os
    console.print("\n🎯 Modo interactivo - Configuración del proyecto")
    
    # Seleccionar tipo de proyecto
    project_types = [
        "Python Library", "Python CLI Tool", "Python Web App (Flask)",
        "Python Web App (Django)", "Python Web App (FastAPI)",
        "Python Data Science", "Python ML/AI", "C++ Project",
        "Node.js Project", "TD_MCP Project", "Otro"
    ]
    
    console.print("\n📋 Selecciona el tipo de proyecto:")
    for i, ptype in enumerate(project_types, 1):
        console.print(f"  {i}. {ptype}")
    
    choice = Prompt.ask("Tipo de proyecto", default="1")
    try:
        project_type = project_types[int(choice) - 1]
    except (ValueError, IndexError):
        project_type = project_types[0]
    
    # Obtener información adicional
    description = Prompt.ask("Descripción del proyecto", default="Proyecto generado con Pre-Cursor")
    author = Prompt.ask("Autor", default="Tu Nombre")
    email = Prompt.ask("Email", default="tu@email.com")
    
    # Determinar ruta del proyecto
    if not path:
        # Mostrar opciones de ruta con directorio actual como primera opción
        current_dir = os.getcwd()
        project_path_current = os.path.join(current_dir, project_name)
        
        console.print(f"\n📍 Selecciona la ubicación del proyecto:")
        console.print(f"  1. [bold green]Directorio actual[/bold green] - {project_path_current}")
        console.print(f"  2. [bold blue]Desktop[/bold blue] - {os.path.join(os.path.expanduser('~'), 'Desktop', project_name)}")
        console.print(f"  3. [bold blue]Documents/Projects[/bold blue] - {os.path.join(os.path.expanduser('~'), 'Documents', 'Projects', project_name)}")
        console.print(f"  4. [bold blue]Developer[/bold blue] - {os.path.join(os.path.expanduser('~'), 'Developer', project_name)}")
        console.print(f"  5. [bold yellow]Personalizada[/bold yellow] - Especificar ruta manualmente")
        
        choice = Prompt.ask("Selecciona una opción", default="1")
        
        if choice == "1":
            path = project_path_current
        elif choice == "2":
            path = os.path.join(os.path.expanduser('~'), 'Desktop', project_name)
        elif choice == "3":
            path = os.path.join(os.path.expanduser('~'), 'Documents', 'Projects', project_name)
        elif choice == "4":
            path = os.path.join(os.path.expanduser('~'), 'Developer', project_name)
        elif choice == "5":
            path = Prompt.ask("Ingresa la ruta completa del proyecto", default=project_path_current)
        else:
            path = project_path_current
    
    # Verificar si el directorio ya existe
    if os.path.exists(path) and not force:
        console.print(f"⚠️ El directorio [bold yellow]{path}[/bold yellow] ya existe.", style="yellow")
        if not Confirm.ask("¿Continuar y sobrescribir el contenido existente?"):
            console.print("❌ Operación cancelada", style="red")
            return None
    elif os.path.exists(path) and force:
        console.print(f"🔄 Forzando creación en directorio existente: [bold yellow]{path}[/bold yellow]", style="yellow")
    
    # Confirmar creación
    console.print(f"\n📋 Resumen del proyecto:")
    console.print(f"   📝 Nombre: [bold blue]{project_name}[/bold blue]")
    console.print(f"   🔧 Tipo: [bold green]{project_type}[/bold green]")
    console.print(f"   📖 Descripción: [bold white]{description}[/bold white]")
    console.print(f"   📍 Ruta: [bold green]{path}[/bold green]")
    
    if not force and not Confirm.ask(f"\n¿Crear proyecto '{project_name}'?"):
        console.print("❌ Operación cancelada", style="red")
        return None
    elif force or Confirm.ask(f"\n¿Crear proyecto '{project_name}'?"):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generando proyecto...", total=None)
            
            generator = ProjectGenerator()
            # Crear configuración temporal
            config_data = {
                "project_name": project_name,
                "description": description,
                "project_type": project_type,
                "author": author,
                "email": email,
                "python_version_min": "3.8",
                "license": "MIT"
            }
            
            # Generar proyecto
            import tempfile
            import json
            from pathlib import Path
            
            # Crear archivo temporal de configuración
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(config_data, f, indent=2)
                temp_config_path = f.name
            
            try:
                generator.generate_project_from_config(Path(temp_config_path), Path(path))
                progress.update(task, description="✅ Proyecto generado!")
            except Exception as e:
                progress.update(task, description="❌ Error en generación")
                console.print(f"\n❌ Error al generar el proyecto: {e}", style="red")
                console.print("🔧 Verifica los permisos y la configuración", style="yellow")
                return None
            finally:
                # Limpiar archivo temporal
                import os
                try:
                    os.unlink(temp_config_path)
                except OSError:
                    pass  # Ignorar errores al limpiar archivo temporal
        
        console.print(f"\n🎉 ¡Proyecto '{project_name}' creado exitosamente!", style="green")
        
        # Mostrar información del proyecto
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column(style="bold cyan", width=12)
        info_table.add_column(style="white")
        
        info_table.add_row("📁 Ubicación:", path)
        info_table.add_row("📝 Descripción:", description)
        info_table.add_row("🔧 Tipo:", project_type)
        info_table.add_row("👤 Autor:", author)
        info_table.add_row("📧 Email:", email)
        info_table.add_row("📅 Creado:", "Hoy")
        
        console.print(info_table)
        
        # Mostrar próximos pasos detallados
        console.print(f"\n🚀 Próximos pasos:")
        steps_table = Table(show_header=False, box=None, padding=(0, 1))
        steps_table.add_column(style="bold yellow", width=3)
        steps_table.add_column(style="white")
        
        steps_table.add_row("1️⃣", f"cd {path}")
        steps_table.add_row("2️⃣", "pip install -r requirements.txt")
        steps_table.add_row("3️⃣", "git remote add origin <URL_de_tu_repo>")
        steps_table.add_row("4️⃣", "cursor .  # o code .")
        steps_table.add_row("5️⃣", "¡Empieza a desarrollar!")
        
        console.print(steps_table)
        
        return path
    else:
        console.print("❌ Operación cancelada", style="red")
        return None

def _direct_create(project_name, description, path, project_type, force=False):
    """Modo directo mejorado."""
    import os
    generator = ProjectGenerator()
    
    # Determinar ruta del proyecto
    if not path:
        path = _get_default_project_path(project_name)
    
    # Verificar si el directorio ya existe
    if os.path.exists(path) and not force:
        console.print(f"⚠️ El directorio [bold yellow]{path}[/bold yellow] ya existe.", style="yellow")
        if not Confirm.ask("¿Continuar y sobrescribir el contenido existente?"):
            console.print("❌ Operación cancelada", style="red")
            return None
    elif os.path.exists(path) and force:
        console.print(f"🔄 Forzando creación en directorio existente: [bold yellow]{path}[/bold yellow]", style="yellow")
    
    # Solicitar descripción si no se proporciona
    if not description:
        console.print(f"\n📝 Descripción para el proyecto '{project_name}':")
        description = Prompt.ask("Descripción", default=f"Proyecto {project_name} generado con Pre-Cursor")
    
    # Usar tipo por defecto si no se proporciona
    if not project_type:
        project_type = "Python Library"
    
    # Mostrar resumen y confirmar
    console.print(f"\n📋 Resumen del proyecto:")
    console.print(f"   📝 Nombre: [bold blue]{project_name}[/bold blue]")
    console.print(f"   📖 Descripción: [bold white]{description}[/bold white]")
    console.print(f"   🔧 Tipo: [bold green]{project_type}[/bold green]")
    console.print(f"   📍 Ubicación: [bold green]{path}[/bold green]")
    
    if not force and not Confirm.ask(f"\n¿Crear proyecto '{project_name}'?"):
        console.print("❌ Operación cancelada", style="red")
        return None
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generando proyecto...", total=None)
        
        # Crear configuración temporal
        config_data = {
            "project_name": project_name,
            "description": description,
            "project_type": project_type,
            "author": "Tu Nombre",
            "email": "tu@email.com",
            "python_version_min": "3.8",
            "license": "MIT"
        }
        
        # Generar proyecto
        import tempfile
        import json
        from pathlib import Path
        
        # Crear archivo temporal de configuración
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f, indent=2)
            temp_config_path = f.name
        
        try:
            generator.generate_project_from_config(Path(temp_config_path), Path(path))
            progress.update(task, description="✅ Proyecto generado!")
        except Exception as e:
            progress.update(task, description="❌ Error en generación")
            console.print(f"\n❌ Error al generar el proyecto: {e}", style="red")
            console.print("🔧 Verifica los permisos y la configuración", style="yellow")
            return None
        finally:
            # Limpiar archivo temporal
            import os
            try:
                os.unlink(temp_config_path)
            except OSError:
                pass  # Ignorar errores al limpiar archivo temporal
    
    console.print(f"\n🎉 ¡Proyecto '{project_name}' creado exitosamente!", style="green")
    
    # Mostrar información del proyecto
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan", width=12)
    info_table.add_column(style="white")
    
    info_table.add_row("📁 Ubicación:", path)
    info_table.add_row("📝 Descripción:", description)
    info_table.add_row("🔧 Tipo:", project_type)
    info_table.add_row("📅 Creado:", "Hoy")
    
    console.print(info_table)
    
    # Mostrar próximos pasos detallados
    console.print(f"\n🚀 Próximos pasos:")
    steps_table = Table(show_header=False, box=None, padding=(0, 1))
    steps_table.add_column(style="bold yellow", width=3)
    steps_table.add_column(style="white")
    
    steps_table.add_row("1️⃣", f"cd {path}")
    steps_table.add_row("2️⃣", "pip install -r requirements.txt")
    steps_table.add_row("3️⃣", "git remote add origin <URL_de_tu_repo>")
    steps_table.add_row("4️⃣", "cursor .  # o code .")
    steps_table.add_row("5️⃣", "¡Empieza a desarrollar!")
    
    console.print(steps_table)
    
    # Mostrar archivos importantes
    console.print(f"\n📚 Archivos importantes:")
    files_table = Table(show_header=False, box=None, padding=(0, 1))
    files_table.add_column(style="bold blue", width=20)
    files_table.add_column(style="white")
    
    files_table.add_row("📖 README.md", "Documentación principal")
    files_table.add_row("📋 TUTORIAL.md", "Guía paso a paso")
    files_table.add_row("📝 BITACORA.md", "Registro de cambios")
    files_table.add_row("🔧 requirements.txt", "Dependencias Python")
    files_table.add_row("⚙️ .gitignore", "Archivos ignorados por Git")
    
    console.print(files_table)
    
    return path

def _show_config_preview(config_data):
    """Mostrar preview de la configuración."""
    console.print("\n📋 Preview de configuración:")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="white")
    
    for key, value in config_data.items():
        if isinstance(value, (dict, list)):
            value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        table.add_row(key, str(value))
    
    console.print(table)

if __name__ == '__main__':
    cli()
