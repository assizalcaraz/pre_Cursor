#!/usr/bin/env python3
"""
Modelos de datos para Pre-Cursor
===============================

Este módulo contiene las clases de datos compartidas entre los diferentes
módulos de Pre-Cursor para evitar importaciones circulares.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class ProjectIssue:
    """Representa un problema detectado en el proyecto"""
    type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    file_path: Optional[str] = None
    suggestion: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class SupervisionReport:
    """Reporte de supervisión del proyecto"""
    timestamp: datetime
    issues_found: List[ProjectIssue]
    recommendations: List[str]
    files_created: List[str] = None
    files_modified: List[str] = None
    structure_changes: List[str] = None
    
    def __post_init__(self):
        if self.files_created is None:
            self.files_created = []
        if self.files_modified is None:
            self.files_modified = []
        if self.structure_changes is None:
            self.structure_changes = []

class CursorInstruction:
    """Instrucción específica para Cursor CLI"""
    
    def __init__(self, action: str, target: str, context: str, 
                 methodology_reference: str = "", priority: str = "medium"):
        self.action = action
        self.target = target
        self.context = context
        self.methodology_reference = methodology_reference
        self.priority = priority
        self.timestamp = datetime.now()
        self.status = "pending"
        self.result = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir instrucción a diccionario"""
        return {
            "action": self.action,
            "target": self.target,
            "context": self.context,
            "methodology_reference": self.methodology_reference,
            "priority": self.priority,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "result": self.result
        }
    
    def __str__(self) -> str:
        return f"CursorInstruction(action={self.action}, target={self.target}, priority={self.priority})"

class ExecutionResult:
    """Resultado de la ejecución de una instrucción"""
    
    def __init__(self, success: bool, output: str = "", error: str = "", 
                 changes_made: List[str] = None, execution_time: float = 0.0):
        self.success = success
        self.output = output
        self.error = error
        self.changes_made = changes_made or []
        self.execution_time = execution_time
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir resultado a diccionario"""
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "changes_made": self.changes_made,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        status = "✅ Éxito" if self.success else "❌ Error"
        return f"ExecutionResult({status}, time={self.execution_time:.2f}s)"
