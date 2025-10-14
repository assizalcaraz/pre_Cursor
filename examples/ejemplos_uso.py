#!/usr/bin/env python3
"""
Ejemplos de Uso - Pre-Cursor
============================

Este script demuestra cómo usar Pre-Cursor con diferentes tipos de configuración.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado."""
    print(f"\n🔄 {description}")
    print(f"Comando: {cmd}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Éxito!")
            if result.stdout:
                print(f"Salida: {result.stdout[:200]}...")
        else:
            print("❌ Error!")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
    except Exception as e:
        print(f"❌ Excepción: {e}")

def main():
    """Ejecutar ejemplos de uso."""
    print("🚀 Ejemplos de Uso - Pre-Cursor")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("init_project.py"):
        print("❌ Error: Ejecuta este script desde el directorio pre_cursor")
        sys.exit(1)
    
    # Ejemplo 1: Crear proyecto Python Library usando configuración
    print("\n📚 Ejemplo 1: Crear Librería Python")
    run_command(
        "python3 init_project.py --config examples/ejemplo_python_library.json",
        "Crear librería Python usando archivo de configuración"
    )
    
    # Ejemplo 2: Crear proyecto FastAPI usando configuración
    print("\n🌐 Ejemplo 2: Crear API FastAPI")
    run_command(
        "python3 init_project.py --config examples/ejemplo_fastapi.json",
        "Crear API FastAPI usando archivo de configuración"
    )
    
    # Ejemplo 3: Crear proyecto TD_MCP usando configuración
    print("\n🎨 Ejemplo 3: Crear Proyecto TD_MCP")
    run_command(
        "python3 init_project.py --config examples/ejemplo_td_mcp.json",
        "Crear proyecto TD_MCP usando archivo de configuración"
    )
    
    # Ejemplo 4: Crear plantilla personalizada
    print("\n📝 Ejemplo 4: Crear Plantilla Personalizada")
    run_command(
        'python3 init_project.py --create-template "Python CLI Tool" -o mi_plantilla.json',
        "Crear plantilla para Python CLI Tool"
    )
    
    # Ejemplo 5: Modo interactivo (simulado)
    print("\n💬 Ejemplo 5: Modo Interactivo")
    print("Para usar el modo interactivo, ejecuta:")
    print("python3 init_project.py")
    print("Y sigue las instrucciones en pantalla.")
    
    # Mostrar archivos generados
    print("\n📁 Archivos Generados:")
    print("-" * 30)
    
    generated_dirs = [
        "mi_libreria_python",
        "mi_api_fastapi", 
        "mi_proyecto_td_mcp"
    ]
    
    for dir_name in generated_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/")
            # Mostrar estructura básica
            try:
                files = list(Path(dir_name).rglob("*"))[:10]  # Primeros 10 archivos
                for file_path in files:
                    if file_path.is_file():
                        print(f"   📄 {file_path.relative_to(dir_name)}")
            except:
                pass
        else:
            print(f"❌ {dir_name}/ (no generado)")
    
    print("\n🎉 ¡Ejemplos completados!")
    print("\n📖 Para más información:")
    print("- Lee QUICKSTART.md para guía detallada")
    print("- Revisa README.md para documentación completa")
    print("- Explora examples/ para más configuraciones")

if __name__ == "__main__":
    main()
