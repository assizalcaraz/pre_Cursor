#!/usr/bin/env python3
"""
Auto Executor - Ejecutor Automático de Cambios
=============================================

Este módulo ejecuta automáticamente los cambios detectados por el supervisor
sin depender de Cursor CLI, implementando las correcciones directamente.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .models import ProjectIssue, CursorInstruction

logger = logging.getLogger(__name__)

class AutoExecutor:
    """Ejecutor automático de cambios detectados por el supervisor"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.logs_dir = self.project_path / ".cursor" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de log de ejecuciones automáticas
        self.auto_execution_log = self.logs_dir / "auto_executions.json"
        
        logger.info(f"AutoExecutor inicializado para {project_path}")
    
    def execute_instruction(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Ejecutar una instrucción automáticamente"""
        logger.info(f"Ejecutando instrucción automática: {instruction.action}")
        
        try:
            if instruction.action == "move_test_files":
                return self._execute_move_test_files(instruction)
            elif instruction.action == "move_file":
                return self._execute_move_file(instruction)
            elif instruction.action == "reorganize_structure":
                return self._execute_reorganize_structure(instruction)
            elif instruction.action == "fix_duplicates":
                return self._execute_fix_duplicates(instruction)
            else:
                logger.warning(f"Acción no soportada: {instruction.action}")
                return {
                    "success": False,
                    "error": f"Acción no soportada: {instruction.action}",
                    "changes_made": []
                }
                
        except Exception as e:
            logger.error(f"Error ejecutando instrucción {instruction.action}: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": []
            }
    
    def _execute_move_test_files(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Mover archivos de test de la raíz al directorio tests/"""
        changes_made = []
        
        try:
            # Buscar archivos de test en la raíz
            test_files = []
            for pattern in ['*_test.py', 'test*.py']:
                test_files.extend(self.project_path.glob(pattern))
            
            if not test_files:
                return {
                    "success": True,
                    "message": "No se encontraron archivos de test en la raíz",
                    "changes_made": []
                }
            
            # Crear directorio tests/ si no existe
            tests_dir = self.project_path / "tests"
            tests_dir.mkdir(exist_ok=True)
            
            # Mover archivos
            for test_file in test_files:
                if test_file.is_file():
                    destination = tests_dir / test_file.name
                    
                    # Verificar si ya existe en tests/
                    if destination.exists():
                        # Crear nombre único
                        counter = 1
                        while destination.exists():
                            name_parts = test_file.stem, counter, test_file.suffix
                            destination = tests_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                            counter += 1
                    
                    # Mover archivo
                    shutil.move(str(test_file), str(destination))
                    changes_made.append(f"Moved {test_file.name} to tests/")
                    logger.info(f"Archivo movido: {test_file.name} -> tests/")
            
            return {
                "success": True,
                "message": f"Movidos {len(changes_made)} archivos de test",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error moviendo archivos de test: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_move_file(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Mover un archivo específico a su ubicación correcta"""
        changes_made = []
        
        try:
            source_path = Path(instruction.target)
            if not source_path.exists():
                return {
                    "success": False,
                    "error": f"Archivo no encontrado: {source_path}",
                    "changes_made": []
                }
            
            # Determinar ubicación correcta basada en el tipo de archivo
            correct_location = self._get_correct_location(source_path)
            
            if correct_location == source_path.parent:
                return {
                    "success": True,
                    "message": "Archivo ya está en la ubicación correcta",
                    "changes_made": []
                }
            
            # Crear directorio de destino si no existe
            correct_location.mkdir(parents=True, exist_ok=True)
            
            # Mover archivo
            destination = correct_location / source_path.name
            shutil.move(str(source_path), str(destination))
            changes_made.append(f"Moved {source_path.name} to {correct_location}")
            
            return {
                "success": True,
                "message": f"Archivo movido a {correct_location}",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error moviendo archivo: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_reorganize_structure(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Reorganizar estructura del proyecto"""
        changes_made = []
        
        try:
            # Esta es una acción compleja que requiere análisis específico
            # Por ahora, solo logueamos la instrucción
            logger.info(f"Reorganización de estructura solicitada para: {instruction.target}")
            
            return {
                "success": True,
                "message": "Reorganización de estructura registrada (requiere intervención manual)",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error reorganizando estructura: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_fix_duplicates(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Eliminar funciones duplicadas"""
        changes_made = []
        
        try:
            # Esta es una acción compleja que requiere análisis de código
            # Por ahora, solo logueamos la instrucción
            logger.info(f"Eliminación de duplicados solicitada para: {instruction.target}")
            
            return {
                "success": True,
                "message": "Eliminación de duplicados registrada (requiere intervención manual)",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error eliminando duplicados: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _get_correct_location(self, file_path: Path) -> Path:
        """Determinar la ubicación correcta de un archivo"""
        file_name = file_path.name.lower()
        
        # Reglas de organización
        if file_name.startswith('test') or file_name.endswith('_test.py'):
            return self.project_path / "tests"
        elif file_name.endswith('.py') and file_name != 'main.py':
            return self.project_path / "src"
        elif file_name.endswith('.md'):
            return self.project_path / "docs"
        elif file_name.endswith('.yaml') or file_name.endswith('.yml'):
            return self.project_path / "config"
        else:
            return self.project_path / "src"
    
    def execute_instructions_batch(self, instructions: List[CursorInstruction]) -> Dict[str, Any]:
        """Ejecutar un lote de instrucciones"""
        logger.info(f"Ejecutando lote de {len(instructions)} instrucciones")
        
        results = []
        total_changes = []
        
        for i, instruction in enumerate(instructions, 1):
            logger.info(f"Ejecutando instrucción {i}/{len(instructions)}: {instruction.action}")
            result = self.execute_instruction(instruction)
            results.append(result)
            
            if result["success"]:
                total_changes.extend(result.get("changes_made", []))
        
        # Guardar log de ejecuciones
        self._save_execution_log(instructions, results)
        
        successful = sum(1 for r in results if r["success"])
        
        return {
            "total_instructions": len(instructions),
            "successful": successful,
            "failed": len(instructions) - successful,
            "total_changes": len(total_changes),
            "changes_made": total_changes,
            "results": results
        }
    
    def _save_execution_log(self, instructions: List[CursorInstruction], results: List[Dict[str, Any]]):
        """Guardar log de ejecuciones automáticas"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "total_instructions": len(instructions),
                "instructions": [
                    {
                        "action": inst.action,
                        "target": inst.target,
                        "priority": inst.priority,
                        "timestamp": inst.timestamp.isoformat()
                    }
                    for inst in instructions
                ],
                "results": results,
                "summary": {
                    "successful": sum(1 for r in results if r["success"]),
                    "failed": sum(1 for r in results if not r["success"]),
                    "total_changes": sum(len(r.get("changes_made", [])) for r in results)
                }
            }
            
            # Leer log existente
            if self.auto_execution_log.exists():
                with open(self.auto_execution_log, 'r', encoding='utf-8') as f:
                    existing_log = json.load(f)
            else:
                existing_log = {"executions": []}
            
            # Agregar nueva ejecución
            existing_log["executions"].append(log_data)
            
            # Guardar log actualizado
            with open(self.auto_execution_log, 'w', encoding='utf-8') as f:
                json.dump(existing_log, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Log de ejecuciones guardado en: {self.auto_execution_log}")
            
        except Exception as e:
            logger.error(f"Error guardando log de ejecuciones: {e}")

# Importar json al final para evitar problemas de importación circular
import json
