#!/usr/bin/env python3
"""
Generador de proyectos openFrameworks
Integra el ProjectGenerator oficial de openFrameworks
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()

class OFProjectGenerator:
    """Integración con el ProjectGenerator oficial de openFrameworks."""
    
    # Ruta por defecto al ProjectGenerator
    DEFAULT_OF_PATH = Path("/Users/joseassizalcarazbaxter/Documents/UNA/POSGRADO/2025_1/PyA/of_v0.12.1_osx_release")
    
    def __init__(self, of_path: Optional[Path] = None):
        """
        Inicializar generador de proyectos openFrameworks.
        
        Args:
            of_path: Ruta a la instalación de openFrameworks (por defecto usa DEFAULT_OF_PATH)
        """
        self.of_path = of_path or self.DEFAULT_OF_PATH
        self.pg_path = self.of_path / "projectGenerator.app" / "Contents" / "MacOS" / "projectGenerator"
        
        if not self.of_path.exists():
            console.print(f"⚠️  openFrameworks no encontrado en: {self.of_path}", style="yellow")
            console.print("💡 Especifica la ruta con: --of-path", style="blue")
        
        if not self.pg_path.exists():
            console.print(f"⚠️  ProjectGenerator no encontrado en: {self.pg_path}", style="yellow")
    
    def check_available(self) -> bool:
        """Verificar si el ProjectGenerator está disponible."""
        return self.pg_path.exists() and os.access(self.pg_path, os.X_OK)
    
    def list_addons(self) -> List[str]:
        """Listar addons disponibles en openFrameworks."""
        addons_path = self.of_path / "addons"
        
        if not addons_path.exists():
            return []
        
        addons = []
        for item in addons_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Verificar que sea un addon válido (tiene addon_config.mk)
                if (addons_path / item.name / "addon_config.mk").exists():
                    addons.append(item.name)
        
        return sorted(addons)
    
    def generate_project(
        self,
        project_name: str,
        output_dir: Optional[Path] = None,
        addons: Optional[List[str]] = None,
        verbose: bool = False
    ) -> bool:
        """
        Generar proyecto usando el ProjectGenerator oficial.
        
        Args:
            project_name: Nombre del proyecto
            output_dir: Directorio de salida (por defecto apps/myApps dentro de openFrameworks)
            addons: Lista de addons a incluir
            verbose: Modo verbose
            
        Returns:
            bool: True si se generó exitosamente
        """
        if not self.check_available():
            console.print("❌ ProjectGenerator no está disponible", style="red")
            console.print(f"   Ruta: {self.pg_path}", style="yellow")
            return False
        
        # Determinar directorio de salida
        if output_dir is None:
            output_dir = self.of_path / "apps" / "myApps"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Construir comando
        cmd = [str(self.pg_path)]
        
        # Opciones del ProjectGenerator
        if addons:
            cmd.extend(["-a"] + addons)
        
        # Directorio de salida y nombre del proyecto
        cmd.extend(["-o", str(output_dir), project_name])
        
        console.print(f"\n🚀 Generando proyecto openFrameworks: [bold blue]{project_name}[/bold blue]")
        console.print(f"📁 Ubicación: [bold green]{output_dir / project_name}[/bold green]")
        
        if addons:
            console.print(f"🔌 Addons: [bold cyan]{', '.join(addons)}[/bold cyan]")
        
        if verbose:
            console.print(f"🔧 Comando: {' '.join(cmd)}")
        
        try:
            # Ejecutar ProjectGenerator
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                console.print(f"✅ Proyecto creado exitosamente: [bold green]{output_dir / project_name}[/bold green]")
                
                # Mostrar información del proyecto
                project_path = output_dir / project_name
                if project_path.exists():
                    console.print(f"\n📁 Estructura del proyecto:")
                    console.print(f"   {project_path}")
                    
                    # Mostrar archivos principales
                    for file in ["src", "bin", "Makefile"]:
                        file_path = project_path / file
                        if file_path.exists():
                            console.print(f"   ✅ {file}")
                
                return True
            else:
                console.print(f"❌ Error al generar proyecto: {result.stderr}", style="red")
                return False
                
        except subprocess.TimeoutExpired:
            console.print("❌ Timeout al generar proyecto", style="red")
            return False
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")
            return False
    
    def create_project_interactive(self) -> bool:
        """Crear proyecto en modo interactivo."""
        console.print("\n🎨 [bold cyan]openFrameworks Project Generator[/bold cyan]")
        console.print("=" * 60)
        
        # Obtener nombre del proyecto
        project_name = Prompt.ask("📝 Nombre del proyecto")
        
        if not project_name:
            console.print("❌ El nombre del proyecto es requerido", style="red")
            return False
        
        # Solicitar directorio de salida
        default_output = self.of_path / "apps" / "myApps"
        console.print(f"\n📁 Directorio de salida (default: {default_output})")
        output_path = Prompt.ask("Ubicación", default=str(default_output))
        
        try:
            output_dir = Path(output_path)
        except Exception as e:
            console.print(f"❌ Error en la ruta: {e}", style="red")
            return False
        
        # Verificar si el directorio existe o preguntar si crearlo
        if not output_dir.exists():
            if Confirm.ask(f"📁 Crear directorio: {output_dir}?"):
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                return False
        
        # Listar addons disponibles
        addons_list = self.list_addons()
        
        if addons_list:
            console.print(f"\n🔌 Addons disponibles ({len(addons_list)}):")
            
            # Mostrar algunos addons
            display_count = min(10, len(addons_list))
            for i, addon in enumerate(addons_list[:display_count]):
                console.print(f"   • {addon}")
            
            if len(addons_list) > display_count:
                console.print(f"   ... y {len(addons_list) - display_count} más")
            
            # Preguntar por addons
            addons_input = Prompt.ask(
                "\n🔌 Addons a incluir (separados por comas, Enter para ninguno)"
            )
            
            if addons_input:
                selected_addons = [addon.strip() for addon in addons_input.split(",")]
                # Validar que los addons existen
                available_addons = {addon.lower() for addon in addons_list}
                valid_addons = []
                
                for addon in selected_addons:
                    if addon.lower() in available_addons:
                        # Encontrar el nombre exacto
                        exact_name = next(a for a in addons_list if a.lower() == addon.lower())
                        valid_addons.append(exact_name)
                    else:
                        console.print(f"⚠️  Addon no encontrado: {addon}", style="yellow")
                
                return self.generate_project(project_name, output_dir, valid_addons if valid_addons else None)
            else:
                return self.generate_project(project_name, output_dir, None)
        else:
            return self.generate_project(project_name, output_dir, None)

def setup_of_config() -> Dict[str, Any]:
    """Configurar la ruta de openFrameworks."""
    config = {}
    
    # Intentar leer de variables de entorno
    of_path_env = os.getenv('OPENFRAMEWORKS_PATH')
    if of_path_env:
        config['of_path'] = Path(of_path_env)
        console.print(f"📁 Usando OF path de variable de entorno: {of_path_env}")
        return config
    
    # Usar ruta por defecto
    default_of_path = Path("/Users/joseassizalcarazbaxter/Documents/UNA/POSGRADO/2025_1/PyA/of_v0.12.1_osx_release")
    
    if default_of_path.exists():
        config['of_path'] = default_of_path
        console.print(f"📁 Usando OF path por defecto: {default_of_path}")
    else:
        console.print(f"⚠️  openFrameworks no encontrado en: {default_of_path}", style="yellow")
        console.print("💡 Especifica la ruta con --of-path o export OPENFRAMEWORKS_PATH", style="blue")
    
    return config

