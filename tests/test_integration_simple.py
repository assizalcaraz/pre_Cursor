#!/usr/bin/env python3
"""
Script de prueba simplificado para la integración
================================================

Este script prueba la integración sin prompts interactivos.

Uso:
    python test_integration_simple.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Añadir src al path
sys.path.insert(0, 'src')

def test_supervisor_only():
    """Probar solo el supervisor"""
    print("🔍 Probando supervisor independiente...")
    
    # Crear directorio temporal
    test_dir = tempfile.mkdtemp(prefix='supervisor_test_')
    project_path = Path(test_dir) / 'supervisor_test_project'
    project_path.mkdir()
    
    try:
        # Crear estructura básica
        (project_path / 'src').mkdir()
        (project_path / 'tests').mkdir()
        (project_path / 'docs').mkdir()
        (project_path / 'logs').mkdir()
        
        # Crear archivo de test en raíz (problema)
        with open(project_path / 'test_main.py', 'w') as f:
            f.write("def test_main(): pass")
        
        # Crear bitácora
        with open(project_path / 'BITACORA.md', 'w') as f:
            f.write("# Bitácora del Proyecto\n\n")
        
        # Importar y probar supervisor
        from pre_cursor.cursor_supervisor import CursorSupervisor
        
        supervisor = CursorSupervisor(str(project_path), check_interval=1)
        report = supervisor.check_project_health()
        
        print(f"   Problemas encontrados: {len(report.issues_found)}")
        for issue in report.issues_found:
            print(f"   - {issue.severity.upper()}: {issue.description}")
        
        # Actualizar bitácora manualmente
        supervisor.update_bitacora(report)
        
        # Verificar que se actualizó la bitácora
        with open(project_path / 'BITACORA.md', 'r') as f:
            content = f.read()
            if "Supervisión Automática" in content:
                print("   ✅ Bitácora actualizada correctamente")
                return True
            else:
                print("   ❌ Bitácora no actualizada")
                print(f"   Contenido actual: {content[:200]}...")
                return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)

def test_integration_module():
    """Probar módulo de integración"""
    print("\n🔗 Probando módulo de integración...")
    
    # Crear directorio temporal
    test_dir = tempfile.mkdtemp(prefix='integration_test_')
    project_path = Path(test_dir) / 'test_project'
    project_path.mkdir()
    
    try:
        # Crear estructura básica
        (project_path / 'src').mkdir()
        (project_path / 'tests').mkdir()
        (project_path / 'docs').mkdir()
        (project_path / 'logs').mkdir()
        
        # Crear bitácora
        with open(project_path / 'BITACORA.md', 'w') as f:
            f.write("# Bitácora del Proyecto\n\n")
        
        # Importar módulo de integración
        from pre_cursor.cursor_integration import CursorIntegrationManager
        
        # Crear configuración del proyecto
        project_config = {
            'tipo_proyecto': 'Python Library',
            'descripcion_proyecto': 'Proyecto de prueba',
            'nombre_proyecto': 'test_project',
            'version': '1.0.0',
            'autor': 'Test User',
            'email': 'test@example.com'
        }
        
        # Crear gestor de integración
        integration_manager = CursorIntegrationManager(str(project_path), enable_supervision=True)
        
        # Generar instrucciones
        instructions = integration_manager.generate_cursor_instructions(
            project_config['tipo_proyecto'],
            project_config['descripcion_proyecto']
        )
        
        print(f"   Instrucciones generadas: {len(instructions)} caracteres")
        
        # Verificar que las instrucciones contienen contenido relevante
        if "Instrucciones para Cursor AI" in instructions:
            print("   ✅ Instrucciones generadas correctamente")
            return True
        else:
            print("   ❌ Instrucciones no generadas correctamente")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)

def test_cursor_generator():
    """Probar generador de Cursor"""
    print("\n🤖 Probando generador de Cursor...")
    
    # Crear directorio temporal
    test_dir = tempfile.mkdtemp(prefix='generator_test_')
    project_path = Path(test_dir) / 'test_project'
    project_path.mkdir()
    
    try:
        # Crear estructura básica
        (project_path / 'src').mkdir()
        (project_path / 'tests').mkdir()
        (project_path / 'docs').mkdir()
        (project_path / 'logs').mkdir()
        
        # Crear bitácora
        with open(project_path / 'BITACORA.md', 'w') as f:
            f.write("# Bitácora del Proyecto\n\n")
        
        # Importar generador
        from pre_cursor.cursor_integration import CursorProjectGenerator
        
        # Crear configuración del proyecto
        project_config = {
            'tipo_proyecto': 'Python Library',
            'descripcion_proyecto': 'Proyecto de prueba',
            'nombre_proyecto': 'test_project',
            'version': '1.0.0',
            'autor': 'Test User',
            'email': 'test@example.com'
        }
        
        # Crear generador
        generator = CursorProjectGenerator(str(project_path), project_config)
        
        # Generar proyecto (sin abrir Cursor)
        generator.integration_manager.enable_supervision = False  # Deshabilitar supervisión para test
        
        # Verificar que se pueden generar instrucciones
        instructions = generator.integration_manager.generate_cursor_instructions(
            project_config['tipo_proyecto'],
            project_config['descripcion_proyecto']
        )
        
        if "Instrucciones para Cursor AI" in instructions:
            print("   ✅ Generador funcionando correctamente")
            return True
        else:
            print("   ❌ Generador no funcionando correctamente")
            return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        shutil.rmtree(test_dir)

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de integración simplificadas")
    
    # Probar componentes individuales
    supervisor_ok = test_supervisor_only()
    integration_ok = test_integration_module()
    generator_ok = test_cursor_generator()
    
    print(f"\n📊 Resultados finales:")
    print(f"   Supervisor independiente: {'✅' if supervisor_ok else '❌'}")
    print(f"   Módulo de integración: {'✅' if integration_ok else '❌'}")
    print(f"   Generador de Cursor: {'✅' if generator_ok else '❌'}")
    
    if supervisor_ok and integration_ok and generator_ok:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
