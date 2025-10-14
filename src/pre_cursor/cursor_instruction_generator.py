#!/usr/bin/env python3
"""
Cursor Instruction Generator - Generador de Instrucciones para Cursor CLI
=======================================================================

Este módulo convierte reportes de supervisión en instrucciones ejecutables
para Cursor CLI, implementando la integración bidireccional propuesta.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .models import SupervisionReport, ProjectIssue, CursorInstruction

logger = logging.getLogger(__name__)

class CursorInstructionGenerator:
    """Generador de instrucciones para Cursor CLI basado en reportes de supervisión"""
    
    def __init__(self, project_path: str, methodology_path: str = None):
        self.project_path = Path(project_path)
        self.methodology_path = Path(methodology_path) if methodology_path else None
        self.methodology = self._load_methodology()
        
        # Usar estructura organizada de Cursor
        self.cursor_dir = self.project_path / ".cursor"
        self.logs_dir = self.cursor_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.instructions_log_path = self.logs_dir / "instructions.json"
        
        # Configuración de instrucciones por tipo de problema
        self.instruction_templates = {
            "misplaced_file": self._create_misplaced_file_instruction,
            "duplicate_function": self._create_duplicate_function_instruction,
            "structure_issue": self._create_structure_issue_instruction,
            "missing_documentation": self._create_missing_documentation_instruction,
            "code_quality": self._create_code_quality_instruction,
            "configuration_issue": self._create_configuration_issue_instruction,
            # Instrucciones específicas para tests
            "create_tests_dir": self._create_tests_dir_instruction,
            "rename_test_files": self._create_rename_test_files_instruction,
            "unify_test_functions": self._create_unify_test_functions_instruction,
            "add_test_imports": self._create_add_test_imports_instruction
        }
    
    def _load_methodology(self) -> Dict[str, Any]:
        """Cargar metodología de desarrollo"""
        if not self.methodology_path or not self.methodology_path.exists():
            # Metodología por defecto
            return {
                "file_organization": {
                    "src": "Código fuente principal",
                    "tests": "Pruebas unitarias y de integración",
                    "docs": "Documentación técnica",
                    "examples": "Ejemplos de uso",
                    "config": "Archivos de configuración"
                },
                "code_standards": {
                    "naming": "snake_case para archivos, PascalCase para clases",
                    "documentation": "Docstrings obligatorios en funciones públicas",
                    "testing": "Tests para casos exitosos, error y límites"
                }
            }
        
        try:
            with open(self.methodology_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error cargando metodología: {e}")
            return {}
    
    def generate_instructions(self, report: SupervisionReport) -> List[CursorInstruction]:
        """
        Generar instrucciones basadas en el reporte de supervisión
        
        Args:
            report: Reporte de supervisión con problemas detectados
            
        Returns:
            Lista de instrucciones para Cursor CLI
        """
        instructions = []
        
        logger.info(f"Generando instrucciones para {len(report.issues_found)} problemas detectados")
        
        # Cargar configuración de severidades a procesar
        process_severities = self._get_process_severities()
        
        for issue in report.issues_found:
            # Procesar problemas según configuración
            if issue.severity in process_severities:
                instruction = self._create_instruction_for_issue(issue)
                if instruction:
                    instructions.append(instruction)
                    logger.debug(f"Instrucción creada: {instruction}")
        
        # Ordenar por prioridad
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        instructions.sort(key=lambda x: priority_order.get(x.priority, 2))
        
        logger.info(f"Generadas {len(instructions)} instrucciones para Cursor CLI")
        return instructions
    
    def _get_process_severities(self) -> List[str]:
        """Obtener severidades a procesar desde configuración"""
        config_path = self.project_path / "config" / "cursor_supervisor.yaml"
        
        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                severities = config.get('cursor_integration', {}).get('process_severities', ['high', 'critical'])
                logger.debug(f"Severidades configuradas: {severities}")
                return severities
            except Exception as e:
                logger.warning(f"Error cargando configuración: {e}")
        
        # Configuración por defecto (conservadora)
        return ['high', 'critical']
    
    def _create_instruction_for_issue(self, issue: ProjectIssue) -> Optional[CursorInstruction]:
        """Crear instrucción específica para un problema"""
        issue_type = self._classify_issue_type(issue)
        
        if issue_type in self.instruction_templates:
            return self.instruction_templates[issue_type](issue)
        else:
            logger.warning(f"Tipo de problema no soportado: {issue_type}")
            return None
    
    def _classify_issue_type(self, issue: ProjectIssue) -> str:
        """Clasificar tipo de problema basado en descripción y archivo"""
        description = issue.description.lower()
        file_path = str(issue.file_path).lower()
        
        # Clasificación específica para tests
        if issue.type == "missing_tests_dir":
            return "create_tests_dir"
        elif issue.type == "missing_init":
            return "create_tests_dir"
        elif issue.type == "no_test_files":
            return "create_tests_dir"
        elif issue.type == "inconsistent_naming":
            return "rename_test_files"
        elif issue.type == "duplicate_test_function":
            return "unify_test_functions"
        elif issue.type == "missing_test_imports":
            return "add_test_imports"
        elif issue.type == "empty_test_function":
            return "unify_test_functions"
        elif issue.type == "no_test_coverage":
            return "create_tests_dir"
        
        # Clasificación general
        elif "fuera de lugar" in description or "misplaced" in description or "en raíz" in description:
            return "misplaced_file"
        elif "duplicado" in description or "duplicate" in description:
            return "duplicate_function"
        elif "estructura" in description or "structure" in description:
            return "structure_issue"
        elif "documentación" in description or "documentation" in description:
            return "missing_documentation"
        elif "calidad" in description or "quality" in description:
            return "code_quality"
        elif "configuración" in description or "configuration" in description:
            return "configuration_issue"
        else:
            return "structure_issue"  # Default
    
    def _create_misplaced_file_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para archivo fuera de lugar"""
        # Caso especial: archivos de test en la raíz (file_path es None)
        if issue.file_path is None and "en raíz" in issue.description.lower():
            return self._create_test_files_in_root_instruction(issue)
        
        file_path = Path(issue.file_path)
        correct_location = self._get_correct_location(file_path)
        
        context = f"""
Archivo detectado fuera de lugar: {file_path.name}
Ubicación actual: {file_path.parent}
Ubicación correcta: {correct_location}

Acción requerida: Mover archivo a la ubicación correcta según metodología establecida.
Metodología: {self.methodology.get('file_organization', {})}
"""
        
        return CursorInstruction(
            action="move_file",
            target=str(file_path),
            context=context,
            methodology_reference="file_organization",
            priority="high"
        )
    
    def _create_test_files_in_root_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción específica para archivos de test en la raíz"""
        # Extraer nombres de archivos de la descripción
        import re
        files_match = re.search(r"\[(.*?)\]", issue.description)
        files = files_match.group(1).replace("'", "").split(", ") if files_match else ["archivos de test"]
        
        context = f"""
Archivos de test detectados en la raíz del proyecto: {', '.join(files)}

Ubicación actual: Raíz del proyecto
Ubicación correcta: tests/

Acción requerida: Mover todos los archivos de test al directorio tests/ según metodología establecida.
Metodología: {self.methodology.get('file_organization', {})}

Instrucciones específicas:
1. Crear directorio tests/ si no existe
2. Mover archivos de test desde la raíz al directorio tests/
3. Verificar que no se rompa funcionalidad existente
4. Actualizar imports si es necesario
"""
        
        return CursorInstruction(
            action="move_test_files",
            target="proyecto",
            context=context,
            methodology_reference="file_organization",
            priority="high"
        )
    
    def _create_duplicate_function_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para función duplicada"""
        context = f"""
Función duplicada detectada: {issue.description}
Archivo: {issue.file_path}

Acción requerida: Refactorizar código duplicado siguiendo principios DRY.
Metodología: Evitar duplicación de código, crear funciones reutilizables.
"""
        
        return CursorInstruction(
            action="refactor_duplicate",
            target=str(issue.file_path),
            context=context,
            methodology_reference="code_standards",
            priority="medium"
        )
    
    def _create_structure_issue_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para problema de estructura"""
        context = f"""
Problema de estructura detectado: {issue.description}
Archivo: {issue.file_path if issue.file_path else "Múltiples archivos"}

Acción requerida: Reorganizar estructura del proyecto según metodología.
Metodología: {self.methodology.get('file_organization', {})}
"""
        
        return CursorInstruction(
            action="reorganize_structure",
            target=str(issue.file_path) if issue.file_path else "proyecto",
            context=context,
            methodology_reference="file_organization",
            priority="high"
        )
    
    def _create_missing_documentation_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para documentación faltante"""
        context = f"""
Documentación faltante detectada: {issue.description}
Archivo: {issue.file_path}

Acción requerida: Añadir documentación apropiada según estándares.
Metodología: {self.methodology.get('code_standards', {}).get('documentation', '')}
"""
        
        return CursorInstruction(
            action="add_documentation",
            target=str(issue.file_path),
            context=context,
            methodology_reference="code_standards",
            priority="medium"
        )
    
    def _create_code_quality_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para problema de calidad de código"""
        context = f"""
Problema de calidad detectado: {issue.description}
Archivo: {issue.file_path}

Acción requerida: Mejorar calidad del código según estándares.
Metodología: {self.methodology.get('code_standards', {})}
"""
        
        return CursorInstruction(
            action="improve_code_quality",
            target=str(issue.file_path),
            context=context,
            methodology_reference="code_standards",
            priority="medium"
        )
    
    def _create_configuration_issue_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para problema de configuración"""
        context = f"""
Problema de configuración detectado: {issue.description}
Archivo: {issue.file_path}

Acción requerida: Corregir configuración según estándares del proyecto.
Metodología: Mantener archivos de configuración en ubicaciones apropiadas.
"""
        
        return CursorInstruction(
            action="fix_configuration",
            target=str(issue.file_path),
            context=context,
            methodology_reference="file_organization",
            priority="high"
        )
    
    def _get_correct_location(self, file_path: Path) -> Path:
        """Determinar ubicación correcta para un archivo"""
        file_name = file_path.name
        
        # Reglas de ubicación basadas en metodología
        if file_name.startswith('test_') or file_name.endswith('_test.py'):
            return self.project_path / "tests"
        elif file_name.endswith('.md') and file_name not in ['README.md', 'CONTEXTO.md']:
            return self.project_path / "docs"
        elif file_name in ['config.py', 'settings.py', 'config.json', 'config.yaml']:
            return self.project_path / "config"
        elif file_name.endswith('.py') and not file_name.startswith('test_'):
            return self.project_path / "src"
        else:
            return self.project_path  # Mantener en raíz si no hay regla específica
    
    def generate_cursor_prompt(self, instruction: CursorInstruction) -> str:
        """Generar prompt específico para Cursor AI"""
        prompt = f"""
# Instrucción para Cursor AI - Corrección Automática

## Contexto del Proyecto
- **Proyecto**: {self.project_path.name}
- **Metodología**: {instruction.methodology_reference}
- **Prioridad**: {instruction.priority}

## Instrucción Específica
**Acción**: {instruction.action}
**Archivo objetivo**: {instruction.target}

## Contexto Detallado
{instruction.context}

## Metodología Aplicable
{self.methodology.get(instruction.methodology_reference, {})}

## Instrucciones para Cursor AI
1. **Revisar** el archivo objetivo y entender el problema
2. **Aplicar** la corrección siguiendo la metodología establecida
3. **Verificar** que la corrección no rompe funcionalidad existente
4. **Documentar** los cambios realizados si es necesario

## Archivos de Referencia
- `CURSOR_GUIDE.md`: Guía específica para Cursor AI
- `METODOLOGIA_DESARROLLO.md`: Metodología establecida
- `BITACORA.md`: Registro de cambios

---
*Esta instrucción fue generada automáticamente por Pre-Cursor Supervisor*
"""
        return prompt
    
    def save_instructions(self, instructions: List[CursorInstruction], 
                         output_path: str = None) -> str:
        """Guardar instrucciones en archivo JSON"""
        if not output_path:
            output_path = self.instructions_log_path
        
        instructions_data = {
            "project_path": str(self.project_path),
            "generated_at": datetime.now().isoformat(),
            "total_instructions": len(instructions),
            "instructions": [inst.to_dict() for inst in instructions]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(instructions_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Instrucciones guardadas en: {output_path}")
        return str(output_path)
    
    def _create_tests_dir_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para crear directorio de tests"""
        return CursorInstruction(
            action="create_tests_dir",
            target="tests/",
            context=f"Crear directorio tests/ con archivo __init__.py\n\nProblema: {issue.description}\nSugerencia: {issue.suggestion}",
            methodology_reference="test_organization",
            priority=issue.severity
        )
    
    def _create_rename_test_files_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para renombrar archivos de test"""
        return CursorInstruction(
            action="rename_test_files",
            target="tests/",
            context=f"Renombrar archivos de test para usar nomenclatura consistente\n\nProblema: {issue.description}\nSugerencia: {issue.suggestion}",
            methodology_reference="test_naming",
            priority=issue.severity
        )
    
    def _create_unify_test_functions_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para unificar funciones de test duplicadas"""
        return CursorInstruction(
            action="unify_test_functions",
            target="tests/",
            context=f"Unificar funciones de test duplicadas o vacías\n\nProblema: {issue.description}\nSugerencia: {issue.suggestion}",
            methodology_reference="test_optimization",
            priority=issue.severity
        )
    
    def _create_add_test_imports_instruction(self, issue: ProjectIssue) -> CursorInstruction:
        """Crear instrucción para agregar imports necesarios a tests"""
        return CursorInstruction(
            action="add_test_imports",
            target=str(issue.file_path) if issue.file_path else "tests/",
            context=f"Agregar imports necesarios (unittest/pytest)\n\nProblema: {issue.description}\nSugerencia: {issue.suggestion}",
            methodology_reference="test_imports",
            priority=issue.severity
        )
