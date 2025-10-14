#!/usr/bin/env python3
"""
Test Validator - Validador de Tests usando LLM
==============================================

Este módulo usa Cursor Agent CLI para validar el contenido real de los tests,
detectar tests falsos/vacíos y unificar tests válidos.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import json
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

from .models import ProjectIssue

logger = logging.getLogger(__name__)

class TestValidator:
    """Validador de tests usando LLM (Cursor Agent CLI)"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.tests_dir = self.project_path / "tests"
        self.logs_dir = self.project_path / ".cursor" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Log específico para test validator
        self.validator_log_path = self.logs_dir / "test_validator.json"
        
        logger.info(f"TestValidator inicializado para {project_path}")
    
    def validate_tests_with_llm(self) -> Dict[str, Any]:
        """Validar tests usando Cursor Agent CLI"""
        logger.info("Iniciando validación de tests con LLM")
        
        if not self.tests_dir.exists():
            return {
                "valid_tests": [],
                "invalid_tests": [],
                "empty_tests": [],
                "unified_content": "",
                "total_analyzed": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Obtener todos los archivos de test
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        
        if not test_files:
            return {
                "valid_tests": [],
                "invalid_tests": [],
                "empty_tests": [],
                "unified_content": "",
                "total_analyzed": 0,
                "timestamp": datetime.now().isoformat()
            }
        
        # Analizar cada archivo de test
        valid_tests = []
        invalid_tests = []
        empty_tests = []
        all_test_content = []
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analizar con LLM
                analysis = self._analyze_test_with_llm(test_file, content)
                
                if analysis["is_valid"]:
                    valid_tests.append({
                        "file": str(test_file),
                        "content": content,
                        "functions": analysis["functions"],
                        "quality_score": analysis["quality_score"]
                    })
                    all_test_content.append(content)
                elif analysis["is_empty"]:
                    empty_tests.append({
                        "file": str(test_file),
                        "reason": analysis["reason"]
                    })
                else:
                    invalid_tests.append({
                        "file": str(test_file),
                        "reason": analysis["reason"],
                        "suggestions": analysis["suggestions"]
                    })
                    
            except Exception as e:
                logger.error(f"Error analizando {test_file}: {e}")
                invalid_tests.append({
                    "file": str(test_file),
                    "reason": f"Error de lectura: {e}",
                    "suggestions": []
                })
        
        # Generar contenido unificado
        unified_content = self._generate_unified_tests(valid_tests)
        
        # Guardar resultados
        results = {
            "valid_tests": valid_tests,
            "invalid_tests": invalid_tests,
            "empty_tests": empty_tests,
            "unified_content": unified_content,
            "total_analyzed": len(test_files),
            "timestamp": datetime.now().isoformat()
        }
        
        self._save_validation_log(results)
        
        return results
    
    def _analyze_test_with_llm(self, test_file: Path, content: str) -> Dict[str, Any]:
        """Analizar un archivo de test usando Cursor Agent CLI"""
        try:
            # Crear prompt para análisis
            prompt = self._create_analysis_prompt(test_file, content)
            
            # Ejecutar con Cursor Agent CLI
            result = self._execute_cursor_agent(prompt)
            
            if result["success"]:
                return self._parse_analysis_result(result["output"])
            else:
                # Fallback: análisis básico
                return self._basic_analysis(test_file, content)
                
        except Exception as e:
            logger.error(f"Error en análisis LLM de {test_file}: {e}")
            return self._basic_analysis(test_file, content)
    
    def _create_analysis_prompt(self, test_file: Path, content: str) -> str:
        """Crear prompt para análisis de test"""
        return f"""Analiza el siguiente archivo de test y determina si es válido, vacío o falso:

ARCHIVO: {test_file.name}
CONTENIDO:
```python
{content}
```

INSTRUCCIONES:
1. Determina si el test es VÁLIDO, VACÍO o FALSO
2. Si es VÁLIDO: identifica las funciones de test y asigna un score de calidad (1-10)
3. Si es VACÍO: explica por qué (solo pass, comentarios, etc.)
4. Si es FALSO: explica por qué y sugiere mejoras

RESPONDE EN FORMATO JSON:
{{
    "is_valid": true/false,
    "is_empty": true/false,
    "is_fake": true/false,
    "functions": ["test_func1", "test_func2"],
    "quality_score": 8,
    "reason": "Explicación del análisis",
    "suggestions": ["sugerencia1", "sugerencia2"]
}}

ANÁLISIS:"""
    
    def _execute_cursor_agent(self, prompt: str) -> Dict[str, Any]:
        """Ejecutar análisis con Cursor Agent CLI"""
        try:
            from .cursor_agent_executor import CursorAgentExecutor
            
            # Crear instrucción temporal
            from .models import CursorInstruction
            instruction = CursorInstruction(
                action="analyze_test",
                target="tests/",
                context=prompt,
                methodology_reference="test_validation",
                priority="medium"
            )
            
            # Ejecutar con Cursor Agent
            executor = CursorAgentExecutor(str(self.project_path))
            result = executor.execute_instruction(instruction)
            
            return {
                "success": result.get("success", False),
                "output": result.get("output", ""),
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Error ejecutando Cursor Agent: {e}")
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    def _parse_analysis_result(self, output: str) -> Dict[str, Any]:
        """Parsear resultado del análisis LLM"""
        try:
            # Buscar JSON en la salida
            import re
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                return {
                    "is_valid": result.get("is_valid", False),
                    "is_empty": result.get("is_empty", False),
                    "is_fake": result.get("is_fake", False),
                    "functions": result.get("functions", []),
                    "quality_score": result.get("quality_score", 0),
                    "reason": result.get("reason", "Análisis completado"),
                    "suggestions": result.get("suggestions", [])
                }
            else:
                # Fallback si no se encuentra JSON
                return self._parse_text_analysis(output)
                
        except Exception as e:
            logger.error(f"Error parseando resultado: {e}")
            return {
                "is_valid": False,
                "is_empty": False,
                "is_fake": True,
                "functions": [],
                "quality_score": 0,
                "reason": f"Error parseando resultado: {e}",
                "suggestions": []
            }
    
    def _parse_text_analysis(self, output: str) -> Dict[str, Any]:
        """Parsear análisis en formato texto"""
        output_lower = output.lower()
        
        is_valid = "válido" in output_lower or "valid" in output_lower
        is_empty = "vacío" in output_lower or "empty" in output_lower
        is_fake = "falso" in output_lower or "fake" in output_lower
        
        return {
            "is_valid": is_valid and not is_empty and not is_fake,
            "is_empty": is_empty,
            "is_fake": is_fake,
            "functions": [],
            "quality_score": 5 if is_valid else 0,
            "reason": output[:200] + "..." if len(output) > 200 else output,
            "suggestions": []
        }
    
    def _basic_analysis(self, test_file: Path, content: str) -> Dict[str, Any]:
        """Análisis básico sin LLM"""
        try:
            # Parsear AST
            tree = ast.parse(content)
            
            # Buscar funciones de test
            test_functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_functions.append(node.name)
            
            # Verificar si está vacío
            is_empty = len(test_functions) == 0 or all(
                len(func.body) == 1 and isinstance(func.body[0], ast.Pass)
                for func in ast.walk(tree) if isinstance(func, ast.FunctionDef) and func.name.startswith('test_')
            )
            
            # Verificar si es falso (solo comentarios o docstrings)
            has_real_code = any(
                not isinstance(node, (ast.Expr, ast.Pass))
                for node in ast.walk(tree)
                if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))
            )
            
            return {
                "is_valid": len(test_functions) > 0 and not is_empty and has_real_code,
                "is_empty": is_empty,
                "is_fake": not has_real_code and len(test_functions) > 0,
                "functions": test_functions,
                "quality_score": len(test_functions) * 2 if not is_empty else 0,
                "reason": "Análisis básico completado",
                "suggestions": []
            }
            
        except Exception as e:
            return {
                "is_valid": False,
                "is_empty": True,
                "is_fake": False,
                "functions": [],
                "quality_score": 0,
                "reason": f"Error en análisis básico: {e}",
                "suggestions": []
            }
    
    def _generate_unified_tests(self, valid_tests: List[Dict[str, Any]]) -> str:
        """Generar archivo unificado con todos los tests válidos"""
        if not valid_tests:
            return ""
        
        # Ordenar por calidad
        valid_tests.sort(key=lambda x: x["quality_score"], reverse=True)
        
        unified_content = '''#!/usr/bin/env python3
"""
Tests Unificados - Generados automáticamente
===========================================

Este archivo contiene todos los tests válidos del proyecto,
unificados y optimizados automáticamente.

Generado: {timestamp}
Total de tests: {total_tests}
"""
import unittest
import pytest
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tests=len(valid_tests)
        )
        
        # Agregar contenido de cada test válido
        for i, test in enumerate(valid_tests):
            unified_content += f"\n# === Test {i+1}: {Path(test['file']).name} ===\n"
            unified_content += f"# Calidad: {test['quality_score']}/10\n"
            unified_content += f"# Funciones: {', '.join(test['functions'])}\n\n"
            unified_content += test['content']
            unified_content += "\n\n"
        
        return unified_content
    
    def _save_validation_log(self, results: Dict[str, Any]):
        """Guardar log de validación"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "validator": "test_validator",
                "results": results
            }
            
            # Leer log existente
            if self.validator_log_path.exists():
                with open(self.validator_log_path, 'r', encoding='utf-8') as f:
                    existing_log = json.load(f)
            else:
                existing_log = {"validations": []}
            
            # Agregar nueva validación
            existing_log["validations"].append(log_data)
            
            # Guardar log actualizado
            with open(self.validator_log_path, 'w', encoding='utf-8') as f:
                json.dump(existing_log, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Log de validación guardado en: {self.validator_log_path}")
            
        except Exception as e:
            logger.error(f"Error guardando log de validación: {e}")
    
    def cleanup_invalid_tests(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Limpiar tests inválidos y vacíos"""
        cleanup_results = {
            "files_removed": [],
            "files_kept": [],
            "unified_file_created": False,
            "errors": []
        }
        
        try:
            # Eliminar tests vacíos e inválidos
            for test in results["empty_tests"] + results["invalid_tests"]:
                test_path = Path(test["file"])
                if test_path.exists():
                    test_path.unlink()
                    cleanup_results["files_removed"].append(str(test_path))
                    logger.info(f"Archivo eliminado: {test_path}")
            
            # Crear archivo unificado si hay tests válidos
            if results["valid_tests"] and results["unified_content"]:
                unified_path = self.tests_dir / "test_unified.py"
                with open(unified_path, 'w', encoding='utf-8') as f:
                    f.write(results["unified_content"])
                cleanup_results["unified_file_created"] = True
                cleanup_results["files_kept"].append(str(unified_path))
                logger.info(f"Archivo unificado creado: {unified_path}")
            
            # Mantener solo el archivo unificado
            for test_file in self.tests_dir.glob("test_*.py"):
                if test_file.name != "test_unified.py":
                    if test_file.exists():
                        test_file.unlink()
                        cleanup_results["files_removed"].append(str(test_file))
            
        except Exception as e:
            cleanup_results["errors"].append(str(e))
            logger.error(f"Error en limpieza: {e}")
        
        return cleanup_results
