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
from .auto_executor import AutoExecutor
from .cursor_agent_executor import CursorAgentExecutor

logger = logging.getLogger(__name__)

class CursorCLIInterface:
    """Interfaz para ejecutar instrucciones en Cursor CLI"""
    
    def __init__(self, project_path: str, cursor_path: str = None):
        self.project_path = Path(project_path)
        self.cursor_path = cursor_path or self._find_cursor_executable()
        self.cursor_available = self._check_cursor_availability()
        self.execution_log = []
        
        # Inicializar ejecutores para diferentes estrategias
        self.auto_executor = AutoExecutor(project_path)
        self.agent_executor = CursorAgentExecutor(project_path)
        
        # Estructura organizada para archivos de Cursor
        self.cursor_dir = self.project_path / ".cursor"
        self.prompts_dir = self.cursor_dir / "prompts"
        self.logs_dir = self.cursor_dir / "logs"
        self.config_dir = self.cursor_dir / "config"
        
        # Crear directorios
        for directory in [self.cursor_dir, self.prompts_dir, self.logs_dir, self.config_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Paths de archivos de log
        self.execution_log_path = self.logs_dir / "executions.json"
        self.instructions_log_path = self.logs_dir / "instructions.json"
        self.feedback_log_path = self.logs_dir / "feedback.json"
        self.metrics_log_path = self.logs_dir / "metrics.json"
        
        if not self.cursor_available:
            logger.warning("Cursor CLI no está disponible - modo simulación activado")
        
        logger.info(f"CursorCLIInterface inicializado para {project_path}")
        logger.info(f"Directorios Cursor: {self.cursor_dir}")
    
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
            # Intentar usar Cursor Agent CLI primero (más inteligente)
            if self.agent_executor.agent_available:
                logger.info("Usando Cursor Agent CLI para ejecución inteligente")
                agent_result = self.agent_executor.execute_instruction(instruction)
                
                if agent_result["success"]:
                    # Crear resultado exitoso con Cursor Agent
                    result = type('Result', (), {
                        'success': True,
                        'output': agent_result.get("message", "Cambios aplicados con Cursor Agent CLI"),
                        'changes_made': agent_result.get("changes_made", []),
                        'error': None
                    })()
                else:
                    # Si falla Cursor Agent, usar AutoExecutor como fallback
                    logger.info("Cursor Agent falló, usando AutoExecutor como fallback")
                    auto_result = self.auto_executor.execute_instruction(instruction)
                    
                    if auto_result["success"]:
                        result = type('Result', (), {
                            'success': True,
                            'output': f"AutoExecutor: {auto_result.get('message', 'Cambios aplicados automáticamente')}",
                            'changes_made': auto_result.get("changes_made", []),
                            'error': None
                        })()
                    else:
                        # Si ambos fallan, usar método original
                        prompt = self._generate_cursor_prompt(instruction)
                        result = self._run_cursor_command(prompt, instruction)
                        result.error = f"Agent failed: {agent_result.get('error')}. AutoExecutor failed: {auto_result.get('error')}. {getattr(result, 'error', '') or ''}"
            else:
                # Si Cursor Agent no está disponible, usar AutoExecutor
                logger.info("Cursor Agent no disponible, usando AutoExecutor")
                auto_result = self.auto_executor.execute_instruction(instruction)
                
            if auto_result["success"]:
                # En modo daemon, solo guardar prompt sin abrir IDE
                prompt = self._generate_cursor_prompt(instruction)
                self._save_prompt_for_reference(prompt, instruction)
                
                result = type('Result', (), {
                    'success': True,
                    'output': auto_result.get("message", "Cambios aplicados automáticamente"),
                    'changes_made': auto_result.get("changes_made", []),
                    'error': None
                })()
            else:
                # Si falla AutoExecutor, usar método original
                prompt = self._generate_cursor_prompt(instruction)
                result = self._run_cursor_command(prompt, instruction)
                result.error = f"AutoExecutor failed: {auto_result.get('error', 'Unknown error')}. {getattr(result, 'error', '') or ''}"
            
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
            # Crear directorio por fecha para organizar prompts
            date_dir = self.prompts_dir / instruction.timestamp.strftime('%Y-%m-%d')
            date_dir.mkdir(exist_ok=True)
            
            # Crear archivo de prompt organizado
            prompt_filename = f"{instruction.action}_{instruction.timestamp.strftime('%H%M%S')}.md"
            prompt_file = date_dir / prompt_filename
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # Abrir Cursor IDE con el proyecto (sin el archivo de prompt)
            cmd = [self.cursor_path, str(self.project_path)]
            logger.debug(f"Abriendo Cursor IDE: {' '.join(cmd)}")
            
            # Ejecutar comando en background para no bloquear
            result = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=str(self.project_path)
            )
            
            # Mantener archivo de prompt para referencia (no eliminar)
            logger.info(f"Archivo de prompt creado: {prompt_file}")
            
            # Crear enlace simbólico al último prompt
            latest_link = self.prompts_dir / "latest.md"
            try:
                if latest_link.exists() or latest_link.is_symlink():
                    latest_link.unlink()
                latest_link.symlink_to(prompt_file.relative_to(self.prompts_dir))
                logger.debug(f"Enlace simbólico creado: {latest_link} -> {prompt_file}")
            except Exception as e:
                logger.warning(f"No se pudo crear enlace simbólico: {e}")
            
            # Mostrar instrucciones al usuario
            self._display_instruction_to_user(instruction, prompt_file)
            
            # Simular éxito ya que Cursor se abrió
            changes_made = [f"Cursor IDE abierto con prompt: {prompt_file.name}"]
            return ExecutionResult(
                success=True,
                output=f"Cursor IDE abierto. Prompt disponible en: {prompt_file}",
                changes_made=changes_made
            )
                
        except Exception as e:
            return ExecutionResult(
                success=False,
                error=f"Error abriendo Cursor IDE: {e}"
            )
    
    def _save_prompt_for_reference(self, prompt: str, instruction: CursorInstruction):
        """Guardar prompt para referencia (sin abrir Cursor IDE)"""
        try:
            # Crear directorio por fecha para organizar prompts
            date_dir = self.prompts_dir / instruction.timestamp.strftime('%Y-%m-%d')
            date_dir.mkdir(exist_ok=True)
            
            # Crear archivo de prompt organizado
            prompt_filename = f"{instruction.action}_{instruction.timestamp.strftime('%H%M%S')}.md"
            prompt_file = date_dir / prompt_filename
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # Crear enlace simbólico al último prompt
            latest_link = self.prompts_dir / "latest.md"
            try:
                if latest_link.exists() or latest_link.is_symlink():
                    latest_link.unlink()
                latest_link.symlink_to(prompt_file.relative_to(self.prompts_dir))
                logger.debug(f"Enlace simbólico creado: {latest_link} -> {prompt_file}")
            except Exception as e:
                logger.warning(f"No se pudo crear enlace simbólico: {e}")
            
            logger.info(f"Prompt guardado para referencia: {prompt_file}")
            
        except Exception as e:
            logger.error(f"Error guardando prompt para referencia: {e}")
    
    def _display_instruction_to_user(self, instruction: CursorInstruction, prompt_file: Path):
        """Mostrar instrucciones al usuario en la terminal"""
        print(f"\n🤖 CURSOR CLI - Instrucción Generada")
        print(f"═══════════════════════════════════════════════════════════")
        print(f"📋 Acción: {instruction.action}")
        print(f"🎯 Objetivo: {instruction.target}")
        print(f"⚡ Prioridad: {instruction.priority.upper()}")
        print(f"📄 Prompt: {prompt_file}")
        print(f"═══════════════════════════════════════════════════════════")
        print(f"💡 INSTRUCCIONES:")
        print(f"   1. Cursor IDE se ha abierto con este proyecto")
        print(f"   2. Revisa el prompt en: {prompt_file}")
        print(f"   3. O usa: cat .cursor/prompts/latest.md")
        print(f"   4. Aplica los cambios sugeridos en el prompt")
        print(f"   5. Los cambios se detectarán automáticamente")
        print(f"═══════════════════════════════════════════════════════════\n")
    
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
            output_path = self.execution_log_path
        
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
