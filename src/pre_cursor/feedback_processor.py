#!/usr/bin/env python3
"""
Feedback Processor - Procesador de Resultados y Actualización de Estado
======================================================================

Este módulo procesa los resultados de la ejecución de instrucciones en Cursor CLI
y actualiza el estado del proyecto, incluyendo la bitácora y métricas.

Autor: Sistema de Generación Automática
Fecha: 2024-12-19
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from .models import CursorInstruction, ExecutionResult

logger = logging.getLogger(__name__)

class FeedbackProcessor:
    """Procesador de feedback y actualización de estado del proyecto"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.bitacora_path = self.project_path / "BITACORA.md"
        
        # Usar estructura organizada de Cursor
        self.cursor_dir = self.project_path / ".cursor"
        self.logs_dir = self.cursor_dir / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_path = self.logs_dir / "metrics.json"
        self.feedback_log = []
        
        # Crear archivos si no existen
        self._initialize_files()
    
    def _initialize_files(self):
        """Inicializar archivos necesarios si no existen"""
        # Crear BITACORA.md si no existe
        if not self.bitacora_path.exists():
            self._create_initial_bitacora()
        
        # Crear directorio para métricas si no existe
        self.metrics_path.parent.mkdir(exist_ok=True)
    
    def _create_initial_bitacora(self):
        """Crear bitácora inicial si no existe"""
        bitacora_content = f"""# BITACORA - {self.project_path.name}

## Log de desarrollo del proyecto

### {datetime.now().strftime('%Y-%m-%d')}
- **INICIO**: Proyecto inicializado con Pre-Cursor
- **OBJETIVO**: Desarrollo con supervisión automática de Cursor
- **ESTADO**: Configuración inicial
- **PRÓXIMOS PASOS**: Implementar funcionalidades core

---
*Bitácora generada automáticamente por Pre-Cursor*
"""
        with open(self.bitacora_path, 'w', encoding='utf-8') as f:
            f.write(bitacora_content)
    
    def process_result(self, result: ExecutionResult, instruction: CursorInstruction) -> None:
        """
        Procesar resultado de ejecución y actualizar estado
        
        Args:
            result: Resultado de la ejecución
            instruction: Instrucción ejecutada
        """
        logger.info(f"Procesando resultado: {result}")
        
        # Crear entrada de feedback
        feedback_entry = self._create_feedback_entry(result, instruction)
        self.feedback_log.append(feedback_entry)
        
        # Actualizar bitácora
        self._update_bitacora(feedback_entry)
        
        # Actualizar métricas
        self._update_metrics(result, instruction)
        
        # Procesar cambios específicos
        if result.success:
            self._process_successful_changes(result, instruction)
        else:
            self._process_failed_execution(result, instruction)
    
    def _create_feedback_entry(self, result: ExecutionResult, instruction: CursorInstruction) -> Dict[str, Any]:
        """Crear entrada de feedback"""
        return {
            "timestamp": datetime.now().isoformat(),
            "instruction": instruction.to_dict(),
            "result": result.to_dict(),
            "success": result.success,
            "changes_made": result.changes_made,
            "execution_time": result.execution_time
        }
    
    def _update_bitacora(self, feedback_entry: Dict[str, Any]) -> None:
        """Actualizar bitácora con entrada de feedback"""
        try:
            # Leer bitácora actual
            with open(self.bitacora_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear nueva entrada
            entry = self._format_bitacora_entry(feedback_entry)
            
            # Insertar antes del último separador
            if "---" in content:
                parts = content.split("---")
                new_content = parts[0] + entry + "\n---" + "---".join(parts[1:])
            else:
                new_content = content + "\n" + entry
            
            # Escribir bitácora actualizada
            with open(self.bitacora_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            logger.debug("Bitácora actualizada con resultado de ejecución")
            
        except Exception as e:
            logger.error(f"Error actualizando bitácora: {e}")
    
    def _format_bitacora_entry(self, feedback_entry: Dict[str, Any]) -> str:
        """Formatear entrada para bitácora"""
        timestamp = datetime.fromisoformat(feedback_entry["timestamp"])
        instruction = feedback_entry["instruction"]
        result = feedback_entry["result"]
        
        status_emoji = "✅" if feedback_entry["success"] else "❌"
        
        entry = f"""
### {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {status_emoji} Aplicación automática de corrección

**Instrucción**: {instruction['action']}
**Archivo**: {instruction['target']}
**Prioridad**: {instruction['priority']}
**Tiempo de ejecución**: {result['execution_time']:.2f}s

**Resultado**: {'Éxito' if feedback_entry['success'] else 'Error'}
"""
        
        if feedback_entry["success"] and result["changes_made"]:
            entry += "\n**Cambios realizados**:\n"
            for change in result["changes_made"]:
                entry += f"- {change}\n"
        
        if not feedback_entry["success"] and result["error"]:
            entry += f"\n**Error**: {result['error']}\n"
        
        entry += f"\n**Metodología aplicada**: {instruction['methodology_reference']}\n"
        
        return entry
    
    def _update_metrics(self, result: ExecutionResult, instruction: CursorInstruction) -> None:
        """Actualizar métricas del proyecto"""
        try:
            # Cargar métricas existentes
            metrics = self._load_metrics()
            
            # Actualizar contadores
            metrics["total_executions"] += 1
            if result.success:
                metrics["successful_executions"] += 1
            else:
                metrics["failed_executions"] += 1
            
            # Actualizar tiempos
            metrics["total_execution_time"] += result.execution_time
            metrics["average_execution_time"] = (
                metrics["total_execution_time"] / metrics["total_executions"]
            )
            
            # Actualizar por tipo de acción
            action = instruction.action
            if action not in metrics["actions"]:
                metrics["actions"][action] = {"total": 0, "successful": 0, "failed": 0}
            
            metrics["actions"][action]["total"] += 1
            if result.success:
                metrics["actions"][action]["successful"] += 1
            else:
                metrics["actions"][action]["failed"] += 1
            
            # Actualizar por prioridad
            priority = instruction.priority
            if priority not in metrics["priorities"]:
                metrics["priorities"][priority] = {"total": 0, "successful": 0, "failed": 0}
            
            metrics["priorities"][priority]["total"] += 1
            if result.success:
                metrics["priorities"][priority]["successful"] += 1
            else:
                metrics["priorities"][priority]["failed"] += 1
            
            # Calcular tasa de éxito
            metrics["success_rate"] = (
                metrics["successful_executions"] / metrics["total_executions"] * 100
            )
            
            # Actualizar timestamp
            metrics["last_updated"] = datetime.now().isoformat()
            
            # Guardar métricas
            self._save_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Error actualizando métricas: {e}")
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Cargar métricas existentes"""
        if self.metrics_path.exists():
            try:
                with open(self.metrics_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error cargando métricas: {e}")
        
        # Métricas iniciales
        return {
            "project_path": str(self.project_path),
            "created_at": datetime.now().isoformat(),
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "success_rate": 0.0,
            "total_execution_time": 0.0,
            "average_execution_time": 0.0,
            "actions": {},
            "priorities": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Guardar métricas"""
        with open(self.metrics_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    def _process_successful_changes(self, result: ExecutionResult, instruction: CursorInstruction) -> None:
        """Procesar cambios exitosos"""
        logger.info(f"Procesando cambios exitosos: {len(result.changes_made)} cambios")
        
        # Verificar si se necesita actualizar documentación
        if instruction.action in ["add_documentation", "improve_code_quality"]:
            self._update_documentation_references(instruction)
        
        # Verificar si se movieron archivos
        if instruction.action == "move_file":
            self._update_file_references(instruction, result)
    
    def _process_failed_execution(self, result: ExecutionResult, instruction: CursorInstruction) -> None:
        """Procesar ejecución fallida"""
        logger.warning(f"Ejecución fallida: {result.error}")
        
        # Crear entrada de error en bitácora
        error_entry = f"""
### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ⚠️ Error en aplicación automática

**Instrucción**: {instruction.action}
**Archivo**: {instruction.target}
**Error**: {result.error}

**Acción requerida**: Revisión manual necesaria
"""
        
        try:
            with open(self.bitacora_path, 'a', encoding='utf-8') as f:
                f.write(error_entry)
        except Exception as e:
            logger.error(f"Error añadiendo entrada de error a bitácora: {e}")
    
    def _update_documentation_references(self, instruction: CursorInstruction) -> None:
        """Actualizar referencias de documentación"""
        # Esta funcionalidad se puede expandir para actualizar
        # referencias cruzadas en documentación
        logger.debug("Actualizando referencias de documentación")
    
    def _update_file_references(self, instruction: CursorInstruction, result: ExecutionResult) -> None:
        """Actualizar referencias de archivos movidos"""
        # Esta funcionalidad se puede expandir para actualizar
        # imports y referencias en otros archivos
        logger.debug("Actualizando referencias de archivos")
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Obtener resumen de feedback procesado"""
        if not self.feedback_log:
            return {"message": "No hay feedback procesado aún"}
        
        total_feedback = len(self.feedback_log)
        successful_feedback = len([f for f in self.feedback_log if f["success"]])
        failed_feedback = total_feedback - successful_feedback
        
        return {
            "total_feedback_entries": total_feedback,
            "successful_entries": successful_feedback,
            "failed_entries": failed_feedback,
            "success_rate": (successful_feedback / total_feedback * 100) if total_feedback > 0 else 0,
            "last_processed": self.feedback_log[-1]["timestamp"] if self.feedback_log else None
        }
    
    def save_feedback_log(self, output_path: str = None) -> str:
        """Guardar log de feedback"""
        if not output_path:
            output_path = self.project_path / "CURSOR_FEEDBACK_LOG.json"
        
        log_data = {
            "project_path": str(self.project_path),
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_feedback_summary(),
            "feedback_entries": self.feedback_log
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Log de feedback guardado en: {output_path}")
        return str(output_path)
    
    def generate_improvement_report(self) -> str:
        """Generar reporte de mejoras basado en feedback"""
        if not self.feedback_log:
            return "No hay datos suficientes para generar reporte de mejoras"
        
        # Analizar patrones en el feedback
        action_stats = {}
        priority_stats = {}
        
        for entry in self.feedback_log:
            action = entry["instruction"]["action"]
            priority = entry["instruction"]["priority"]
            
            if action not in action_stats:
                action_stats[action] = {"total": 0, "successful": 0}
            action_stats[action]["total"] += 1
            if entry["success"]:
                action_stats[action]["successful"] += 1
            
            if priority not in priority_stats:
                priority_stats[priority] = {"total": 0, "successful": 0}
            priority_stats[priority]["total"] += 1
            if entry["success"]:
                priority_stats[priority]["successful"] += 1
        
        # Generar reporte
        report = f"""# Reporte de Mejoras - {self.project_path.name}

**Generado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Período**: {len(self.feedback_log)} ejecuciones procesadas

## Resumen General
- **Total de ejecuciones**: {len(self.feedback_log)}
- **Exitosas**: {len([f for f in self.feedback_log if f['success']])}
- **Fallidas**: {len([f for f in self.feedback_log if not f['success']])}

## Estadísticas por Acción
"""
        
        for action, stats in action_stats.items():
            success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
            report += f"- **{action}**: {stats['successful']}/{stats['total']} ({success_rate:.1f}% éxito)\n"
        
        report += "\n## Estadísticas por Prioridad\n"
        for priority, stats in priority_stats.items():
            success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
            report += f"- **{priority}**: {stats['successful']}/{stats['total']} ({success_rate:.1f}% éxito)\n"
        
        report += "\n## Recomendaciones\n"
        
        # Generar recomendaciones basadas en estadísticas
        for action, stats in action_stats.items():
            success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
            if success_rate < 70:
                report += f"- Revisar proceso de {action}: {success_rate:.1f}% de éxito\n"
        
        return report
