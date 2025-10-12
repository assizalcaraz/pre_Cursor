#!/usr/bin/env python3
"""
Script para ejecutar tests y análisis de cobertura.

Este script ejecuta todos los tests del generador de proyectos
y genera reportes de cobertura detallados.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Ejecutar comando y mostrar resultado."""
    print(f"\n🔧 {description}")
    print("=" * 60)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Éxito")
        if result.stdout:
            print(result.stdout)
    else:
        print("❌ Error")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
    
    return result.returncode == 0


def main():
    """Función principal."""
    print("🧪 Ejecutando Tests y Análisis de Cobertura")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Verificar que pytest está instalado
    try:
        import pytest
        print(f"✅ pytest {pytest.__version__} encontrado")
    except ImportError:
        print("❌ pytest no está instalado")
        print("💡 Instalar con: pip install pytest pytest-cov")
        return 1
    
    # Verificar que pytest-cov está instalado
    try:
        import pytest_cov
        print(f"✅ pytest-cov encontrado")
    except ImportError:
        print("❌ pytest-cov no está instalado")
        print("💡 Instalar con: pip install pytest-cov")
        return 1
    
    # Ejecutar tests unitarios
    success = True
    
    success &= run_command(
        "python -m pytest tests/test_validator.py -v",
        "Tests Unitarios - Validator"
    )
    
    success &= run_command(
        "python -m pytest tests/test_config_loader.py -v",
        "Tests Unitarios - Config Loader"
    )
    
    success &= run_command(
        "python -m pytest tests/test_init_project.py -v",
        "Tests Unitarios - Init Project"
    )
    
    # Ejecutar tests de integración
    success &= run_command(
        "python -m pytest tests/test_integration.py -v",
        "Tests de Integración"
    )
    
    # Ejecutar todos los tests con cobertura
    success &= run_command(
        "python -m pytest tests/ --cov=src --cov=init_project --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml --cov-fail-under=80",
        "Análisis de Cobertura Completo"
    )
    
    # Mostrar resumen
    print("\n📊 Resumen de Resultados")
    print("=" * 60)
    
    if success:
        print("✅ Todos los tests pasaron exitosamente")
        print("✅ Cobertura de código >= 80%")
        print("\n📁 Reportes generados:")
        print("   - htmlcov/index.html (Reporte HTML)")
        print("   - coverage.xml (Reporte XML)")
        print("   - Terminal (Reporte texto)")
        
        # Mostrar estadísticas de archivos
        if Path("htmlcov").exists():
            print(f"\n📈 Reporte HTML disponible en: {Path('htmlcov').absolute()}/index.html")
        
        return 0
    else:
        print("❌ Algunos tests fallaron o cobertura insuficiente")
        print("💡 Revisar los errores arriba y corregir")
        return 1


if __name__ == "__main__":
    sys.exit(main())
