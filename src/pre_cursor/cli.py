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
@click.version_option(version="1.0.2", prog_name="pre-cursor")
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

@cli.group()
def supervisor():
    """
    🤖 Gestión del Cursor Supervisor
    
    Comandos para gestionar la supervisión automática de proyectos.
    """
    pass

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--interval', '-i', type=int, default=300, help='Intervalo de supervisión en segundos')
@click.option('--daemon', '-d', is_flag=True, help='Ejecutar como daemon en background')
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def start(project_path, interval, daemon, path):
    """
    🚀 Iniciar supervisión del proyecto
    
    Ejemplos:
    pre-cursor supervisor start /path/to/project
    pre-cursor supervisor start /path/to/project --interval 600
    pre-cursor supervisor start /path/to/project --daemon
    pre-cursor supervisor start -p  # Usar directorio actual
    pre-cursor supervisor start -p --daemon --interval 600
    """
    try:
        from pre_cursor.cursor_supervisor import CursorSupervisor
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        console.print(f"\n🤖 Iniciando supervisión de: [bold blue]{project_path}[/bold blue]")
        console.print(f"⏱️ Intervalo: [bold green]{interval}[/bold green] segundos")
        
        supervisor = CursorSupervisor(project_path, check_interval=interval)
        
        if daemon:
            console.print("🔄 Ejecutando como daemon...", style="yellow")
            supervisor.start_supervision()
        else:
            console.print("🔄 Ejecutando verificación única...", style="yellow")
            report = supervisor.check_project_health()
            _display_supervision_report(report)
            
    except ImportError:
        console.print("❌ Error: Módulo cursor_supervisor no encontrado", style="red")
        console.print("💡 Instala las dependencias: pip install watchdog psutil", style="yellow")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def status(project_path, path):
    """
    📊 Verificar estado del supervisor
    
    Ejemplos:
    pre-cursor supervisor status /path/to/project
    pre-cursor supervisor status -p  # Usar directorio actual
    """
    try:
        from pre_cursor.cursor_supervisor import CursorSupervisor
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        console.print(f"\n📊 Estado del supervisor para: [bold blue]{project_path}[/bold blue]")
        
        supervisor = CursorSupervisor(project_path)
        report = supervisor.check_project_health()
        
        _display_supervision_report(report)
        
        # Verificar si hay supervisión activa
        _check_active_supervision(project_path)
        
    except ImportError:
        console.print("❌ Error: Módulo cursor_supervisor no encontrado", style="red")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--interval', '-i', type=int, help='Nuevo intervalo en segundos')
@click.option('--auto-fix', type=click.Choice(['true', 'false']), help='Habilitar/deshabilitar corrección automática')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Nivel de logging')
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def config(project_path, interval, auto_fix, log_level, path):
    """
    ⚙️ Configurar supervisor del proyecto
    
    Ejemplos:
    pre-cursor supervisor config /path/to/project --interval 600
    pre-cursor supervisor config /path/to/project --auto-fix true
    pre-cursor supervisor config /path/to/project --log-level DEBUG
    pre-cursor supervisor config -p --interval 600  # Usar directorio actual
    """
    try:
        import yaml
        from pathlib import Path
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        config_path = Path(project_path) / 'config' / 'cursor_supervisor.yaml'
        
        # Crear directorio config si no existe
        config_path.parent.mkdir(exist_ok=True)
        
        # Cargar configuración existente o crear nueva
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
        else:
            config_data = {}
        
        # Actualizar configuración
        if interval:
            config_data.setdefault('supervisor', {})['check_interval'] = interval
            console.print(f"✅ Intervalo actualizado a {interval} segundos", style="green")
        
        if auto_fix:
            config_data.setdefault('supervisor', {})['auto_fix'] = auto_fix == 'true'
            console.print(f"✅ Corrección automática: {auto_fix}", style="green")
        
        if log_level:
            config_data.setdefault('supervisor', {})['log_level'] = log_level
            console.print(f"✅ Nivel de logging: {log_level}", style="green")
        
        # Guardar configuración
        with open(config_path, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
        
        console.print(f"✅ Configuración guardada en: [bold green]{config_path}[/bold green]")
        
        # Mostrar configuración actual
        _display_supervisor_config(config_data)
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def stop(project_path, path):
    """
    🛑 Detener supervisión del proyecto
    
    Ejemplos:
    pre-cursor supervisor stop /path/to/project
    pre-cursor supervisor stop -p  # Usar directorio actual
    """
    try:
        import psutil
        import os
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        console.print(f"\n🛑 Deteniendo supervisión de: [bold blue]{project_path}[/bold blue]")
        
        # Buscar procesos de supervisor activos
        supervisor_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and any('cursor_supervisor' in arg for arg in proc.info['cmdline']):
                    if project_path in ' '.join(proc.info['cmdline']):
                        supervisor_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if supervisor_processes:
            for proc in supervisor_processes:
                console.print(f"🔄 Deteniendo proceso PID {proc.pid}...", style="yellow")
                proc.terminate()
                proc.wait(timeout=5)
            console.print("✅ Supervisión detenida", style="green")
        else:
            console.print("ℹ️ No se encontraron procesos de supervisión activos", style="blue")
        
        # Verificar si hay archivos de lock
        lock_files = [
            Path(project_path) / '.supervisor.lock',
            Path(project_path) / 'logs' / 'supervisor.lock'
        ]
        
        for lock_file in lock_files:
            if lock_file.exists():
                lock_file.unlink()
                console.print(f"🗑️ Archivo de lock eliminado: {lock_file}", style="yellow")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--fix', '-f', is_flag=True, help='Aplicar correcciones automáticas')
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def fix(project_path, fix, path):
    """
    🔧 Corregir problemas detectados en el proyecto
    
    Ejemplos:
    pre-cursor supervisor fix /path/to/project
    pre-cursor supervisor fix /path/to/project --fix
    pre-cursor supervisor fix -p --fix  # Usar directorio actual
    """
    try:
        from pre_cursor.cursor_supervisor import CursorSupervisor
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        console.print(f"\n🔧 Corrigiendo problemas en: [bold blue]{project_path}[/bold blue]")
        
        supervisor = CursorSupervisor(project_path)
        report = supervisor.check_project_health()
        
        if not report.issues_found:
            console.print("✅ No se encontraron problemas que corregir", style="green")
            return
        
        console.print(f"📊 Problemas encontrados: [bold yellow]{len(report.issues_found)}[/bold yellow]")
        
        # Mostrar problemas
        for issue in report.issues_found:
            severity_color = {
                'low': 'green',
                'medium': 'yellow', 
                'high': 'red',
                'critical': 'bold red'
            }.get(issue.severity, 'white')
            
            console.print(f"  • [{severity_color}]{issue.severity.upper()}[/{severity_color}]: {issue.description}")
            if issue.suggestion:
                console.print(f"    💡 Sugerencia: {issue.suggestion}")
        
        if fix:
            console.print("\n🔧 Aplicando correcciones automáticas...", style="yellow")
            # Aquí se implementarían las correcciones automáticas
            console.print("⚠️ Corrección automática no implementada aún", style="yellow")
        else:
            console.print("\n💡 Usa --fix para aplicar correcciones automáticas", style="blue")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@supervisor.command()
@click.argument('project_path', type=click.Path(exists=True), required=False)
@click.option('--path', '-p', is_flag=True, help='Usar directorio actual como path del proyecto')
def logs(project_path, path):
    """
    📋 Mostrar logs del supervisor
    
    Ejemplos:
    pre-cursor supervisor logs /path/to/project
    pre-cursor supervisor logs -p  # Usar directorio actual
    """
    try:
        from pathlib import Path
        
        # Determinar path del proyecto
        if path:
            project_path = os.getcwd()
            console.print(f"📍 Usando directorio actual: [bold blue]{project_path}[/bold blue]")
        elif not project_path:
            console.print("❌ Error: Debes especificar el path del proyecto o usar -p para directorio actual", style="red")
            return
        
        log_files = [
            Path(project_path) / 'logs' / 'supervisor.log',
            Path(project_path) / 'logs' / 'cursor_supervisor.log',
            Path(project_path) / '.supervisor.log'
        ]
        
        console.print(f"\n📋 Logs del supervisor para: [bold blue]{project_path}[/bold blue]")
        
        log_found = False
        for log_file in log_files:
            if log_file.exists():
                log_found = True
                console.print(f"\n📄 Archivo: [bold green]{log_file}[/bold green]")
                console.print("─" * 60)
                
                # Mostrar últimas 20 líneas
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:
                        console.print(line.rstrip())
                
                console.print("─" * 60)
        
        if not log_found:
            console.print("ℹ️ No se encontraron archivos de log", style="blue")
            console.print("💡 Los logs se crean cuando se ejecuta la supervisión", style="yellow")
        
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")

@cli.command()
@click.option('--examples', is_flag=True, help='Mostrar ejemplos de uso')
def info(examples):
    """
    ℹ️ Información sobre Pre-Cursor
    """
    console.print(Panel.fit(
        "[bold blue]🚀 Pre-Cursor v1.0.2[/bold blue]\n\n"
        "Generador de proyectos optimizado para agentes de IA\n"
        "Crea estructuras completas con metodología establecida\n\n"
        "[bold green]Características:[/bold green]\n"
        "• Soporte para múltiples lenguajes y frameworks\n"
        "• Plantillas profesionales y documentación completa\n"
        "• Integración con Git y herramientas de desarrollo\n"
        "• Optimizado para trabajo con agentes de IA\n"
        "• Supervisión automática con Cursor Supervisor\n\n"
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
        console.print("• pre-cursor supervisor start /path/to/project")
        console.print("• pre-cursor supervisor start -p  # Usar directorio actual")
        console.print("• pre-cursor supervisor status /path/to/project")
        console.print("• pre-cursor supervisor config -p --interval 600")

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

def _display_supervision_report(report):
    """Mostrar reporte de supervisión."""
    from datetime import datetime
    
    console.print(f"\n📊 Reporte de Supervisión - {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    console.print("─" * 60)
    
    # Resumen
    console.print(f"📈 Problemas encontrados: [bold yellow]{len(report.issues_found)}[/bold yellow]")
    console.print(f"📁 Archivos creados: [bold green]{len(report.files_created)}[/bold green]")
    console.print(f"✏️ Archivos modificados: [bold blue]{len(report.files_modified)}[/bold blue]")
    console.print(f"🏗️ Cambios de estructura: [bold cyan]{len(report.structure_changes)}[/bold cyan]")
    
    # Problemas por severidad
    if report.issues_found:
        console.print("\n🚨 Problemas detectados:")
        
        severity_counts = {}
        for issue in report.issues_found:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
        
        for severity, count in severity_counts.items():
            color = {
                'low': 'green',
                'medium': 'yellow',
                'high': 'red',
                'critical': 'bold red'
            }.get(severity, 'white')
            console.print(f"  • [{color}]{severity.upper()}[/{color}]: {count} problemas")
        
        # Mostrar problemas críticos y altos
        critical_issues = [i for i in report.issues_found if i.severity in ['critical', 'high']]
        if critical_issues:
            console.print("\n⚠️ Problemas críticos/altos:")
            for issue in critical_issues[:5]:  # Mostrar solo los primeros 5
                console.print(f"  • {issue.description}")
                if issue.suggestion:
                    console.print(f"    💡 {issue.suggestion}")
    
    # Recomendaciones
    if report.recommendations:
        console.print("\n💡 Recomendaciones:")
        for rec in report.recommendations[:3]:  # Mostrar solo las primeras 3
            console.print(f"  • {rec}")

def _check_active_supervision(project_path):
    """Verificar si hay supervisión activa."""
    try:
        import psutil
        from pathlib import Path
        
        # Buscar procesos de supervisor
        supervisor_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and any('cursor_supervisor' in arg for arg in proc.info['cmdline']):
                    if project_path in ' '.join(proc.info['cmdline']):
                        supervisor_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if supervisor_processes:
            console.print(f"\n🔄 Supervisión activa: [bold green]SÍ[/bold green]")
            for proc in supervisor_processes:
                console.print(f"  • PID {proc.pid} - {proc.info['name']}")
        else:
            console.print(f"\n🔄 Supervisión activa: [bold red]NO[/bold red]")
            console.print("💡 Usa 'pre-cursor supervisor start' para iniciar supervisión")
        
        # Verificar archivos de configuración
        config_path = Path(project_path) / 'config' / 'cursor_supervisor.yaml'
        if config_path.exists():
            console.print(f"⚙️ Configuración: [bold green]Encontrada[/bold green] ({config_path})")
        else:
            console.print(f"⚙️ Configuración: [bold yellow]No encontrada[/bold yellow]")
            console.print("💡 Usa 'pre-cursor supervisor config' para crear configuración")
        
    except Exception as e:
        console.print(f"⚠️ Error verificando supervisión activa: {e}", style="yellow")

def _display_supervisor_config(config_data):
    """Mostrar configuración del supervisor."""
    console.print("\n⚙️ Configuración actual del supervisor:")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Parámetro", style="cyan")
    table.add_column("Valor", style="white")
    
    # Configuración del supervisor
    supervisor_config = config_data.get('supervisor', {})
    table.add_row("Intervalo de verificación", f"{supervisor_config.get('check_interval', 300)} segundos")
    table.add_row("Corrección automática", str(supervisor_config.get('auto_fix', False)))
    table.add_row("Nivel de logging", supervisor_config.get('log_level', 'INFO'))
    table.add_row("Máximo de problemas", str(supervisor_config.get('max_issues', 10)))
    
    # Configuración de detección
    detection_config = config_data.get('detection', {})
    table.add_row("Verificar archivos fuera de lugar", str(detection_config.get('check_misplaced_files', True)))
    table.add_row("Verificar duplicados", str(detection_config.get('check_duplicates', True)))
    table.add_row("Verificar estructura", str(detection_config.get('check_structure', True)))
    
    # Configuración de notificaciones
    notifications_config = config_data.get('notifications', {})
    table.add_row("Notificaciones en consola", str(notifications_config.get('console', True)))
    table.add_row("Logging a archivo", str(notifications_config.get('file_logging', True)))
    
    console.print(table)

if __name__ == '__main__':
    cli()
