#!/usr/bin/env python3
"""
UnifiedSupervisor - Supervisor Unificado con Prioridad en Cursor Agent CLI
=======================================================================

Supervisor unificado que integra todas las funcionalidades de supervisión
y prioriza el uso de Cursor Agent CLI para todas las operaciones.
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from .cursor_supervisor import CursorSupervisor
from .test_supervisor import TestSupervisor
from .cursor_agent_executor import CursorAgentExecutor
from .auto_executor import AutoExecutor
from .trigger_system import TriggerSystem
from .models import ProjectIssue, SupervisionReport

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MonitorConfig:
    """Configuración del monitor unificado"""
    project_path: str
    daemon: bool = False
    interval: int = 300
    auto_fix: bool = True
    test_supervisor: bool = True
    llm_validation: bool = True
    cursor_agent_priority: bool = True

class UnifiedSupervisor:
    """
    Supervisor Unificado que integra todas las funcionalidades
    y prioriza Cursor Agent CLI para todas las operaciones.
    """
    
    def __init__(self, project_path: str, **options):
        self.config = MonitorConfig(
            project_path=project_path,
            **options
        )
        
        self.project_path = Path(project_path)
        self.cursor_agent_available = self._check_cursor_agent()
        
        # Inicializar componentes
        self._init_components()
        
        # Configurar logging
        self._setup_logging()
        
        logger.info(f"UnifiedSupervisor inicializado para {project_path}")
        logger.info(f"Cursor Agent CLI disponible: {self.cursor_agent_available}")
    
    def _check_cursor_agent(self) -> bool:
        """Verificar si Cursor Agent CLI está disponible"""
        try:
            result = subprocess.run(
                ['cursor-agent', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _init_components(self):
        """Inicializar todos los componentes necesarios"""
        try:
            # Supervisor principal
            self.cursor_supervisor = CursorSupervisor(
                project_path=str(self.project_path),
                enable_bidirectional=True
            )
            
            # Test Supervisor (si está habilitado)
            if self.config.test_supervisor:
                self.test_supervisor = TestSupervisor(str(self.project_path))
            else:
                self.test_supervisor = None
            
            # Cursor Agent Executor (prioridad)
            if self.cursor_agent_available:
                self.cursor_agent_executor = CursorAgentExecutor(str(self.project_path))
                self.auto_executor = None  # No usar AutoExecutor si Cursor Agent está disponible
            else:
                self.cursor_agent_executor = None
                self.auto_executor = AutoExecutor(str(self.project_path))
            
            # Sistema de triggers
            self.trigger_system = TriggerSystem(str(self.project_path))
            
            logger.info("Componentes inicializados correctamente")
            
        except Exception as e:
            logger.error(f"Error inicializando componentes: {e}")
            raise
    
    def _setup_logging(self):
        """Configurar logging unificado"""
        log_dir = self.project_path / '.cursor' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar logger específico
        handler = logging.FileHandler(log_dir / 'unified_supervisor.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    def start_daemon(self):
        """Iniciar supervisión en modo daemon"""
        logger.info("Iniciando daemon unificado")
        
        try:
            # Crear trigger para activación
            self.trigger_system.create_trigger()
            
            # Iniciar monitoreo continuo
            self.trigger_system.run_continuous_monitoring(
                auto_supervise=True
            )
            
        except KeyboardInterrupt:
            logger.info("Daemon detenido por el usuario")
        except Exception as e:
            logger.error(f"Error en daemon: {e}")
            raise
    
    def start_interactive(self):
        """Iniciar supervisión en modo interactivo"""
        logger.info("Iniciando supervisión interactiva")
        
        try:
            while True:
                # Ejecutar ciclo de supervisión
                self._run_supervision_cycle()
                
                # Esperar intervalo
                time.sleep(self.config.interval)
                
        except KeyboardInterrupt:
            logger.info("Supervisión interactiva detenida por el usuario")
        except Exception as e:
            logger.error(f"Error en supervisión interactiva: {e}")
            raise
    
    def _run_supervision_cycle(self):
        """Ejecutar un ciclo completo de supervisión"""
        logger.info("Ejecutando ciclo de supervisión")
        
        try:
            # 1. Supervisión general del proyecto
            general_issues = self._supervise_general()
            
            # 2. Supervisión de tests (si está habilitada)
            test_issues = []
            if self.config.test_supervisor:
                test_issues = self._supervise_tests()
            
            # 3. Aplicar correcciones automáticas (si está habilitado)
            if self.config.auto_fix:
                self._apply_automatic_corrections(general_issues + test_issues)
            
            # 4. Generar reporte unificado
            self._generate_unified_report(general_issues, test_issues)
            
        except Exception as e:
            logger.error(f"Error en ciclo de supervisión: {e}")
    
    def _supervise_general(self) -> List[ProjectIssue]:
        """Supervisión general del proyecto"""
        try:
            # Ejecutar supervisión general
            report = self.cursor_supervisor.check_project_health()
            return report.issues if hasattr(report, 'issues') else []
            
        except Exception as e:
            logger.error(f"Error en supervisión general: {e}")
            return []
    
    def _supervise_tests(self) -> List[ProjectIssue]:
        """Supervisión especializada de tests"""
        try:
            if not self.test_supervisor:
                return []
            
            # Ejecutar supervisión de tests
            result = self.test_supervisor.run_test_supervision()
            return result.get('issues', [])
            
        except Exception as e:
            logger.error(f"Error en supervisión de tests: {e}")
            return []
    
    def _apply_automatic_corrections(self, issues: List[ProjectIssue]):
        """Aplicar correcciones automáticas usando Cursor Agent CLI prioritariamente"""
        if not issues:
            return
        
        logger.info(f"Aplicando correcciones automáticas para {len(issues)} problemas")
        
        try:
            # Priorizar Cursor Agent CLI
            if self.cursor_agent_available and self.cursor_agent_executor:
                self._apply_corrections_with_cursor_agent(issues)
            elif self.auto_executor:
                self._apply_corrections_with_auto_executor(issues)
            else:
                logger.warning("No hay ejecutores disponibles para aplicar correcciones")
                
        except Exception as e:
            logger.error(f"Error aplicando correcciones: {e}")
    
    def _apply_corrections_with_cursor_agent(self, issues: List[ProjectIssue]):
        """Aplicar correcciones usando Cursor Agent CLI"""
        logger.info("Aplicando correcciones con Cursor Agent CLI")
        
        try:
            # Generar instrucciones para Cursor Agent
            from .cursor_instruction_generator import CursorInstructionGenerator
            
            instruction_generator = CursorInstructionGenerator(str(self.project_path))
            instructions = []
            
            for issue in issues:
                instruction = instruction_generator.create_instruction(issue)
                if instruction:
                    instructions.append(instruction)
            
            # Ejecutar instrucciones con Cursor Agent
            for instruction in instructions:
                try:
                    result = self.cursor_agent_executor.execute_instruction(instruction)
                    logger.info(f"Instrucción ejecutada: {instruction.action}")
                    logger.info(f"Resultado: {result}")
                except Exception as e:
                    logger.error(f"Error ejecutando instrucción {instruction.action}: {e}")
            
        except Exception as e:
            logger.error(f"Error en correcciones con Cursor Agent: {e}")
    
    def _apply_corrections_with_auto_executor(self, issues: List[ProjectIssue]):
        """Aplicar correcciones usando AutoExecutor como fallback"""
        logger.info("Aplicando correcciones con AutoExecutor (fallback)")
        
        try:
            for issue in issues:
                try:
                    # Crear instrucción simple para AutoExecutor
                    from .models import CursorInstruction
                    
                    instruction = CursorInstruction(
                        action=self._map_issue_to_action(issue),
                        context=issue.suggestion,
                        target=str(issue.file_path) if issue.file_path else "proyecto"
                    )
                    
                    result = self.auto_executor.execute_instruction(instruction)
                    logger.info(f"Corrección aplicada: {instruction.action}")
                    
                except Exception as e:
                    logger.error(f"Error aplicando corrección para {issue.type}: {e}")
            
        except Exception as e:
            logger.error(f"Error en correcciones con AutoExecutor: {e}")
    
    def _map_issue_to_action(self, issue: ProjectIssue) -> str:
        """Mapear tipo de issue a acción de AutoExecutor"""
        mapping = {
            'missing_tests_dir': 'create_tests_dir',
            'inconsistent_naming': 'rename_test_files',
            'duplicate_test_function': 'unify_test_functions',
            'missing_test_imports': 'add_test_imports',
            'file_out_of_place': 'move_file',
            'duplicate_file': 'remove_duplicate'
        }
        return mapping.get(issue.type, 'general_fix')
    
    def _generate_unified_report(self, general_issues: List[ProjectIssue], test_issues: List[ProjectIssue]):
        """Generar reporte unificado"""
        try:
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'project_path': str(self.project_path),
                'supervisor': 'unified',
                'general_issues': len(general_issues),
                'test_issues': len(test_issues),
                'total_issues': len(general_issues) + len(test_issues),
                'cursor_agent_available': self.cursor_agent_available,
                'auto_fix_enabled': self.config.auto_fix,
                'test_supervisor_enabled': self.config.test_supervisor,
                'llm_validation_enabled': self.config.llm_validation,
                'issues': [
                    {
                        'type': issue.type,
                        'severity': issue.severity,
                        'description': issue.description,
                        'suggestion': issue.suggestion,
                        'file_path': str(issue.file_path) if issue.file_path else None,
                        'category': 'general'
                    } for issue in general_issues
                ] + [
                    {
                        'type': issue.type,
                        'severity': issue.severity,
                        'description': issue.description,
                        'suggestion': issue.suggestion,
                        'file_path': str(issue.file_path) if issue.file_path else None,
                        'category': 'test'
                    } for issue in test_issues
                ]
            }
            
            # Guardar reporte
            report_file = self.project_path / '.cursor' / 'logs' / 'unified_report.json'
            with open(report_file, 'w', encoding='utf-8') as f:
                import json
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte unificado guardado: {report_file}")
            
        except Exception as e:
            logger.error(f"Error generando reporte unificado: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado actual del supervisor unificado"""
        return {
            'project_path': str(self.project_path),
            'daemon_mode': self.config.daemon,
            'interval': self.config.interval,
            'auto_fix_enabled': self.config.auto_fix,
            'test_supervisor_enabled': self.config.test_supervisor,
            'llm_validation_enabled': self.config.llm_validation,
            'cursor_agent_available': self.cursor_agent_available,
            'components_initialized': {
                'cursor_supervisor': self.cursor_supervisor is not None,
                'test_supervisor': self.test_supervisor is not None,
                'cursor_agent_executor': self.cursor_agent_executor is not None,
                'auto_executor': self.auto_executor is not None,
                'trigger_system': self.trigger_system is not None
            }
        }
