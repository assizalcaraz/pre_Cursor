#!/usr/bin/env python3
"""
Ejemplo de uso del Generador de Proyectos

Este script demuestra cómo usar el generador de proyectos
de manera programática.
"""

from init_project import ProjectGenerator
from pathlib import Path

def ejemplo_basico():
    """Ejemplo básico de generación de proyecto."""
    print("🔧 Ejemplo básico de generación de proyecto")
    
    generator = ProjectGenerator()
    
    # Configurar datos del proyecto
    generator.project_data = {
        "NOMBRE_PROYECTO": "MiProyectoEjemplo",
        "DESCRIPCION_PROYECTO": "Un proyecto de ejemplo generado automáticamente",
        "DESCRIPCION_DETALLADA": "Este es un proyecto de ejemplo que demuestra las capacidades del generador de proyectos optimizado para agentes de IA.",
        "OBJETIVO_PROYECTO": "Demostrar la generación automática de proyectos",
        "FUNCIONALIDAD_PRINCIPAL": "Procesamiento de datos",
        "TIPO_PROYECTO": "Python Library",
        "AUTOR": "Sistema de Generación",
        "EMAIL_CONTACTO": "ejemplo@email.com",
        "GITHUB_USER": "ejemplo",
        "REPOSITORIO_URL": "https://github.com/ejemplo/MiProyectoEjemplo",
        "PYTHON_VERSION_MIN": "3.8",
        "LICENCIA": "MIT",
        "FECHA_CREACION": "2024-12-19",
        "FECHA_ACTUALIZACION": "2024-12-19",
        "MODULO_PRINCIPAL": "mi_proyecto_ejemplo",
        "CLASE_PRINCIPAL": "MiProyectoEjemplo",
        "ESTADO_INICIAL": "Fase inicial - Configuración",
        "PRIMER_PASO": "Implementar funcionalidades core",
        "SEGUNDO_PASO": "Crear tests unitarios",
        "TERCER_PASO": "Documentar API",
        "SIGUIENTE_PASO": "Implementar primera funcionalidad",
        "EJEMPLO_USO": "# Crear instancia\ninstancia = MiProyectoEjemplo()\n# Usar funcionalidad\nresultado = instancia.procesar()",
        "CONFIGURACION_EJEMPLO": "# Configuración para MiProyectoEjemplo\nDEBUG = True\nLOG_LEVEL = 'INFO'",
        "DEPENDENCIAS_PRINCIPALES": "# Dependencias principales\n# requests>=2.28.0",
        "DEPENDENCIAS_DESARROLLO": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
        "DEPENDENCIAS_TESTING": "pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0",
        "DEPENDENCIAS_OPCIONALES": "# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0",
    }
    
    # Generar proyecto
    project_path = Path.cwd() / "ejemplo_generado"
    generator.generate_project("MiProyectoEjemplo", project_path)
    
    print("✅ Proyecto de ejemplo generado exitosamente")

def ejemplo_con_configuracion():
    """Ejemplo con configuración personalizada."""
    print("🔧 Ejemplo con configuración personalizada")
    
    # Aquí podrías cargar configuración desde un archivo JSON
    config_data = {
        "NOMBRE_PROYECTO": "ProyectoPersonalizado",
        "DESCRIPCION_PROYECTO": "Proyecto con configuración personalizada",
        "TIPO_PROYECTO": "Python CLI Tool",
        "AUTOR": "Desarrollador Personalizado",
        "DEPENDENCIAS_PRINCIPALES": "# Dependencias principales\nclick>=8.0.0\nrich>=12.0.0",
    }
    
    generator = ProjectGenerator()
    generator.project_data.update(config_data)
    
    # Completar datos faltantes con valores por defecto
    generator.project_data.update({
        "DESCRIPCION_DETALLADA": "Proyecto con configuración personalizada",
        "OBJETIVO_PROYECTO": "Demostrar configuración personalizada",
        "FUNCIONALIDAD_PRINCIPAL": "Herramienta de línea de comandos",
        "EMAIL_CONTACTO": "personalizado@email.com",
        "GITHUB_USER": "personalizado",
        "REPOSITORIO_URL": "https://github.com/personalizado/ProyectoPersonalizado",
        "PYTHON_VERSION_MIN": "3.8",
        "LICENCIA": "MIT",
        "FECHA_CREACION": "2024-12-19",
        "FECHA_ACTUALIZACION": "2024-12-19",
        "MODULO_PRINCIPAL": "proyecto_personalizado",
        "CLASE_PRINCIPAL": "ProyectoPersonalizado",
        "ESTADO_INICIAL": "Fase inicial - Configuración",
        "PRIMER_PASO": "Implementar funcionalidades core",
        "SEGUNDO_PASO": "Crear tests unitarios",
        "TERCER_PASO": "Documentar API",
        "SIGUIENTE_PASO": "Implementar primera funcionalidad",
        "EJEMPLO_USO": "# Crear instancia\ninstancia = ProyectoPersonalizado()\n# Usar funcionalidad\nresultado = instancia.procesar()",
        "CONFIGURACION_EJEMPLO": "# Configuración para ProyectoPersonalizado\nDEBUG = True\nLOG_LEVEL = 'INFO'",
        "DEPENDENCIAS_DESARROLLO": "pytest>=7.0.0\npytest-cov>=4.0.0\nblack>=22.0.0\nflake8>=5.0.0",
        "DEPENDENCIAS_TESTING": "pytest>=7.0.0\npytest-cov>=4.0.0\npytest-asyncio>=0.21.0",
        "DEPENDENCIAS_OPCIONALES": "# Dependencias opcionales\n# requests>=2.28.0\n# numpy>=1.21.0",
    })
    
    project_path = Path.cwd() / "ejemplo_personalizado"
    generator.generate_project("ProyectoPersonalizado", project_path)
    
    print("✅ Proyecto personalizado generado exitosamente")

if __name__ == "__main__":
    print("🚀 Ejemplos de uso del Generador de Proyectos")
    print("=" * 50)
    
    try:
        # Ejecutar ejemplos
        ejemplo_basico()
        print()
        ejemplo_con_configuracion()
        
        print()
        print("🎉 Todos los ejemplos ejecutados exitosamente")
        print("📂 Revisa los directorios 'ejemplo_generado' y 'ejemplo_personalizado'")
        
    except Exception as e:
        print(f"❌ Error ejecutando ejemplos: {e}")
