#!/usr/bin/env python3
"""
Test script para la integración bidireccional Cursor CLI
======================================================

Este script prueba las nuevas funcionalidades de integración bidireccional
implementadas en Pre-Cursor.

Uso:
    python test_bidirectional_integration.py
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

def test_bidirectional_integration():
    """Probar las funcionalidades de integración bidireccional."""
    print("🧪 Probando integración bidireccional Cursor CLI...")
    
    # Crear directorio temporal para pruebas
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project = Path(temp_dir) / "test_bidirectional_project"
        test_project.mkdir()
        
        print(f"📁 Directorio de prueba: {test_project}")
        
        # Crear estructura básica del proyecto
        (test_project / "src").mkdir()
        (test_project / "tests").mkdir()
        (test_project / "docs").mkdir()
        (test_project / "config").mkdir()
        
        # Crear algunos archivos de prueba con problemas intencionales
        (test_project / "README.md").write_text("# Test Project\n")
        (test_project / "main.py").write_text("print('Hello World')\n")
        (test_project / "test_main.py").write_text("def test_main():\n    pass\n")  # Problema: test en raíz
        (test_project / "src" / "config.py").write_text("# Config file\n")  # Problema: config en src
        
        print("📝 Archivos de prueba creados con problemas intencionales")
        
        # Probar comando instructions
        print("\n1️⃣ Probando comando 'instructions'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "instructions", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando instructions ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando instructions: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando instructions: {e}")
        
        # Probar comando apply
        print("\n2️⃣ Probando comando 'apply'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "apply", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando apply ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando apply: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando apply: {e}")
        
        # Probar comando metrics
        print("\n3️⃣ Probando comando 'metrics'...")
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.pre_cursor.cli", 
                "supervisor", "metrics", str(test_project)
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("   ✅ Comando metrics ejecutado correctamente")
                print(f"   📊 Salida: {result.stdout[:200]}...")
            else:
                print(f"   ❌ Error en comando metrics: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error ejecutando metrics: {e}")
        
        # Verificar archivos generados
        print("\n4️⃣ Verificando archivos generados...")
        generated_files = [
            "CURSOR_INSTRUCTIONS.json",
            "CURSOR_EXECUTION_LOG.json", 
            "CURSOR_FEEDBACK_LOG.json",
            "CURSOR_METRICS.json"
        ]
        
        for file_name in generated_files:
            file_path = test_project / file_name
            if file_path.exists():
                print(f"   ✅ {file_name} generado correctamente")
            else:
                print(f"   ⚠️ {file_name} no encontrado (puede ser normal si no se ejecutaron correcciones)")
        
        # Verificar bitácora actualizada
        bitacora_path = test_project / "BITACORA.md"
        if bitacora_path.exists():
            print("   ✅ BITACORA.md creada/actualizada")
        else:
            print("   ⚠️ BITACORA.md no encontrada")
        
        print("\n🎉 Pruebas de integración bidireccional completadas")
        print("💡 Revisa los archivos generados para ver los resultados detallados")

def test_import_modules():
    """Probar que los módulos se pueden importar correctamente."""
    print("\n🔍 Probando importación de módulos...")
    
    try:
        # Añadir src al path
        sys.path.insert(0, 'src')
        
        # Importar módulos de integración bidireccional
        from pre_cursor.cursor_instruction_generator import CursorInstructionGenerator, CursorInstruction
        from pre_cursor.cursor_cli_interface import CursorCLIInterface, ExecutionResult
        from pre_cursor.feedback_processor import FeedbackProcessor
        from pre_cursor.cursor_supervisor import CursorSupervisor
        
        print("   ✅ Todos los módulos importados correctamente")
        
        # Probar creación de instancias básicas
        with tempfile.TemporaryDirectory() as temp_dir:
            # CursorInstructionGenerator
            generator = CursorInstructionGenerator(temp_dir)
            print("   ✅ CursorInstructionGenerator creado")
            
            # CursorCLIInterface
            interface = CursorCLIInterface(temp_dir)
            print("   ✅ CursorCLIInterface creado")
            
            # FeedbackProcessor
            processor = FeedbackProcessor(temp_dir)
            print("   ✅ FeedbackProcessor creado")
            
            # CursorSupervisor con integración bidireccional
            supervisor = CursorSupervisor(temp_dir, enable_bidirectional=True)
            print("   ✅ CursorSupervisor con integración bidireccional creado")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def main():
    """Función principal del test."""
    print("🚀 Iniciando pruebas de integración bidireccional Cursor CLI")
    print("=" * 60)
    
    # Probar importación de módulos
    if not test_import_modules():
        print("\n❌ Falló la importación de módulos - abortando pruebas")
        return
    
    # Probar funcionalidades de integración
    test_bidirectional_integration()
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("💡 Para más detalles, revisa los logs y archivos generados")

if __name__ == "__main__":
    main()
