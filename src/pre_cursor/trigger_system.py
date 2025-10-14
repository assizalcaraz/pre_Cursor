#!/usr/bin/env python3
"""
Trigger System - Sistema de Activación para Cursor CLI
====================================================

Este módulo implementa un sistema de triggers que permite activar
la supervisión de Cursor CLI mediante archivos de activación.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from .models import SupervisionReport, ProjectIssue
from .cursor_supervisor import CursorSupervisor

logger = logging.getLogger(__name__)

class TriggerSystem:
    """Sistema de triggers para activación de Cursor CLI"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.trigger_dir = self.project_path / ".cursor" / "triggers"
        self.trigger_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos de trigger
        self.trigger_file = self.trigger_dir / "activate.trigger"
        self.role_file = self.trigger_dir / "role.json"
        self.methodology_file = self.trigger_dir / "methodology.json"
        self.state_file = self.trigger_dir / "state.json"
        
        # Inicializar archivos si no existen
        self._initialize_trigger_files()
        
        logger.info(f"TriggerSystem inicializado para {project_path}")
    
    def _initialize_trigger_files(self):
        """Inicializar archivos de trigger si no existen"""
        
        # Archivo de activación
        if not self.trigger_file.exists():
            self.trigger_file.write_text("")
        
        # Archivo de rol
        if not self.role_file.exists():
            role_data = {
                "role": "cursor_supervisor",
                "description": "Supervisor automático de proyecto con integración Cursor CLI",
                "capabilities": [
                    "detect_problems",
                    "generate_instructions", 
                    "apply_corrections",
                    "monitor_changes",
                    "update_documentation"
                ],
                "created_at": datetime.now().isoformat()
            }
            self.role_file.write_text(json.dumps(role_data, indent=2))
        
        # Archivo de metodología
        if not self.methodology_file.exists():
            methodology_data = {
                "file_organization": {
                    "src": "Código fuente principal",
                    "tests": "Pruebas unitarias y de integración", 
                    "docs": "Documentación técnica",
                    "examples": "Ejemplos de uso",
                    "config": "Archivos de configuración"
                },
                "code_standards": {
                    "naming": "snake_case para funciones y variables",
                    "classes": "PascalCase para clases",
                    "constants": "UPPER_CASE para constantes"
                },
                "documentation": {
                    "readme": "README.md con descripción del proyecto",
                    "context": "CONTEXTO.md con contexto técnico",
                    "tutorial": "TUTORIAL.md con guía de uso",
                    "bitacora": "BITACORA.md con log de desarrollo"
                }
            }
            self.methodology_file.write_text(json.dumps(methodology_data, indent=2))
        
        # Archivo de estado
        if not self.state_file.exists():
            state_data = {
                "last_check": None,
                "pending_corrections": [],
                "applied_corrections": [],
                "cycle_count": 0,
                "status": "idle"
            }
            self.state_file.write_text(json.dumps(state_data, indent=2))
    
    def check_trigger(self) -> bool:
        """Verificar si hay un trigger activo"""
        return self.trigger_file.exists() and self.trigger_file.stat().st_size > 0
    
    def read_trigger(self) -> Optional[Dict[str, Any]]:
        """Leer contenido del trigger"""
        if not self.check_trigger():
            return None
        
        try:
            content = self.trigger_file.read_text().strip()
            if not content:
                return None
            
            # Parsear contenido del trigger
            trigger_data = {
                "action": "supervise",
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "project_path": str(self.project_path)
            }
            
            # Limpiar trigger después de leerlo
            self.trigger_file.write_text("")
            
            return trigger_data
            
        except Exception as e:
            logger.error(f"Error leyendo trigger: {e}")
            return None
    
    def load_role(self) -> Dict[str, Any]:
        """Cargar rol del sistema"""
        try:
            return json.loads(self.role_file.read_text())
        except Exception as e:
            logger.error(f"Error cargando rol: {e}")
            return {"role": "cursor_supervisor"}
    
    def load_methodology(self) -> Dict[str, Any]:
        """Cargar metodología del proyecto"""
        try:
            return json.loads(self.methodology_file.read_text())
        except Exception as e:
            logger.error(f"Error cargando metodología: {e}")
            return {}
    
    def load_state(self) -> Dict[str, Any]:
        """Cargar estado actual del sistema"""
        try:
            return json.loads(self.state_file.read_text())
        except Exception as e:
            logger.error(f"Error cargando estado: {e}")
            return {"status": "idle"}
    
    def save_state(self, state: Dict[str, Any]):
        """Guardar estado actual del sistema"""
        try:
            state["last_updated"] = datetime.now().isoformat()
            self.state_file.write_text(json.dumps(state, indent=2))
        except Exception as e:
            logger.error(f"Error guardando estado: {e}")
    
    def create_trigger(self, action: str = "supervise", content: str = ""):
        """Crear un trigger para activar el sistema"""
        trigger_data = {
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "project_path": str(self.project_path)
        }
        
        self.trigger_file.write_text(json.dumps(trigger_data, indent=2))
        logger.info(f"Trigger creado: {action}")
    
    def run_supervision_cycle(self) -> Dict[str, Any]:
        """Ejecutar un ciclo completo de supervisión"""
        logger.info("Iniciando ciclo de supervisión")
        
        # Cargar estado actual
        state = self.load_state()
        state["cycle_count"] += 1
        state["status"] = "running"
        state["last_check"] = datetime.now().isoformat()
        
        # Crear supervisor
        supervisor = CursorSupervisor(
            str(self.project_path),
            enable_bidirectional=True
        )
        
        # Ejecutar supervisión
        report = supervisor.check_project_health()
        
        # Procesar problemas encontrados
        if report.issues_found:
            logger.info(f"Procesando {len(report.issues_found)} problemas")
            
            # Generar instrucciones
            instructions = supervisor.instruction_generator.generate_instructions(report)
            
            if instructions:
                # Aplicar correcciones automáticas
                results = supervisor._apply_automatic_corrections(report)
                
                # Actualizar estado con correcciones aplicadas
                state["applied_corrections"].extend([
                    {
                        "instruction": inst.action,
                        "target": inst.target,
                        "timestamp": datetime.now().isoformat(),
                        "success": True
                    }
                    for inst in instructions
                ])
                
                logger.info(f"Aplicadas {len(instructions)} correcciones")
            else:
                logger.info("No se generaron instrucciones")
        else:
            logger.info("No se encontraron problemas - proyecto saludable")
        
        # Actualizar estado final
        state["status"] = "completed"
        self.save_state(state)
        
        return {
            "cycle_count": state["cycle_count"],
            "issues_found": len(report.issues_found) if report.issues_found else 0,
            "corrections_applied": len(state["applied_corrections"]),
            "status": state["status"]
        }
    
    def run_continuous_monitoring(self, check_interval: int = 60, auto_supervise: bool = True):
        """Ejecutar monitoreo continuo del sistema de triggers"""
        logger.info(f"Iniciando monitoreo continuo cada {check_interval} segundos")
        if auto_supervise:
            logger.info("Supervisión automática habilitada - ejecutando ciclos automáticamente")
        
        try:
            while True:
                # Verificar triggers primero
                if self.check_trigger():
                    logger.info("Trigger detectado - ejecutando ciclo de supervisión")
                    result = self.run_supervision_cycle()
                    logger.info(f"Ciclo completado: {result}")
                elif auto_supervise:
                    # Si no hay triggers pero auto_supervise está habilitado, ejecutar supervisión automática
                    logger.info("Ejecutando supervisión automática")
                    result = self.run_supervision_cycle()
                    logger.info(f"Supervisión automática completada: {result}")
                else:
                    logger.debug("No hay triggers activos y supervisión automática deshabilitada")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoreo continuo detenido por el usuario")
        except Exception as e:
            logger.error(f"Error en monitoreo continuo: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado actual del sistema"""
        state = self.load_state()
        role = self.load_role()
        
        return {
            "status": state.get("status", "idle"),
            "last_check": state.get("last_check"),
            "cycle_count": state.get("cycle_count", 0),
            "pending_corrections": len(state.get("pending_corrections", [])),
            "applied_corrections": len(state.get("applied_corrections", [])),
            "role": role.get("role", "unknown"),
            "trigger_active": self.check_trigger()
        }
