#!/usr/bin/env python3
"""
Cursor Supervisor - Supervisión automática de generación de código
================================================================

Este módulo implementa un sistema de supervisión dual para Cursor IDE:
- Instancia 1: Supervisor que monitorea y controla la calidad
- Instancia 2: Generador que ejecuta tareas específicas

Autor: Assiz Alcaraz Baxter
Fecha: 2024-10-13
"""

import os
import time
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Importar módulos de integración bidireccional
from .cursor_instruction_generator import CursorInstructionGenerator
from .cursor_cli_interface import CursorCLIInterface
from .feedback_processor import FeedbackProcessor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProjectIssue:
    """Representa un problema detectado en el proyecto"""
    type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    file_path: Optional[str] = None
    suggestion: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class SupervisionReport:
    """Reporte de supervisión del proyecto"""
    timestamp: datetime
    issues_found: List[ProjectIssue]
    files_created: List[str]
    files_modified: List[str]
    structure_changes: List[str]
    recommendations: List[str]

class ProjectStructureMonitor:
    """Monitor de estructura del proyecto"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.expected_structure = {
            'src/': 'Código fuente principal',
            'tests/': 'Pruebas unitarias',
            'docs/': 'Documentación',
            'examples/': 'Ejemplos de uso',
            'logs/': 'Archivos de log'
        }
    
    def check_structure(self) -> List[ProjectIssue]:
        """Verificar estructura del proyecto"""
        issues = []
        
        for dir_path, description in self.expected_structure.items():
            full_path = self.project_path / dir_path
            if not full_path.exists():
                issues.append(ProjectIssue(
                    type='missing_directory',
                    severity='medium',
                    description=f"Directorio requerido no encontrado: {dir_path}",
                    suggestion=f"Crear directorio {dir_path} para {description}"
                ))
        
        return issues
    
    def check_files_out_of_place(self) -> List[ProjectIssue]:
        """Detectar archivos fuera de lugar"""
        issues = []
        
        # Archivos de test en raíz
        test_files = list(self.project_path.glob('*_test.py'))
        if test_files:
            issues.append(ProjectIssue(
                type='misplaced_files',
                severity='high',
                description=f"Archivos de test en raíz: {[f.name for f in test_files]}",
                suggestion="Mover archivos de test al directorio tests/"
            ))
        
        # Scripts de configuración en src/
        config_files = list((self.project_path / 'src').glob('*config*.py'))
        if config_files:
            issues.append(ProjectIssue(
                type='misplaced_files',
                severity='medium',
                description=f"Archivos de configuración en src/: {[f.name for f in config_files]}",
                suggestion="Mover archivos de configuración al directorio raíz"
            ))
        
        return issues

class DuplicateDetector:
    """Detector de archivos y código duplicado"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def find_duplicate_files(self) -> List[ProjectIssue]:
        """Encontrar archivos duplicados"""
        issues = []
        file_hashes = {}
        
        for file_path in self.project_path.rglob('*.py'):
            if file_path.is_file():
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        file_hash = hash(content)
                        
                        if file_hash in file_hashes:
                            issues.append(ProjectIssue(
                                type='duplicate_file',
                                severity='medium',
                                description=f"Archivo duplicado: {file_path.name}",
                                file_path=str(file_path),
                                suggestion=f"Revisar si {file_path} es necesario o si debe ser eliminado"
                            ))
                        else:
                            file_hashes[file_hash] = file_path
                except Exception as e:
                    logger.warning(f"Error al procesar archivo {file_path}: {e}")
        
        return issues
    
    def find_duplicate_functions(self) -> List[ProjectIssue]:
        """Encontrar funciones duplicadas (básico)"""
        issues = []
        function_signatures = {}
        
        for file_path in self.project_path.rglob('*.py'):
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        for i, line in enumerate(lines):
                            if line.strip().startswith('def '):
                                func_name = line.strip().split('(')[0].replace('def ', '')
                                if func_name in function_signatures:
                                    issues.append(ProjectIssue(
                                        type='duplicate_function',
                                        severity='low',
                                        description=f"Función duplicada: {func_name}",
                                        file_path=str(file_path),
                                        suggestion=f"Revisar si la función {func_name} en línea {i+1} es necesaria"
                                    ))
                                else:
                                    function_signatures[func_name] = file_path
                except Exception as e:
                    logger.warning(f"Error al procesar archivo {file_path}: {e}")
        
        return issues

class CursorSupervisor:
    """Supervisor principal para Cursor IDE"""
    
    def __init__(self, project_path: str, check_interval: int = 300, 
                 enable_bidirectional: bool = False, methodology_path: str = None):
        self.project_path = Path(project_path)
        self.check_interval = check_interval
        self.enable_bidirectional = enable_bidirectional
        self.structure_monitor = ProjectStructureMonitor(project_path)
        self.duplicate_detector = DuplicateDetector(project_path)
        self.bitacora_path = self.project_path / 'BITACORA.md'
        self.supervision_log = self.project_path / 'logs' / 'supervisor.log'
        
        # Crear directorio de logs si no existe
        self.supervision_log.parent.mkdir(exist_ok=True)
        
        # Configurar logging específico del supervisor
        self.logger = logging.getLogger('CursorSupervisor')
        handler = logging.FileHandler(self.supervision_log)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        
        # Inicializar componentes de integración bidireccional
        if self.enable_bidirectional:
            self.instruction_generator = CursorInstructionGenerator(
                str(project_path), methodology_path
            )
            self.cursor_interface = CursorCLIInterface(str(project_path))
            self.feedback_processor = FeedbackProcessor(str(project_path))
            self.logger.info("Integración bidireccional habilitada")
    
    def start_supervision(self):
        """Iniciar supervisión continua"""
        self.logger.info("Iniciando supervisión del proyecto")
        
        try:
            while True:
                report = self.check_project_health()
                self.update_bitacora(report)
                self.logger.info(f"Supervisión completada. {len(report.issues_found)} problemas encontrados")
                
                # Aplicar correcciones automáticas si está habilitado
                if self.enable_bidirectional and report.issues_found:
                    self._apply_automatic_corrections(report)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info("Supervisión detenida por el usuario")
        except Exception as e:
            self.logger.error(f"Error en supervisión: {e}")
    
    def start_supervision_with_cursor(self):
        """Iniciar supervisión con integración bidireccional de Cursor CLI"""
        if not self.enable_bidirectional:
            self.logger.warning("Integración bidireccional no habilitada - iniciando supervisión normal")
            return self.start_supervision()
        
        self.logger.info("Iniciando supervisión con integración bidireccional de Cursor CLI")
        
        try:
            while True:
                report = self.check_project_health()
                self.update_bitacora(report)
                
                if report.issues_found:
                    self.logger.info(f"Procesando {len(report.issues_found)} problemas con Cursor CLI")
                    self._apply_automatic_corrections(report)
                else:
                    self.logger.info("No se encontraron problemas - proyecto saludable")
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info("Supervisión con Cursor CLI detenida por el usuario")
        except Exception as e:
            self.logger.error(f"Error en supervisión con Cursor CLI: {e}")
    
    def _apply_automatic_corrections(self, report: SupervisionReport):
        """Aplicar correcciones automáticas usando Cursor CLI"""
        try:
            # Generar instrucciones basadas en el reporte
            instructions = self.instruction_generator.generate_instructions(report)
            
            if not instructions:
                self.logger.info("No se generaron instrucciones para los problemas detectados")
                return
            
            self.logger.info(f"Generadas {len(instructions)} instrucciones para Cursor CLI")
            
            # Guardar instrucciones para referencia
            instructions_file = self.instruction_generator.save_instructions(instructions)
            self.logger.info(f"Instrucciones guardadas en: {instructions_file}")
            
            # Ejecutar instrucciones en lote
            results = self.cursor_interface.execute_instructions_batch(instructions)
            
            # Procesar resultados
            for instruction, result in zip(instructions, results):
                self.feedback_processor.process_result(result, instruction)
            
            # Generar resumen
            summary = self.cursor_interface.get_execution_summary()
            self.logger.info(f"Correcciones aplicadas: {summary['successful_executions']}/{summary['total_executions']} exitosas")
            
            # Guardar logs
            self.cursor_interface.save_execution_log()
            self.feedback_processor.save_feedback_log()
            
        except Exception as e:
            self.logger.error(f"Error aplicando correcciones automáticas: {e}")
    
    def apply_single_correction(self, issue: ProjectIssue) -> bool:
        """Aplicar corrección individual para un problema específico"""
        if not self.enable_bidirectional:
            self.logger.warning("Integración bidireccional no habilitada")
            return False
        
        try:
            # Crear reporte temporal con un solo problema
            temp_report = SupervisionReport(
                timestamp=datetime.now(),
                issues_found=[issue],
                recommendations=[]
            )
            
            # Generar instrucción
            instructions = self.instruction_generator.generate_instructions(temp_report)
            
            if not instructions:
                self.logger.warning("No se pudo generar instrucción para el problema")
                return False
            
            # Ejecutar instrucción
            result = self.cursor_interface.execute_instruction(instructions[0])
            
            # Procesar resultado
            self.feedback_processor.process_result(result, instructions[0])
            
            self.logger.info(f"Corrección individual aplicada: {result}")
            return result.success
            
        except Exception as e:
            self.logger.error(f"Error aplicando corrección individual: {e}")
            return False
    
    def check_project_health(self) -> SupervisionReport:
        """Verificar salud general del proyecto"""
        issues = []
        
        # Verificar estructura
        issues.extend(self.structure_monitor.check_structure())
        
        # Verificar archivos fuera de lugar
        issues.extend(self.structure_monitor.check_files_out_of_place())
        
        # Verificar duplicados
        issues.extend(self.duplicate_detector.find_duplicate_files())
        issues.extend(self.duplicate_detector.find_duplicate_functions())
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(issues)
        
        return SupervisionReport(
            timestamp=datetime.now(),
            issues_found=issues,
            files_created=[],  # TODO: Implementar tracking de archivos
            files_modified=[],  # TODO: Implementar tracking de modificaciones
            structure_changes=[],  # TODO: Implementar tracking de cambios
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, issues: List[ProjectIssue]) -> List[str]:
        """Generar recomendaciones basadas en los problemas encontrados"""
        recommendations = []
        
        critical_issues = [i for i in issues if i.severity == 'critical']
        high_issues = [i for i in issues if i.severity == 'high']
        
        if critical_issues:
            recommendations.append("🚨 ATENCIÓN: Problemas críticos detectados que requieren intervención inmediata")
        
        if high_issues:
            recommendations.append("⚠️ Problemas de alta prioridad detectados que deben ser corregidos")
        
        # Recomendaciones específicas
        if any(i.type == 'misplaced_files' for i in issues):
            recommendations.append("📁 Reorganizar archivos según la estructura del proyecto")
        
        if any(i.type == 'duplicate_file' for i in issues):
            recommendations.append("🔄 Revisar y eliminar archivos duplicados")
        
        if any(i.type == 'duplicate_function' for i in issues):
            recommendations.append("🔧 Refactorizar funciones duplicadas")
        
        return recommendations
    
    def update_bitacora(self, report: SupervisionReport):
        """Actualizar bitácora del proyecto"""
        if not self.bitacora_path.exists():
            self.logger.warning("Bitácora no encontrada, creando nueva")
            self._create_bitacora()
        
        try:
            with open(self.bitacora_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Añadir entrada de supervisión
            entry = self._format_supervision_entry(report)
            
            # Insertar al final del archivo
            if "## 🤖 Supervisión Automática" not in content:
                content += "\n\n## 🤖 Supervisión Automática\n\n"
            
            content += entry
            
            with open(self.bitacora_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info("Bitácora actualizada correctamente")
            return True
                
        except Exception as e:
            self.logger.error(f"Error al actualizar bitácora: {e}")
            return False
    
    def _create_bitacora(self):
        """Crear bitácora básica si no existe"""
        content = """# 📝 Bitácora del Proyecto

## 🤖 Supervisión Automática

"""
        with open(self.bitacora_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _format_supervision_entry(self, report: SupervisionReport) -> str:
        """Formatear entrada de supervisión para la bitácora"""
        entry = f"""
### {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - Supervisión Automática

**Problemas detectados**: {len(report.issues_found)}

"""
        
        if report.issues_found:
            entry += "**Problemas encontrados:**\n"
            for issue in report.issues_found:
                severity_emoji = {
                    'low': '🟢',
                    'medium': '🟡', 
                    'high': '🟠',
                    'critical': '🔴'
                }.get(issue.severity, '⚪')
                
                entry += f"- {severity_emoji} **{issue.type}**: {issue.description}\n"
                if issue.suggestion:
                    entry += f"  💡 *Sugerencia*: {issue.suggestion}\n"
        
        if report.recommendations:
            entry += "\n**Recomendaciones:**\n"
            for rec in report.recommendations:
                entry += f"- {rec}\n"
        
        entry += "\n---\n\n"
        return entry

class CursorGenerator:
    """Generador de código usando Cursor CLI"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.cursor_process = None
    
    def open_project(self) -> bool:
        """Abrir proyecto en Cursor"""
        try:
            subprocess.run(['cursor', str(self.project_path)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error al abrir proyecto en Cursor: {e}")
            return False
        except FileNotFoundError:
            logger.error("Cursor CLI no encontrado. Asegúrate de que Cursor esté instalado")
            return False
    
    def generate_code(self, task_description: str) -> bool:
        """Generar código según descripción de tarea"""
        # TODO: Implementar generación de código específica
        # Por ahora, solo abrir el proyecto
        return self.open_project()

def main():
    """Función principal para testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cursor Supervisor')
    parser.add_argument('project_path', help='Ruta del proyecto a supervisar')
    parser.add_argument('--interval', type=int, default=300, help='Intervalo de supervisión en segundos')
    parser.add_argument('--once', action='store_true', help='Ejecutar supervisión una sola vez')
    
    args = parser.parse_args()
    
    supervisor = CursorSupervisor(args.project_path, args.interval)
    
    if args.once:
        report = supervisor.check_project_health()
        print(f"Supervisión completada. {len(report.issues_found)} problemas encontrados")
        for issue in report.issues_found:
            print(f"- {issue.severity.upper()}: {issue.description}")
    else:
        supervisor.start_supervision()

if __name__ == "__main__":
    main()
