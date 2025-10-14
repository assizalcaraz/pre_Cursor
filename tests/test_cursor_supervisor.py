#!/usr/bin/env python3
"""
Script de prueba para Cursor Supervisor
======================================

Este script prueba las funcionalidades del Cursor Supervisor
creando un proyecto de ejemplo con problemas intencionales.

Uso:
    python test_cursor_supervisor.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Añadir src al path para importar módulos
sys.path.insert(0, 'src')

from pre_cursor.cursor_supervisor import CursorSupervisor, ProjectStructureMonitor, DuplicateDetector

def create_test_project():
    """Crear proyecto de prueba con problemas intencionales"""
    # Crear directorio temporal
    test_dir = tempfile.mkdtemp(prefix='cursor_supervisor_test_')
    project_path = Path(test_dir) / 'test_project'
    project_path.mkdir()
    
    print(f"📁 Creando proyecto de prueba en: {project_path}")
    
    # Crear estructura básica
    (project_path / 'src').mkdir()
    (project_path / 'tests').mkdir()
    (project_path / 'docs').mkdir()
    (project_path / 'logs').mkdir()
    
    # Crear archivos con problemas intencionales
    
    # 1. Archivo de test en raíz (problema)
    with open(project_path / 'test_main.py', 'w') as f:
        f.write("""
def test_main():
    assert True
""")
    
    # 2. Archivo de configuración en src/ (problema)
    with open(project_path / 'src' / 'config.py', 'w') as f:
        f.write("""
CONFIG = {
    'debug': True
}
""")
    
    # 3. Archivo duplicado
    with open(project_path / 'duplicate_file.py', 'w') as f:
        f.write("""
def duplicate_function():
    return "duplicate"
""")
    
    with open(project_path / 'src' / 'duplicate_file.py', 'w') as f:
        f.write("""
def duplicate_function():
    return "duplicate"
""")
    
    # 4. Función duplicada en diferentes archivos
    with open(project_path / 'src' / 'utils.py', 'w') as f:
        f.write("""
def helper_function():
    return "helper"
""")
    
    with open(project_path / 'src' / 'helpers.py', 'w') as f:
        f.write("""
def helper_function():
    return "helper"
""")
    
    # 5. Crear bitácora básica
    with open(project_path / 'BITACORA.md', 'w') as f:
        f.write("""# Bitácora del Proyecto

## Desarrollo
- Proyecto creado para pruebas del supervisor

""")
    
    return project_path

def test_structure_monitor(project_path):
    """Probar monitor de estructura"""
    print("\n🔍 Probando monitor de estructura...")
    
    monitor = ProjectStructureMonitor(str(project_path))
    
    # Verificar estructura
    structure_issues = monitor.check_structure()
    print(f"   Problemas de estructura encontrados: {len(structure_issues)}")
    for issue in structure_issues:
        print(f"   - {issue.severity.upper()}: {issue.description}")
    
    # Verificar archivos fuera de lugar
    misplaced_issues = monitor.check_files_out_of_place()
    print(f"   Archivos fuera de lugar: {len(misplaced_issues)}")
    for issue in misplaced_issues:
        print(f"   - {issue.severity.upper()}: {issue.description}")

def test_duplicate_detector(project_path):
    """Probar detector de duplicados"""
    print("\n🔍 Probando detector de duplicados...")
    
    detector = DuplicateDetector(str(project_path))
    
    # Buscar archivos duplicados
    duplicate_files = detector.find_duplicate_files()
    print(f"   Archivos duplicados encontrados: {len(duplicate_files)}")
    for issue in duplicate_files:
        print(f"   - {issue.severity.upper()}: {issue.description}")
    
    # Buscar funciones duplicadas
    duplicate_functions = detector.find_duplicate_functions()
    print(f"   Funciones duplicadas encontradas: {len(duplicate_functions)}")
    for issue in duplicate_functions:
        print(f"   - {issue.severity.upper()}: {issue.description}")

def test_supervisor(project_path):
    """Probar supervisor completo"""
    print("\n🤖 Probando supervisor completo...")
    
    supervisor = CursorSupervisor(str(project_path), check_interval=1)
    
    # Ejecutar una verificación
    report = supervisor.check_project_health()
    
    print(f"   Problemas totales encontrados: {len(report.issues_found)}")
    print(f"   Recomendaciones generadas: {len(report.recommendations)}")
    
    # Mostrar problemas por severidad
    severity_counts = {}
    for issue in report.issues_found:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
    
    print("   Problemas por severidad:")
    for severity, count in severity_counts.items():
        print(f"   - {severity.upper()}: {count}")
    
    # Mostrar recomendaciones
    if report.recommendations:
        print("   Recomendaciones:")
        for rec in report.recommendations:
            print(f"   - {rec}")
    
    # Verificar si se actualizó la bitácora
    bitacora_path = project_path / 'BITACORA.md'
    if bitacora_path.exists():
        with open(bitacora_path, 'r') as f:
            content = f.read()
            if "Supervisión Automática" in content:
                print("   ✅ Bitácora actualizada correctamente")
            else:
                print("   ❌ Bitácora no fue actualizada")

def main():
    """Función principal de prueba"""
    print("🧪 Iniciando pruebas del Cursor Supervisor")
    
    # Crear proyecto de prueba
    project_path = create_test_project()
    
    try:
        # Probar componentes individuales
        test_structure_monitor(project_path)
        test_duplicate_detector(project_path)
        test_supervisor(project_path)
        
        print("\n✅ Pruebas completadas exitosamente")
        
        # Mostrar estructura del proyecto de prueba
        print(f"\n📁 Estructura del proyecto de prueba:")
        for root, dirs, files in os.walk(project_path):
            level = root.replace(str(project_path), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
    finally:
        # Limpiar proyecto de prueba
        print(f"\n🧹 Limpiando proyecto de prueba...")
        shutil.rmtree(project_path.parent)
        print("✅ Limpieza completada")

if __name__ == "__main__":
    main()
