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
            elif instruction.action == "create_tests_dir":
                return self._execute_create_tests_dir(instruction)
            elif instruction.action == "rename_test_files":
                return self._execute_rename_test_files(instruction)
            elif instruction.action == "unify_test_functions":
                return self._execute_unify_test_functions(instruction)
            elif instruction.action == "add_test_imports":
                return self._execute_add_test_imports(instruction)
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
    
    def _execute_create_tests_dir(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Crear directorio tests/ con archivo __init__.py"""
        changes_made = []
        
        try:
            tests_dir = self.project_path / "tests"
            
            if not tests_dir.exists():
                tests_dir.mkdir(exist_ok=True)
                changes_made.append("Creado directorio tests/")
                logger.info("Directorio tests/ creado")
            
            # Crear __init__.py si no existe
            init_file = tests_dir / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Tests package\n")
                changes_made.append("Creado tests/__init__.py")
                logger.info("Archivo tests/__init__.py creado")
            
            return {
                "success": True,
                "message": f"Directorio tests/ configurado correctamente",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error creando directorio tests: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_rename_test_files(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Renombrar archivos de test para usar nomenclatura consistente"""
        changes_made = []
        
        try:
            tests_dir = self.project_path / "tests"
            if not tests_dir.exists():
                return {
                    "success": False,
                    "error": "Directorio tests/ no existe",
                    "changes_made": []
                }
            
            # Buscar archivos con nomenclatura inconsistente
            inconsistent_files = []
            for file_path in tests_dir.glob("*.py"):
                if not (file_path.name.startswith('test_') or file_path.name.endswith('_test.py')):
                    inconsistent_files.append(file_path)
            
            for file_path in inconsistent_files:
                # Renombrar a test_*.py
                new_name = f"test_{file_path.name}"
                new_path = file_path.parent / new_name
                
                # Verificar que no exista ya
                counter = 1
                while new_path.exists():
                    name_parts = file_path.stem, counter, file_path.suffix
                    new_name = f"test_{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                    new_path = file_path.parent / new_name
                    counter += 1
                
                file_path.rename(new_path)
                changes_made.append(f"Renombrado {file_path.name} -> {new_name}")
                logger.info(f"Archivo renombrado: {file_path.name} -> {new_name}")
            
            return {
                "success": True,
                "message": f"Renombrados {len(changes_made)} archivos de test",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error renombrando archivos de test: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_unify_test_functions(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Unificar funciones de test duplicadas"""
        changes_made = []
        
        try:
            # Esta es una acción compleja que requiere análisis de código
            # Por ahora, solo logueamos la instrucción
            logger.info(f"Unificación de funciones de test solicitada para: {instruction.target}")
            
            return {
                "success": True,
                "message": "Unificación de funciones de test registrada (requiere intervención manual)",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error unificando funciones de test: {e}")
            return {
                "success": False,
                "error": str(e),
                "changes_made": changes_made
            }
    
    def _execute_add_test_imports(self, instruction: CursorInstruction) -> Dict[str, Any]:
        """Agregar imports necesarios a archivos de test"""
        changes_made = []
        
        try:
            tests_dir = self.project_path / "tests"
            if not tests_dir.exists():
                return {
                    "success": False,
                    "error": "Directorio tests/ no existe",
                    "changes_made": []
                }
            
            test_files = list(tests_dir.glob("test_*.py")) + list(tests_dir.glob("*_test.py"))
            
            for test_file in test_files:
                try:
                    with open(test_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Verificar si necesita imports
                    needs_unittest = 'import unittest' not in content and 'unittest.' in content
                    needs_pytest = 'import pytest' not in content and 'pytest.' in content
                    
                    if needs_unittest or needs_pytest:
                        # Agregar imports al inicio del archivo
                        imports = []
                        if needs_unittest:
                            imports.append("import unittest")
                        if needs_pytest:
                            imports.append("import pytest")
                        
                        # Insertar imports después de docstring si existe
                        lines = content.split('\n')
                        insert_index = 0
                        
                        # Buscar docstring
                        if lines and lines[0].strip().startswith('"""'):
                            for i, line in enumerate(lines[1:], 1):
                                if line.strip().endswith('"""'):
                                    insert_index = i + 1
                                    break
                        
                        # Insertar imports
                        for import_line in imports:
                            lines.insert(insert_index, import_line)
                            insert_index += 1
                        
                        new_content = '\n'.join(lines)
                        
                        with open(test_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        changes_made.append(f"Agregados imports a {test_file.name}")
                        logger.info(f"Imports agregados a {test_file.name}")
                
                except Exception as e:
                    logger.warning(f"Error procesando {test_file.name}: {e}")
                    continue
            
            return {
                "success": True,
                "message": f"Imports agregados a {len(changes_made)} archivos de test",
                "changes_made": changes_made
            }
            
        except Exception as e:
            logger.error(f"Error agregando imports de test: {e}")
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
