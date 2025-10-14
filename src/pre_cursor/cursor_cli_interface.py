#!/usr/bin/env python3
"""
Cursor CLI Interface - Interfaz para Ejecución de Instrucciones en Cursor CLI
============================================================================

Este módulo ejecuta instrucciones generadas por CursorInstructionGenerator
utilizando la interfaz de Cursor CLI para aplicar correcciones automáticas.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from .models import CursorInstruction, ExecutionResult

logger = logging.getLogger(__name__)

class CursorCLIInterface:
    """Interfaz para ejecutar instrucciones en Cursor CLI"""
    
    def __init__(self, project_path: str, cursor_path: str = None):
        self.project_path = Path(project_path)
        self.cursor_path = cursor_path or self._find_cursor_executable()
        self.cursor_available = self._check_cursor_availability()
        self.execution_log = []
        
        if not self.cursor_available:
            logger.warning("Cursor CLI no está disponible - modo simulación activado")
    
    def _find_cursor_executable(self) -> Optional[str]:
        """Buscar ejecutable de Cursor en el sistema"""
        possible_paths = [
            "cursor",  # En PATH
            "/Applications/Cursor.app/Contents/MacOS/Cursor",  # macOS
            "/usr/local/bin/cursor",
            "/opt/cursor/bin/cursor",
            os.path.expanduser("~/bin/cursor")
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.info(f"Cursor encontrado en: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        
        logger.warning("Cursor CLI no encontrado en el sistema")
        return None
    
    def _check_cursor_availability(self) -> bool:
        """Verificar si Cursor CLI está disponible"""
        if not self.cursor_path:
            return False
        
        try:
            result = subprocess.run([self.cursor_path, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
            logger.error(f"Error verificando Cursor: {e}")
            return False
    
    def execute_instruction(self, instruction: CursorInstruction) -> ExecutionResult:
        """
        Ejecutar una instrucción en Cursor CLI
        
        Args:
            instruction: Instrucción a ejecutar
            
        Returns:
            Resultado de la ejecución
        """
        start_time = time.time()
        
        logger.info(f"Ejecutando instrucción: {instruction.action} en {instruction.target}")
        
        if not self.cursor_available:
            return self._simulate_execution(instruction)
        
        try:
            # Generar prompt para Cursor
            prompt = self._generate_cursor_prompt(instruction)
            
            # Ejecutar en Cursor CLI
            result = self._run_cursor_command(prompt, instruction)
            
            execution_time = time.time() - start_time
            
            # Procesar resultado
            execution_result = ExecutionResult(
                success=result.success,
                output=result.output,
                error=result.error,
                changes_made=result.changes_made,
                execution_time=execution_time
            )
            
            # Actualizar estado de la instrucción
            instruction.status = "completed" if result.success else "failed"
            instruction.result = execution_result.to_dict()
            
            # Registrar en log
            self.execution_log.append({
                "instruction": instruction.to_dict(),
                "result": execution_result.to_dict()
            })
            
            logger.info(f"Instrucción ejecutada: {execution_result}")
            return execution_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Error ejecutando instrucción: {e}"
            logger.error(error_msg)
            
            execution_result = ExecutionResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
            
            instruction.status = "failed"
            instruction.result = execution_result.to_dict()
            
            return execution_result
    
    def _simulate_execution(self, instruction: CursorInstruction) -> ExecutionResult:
        """Simular ejecución cuando Cursor no está disponible"""
        logger.info("Simulando ejecución (Cursor no disponible)")
        
        # Simular tiempo de ejecución
        time.sleep(1)
        
        # Generar resultado simulado
        changes_made = [f"Simulación: {instruction.action} en {instruction.target}"]
        
        return ExecutionResult(
            success=True,
            output="Ejecución simulada - Cursor no disponible",
            changes_made=changes_made,
            execution_time=1.0
        )
    
    def _generate_cursor_prompt(self, instruction: CursorInstruction) -> str:
        """Generar prompt específico para Cursor AI"""
        prompt = f"""
# Instrucción Automática de Pre-Cursor Supervisor

## Contexto del Proyecto
- **Proyecto**: {self.project_path.name}
- **Acción**: {instruction.action}
- **Archivo**: {instruction.target}
- **Prioridad**: {instruction.priority}

## Instrucción Específica
{instruction.context}

## Metodología de Referencia
{instruction.methodology_reference}

## Tareas a Realizar
1. **Analizar** el archivo objetivo: {instruction.target}
2. **Aplicar** la corrección: {instruction.action}
3. **Verificar** que no se rompa funcionalidad existente
4. **Documentar** cambios si es necesario

## Archivos de Referencia
- `CURSOR_GUIDE.md`: Guía específica para Cursor AI
- `METODOLOGIA_DESARROLLO.md`: Metodología establecida
- `BITACORA.md`: Registro de cambios

## Instrucciones para Cursor AI
Por favor, ejecuta esta corrección automática siguiendo la metodología establecida.
Mantén la funcionalidad existente y asegúrate de que los cambios sean consistentes.

---
*Generado automáticamente por Pre-Cursor Supervisor*
"""
        return prompt
    
    def _run_cursor_command(self, prompt: str, instruction: CursorInstruction) -> ExecutionResult:
        """Ejecutar comando en Cursor CLI"""
        try:
            # Crear archivo temporal con el prompt
            prompt_file = self.project_path / f".cursor_prompt_{instruction.timestamp.strftime('%Y%m%d_%H%M%S')}.md"
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # Comando para abrir Cursor con el archivo de prompt
            cmd = [
                self.cursor_path,
                str(self.project_path),
                str(prompt_file)
            ]
            
            logger.debug(f"Ejecutando comando: {' '.join(cmd)}")
            
            # Ejecutar comando
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos máximo
                cwd=str(self.project_path)
            )
            
            # Limpiar archivo temporal
            try:
                prompt_file.unlink()
            except OSError:
                pass
            
            # Procesar resultado
            if result.returncode == 0:
                changes_made = self._detect_changes(instruction)
                return ExecutionResult(
                    success=True,
                    output=result.stdout,
                    changes_made=changes_made
                )
            else:
                return ExecutionResult(
                    success=False,
                    error=result.stderr,
                    output=result.stdout
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                error="Timeout ejecutando comando en Cursor"
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Error ejecutando comando: {e}"
            )
    
    def _detect_changes(self, instruction: CursorInstruction) -> List[str]:
        """Detectar cambios realizados por la instrucción"""
        changes = []
        
        # Verificar si el archivo objetivo existe y fue modificado
        target_path = Path(instruction.target)
        if target_path.exists():
            # Verificar timestamp de modificación
            mod_time = target_path.stat().st_mtime
            if mod_time > instruction.timestamp.timestamp():
                changes.append(f"Archivo modificado: {target_path}")
        
        # Verificar cambios en estructura según el tipo de acción
        if instruction.action == "move_file":
            # Verificar si el archivo se movió
            original_path = Path(instruction.target)
            if not original_path.exists():
                changes.append(f"Archivo movido desde: {original_path}")
        
        return changes
    
    def execute_instructions_batch(self, instructions: List[CursorInstruction]) -> List[ExecutionResult]:
        """Ejecutar múltiples instrucciones en lote"""
        results = []
        
        logger.info(f"Ejecutando lote de {len(instructions)} instrucciones")
        
        for i, instruction in enumerate(instructions, 1):
            logger.info(f"Ejecutando instrucción {i}/{len(instructions)}: {instruction.action}")
            
            result = self.execute_instruction(instruction)
            results.append(result)
            
            # Pausa entre instrucciones para evitar sobrecarga
            if i < len(instructions):
                time.sleep(2)
        
        logger.info(f"Lote completado: {len([r for r in results if r.success])}/{len(results)} exitosas")
        return results
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Obtener resumen de ejecuciones"""
        total_executions = len(self.execution_log)
        successful_executions = len([log for log in self.execution_log 
                                   if log["result"]["success"]])
        failed_executions = total_executions - successful_executions
        
        total_time = sum(log["result"]["execution_time"] for log in self.execution_log)
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            "total_execution_time": total_time,
            "average_execution_time": total_time / total_executions if total_executions > 0 else 0
        }
    
    def save_execution_log(self, output_path: str = None) -> str:
        """Guardar log de ejecuciones"""
        if not output_path:
            output_path = self.project_path / "CURSOR_EXECUTION_LOG.json"
        
        log_data = {
            "project_path": str(self.project_path),
            "cursor_available": self.cursor_available,
            "cursor_path": self.cursor_path,
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_execution_summary(),
            "executions": self.execution_log
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Log de ejecuciones guardado en: {output_path}")
        return str(output_path)
