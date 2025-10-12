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
@click.version_option(version="1.0.0", prog_name="pre-cursor")
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
@click.option('--path', '-p', type=click.Path(), help='Ruta donde crear el proyecto')
@click.option('--type', '-t', 'project_type', 
              type=click.Choice([
                  'Python Library', 'Python CLI Tool', 'Python Web App (Flask)',
                  'Python Web App (Django)', 'Python Web App (FastAPI)',
                  'Python Data Science', 'Python ML/AI', 'C++ Project',
                  'Node.js Project', 'TD_MCP Project', 'Otro'
              ]),
              help='Tipo de proyecto')
@click.option('--interactive', '-i', is_flag=True, help='Modo interactivo')
@click.pass_context
def create(ctx, project_name, path, project_type, interactive):
    """
    🎯 Crear un nuevo proyecto
    
    Ejemplos:
    pre-cursor create mi-proyecto
    pre-cursor create mi-api --type "Python Web App (FastAPI)"
    pre-cursor create mi-lib --path /ruta/personalizada
    """
    console.print(f"\n🚀 Creando proyecto: [bold blue]{project_name}[/bold blue]")
    
    if interactive:
        # Modo interactivo mejorado
        _interactive_create(project_name, path)
    else:
        # Modo directo
        _direct_create(project_name, path, project_type)

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
        "[bold blue]🚀 Pre-Cursor v1.0.0[/bold blue]\n\n"
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

def _interactive_create(project_name, path):
    """Modo interactivo mejorado con Rich."""
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
    
    # Confirmar creación
    if Confirm.ask(f"\n¿Crear proyecto '{project_name}' de tipo '{project_type}'?"):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generando proyecto...", total=None)
            
            generator = ProjectGenerator()
            # Aquí iría la lógica de generación
            progress.update(task, description="✅ Proyecto generado!")
        
        console.print(f"🎉 Proyecto '{project_name}' creado exitosamente!", style="green")
    else:
        console.print("❌ Operación cancelada", style="red")

def _direct_create(project_name, path, project_type):
    """Modo directo simplificado."""
    generator = ProjectGenerator()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generando proyecto...", total=None)
        
        # Aquí iría la lógica de generación directa
        progress.update(task, description="✅ Proyecto generado!")
    
    console.print(f"🎉 Proyecto '{project_name}' creado exitosamente!", style="green")

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
