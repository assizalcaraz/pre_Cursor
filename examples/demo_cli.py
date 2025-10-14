#!/usr/bin/env python3
"""
Demo del CLI mejorado de Pre-Cursor
==================================

Este script demuestra las nuevas funcionalidades del CLI mejorado.
"""

import subprocess
import sys
import os

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
                print(f"Salida:\n{result.stdout}")
        else:
            print("❌ Error!")
            if result.stderr:
                print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

def main():
    """Ejecutar demo del CLI mejorado."""
    print("🚀 Demo del CLI Mejorado - Pre-Cursor")
    print("=" * 50)
    
    # Verificar que el CLI esté instalado
    if not os.path.exists("cli.py"):
        print("❌ Error: cli.py no encontrado")
        sys.exit(1)
    
    # Demo 1: Ayuda general
    print("\n📚 Demo 1: Ayuda general")
    run_command("python3 cli.py --help", "Mostrar ayuda general")
    
    # Demo 2: Listar tipos de proyecto
    print("\n📋 Demo 2: Listar tipos de proyecto")
    run_command("python3 cli.py list-types", "Listar tipos disponibles")
    
    # Demo 3: Información del proyecto
    print("\nℹ️ Demo 3: Información del proyecto")
    run_command("python3 cli.py info --examples", "Mostrar información con ejemplos")
    
    # Demo 4: Crear plantilla
    print("\n📝 Demo 4: Crear plantilla")
    run_command("python3 cli.py template --type 'Python Library' --output demo_template.json", "Crear plantilla Python Library")
    
    # Demo 5: Crear proyecto (dry-run)
    print("\n🎯 Demo 5: Crear proyecto (simulación)")
    run_command("python3 cli.py create demo-project --type 'Python Web App (FastAPI)' --dry-run", "Crear proyecto FastAPI (simulación)")
    
    # Demo 6: Generar desde configuración
    print("\n⚡ Demo 6: Generar desde configuración")
    if os.path.exists("demo_template.json"):
        run_command("python3 cli.py generate demo_template.json --dry-run", "Generar desde template (simulación)")
    
    # Demo 7: Modo interactivo (simulado)
    print("\n💬 Demo 7: Modo interactivo")
    print("Para usar el modo interactivo completo:")
    print("python3 cli.py create mi-proyecto --interactive")
    
    # Demo 8: Autocompletado
    print("\n🔧 Demo 8: Configurar autocompletado")
    print("Para activar autocompletado:")
    print("source completion.sh")
    print("pre-cursor <TAB>  # Verá las opciones disponibles")
    
    # Limpiar archivos de demo
    print("\n🧹 Limpiando archivos de demo...")
    if os.path.exists("demo_template.json"):
        os.remove("demo_template.json")
        print("✅ demo_template.json eliminado")
    
    print("\n🎉 Demo completado!")
    print("\n📖 Para más información:")
    print("• python3 cli.py --help")
    print("• python3 cli.py info --examples")
    print("• Revisar QUICKSTART.md para guía detallada")

if __name__ == "__main__":
    main()
