#!/usr/bin/env python3
"""
Script de prueba para la integración completa
============================================

Este script prueba la integración completa entre init_project.py
y el Cursor Supervisor.

Uso:
    python test_integration.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Añadir src al path
sys.path.insert(0, 'src')

def test_integration():
    """Probar integración completa"""
    print("🧪 Iniciando prueba de integración completa")
    
    # Crear directorio temporal
    test_dir = tempfile.mkdtemp(prefix='integration_test_')
    project_path = Path(test_dir) / 'test_integration_project'
    
    try:
        # Importar el generador
        from init_project import ProjectGenerator
        
        # Crear generador
        generator = ProjectGenerator(verbose=True)
        
        print(f"📁 Creando proyecto en: {project_path}")
        
        # Generar proyecto
        generator.generate_project('test_integration_project', project_path)
        
        # Verificar que se crearon los archivos esperados
        expected_files = [
            'README.md',
            'CURSOR_GUIDE.md',
            'TUTORIAL.md',
            'BITACORA.md',
            'requirements.txt',
            'src/',
            'tests/',
            'docs/',
            'examples/',
            'logs/'
        ]
        
        print("\n🔍 Verificando archivos generados:")
        missing_files = []
        for file_path in expected_files:
            full_path = project_path / file_path
            if full_path.exists():
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path}")
                missing_files.append(file_path)
        
        # Verificar archivos específicos de integración
        integration_files = [
            'CURSOR_INSTRUCTIONS.md',
            'logs/supervisor.log'
        ]
        
        print("\n🤖 Verificando archivos de integración:")
        for file_path in integration_files:
            full_path = project_path / file_path
            if full_path.exists():
                print(f"   ✅ {file_path}")
            else:
                print(f"   ⚠️  {file_path} (opcional)")
        
        # Verificar contenido de CURSOR_INSTRUCTIONS.md
        instructions_file = project_path / 'CURSOR_INSTRUCTIONS.md'
        if instructions_file.exists():
            print("\n📝 Contenido de CURSOR_INSTRUCTIONS.md:")
            with open(instructions_file, 'r') as f:
                content = f.read()
                lines = content.split('\n')[:10]  # Primeras 10 líneas
                for line in lines:
                    print(f"   {line}")
                if len(content.split('\n')) > 10:
                    print("   ...")
        
        # Verificar logs del supervisor
        supervisor_log = project_path / 'logs' / 'supervisor.log'
        if supervisor_log.exists():
            print("\n📊 Logs del supervisor:")
            with open(supervisor_log, 'r') as f:
                lines = f.readlines()
                for line in lines[-5:]:  # Últimas 5 líneas
                    print(f"   {line.strip()}")
        
        # Verificar bitácora
        bitacora_file = project_path / 'BITACORA.md'
        if bitacora_file.exists():
            with open(bitacora_file, 'r') as f:
                content = f.read()
                if "Supervisión Automática" in content:
                    print("\n📋 Bitácora actualizada con supervisión: ✅")
                else:
                    print("\n📋 Bitácora sin supervisión: ⚠️")
        
        # Resumen
        print(f"\n📊 Resumen de la prueba:")
        print(f"   Archivos esperados: {len(expected_files)}")
        print(f"   Archivos faltantes: {len(missing_files)}")
        print(f"   Archivos de integración: {len([f for f in integration_files if (project_path / f).exists()])}")
        
        if missing_files:
            print(f"\n❌ Archivos faltantes: {missing_files}")
            return False
        else:
            print("\n✅ Integración completa exitosa")
            return True
            
    except Exception as e:
        print(f"\n❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpiar
        print(f"\n🧹 Limpiando directorio de prueba...")
        shutil.rmtree(test_dir)
        print("✅ Limpieza completada")

def test_supervisor_only():
    """Probar solo el supervisor"""
    print("\n🔍 Probando supervisor independiente...")
    
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
        
        # Verificar que se actualizó la bitácora
        with open(project_path / 'BITACORA.md', 'r') as f:
            content = f.read()
            if "Supervisión Automática" in content:
                print("   ✅ Bitácora actualizada correctamente")
            else:
                print("   ❌ Bitácora no actualizada")
        
        return len(report.issues_found) > 0
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
        
    finally:
        shutil.rmtree(test_dir)

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de integración")
    
    # Probar supervisor independiente
    supervisor_ok = test_supervisor_only()
    
    # Probar integración completa
    integration_ok = test_integration()
    
    print(f"\n📊 Resultados finales:")
    print(f"   Supervisor independiente: {'✅' if supervisor_ok else '❌'}")
    print(f"   Integración completa: {'✅' if integration_ok else '❌'}")
    
    if supervisor_ok and integration_ok:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        return 0
    else:
        print("\n❌ Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())
