#!/usr/bin/env python3
"""
Cursor Integration - Integración del Supervisor con el Generador
==============================================================

Este módulo integra el CursorSupervisor con init_project.py para
proporcionar supervisión automática durante la generación de proyectos.

Autor: Assiz Alcaraz Baxter
Fecha: 2024-10-13
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from .cursor_supervisor import CursorSupervisor, SupervisionReport

# Configurar logging
logger = logging.getLogger(__name__)

class CursorIntegrationManager:
    """Gestor de integración entre el generador y Cursor Supervisor"""
    
    def __init__(self, project_path: str, enable_supervision: bool = True):
        self.project_path = Path(project_path)
        self.enable_supervision = enable_supervision
        self.supervisor: Optional[CursorSupervisor] = None
        self.supervision_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.cursor_process: Optional[subprocess.Popen] = None
        
        # Configuración
        self.supervision_interval = 60  # 1 minuto para proyectos en desarrollo
        self.max_supervision_time = 3600  # 1 hora máximo
        
    def start_supervision(self) -> bool:
        """Iniciar supervisión del proyecto"""
        if not self.enable_supervision:
            logger.info("Supervisión deshabilitada")
            return True
            
        try:
            # Crear supervisor
            self.supervisor = CursorSupervisor(
                str(self.project_path), 
                check_interval=self.supervision_interval
            )
            
            # Iniciar hilo de supervisión
            self.supervision_thread = threading.Thread(
                target=self._supervision_loop,
                daemon=True
            )
            self.supervision_thread.start()
            
            self.is_running = True
            logger.info(f"Supervisión iniciada para proyecto: {self.project_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al iniciar supervisión: {e}")
            return False
    
    def stop_supervision(self):
        """Detener supervisión del proyecto"""
        self.is_running = False
        
        if self.supervision_thread and self.supervision_thread.is_alive():
            self.supervision_thread.join(timeout=5)
        
        if self.cursor_process:
            try:
                self.cursor_process.terminate()
                self.cursor_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.cursor_process.kill()
            except Exception as e:
                logger.warning(f"Error al detener proceso de Cursor: {e}")
        
        logger.info("Supervisión detenida")
    
    def _supervision_loop(self):
        """Loop principal de supervisión"""
        start_time = time.time()
        
        while self.is_running and (time.time() - start_time) < self.max_supervision_time:
            try:
                if self.supervisor:
                    report = self.supervisor.check_project_health()
                    self._handle_supervision_report(report)
                
                time.sleep(self.supervision_interval)
                
            except Exception as e:
                logger.error(f"Error en loop de supervisión: {e}")
                time.sleep(10)  # Esperar antes de reintentar
    
    def _handle_supervision_report(self, report: SupervisionReport):
        """Manejar reporte de supervisión"""
        if not report.issues_found:
            logger.debug("No se encontraron problemas en la supervisión")
            return
        
        # Log de problemas encontrados
        logger.info(f"Supervisión: {len(report.issues_found)} problemas encontrados")
        
        # Manejar problemas críticos
        critical_issues = [i for i in report.issues_found if i.severity == 'critical']
        if critical_issues:
            logger.warning(f"Problemas críticos detectados: {len(critical_issues)}")
            self._handle_critical_issues(critical_issues)
        
        # Manejar problemas de alta prioridad
        high_issues = [i for i in report.issues_found if i.severity == 'high']
        if high_issues:
            logger.warning(f"Problemas de alta prioridad: {len(high_issues)}")
            self._handle_high_priority_issues(high_issues)
    
    def _handle_critical_issues(self, issues: List):
        """Manejar problemas críticos"""
        for issue in issues:
            logger.error(f"PROBLEMA CRÍTICO: {issue.description}")
            
            # Intentar corrección automática para problemas críticos
            if issue.type == 'missing_directory':
                self._create_missing_directory(issue)
            elif issue.type == 'misplaced_files':
                self._fix_misplaced_files(issue)
    
    def _handle_high_priority_issues(self, issues: List):
        """Manejar problemas de alta prioridad"""
        for issue in issues:
            logger.warning(f"PROBLEMA ALTA PRIORIDAD: {issue.description}")
            
            # Corrección automática para problemas de alta prioridad
            if issue.type == 'duplicate_file':
                self._handle_duplicate_files(issue)
    
    def _create_missing_directory(self, issue):
        """Crear directorio faltante"""
        try:
            if 'examples/' in issue.description:
                (self.project_path / 'examples').mkdir(exist_ok=True)
                logger.info("Directorio examples/ creado automáticamente")
        except Exception as e:
            logger.error(f"Error al crear directorio: {e}")
    
    def _fix_misplaced_files(self, issue):
        """Corregir archivos fuera de lugar"""
        try:
            if 'tests' in issue.description and 'raíz' in issue.description:
                # Mover archivos de test a tests/
                test_files = list(self.project_path.glob('*_test.py'))
                for test_file in test_files:
                    target = self.project_path / 'tests' / test_file.name
                    test_file.rename(target)
                    logger.info(f"Archivo {test_file.name} movido a tests/")
        except Exception as e:
            logger.error(f"Error al corregir archivos fuera de lugar: {e}")
    
    def _handle_duplicate_files(self, issue):
        """Manejar archivos duplicados"""
        logger.warning(f"Archivo duplicado detectado: {issue.file_path}")
        # Por ahora solo loguear, la corrección manual es más segura
    
    def open_cursor_with_context(self, context: str = "") -> bool:
        """Abrir Cursor con contexto específico del proyecto"""
        try:
            # Crear archivo de contexto temporal
            context_file = self.project_path / '.cursor_context.md'
            with open(context_file, 'w', encoding='utf-8') as f:
                f.write(f"""# Contexto del Proyecto para Cursor AI

**Proyecto**: {self.project_path.name}
**Fecha**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instrucciones para Cursor AI

{context}

## Archivos importantes:
- `CURSOR_GUIDE.md`: Guía específica para Cursor AI
- `README.md`: Documentación del proyecto
- `TUTORIAL.md`: Tutorial paso a paso
- `BITACORA.md`: Registro de cambios

## Estructura del proyecto:
- `src/`: Código fuente principal
- `tests/`: Pruebas unitarias
- `docs/`: Documentación
- `examples/`: Ejemplos de uso

---
*Este archivo fue generado automáticamente por Pre-Cursor*
""")
            
            # Abrir Cursor
            cmd = ['cursor', str(self.project_path)]
            self.cursor_process = subprocess.Popen(cmd)
            
            logger.info(f"Cursor abierto con contexto para proyecto: {self.project_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error al abrir Cursor: {e}")
            return False
    
    def generate_cursor_instructions(self, project_type: str, description: str) -> str:
        """Generar instrucciones específicas para Cursor basadas en el tipo de proyecto"""
        
        instructions = f"""# Instrucciones para Cursor AI - {self.project_path.name}

## Objetivo del Proyecto
{description}

## Tipo de Proyecto
{project_type}

## Instrucciones Específicas:

### 1. Estructura del Proyecto
- Mantener archivos de test en `tests/`
- Configuración en directorio raíz, no en `src/`
- Documentación en `docs/`
- Ejemplos en `examples/`

### 2. Generación de Código
- Seguir las convenciones del tipo de proyecto
- Crear funciones modulares y reutilizables
- Incluir docstrings completos
- Añadir type hints donde sea apropiado

### 3. Testing
- Crear tests para cada nueva funcionalidad
- Usar nombres descriptivos para los tests
- Mantener cobertura de código alta

### 4. Documentación
- Actualizar README.md con nuevas funcionalidades
- Mantener BITACORA.md actualizada
- Documentar cambios importantes

### 5. Prevención de Problemas
- NO crear archivos de test en la raíz
- NO duplicar funciones existentes
- NO crear archivos de configuración en `src/`
- Verificar que los imports sean correctos

## Archivos de Referencia:
- `CURSOR_GUIDE.md`: Guía completa para Cursor AI
- `TUTORIAL.md`: Tutorial de desarrollo
- `METODOLOGIA_DESARROLLO.md`: Metodología establecida

---
*Instrucciones generadas por Pre-Cursor Integration Manager*
"""
        
        return instructions

class CursorProjectGenerator:
    """Generador de proyectos con supervisión integrada"""
    
    def __init__(self, project_path: str, project_config: Dict[str, Any]):
        self.project_path = Path(project_path)
        self.project_config = project_config
        self.integration_manager = CursorIntegrationManager(
            project_path, 
            enable_supervision=True
        )
    
    def generate_with_supervision(self) -> bool:
        """Generar proyecto con supervisión automática"""
        try:
            # Iniciar supervisión
            if not self.integration_manager.start_supervision():
                logger.warning("No se pudo iniciar supervisión, continuando sin ella")
            
            # Generar instrucciones para Cursor
            instructions = self.integration_manager.generate_cursor_instructions(
                self.project_config.get('tipo_proyecto', 'Python Library'),
                self.project_config.get('descripcion_proyecto', 'Proyecto generado')
            )
            
            # Guardar instrucciones
            instructions_file = self.project_path / 'CURSOR_INSTRUCTIONS.md'
            with open(instructions_file, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            # Abrir Cursor con contexto
            if not self.integration_manager.open_cursor_with_context(instructions):
                logger.warning("No se pudo abrir Cursor, pero el proyecto está listo")
            
            logger.info("Proyecto generado con supervisión integrada")
            return True
            
        except Exception as e:
            logger.error(f"Error en generación con supervisión: {e}")
            return False
        finally:
            # La supervisión continúa en background
            pass
    
    def stop_generation(self):
        """Detener generación y supervisión"""
        self.integration_manager.stop_supervision()

def integrate_with_init_project(project_path: str, project_config: Dict[str, Any]) -> bool:
    """Función de integración para init_project.py"""
    try:
        generator = CursorProjectGenerator(project_path, project_config)
        return generator.generate_with_supervision()
    except Exception as e:
        logger.error(f"Error en integración: {e}")
        return False

def main():
    """Función principal para testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cursor Integration Manager')
    parser.add_argument('project_path', help='Ruta del proyecto')
    parser.add_argument('--type', default='Python Library', help='Tipo de proyecto')
    parser.add_argument('--description', default='Proyecto de prueba', help='Descripción del proyecto')
    parser.add_argument('--no-supervision', action='store_true', help='Deshabilitar supervisión')
    
    args = parser.parse_args()
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Crear configuración del proyecto
    config = {
        'tipo_proyecto': args.type,
        'descripcion_proyecto': args.description
    }
    
    # Crear generador
    generator = CursorProjectGenerator(args.project_path, config)
    
    if args.no_supervision:
        generator.integration_manager.enable_supervision = False
    
    # Generar proyecto
    success = generator.generate_with_supervision()
    
    if success:
        print("✅ Proyecto generado con supervisión integrada")
        print(f"📁 Ubicación: {args.project_path}")
        print("🤖 Cursor debería abrirse automáticamente")
        print("📝 Revisa CURSOR_INSTRUCTIONS.md para instrucciones específicas")
    else:
        print("❌ Error en la generación del proyecto")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
