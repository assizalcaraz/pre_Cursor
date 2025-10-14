#!/usr/bin/env python3
"""
Cursor Agent Executor - Ejecutor usando Cursor Agent CLI
========================================================

Este módulo ejecuta instrucciones usando Cursor Agent CLI real,
que SÍ puede ejecutar prompts automáticamente.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .models import CursorInstruction

logger = logging.getLogger(__name__)

class CursorAgentExecutor:
    """Ejecutor usando Cursor Agent CLI real"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.logs_dir = self.project_path / ".cursor" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de log de ejecuciones con Cursor Agent
        self.agent_execution_log = self.logs_dir / "agent_executions.json"
        
        # Verificar si cursor-agent está disponible
        self.agent_available = self._check_cursor_agent_availability()
        
        logger.info(f"CursorAgentExecutor inicializado para {project_path}")
        logger.info(f"Cursor Agent CLI disponible: {self.agent_available}")
    
    def _check_cursor_agent_availability(self) -> bool:
        """Verificar si cursor-agent está disponible"""
        try:
            result = subprocess.run(
                ['cursor-agent', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def execute_instruction(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Ejecutar una instrucción usando Cursor Agent CLI"""
        logger.info(f"Ejecutando instrucción con Cursor Agent: {instruction.action}")
        
        if not self.agent_available:
            return {
                "success": False,
                "error": "Cursor Agent CLI no está disponible",
                "changes_made": []
            }
        
        try:
            # Generar prompt específico para Cursor Agent
            prompt = self._generate_agent_prompt(instruction)
            
            # Ejecutar con Cursor Agent CLI
            result = self._run_cursor_agent_command(prompt, instruction)
            
            return result
            
        except Exception as e:
            logger.error(f"Error ejecutando instrucción con Cursor Agent {instruction.action}: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": []
            }
    
    def _generate_agent_prompt(self, instruction: CursorInstruction) -> str:
        """Generar prompt específico para Cursor Agent CLI"""
        
        if instruction.action == "move_test_files":
            return f"""
Mover archivos de test de la raíz del proyecto al directorio tests/.

Instrucciones específicas:
1. Buscar archivos que empiecen con 'test' o terminen con '_test.py' en la raíz
2. Crear el directorio tests/ si no existe
3. Mover todos los archivos de test encontrados al directorio tests/
4. Si ya existe un archivo con el mismo nombre en tests/, crear un nombre único
5. Confirmar que los archivos se movieron correctamente

Proyecto: {self.project_path}
Contexto: {instruction.context}
"""
        
        elif instruction.action == "move_file":
            return f"""
Mover archivo específico a su ubicación correcta según la metodología del proyecto.

Archivo: {instruction.target}
Instrucciones:
1. Determinar la ubicación correcta según el tipo de archivo
2. Crear directorios necesarios si no existen
3. Mover el archivo a la nueva ubicación
4. Verificar que el archivo se movió correctamente

Proyecto: {self.project_path}
Contexto: {instruction.context}
"""
        
        elif instruction.action == "reorganize_structure":
            return f"""
Reorganizar la estructura del proyecto según la metodología establecida.

Archivo objetivo: {instruction.target}
Instrucciones:
1. Analizar la estructura actual del archivo
2. Identificar problemas de organización
3. Reorganizar el código según las mejores prácticas
4. Mantener la funcionalidad existente
5. Aplicar las correcciones necesarias

Proyecto: {self.project_path}
Contexto: {instruction.context}
"""
        
        else:
            return f"""
Ejecutar la siguiente instrucción en el proyecto:

Acción: {instruction.action}
Objetivo: {instruction.target}
Prioridad: {instruction.priority}

Contexto: {instruction.context}

Proyecto: {self.project_path}
"""
    
    def _run_cursor_agent_command(self, prompt: str, instruction: CursorInstruction) -> Dict[str, Any]:
        """Ejecutar comando con Cursor Agent CLI"""
        try:
            # Comando para Cursor Agent CLI
            cmd = [
                'cursor-agent',
                '-p',  # Modo no interactivo
                prompt,
                '--output-format', 'json'  # Formato JSON para parsing
            ]
            
            logger.debug(f"Ejecutando comando Cursor Agent: {' '.join(cmd)}")
            
            # Ejecutar comando
            result = subprocess.run(
                cmd,
                cwd=str(self.project_path),
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            
            # Procesar resultado
            if result.returncode == 0:
                try:
                    # Intentar parsear JSON
                    response = json.loads(result.stdout)
                    changes_made = self._extract_changes_from_response(response)
                    
                    return {
                        "success": True,
                        "message": "Instrucción ejecutada con Cursor Agent CLI",
                        "changes_made": changes_made,
                        "raw_output": result.stdout,
                        "raw_stderr": result.stderr
                    }
                except json.JSONDecodeError:
                    # Si no es JSON válido, usar texto plano
                    changes_made = self._extract_changes_from_text(result.stdout)
                    
                    return {
                        "success": True,
                        "message": "Instrucción ejecutada con Cursor Agent CLI",
                        "changes_made": changes_made,
                        "raw_output": result.stdout,
                        "raw_stderr": result.stderr
                    }
            else:
                return {
                    "success": False,
                    "error": f"Cursor Agent CLI falló: {result.stderr}",
                    "changes_made": [],
                    "raw_output": result.stdout,
                    "raw_stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Cursor Agent CLI timeout (5 minutos)",
                "changes_made": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error ejecutando Cursor Agent CLI: {e}",
                "changes_made": []
            }
    
    def _extract_changes_from_response(self, response: Dict[str, Any]) -> List[str]:
        """Extraer cambios de la respuesta JSON de Cursor Agent"""
        changes = []
        
        if isinstance(response, dict):
            # Buscar información de cambios en la respuesta
            if 'changes' in response:
                changes.extend(response['changes'])
            elif 'files_modified' in response:
                changes.extend([f"Modified: {f}" for f in response['files_modified']])
            elif 'files_created' in response:
                changes.extend([f"Created: {f}" for f in response['files_created']])
            elif 'files_moved' in response:
                changes.extend([f"Moved: {f}" for f in response['files_moved']])
        
        return changes
    
    def _extract_changes_from_text(self, text: str) -> List[str]:
        """Extraer cambios del texto de respuesta de Cursor Agent"""
        changes = []
        
        # Buscar patrones comunes de cambios en el texto
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['moved', 'created', 'modified', 'deleted', 'renamed']):
                changes.append(line)
        
        return changes
    
    def execute_instructions_batch(self, instructions: List[CursorInstruction]) -> Dict[str, Any]:
        """Ejecutar un lote de instrucciones con Cursor Agent CLI"""
        logger.info(f"Ejecutando lote de {len(instructions)} instrucciones con Cursor Agent CLI")
        
        results = []
        total_changes = []
        
        for i, instruction in enumerate(instructions, 1):
            logger.info(f"Ejecutando instrucción {i}/{len(instructions)}: {instruction.action}")
            result = self.execute_instruction(instruction)
            results.append(result)
            
            if result["success"]:
                total_changes.extend(result.get("changes_made", []))
        
        # Guardar log de ejecuciones
        self._save_agent_execution_log(instructions, results)
        
        successful = sum(1 for r in results if r["success"])
        
        return {
            "total_instructions": len(instructions),
            "successful": successful,
            "failed": len(instructions) - successful,
            "total_changes": len(total_changes),
            "changes_made": total_changes,
            "results": results
        }
    
    def _save_agent_execution_log(self, instructions: List[CursorInstruction], results: List[Dict[str, Any]]):
        """Guardar log de ejecuciones con Cursor Agent CLI"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "executor": "cursor_agent_cli",
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
            if self.agent_execution_log.exists():
                with open(self.agent_execution_log, 'r', encoding='utf-8') as f:
                    existing_log = json.load(f)
            else:
                existing_log = {"executions": []}
            
            # Agregar nueva ejecución
            existing_log["executions"].append(log_data)
            
            # Guardar log actualizado
            with open(self.agent_execution_log, 'w', encoding='utf-8') as f:
                json.dump(existing_log, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Log de ejecuciones con Cursor Agent guardado en: {self.agent_execution_log}")
            
        except Exception as e:
            logger.error(f"Error guardando log de ejecuciones con Cursor Agent: {e}")
