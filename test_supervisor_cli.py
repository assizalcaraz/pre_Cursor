#!/usr/bin/env python3
"""
Test script para las nuevas funcionalidades del CLI del supervisor
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def test_supervisor_cli():
    """Probar las nuevas funcionalidades del CLI del supervisor."""
    print("🧪 Probando funcionalidades del CLI del supervisor...")
    
    # Crear directorio temporal para pruebas
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project = Path(temp_dir) / "test_supervisor_project"
        test_project.mkdir()
        
        print(f"📁 Directorio de prueba: {test_project}")
        
        # Crear estructura básica del proyecto
        (test_project / "src").mkdir()
        (test_project / "tests").mkdir()
        (test_project / "docs").mkdir()
        (test_project / "config").mkdir()
        
        # Crear algunos archivos de prueba
        (test_project / "README.md").write_text("# Test Project\n")
        (test_project / "main.py").write_text("print('Hello World')\n")
        (test_project / "test_main.py").write_text("def test_main():\n    pass\n")
        
        # Probar comando status
        print("\n1️⃣ Probando comando 'status'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "status", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando status ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando status: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando status: {e}")
        
        # Probar comando config
        print("\n2️⃣ Probando comando 'config'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "config", str(test_project),
                "--interval", "600",
                "--auto-fix", "true",
                "--log-level", "DEBUG"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando config ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
                
                # Verificar que se creó el archivo de configuración
                config_file = test_project / "config" / "cursor_supervisor.yaml"
                if config_file.exists():
                    print("   ✅ Archivo de configuración creado")
                    print(f"   📄 Contenido: {config_file.read_text()[:200]}...")
                else:
                    print("   ❌ Archivo de configuración no encontrado")
            else:
                print(f"   ❌ Error en comando config: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando config: {e}")
        
        # Probar comando start (verificación única)
        print("\n3️⃣ Probando comando 'start' (verificación única)...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "start", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando start ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando start: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando start: {e}")
        
        # Probar comando fix
        print("\n4️⃣ Probando comando 'fix'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "fix", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando fix ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando fix: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando fix: {e}")
        
        # Probar comando logs
        print("\n5️⃣ Probando comando 'logs'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "logs", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando logs ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando logs: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando logs: {e}")
        
        # Probar comando stop
        print("\n6️⃣ Probando comando 'stop'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "stop", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando stop ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando stop: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando stop: {e}")
    
    print("\n🎉 Pruebas del CLI del supervisor completadas!")

def test_help_commands():
    """Probar comandos de ayuda."""
    print("\n📚 Probando comandos de ayuda...")
    
    commands_to_test = [
        ["supervisor", "--help"],
        ["supervisor", "start", "--help"],
        ["supervisor", "status", "--help"],
        ["supervisor", "config", "--help"],
        ["supervisor", "fix", "--help"],
        ["supervisor", "logs", "--help"],
        ["supervisor", "stop", "--help"],
        ["--help"],
        ["info", "--help"]
    ]
    
    for cmd in commands_to_test:
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli"
            ] + cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print(f"   ✅ {' '.join(cmd)}: OK")
            else:
                print(f"   ❌ {' '.join(cmd)}: Error")
        except Exception as e:
            print(f"   ❌ {' '.join(cmd)}: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del CLI del supervisor...")
    
    # Verificar que estamos en el directorio correcto
    if not Path("src/pre_cursor/cli.py").exists():
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Instalar dependencias si es necesario
    try:
        import watchdog
        import psutil
        print("✅ Dependencias del supervisor encontradas")
    except ImportError:
        print("⚠️ Instalando dependencias del supervisor...")
        subprocess.run([sys.executable, "-m", "pip", "install", "watchdog", "psutil"])
    
    # Ejecutar pruebas
    test_help_commands()
    test_supervisor_cli()
    
    print("\n✅ Todas las pruebas completadas!")
