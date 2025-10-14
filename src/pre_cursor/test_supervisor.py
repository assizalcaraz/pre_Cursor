#!/usr/bin/env python3
"""
Test Supervisor - Supervisor Especializado para Tests
====================================================

Este módulo se encarga específicamente de supervisar y mantener
la carpeta de tests, unificando nombres y funciones, y sincronizando
con la documentación.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import logging

from .models import ProjectIssue

logger = logging.getLogger(__name__)

class TestSupervisor:
    """Supervisor especializado para la carpeta de tests"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.tests_dir = self.project_path / "tests"
        self.logs_dir = self.project_path / ".cursor" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivos de documentación a sincronizar
        self.docs_files = [
            self.project_path / "README.md",
            self.project_path / "BITACORA.md",
            self.project_path / "CONTEXTO.md",
            self.project_path / "docs" / "TUTORIAL.md"
        ]
        
        # Log específico para test supervisor
        self.test_log_path = self.logs_dir / "test_supervisor.json"
        
        logger.info(f"TestSupervisor inicializado para {project_path}")
    
    def run_test_supervision(self) -> Dict[str, Any]:
        """Ejecutar supervisión completa de tests"""
        logger.info("Iniciando supervisión especializada de tests")
        
        issues = []
        
        # 1. Analizar estructura de tests
        structure_issues = self._analyze_test_structure()
        issues.extend(structure_issues)
        
        # 2. Detectar tests duplicados o innecesarios
        duplicate_issues = self._detect_duplicate_tests()
        issues.extend(duplicate_issues)
        
        # 3. Verificar sincronización con documentación
        sync_issues = self._check_documentation_sync()
        issues.extend(sync_issues)
        
        # 4. Detectar funciones de test inconsistentes
        function_issues = self._analyze_test_functions()
        issues.extend(function_issues)
        
        # 5. Verificar cobertura de tests
        coverage_issues = self._check_test_coverage()
        issues.extend(coverage_issues)
        
        # 6. Aplicar correcciones automáticas
        corrections_applied = self._apply_automatic_corrections(issues)
        
        # 7. Validar tests con LLM
        validation_results = self._validate_tests_with_llm()
        
        # Guardar log de supervisión
        self._save_supervision_log(issues)
        
        return {
            "total_issues": len(issues),
            "issues": issues,
            "corrections_applied": corrections_applied,
            "validation_results": validation_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_test_structure(self) -> List[ProjectIssue]:
        """Analizar estructura de la carpeta de tests"""
        issues = []
        
        if not self.tests_dir.exists():
            issues.append(ProjectIssue(
                type='missing_tests_dir',
                severity='high',
                description="Directorio tests/ no existe",
                suggestion="Crear directorio tests/ y agregar archivo __init__.py",
                file_path=None
            ))
            return issues
        
        # Verificar archivo __init__.py
        init_file = self.tests_dir / "__init__.py"
        if not init_file.exists():
            issues.append(ProjectIssue(
                type='missing_init',
                severity='medium',
                description="Archivo tests/__init__.py no existe",
                suggestion="Crear archivo __init__.py en tests/",
                file_path=init_file
            ))
        
        # Analizar archivos de test
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        
        if not test_files:
            issues.append(ProjectIssue(
                type='no_test_files',
                severity='high',
                description="No se encontraron archivos de test",
                suggestion="Crear archivos de test con nomenclatura test_*.py o *_test.py",
                file_path=self.tests_dir
            ))
        
        # Verificar nomenclatura consistente
        inconsistent_files = []
        for test_file in test_files:
            if not (test_file.name.startswith('test_') or test_file.name.endswith('_test.py')):
                inconsistent_files.append(test_file.name)
        
        if inconsistent_files:
            issues.append(ProjectIssue(
                type='inconsistent_naming',
                severity='medium',
                description=f"Archivos con nomenclatura inconsistente: {inconsistent_files}",
                suggestion="Renombrar archivos para usar test_*.py o *_test.py",
                file_path=self.tests_dir
            ))
        
        return issues
    
    def _detect_duplicate_tests(self) -> List[ProjectIssue]:
        """Detectar tests duplicados o innecesarios"""
        issues = []
        
        if not self.tests_dir.exists():
            return issues
        
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        
        # Analizar contenido de archivos de test
        test_functions = {}
        duplicate_functions = []
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraer funciones de test
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        func_name = node.name
                        if func_name in test_functions:
                            duplicate_functions.append({
                                'function': func_name,
                                'files': [test_functions[func_name], str(test_file)]
                            })
                        else:
                            test_functions[func_name] = str(test_file)
            
            except Exception as e:
                logger.warning(f"Error analizando {test_file}: {e}")
        
        if duplicate_functions:
            for dup in duplicate_functions:
                issues.append(ProjectIssue(
                    type='duplicate_test_function',
                    severity='medium',
                    description=f"Función de test duplicada '{dup['function']}' en {dup['files']}",
                    suggestion="Unificar funciones duplicadas en un solo archivo",
                    file_path=self.tests_dir
                ))
        
        return issues
    
    def _check_documentation_sync(self) -> List[ProjectIssue]:
        """Verificar sincronización con documentación"""
        issues = []
        
        if not self.tests_dir.exists():
            return issues
        
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        test_names = [f.stem for f in test_files]
        
        for doc_file in self.docs_files:
            if not doc_file.exists():
                continue
            
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Buscar referencias a tests en la documentación
                for test_name in test_names:
                    if test_name not in content:
                        issues.append(ProjectIssue(
                            type='missing_doc_reference',
                            severity='low',
                            description=f"Test '{test_name}' no referenciado en {doc_file.name}",
                            suggestion=f"Agregar referencia a {test_name} en {doc_file.name}",
                            file_path=doc_file
                        ))
            
            except Exception as e:
                logger.warning(f"Error leyendo {doc_file}: {e}")
        
        return issues
    
    def _analyze_test_functions(self) -> List[ProjectIssue]:
        """Analizar funciones de test para detectar inconsistencias"""
        issues = []
        
        if not self.tests_dir.exists():
            return issues
        
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Verificar imports necesarios
                if 'import unittest' not in content and 'import pytest' not in content:
                    issues.append(ProjectIssue(
                        type='missing_test_imports',
                        severity='medium',
                        description=f"Archivo {test_file.name} no importa unittest o pytest",
                        suggestion="Agregar import unittest o import pytest",
                        file_path=test_file
                    ))
                
                # Verificar funciones de test vacías
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        if not node.body or (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                            issues.append(ProjectIssue(
                                type='empty_test_function',
                                severity='medium',
                                description=f"Función de test vacía '{node.name}' en {test_file.name}",
                                suggestion="Implementar tests o eliminar función vacía",
                                file_path=test_file
                            ))
            
            except Exception as e:
                logger.warning(f"Error analizando {test_file}: {e}")
        
        return issues
    
    def _check_test_coverage(self) -> List[ProjectIssue]:
        """Verificar cobertura de tests"""
        issues = []
        
        if not self.tests_dir.exists():
            return issues
        
        # Buscar archivos fuente principales
        src_files = []
        if (self.project_path / "src").exists():
            src_files.extend((self.project_path / "src").glob("*.py"))
        else:
            src_files.extend(self.project_path.glob("*.py"))
        
        # Filtrar archivos de test y __init__.py
        src_files = [f for f in src_files if not f.name.startswith('test_') and f.name != '__init__.py']
        
        test_files = list(self.tests_dir.glob("test_*.py")) + list(self.tests_dir.glob("*_test.py"))
        
        if src_files and not test_files:
            issues.append(ProjectIssue(
                type='no_test_coverage',
                severity='high',
                description=f"Archivos fuente sin tests: {[f.name for f in src_files]}",
                suggestion="Crear tests para los archivos fuente principales",
                file_path=self.tests_dir
            ))
        
        return issues
    
    def _apply_automatic_corrections(self, issues: List[ProjectIssue]) -> Dict[str, Any]:
        """Aplicar correcciones automáticas para problemas de tests"""
        corrections_applied = {
            "total_corrections": 0,
            "successful": 0,
            "failed": 0,
            "changes_made": []
        }
        
        try:
            from .auto_executor import AutoExecutor
            from .cursor_instruction_generator import CursorInstructionGenerator
            
            # Inicializar componentes
            auto_executor = AutoExecutor(str(self.project_path))
            instruction_generator = CursorInstructionGenerator(str(self.project_path))
            
            # Crear reporte temporal para generar instrucciones
            from .models import SupervisionReport
            report = SupervisionReport(
                timestamp=datetime.now(),
                issues_found=issues,
                recommendations=[]
            )
            
            # Generar instrucciones para problemas de tests
            instructions = instruction_generator.generate_instructions(report)
            
            # Filtrar solo instrucciones de tests
            test_instructions = [
                inst for inst in instructions 
                if inst.action in ["create_tests_dir", "rename_test_files", "add_test_imports"]
            ]
            
            if test_instructions:
                logger.info(f"Aplicando {len(test_instructions)} correcciones automáticas de tests")
                
                # Ejecutar correcciones
                result = auto_executor.execute_instructions_batch(test_instructions)
                
                corrections_applied["total_corrections"] = result["total_instructions"]
                corrections_applied["successful"] = result["successful"]
                corrections_applied["failed"] = result["failed"]
                corrections_applied["changes_made"] = result["changes_made"]
                
                logger.info(f"Correcciones aplicadas: {result['successful']}/{result['total_instructions']}")
            
        except Exception as e:
            logger.error(f"Error aplicando correcciones automáticas: {e}")
            corrections_applied["error"] = str(e)
        
        return corrections_applied
    
    def _validate_tests_with_llm(self) -> Dict[str, Any]:
        """Validar tests usando LLM"""
        try:
            from .test_validator import TestValidator
            
            validator = TestValidator(str(self.project_path))
            validation_results = validator.validate_tests_with_llm()
            
            # Si hay tests inválidos o vacíos, limpiarlos
            if validation_results["invalid_tests"] or validation_results["empty_tests"]:
                cleanup_results = validator.cleanup_invalid_tests(validation_results)
                validation_results["cleanup_results"] = cleanup_results
                logger.info(f"Tests limpiados: {len(cleanup_results['files_removed'])} eliminados, {len(cleanup_results['files_kept'])} mantenidos")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validando tests con LLM: {e}")
            return {
                "valid_tests": [],
                "invalid_tests": [],
                "empty_tests": [],
                "unified_content": "",
                "total_analyzed": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _save_supervision_log(self, issues: List[ProjectIssue]):
        """Guardar log de supervisión de tests"""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "project_path": str(self.project_path),
                "supervisor": "test_supervisor",
                "total_issues": len(issues),
                "issues": [
                    {
                        "type": issue.type,
                        "severity": issue.severity,
                        "description": issue.description,
                        "suggestion": issue.suggestion,
                        "file_path": str(issue.file_path) if issue.file_path else None
                    }
                    for issue in issues
                ]
            }
            
            # Leer log existente
            if self.test_log_path.exists():
                with open(self.test_log_path, 'r', encoding='utf-8') as f:
                    existing_log = json.load(f)
            else:
                existing_log = {"supervisions": []}
            
            # Agregar nueva supervisión
            existing_log["supervisions"].append(log_data)
            
            # Guardar log actualizado
            with open(self.test_log_path, 'w', encoding='utf-8') as f:
                json.dump(existing_log, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Log de supervisión de tests guardado en: {self.test_log_path}")
            
        except Exception as e:
            logger.error(f"Error guardando log de supervisión de tests: {e}")

# Importar json al final para evitar problemas de importación circular
import json

