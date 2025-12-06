#!/usr/bin/env python3
"""
Gestor de Documentación para Pre-Cursor

Este módulo proporciona funcionalidades para gestionar documentación de proyectos:
- Procesamiento de documentación temporal
- Reorganización de documentación
- Gestión de cron jobs para procesamiento automático
"""

import os
import sys
import logging
import hashlib
import re
import shutil
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Intentar importar CursorAgentExecutor para análisis semántico
try:
    from .cursor_agent_executor import CursorAgentExecutor
    CURSOR_AGENT_AVAILABLE = True
except ImportError:
    CURSOR_AGENT_AVAILABLE = False
    logger.warning("CursorAgentExecutor no disponible - análisis semántico deshabilitado")


class DocumentationProcessor:
    """Procesador de documentación con análisis de redundancia e incompatibilidad."""
    
    def __init__(self, project_root: Path, dry_run: bool = False, verbose: bool = False, use_llm: bool = True):
        project_root = Path(project_root).resolve()
        
        # Detectar si el path dado ya es un subdirectorio de docs
        # Si estamos en docs/temp/, docs/juce/, etc., subir hasta la raíz del proyecto
        if project_root.name in ['temp', 'legacy', 'juce']:
            # Estamos en un subdirectorio de docs, subir dos niveles
            if project_root.parent.name == 'docs':
                self.project_root = project_root.parent.parent
            else:
                # No estamos en estructura esperada, asumir que es la raíz
                self.project_root = project_root
        elif project_root.name == 'docs':
            # Estamos en docs/, subir un nivel
            self.project_root = project_root.parent
        else:
            # Asumir que es la raíz del proyecto
            self.project_root = project_root
        
        if verbose:
            logger.info(f"Project root detectado: {self.project_root}")
            logger.info(f"Temp dir será: {self.project_root / 'docs' / 'temp'}")
        
        self.dry_run = dry_run
        self.verbose = verbose
        self.use_llm = use_llm and CURSOR_AGENT_AVAILABLE
        self.docs_root = self.project_root / 'docs'
        self.temp_dir = self.docs_root / 'temp'
        self.official_dir = self.docs_root
        self.legacy_dir = self.docs_root / 'legacy'
        self.juce_dir = self.docs_root / 'juce'
        
        # Inicializar CursorAgentExecutor para análisis semántico
        if self.use_llm:
            try:
                from .cursor_agent_executor import CursorAgentExecutor
                self.cursor_agent = CursorAgentExecutor(str(self.project_root))
                if not self.cursor_agent.agent_available:
                    logger.warning("Cursor Agent CLI no disponible - usando análisis básico")
                    self.use_llm = False
            except Exception as e:
                logger.warning(f"Error inicializando Cursor Agent: {e} - usando análisis básico")
                self.use_llm = False
        else:
            self.cursor_agent = None
        
        # Estadísticas
        self.stats = {
            'analyzed': 0,
            'moved': 0,
            'merged': 0,
            'skipped': 0,
            'errors': 0,
            'llm_evaluated': 0
        }
    
    def analyze_document(self, file_path: Path) -> Optional[Dict]:
        """Analizar un documento y extraer metadatos."""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            metadata = {
                'path': file_path,
                'name': file_path.name,
                'size': file_path.stat().st_size,
                'hash': hashlib.md5(content.encode()).hexdigest(),
                'lines': len(content.splitlines()),
                'title': self._extract_title(content),
                'sections': self._extract_sections(content),
                'references': self._extract_references(content),
                'last_modified': file_path.stat().st_mtime
            }
            
            return metadata
        except Exception as e:
            logger.error(f"Error analizando {file_path}: {e}")
            self.stats['errors'] += 1
            return None
    
    def _extract_title(self, content: str) -> str:
        """Extraer título del documento."""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Sin título"
    
    def _extract_sections(self, content: str) -> List[str]:
        """Extraer secciones del documento."""
        sections = []
        for match in re.finditer(r'^##+\s+(.+)$', content, re.MULTILINE):
            sections.append(match.group(1).strip())
        return sections
    
    def _extract_references(self, content: str) -> List[str]:
        """Extraer referencias a otros documentos."""
        references = []
        for match in re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content):
            references.append(match.group(2))
        return references
    
    def evaluate_content_semantic(self, temp_doc: Dict, official_docs: List[Dict], destination: Path) -> Dict:
        """
        Evaluar semánticamente el documento usando LLM.
        
        Args:
            temp_doc: Metadatos del documento temporal
            official_docs: Lista de documentos oficiales en el destino
            destination: Directorio de destino propuesto
            
        Returns:
            Dict con evaluación semántica: {
                'is_valuable': bool,
                'score': float (0-1),
                'reasons': List[str],
                'should_move': bool,
                'redundancy_level': str,
                'suggestions': List[str]
            }
        """
        if not self.use_llm or not self.cursor_agent:
            # Fallback a evaluación básica
            return self.evaluate_content_quality(temp_doc)
        
        try:
            self.stats['llm_evaluated'] += 1
            
            # Leer contenido del documento temporal
            temp_content = temp_doc['path'].read_text(encoding='utf-8')
            
            # Obtener contexto de documentación oficial en el destino
            context_docs = []
            if destination.exists():
                for doc_file in destination.glob('*.md'):
                    if doc_file.name != 'README.md':
                        try:
                            context_content = doc_file.read_text(encoding='utf-8')
                            context_docs.append({
                                'name': doc_file.name,
                                'content': context_content[:2000]  # Limitar tamaño para contexto
                            })
                        except Exception:
                            continue
            
            # Crear prompt para análisis semántico
            prompt = self._create_semantic_analysis_prompt(
                temp_doc, temp_content, context_docs, destination.name
            )
            
            # Ejecutar análisis con Cursor Agent CLI
            result = self._execute_semantic_analysis(prompt)
            
            if result.get('success'):
                return self._parse_semantic_result(result, temp_doc)
            else:
                # Fallback a evaluación básica si LLM falla
                logger.warning("Análisis LLM falló, usando evaluación básica")
                return self.evaluate_content_quality(temp_doc)
                
        except Exception as e:
            logger.error(f"Error en análisis semántico: {e}")
            # Fallback a evaluación básica
            return self.evaluate_content_quality(temp_doc)
    
    def _create_semantic_analysis_prompt(self, temp_doc: Dict, temp_content: str, 
                                         context_docs: List[Dict], destination_name: str) -> str:
        """Crear prompt para análisis semántico con LLM."""
        
        context_summary = ""
        if context_docs:
            context_summary = "\n\n## Documentación Existente en el Destino:\n\n"
            for ctx_doc in context_docs[:5]:  # Limitar a 5 documentos para no exceder contexto
                context_summary += f"### {ctx_doc['name']}\n"
                context_summary += f"{ctx_doc['content'][:500]}...\n\n"
        else:
            context_summary = "\n\n(No hay documentación existente en el destino)\n"
        
        prompt = f"""Evalúa semánticamente el siguiente documento de documentación temporal y determina si debe moverse a la documentación oficial.

## Documento a Evaluar

**Nombre**: {temp_doc['name']}
**Título**: {temp_doc['title']}
**Líneas**: {temp_doc['lines']}
**Secciones**: {len(temp_doc['sections'])}

**Contenido**:
```markdown
{temp_content}
```

## Contexto

**Destino propuesto**: {destination_name}/
{context_summary}

## Instrucciones de Evaluación

Analiza el documento y determina:

1. **¿Aporta información valiosa?**
   - ¿Tiene contenido sustancial y útil?
   - ¿Es solo un borrador, prueba o placeholder?
   - ¿Tiene información nueva o es redundante?

2. **¿Es redundante con documentación existente?**
   - Compara con la documentación existente en el destino
   - ¿Aporta información nueva o solo repite lo existente?
   - ¿Complementa o duplica información?

3. **¿Está completo y listo para documentación oficial?**
   - ¿Es un borrador que necesita más trabajo?
   - ¿Está completo y bien estructurado?
   - ¿Requiere revisión antes de ser oficial?

## Formato de Respuesta (JSON)

Responde ÚNICAMENTE en formato JSON válido:

{{
    "is_valuable": true/false,
    "score": 0.0-1.0,
    "should_move": true/false,
    "redundancy_level": "none" | "low" | "medium" | "high",
    "reasons": [
        "razón 1",
        "razón 2"
    ],
    "suggestions": [
        "sugerencia 1",
        "sugerencia 2"
    ],
    "summary": "Resumen breve del análisis"
}}

## Análisis:"""
        
        return prompt
    
    def _execute_semantic_analysis(self, prompt: str) -> Dict:
        """Ejecutar análisis semántico usando Cursor Agent CLI."""
        try:
            # Ejecutar directamente con cursor-agent CLI
            import subprocess
            
            # Crear archivo temporal con el prompt
            temp_prompt_file = self.project_root / '.cursor' / 'temp_analysis_prompt.md'
            temp_prompt_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(temp_prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            # Intentar diferentes formas de ejecutar Cursor CLI
            # Opción 1: cursor-agent (si existe)
            # Opción 2: Usar Cursor directamente con prompt file
            # Opción 3: Usar CursorAgentExecutor si está disponible
            
            # Intentar diferentes métodos de ejecución
            # Opción 1: cursor-agent analyze_documentation (nuevo comando)
            # Opción 2: agent-cli chat (directo)
            # Opción 3: cursor-agent analyze_test (fallback)
            
            methods_to_try = [
                (['cursor-agent', 'analyze_documentation', str(temp_prompt_file)], 'cursor-agent analyze_documentation', False),
                (['cursor-agent', 'analyze_test', str(temp_prompt_file)], 'cursor-agent analyze_test (fallback)', False),
                # agent-cli puede necesitar el prompt de otra forma, intentar con archivo también
                (['agent-cli', 'chat'], 'agent-cli direct', True)  # True = usar stdin
            ]
            
            cmd = None
            method_name = None
            use_stdin = False
            
            for cmd_to_try, method, stdin_flag in methods_to_try:
                try:
                    # Verificar si el primer comando existe
                    check_cmd = cmd_to_try[0]
                    check_result = subprocess.run(
                        [check_cmd, '--version'] if check_cmd in ['cursor-agent'] else [check_cmd, '--help'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    # Si el comando existe (o al menos no es FileNotFoundError)
                    cmd = cmd_to_try
                    method_name = method
                    use_stdin = stdin_flag
                    logger.debug(f"Usando método: {method}")
                    break
                except FileNotFoundError:
                    continue
                except Exception:
                    # Si el comando existe pero falla la verificación, intentar usarlo de todas formas
                    cmd = cmd_to_try
                    method_name = method
                    use_stdin = stdin_flag
                    logger.debug(f"Usando método (sin verificación): {method}")
                    break
            
            if not cmd:
                logger.warning("No se encontró cursor-agent ni agent-cli en PATH")
                # Limpiar archivo temporal
                try:
                    temp_prompt_file.unlink()
                except Exception:
                    pass
                return {'success': False, 'error': 'cursor-agent/agent-cli no disponible'}
            
            logger.debug(f"Ejecutando análisis semántico ({method_name}): {' '.join(cmd)}")
            
            # Ejecutar comando
            if use_stdin:
                # Para agent-cli, enviar prompt como stdin
                result = subprocess.run(
                    cmd,
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=120,
                    input=prompt
                )
            else:
                # Para otros métodos, el archivo contiene el prompt
                result = subprocess.run(
                    cmd,
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minutos timeout para análisis
                )
            
            # Limpiar archivo temporal
            try:
                temp_prompt_file.unlink()
            except Exception:
                pass
            
            if result.returncode == 0:
                # Verificar que la salida no esté vacía
                output = result.stdout.strip()
                if not output:
                    logger.warning(f"{method_name} ejecutó pero no devolvió salida")
                    return {
                        'success': False,
                        'error': f'No output from {method_name}',
                        'raw_output': ''
                    }
                return {
                    'success': True,
                    'raw_output': output,
                    'raw_stderr': result.stderr,
                    'method': method_name
                }
            else:
                error_msg = (result.stderr.strip() or result.stdout.strip() or "Error desconocido")[:200]
                logger.warning(f"Cursor Agent CLI falló (code {result.returncode}): {error_msg}")
                if self.verbose:
                    logger.debug(f"Comando ejecutado: {' '.join(cmd)}")
                    logger.debug(f"Return code: {result.returncode}")
                    if result.stdout:
                        logger.debug(f"Stdout: {result.stdout[:500]}")
                    if result.stderr:
                        logger.debug(f"Stderr: {result.stderr[:500]}")
                return {
                    'success': False,
                    'error': error_msg,
                    'raw_output': result.stdout
                }
            
        except FileNotFoundError:
            logger.warning("cursor-agent no encontrado en PATH")
            return {'success': False, 'error': 'cursor-agent no disponible'}
        except subprocess.TimeoutExpired:
            logger.warning("Timeout en análisis semántico (120s)")
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            logger.error(f"Error ejecutando análisis semántico: {e}")
            if self.verbose:
                import traceback
                logger.debug(traceback.format_exc())
            return {'success': False, 'error': str(e)}
    
    def _parse_semantic_result(self, result: Dict, temp_doc: Dict) -> Dict:
        """Parsear resultado del análisis semántico."""
        try:
            output = result.get('raw_output', '')
            
            # Intentar extraer JSON de la respuesta
            # El LLM puede devolver texto con JSON embebido
            json_match = re.search(r'\{[^{}]*"is_valuable"[^{}]*\}', output, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                analysis = json.loads(json_str)
            else:
                # Intentar parsear todo el output como JSON
                analysis = json.loads(output)
            
            # Validar y normalizar resultado
            return {
                'is_valuable': analysis.get('is_valuable', False),
                'score': float(analysis.get('score', 0.0)),
                'should_move': analysis.get('should_move', False),
                'redundancy_level': analysis.get('redundancy_level', 'unknown'),
                'reasons': analysis.get('reasons', []),
                'suggestions': analysis.get('suggestions', []),
                'summary': analysis.get('summary', ''),
                'method': 'semantic_llm'
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando resultado LLM: {e}")
            logger.debug(f"Output recibido: {output[:500]}")
            # Fallback a evaluación básica
            return self.evaluate_content_quality(temp_doc)
        except Exception as e:
            logger.error(f"Error procesando resultado semántico: {e}")
            return self.evaluate_content_quality(temp_doc)
    
    def evaluate_content_quality(self, doc_metadata: Dict) -> Dict:
        """
        Evaluar la calidad y utilidad del contenido del documento.
        
        Returns:
            Dict con evaluación: {
                'is_valuable': bool,
                'score': float (0-1),
                'reasons': List[str],
                'should_move': bool
            }
        """
        reasons = []
        score = 1.0
        is_valuable = True
        
        # Criterios de evaluación
        content = doc_metadata['path'].read_text(encoding='utf-8')
        lines = doc_metadata['lines']
        sections = len(doc_metadata['sections'])
        
        # 1. Tamaño mínimo (al menos 10 líneas de contenido real)
        if lines < 10:
            score -= 0.3
            reasons.append(f"Documento muy corto ({lines} líneas)")
            if lines < 5:
                is_valuable = False
                reasons.append("Demasiado corto para ser útil")
        
        # 2. Contenido mínimo (al menos 200 caracteres)
        content_length = len(content.strip())
        if content_length < 200:
            score -= 0.2
            reasons.append(f"Contenido muy breve ({content_length} caracteres)")
            if content_length < 100:
                is_valuable = False
                reasons.append("Contenido insuficiente")
        
        # 3. Secciones (al menos 2 secciones para documentos estructurados)
        if sections == 0 and lines > 5:
            score -= 0.2
            reasons.append("Sin estructura de secciones")
        
        # 4. Detectar borradores/pruebas
        content_lower = content.lower()
        test_indicators = [
            'esto es un', 'test', 'prueba', 'borrador', 'draft',
            'temporal', 'temp', 'xxx', 'zzz', 'asdf'
        ]
        if any(indicator in content_lower[:200] for indicator in test_indicators):
            if lines < 10:
                is_valuable = False
                score = 0.0
                reasons.append("Parece ser un archivo de prueba/borrador")
        
        # 5. Contenido vacío o solo espacios
        if not content.strip() or len(content.strip()) < 50:
            is_valuable = False
            score = 0.0
            reasons.append("Contenido vacío o casi vacío")
        
        should_move = is_valuable and score >= 0.5
        
        return {
            'is_valuable': is_valuable,
            'score': max(0.0, min(1.0, score)),
            'reasons': reasons,
            'should_move': should_move
        }
    
    def find_redundancy(self, temp_doc: Dict, official_docs: List[Dict]) -> List[Dict]:
        """Encontrar documentos oficiales que pueden ser redundantes con el temporal."""
        redundant = []
        
        temp_content = temp_doc['path'].read_text(encoding='utf-8').lower()
        
        for official in official_docs:
            # Comparar por nombre exacto
            if official['name'].lower() == temp_doc['name'].lower():
                redundant.append(official)
                continue
            
            # Comparar por título
            if official['title'].lower() == temp_doc['title'].lower():
                redundant.append(official)
                continue
            
            # Comparar contenido (similitud de texto)
            official_content = official.get('content', '').lower()
            if official_content:
                # Calcular similitud básica
                temp_words = set(temp_content.split())
                official_words = set(official_content.split())
                
                if len(temp_words) > 0 and len(official_words) > 0:
                    similarity = len(temp_words & official_words) / len(temp_words | official_words)
                    if similarity > 0.7:  # 70% de similitud
                        redundant.append(official)
                        continue
            
            # Comparar por secciones
            temp_sections = set(s.lower() for s in temp_doc['sections'])
            official_sections = set(s.lower() for s in official['sections'])
            
            if len(temp_sections) > 0 and len(official_sections) > 0:
                section_overlap = len(temp_sections & official_sections) / len(temp_sections)
                if section_overlap > 0.5:
                    redundant.append(official)
        
        return redundant
    
    def determine_destination(self, doc_metadata: Dict) -> Path:
        """Determinar destino del documento basado en su contenido."""
        name = doc_metadata['name'].lower()
        content = doc_metadata['path'].read_text(encoding='utf-8').lower()
        
        # JUCE/C++ related
        if any(keyword in name or keyword in content for keyword in 
               ['juce', 'c++', 'cpp', 'refactorizacion', 'migracion']):
            return self.juce_dir
        
        # Legacy/Python related
        if any(keyword in name or keyword in content for keyword in 
               ['python', 'flask', 'legacy', 'bitacora', 'tutorial']):
            return self.legacy_dir
        
        # Default: official
        return self.official_dir
    
    def process_temp_documents(self):
        """Procesar todos los documentos en docs/temp/."""
        if not self.temp_dir.exists():
            logger.info(f"Directorio temporal no existe: {self.temp_dir}")
            return
        
        temp_files = list(self.temp_dir.glob('*.md'))
        
        # Excluir README.md de temp/ (es documentación explicativa, no temporal)
        temp_files = [f for f in temp_files if f.name != 'README.md']
        
        if not temp_files:
            logger.info("No hay documentos temporales para procesar")
            return
        
        logger.info(f"Procesando {len(temp_files)} documentos temporales...")
        
        # Analizar documentos oficiales
        official_docs = []
        for doc_dir in [self.official_dir, self.legacy_dir, self.juce_dir]:
            if doc_dir.exists():
                for md_file in doc_dir.glob('*.md'):
                    if md_file.name != 'README.md':
                        metadata = self.analyze_document(md_file)
                        if metadata:
                            metadata['content'] = md_file.read_text(encoding='utf-8')
                            official_docs.append(metadata)
        
        # Procesar cada documento temporal
        for temp_file in temp_files:
            self.stats['analyzed'] += 1
            logger.info(f"Analizando: {temp_file.name}")
            
            temp_metadata = self.analyze_document(temp_file)
            if not temp_metadata:
                self.stats['errors'] += 1
                continue
            
            # Variable de control para evitar contar múltiples veces el mismo archivo como skipped
            file_skipped = False
            
            # 1. Filtro rápido (evaluación básica)
            basic_quality = self.evaluate_content_quality(temp_metadata)
            
            # Si falla el filtro básico, no usar LLM (ahorro de recursos)
            if not basic_quality['is_valuable'] or basic_quality['score'] < 0.3:
                logger.warning(f"  ⚠️  Documento no cumple criterios básicos:")
                for reason in basic_quality['reasons']:
                    logger.warning(f"     - {reason}")
                logger.info(f"  ❌ Omitido (no se moverá)")
                if not file_skipped:
                    self.stats['skipped'] += 1
                    file_skipped = True
                continue
            
            # 2. Determinar destino propuesto
            destination = self.determine_destination(temp_metadata)
            
            # 3. Evaluación semántica con LLM (si está habilitada)
            if self.use_llm:
                logger.info(f"  🤖 Evaluando con LLM...")
                quality = self.evaluate_content_semantic(temp_metadata, official_docs, destination)
                if quality.get('method') == 'semantic_llm':
                    logger.info(f"  📊 Análisis semántico: {quality.get('summary', 'N/A')}")
                    if quality.get('redundancy_level'):
                        logger.info(f"  🔍 Redundancia: {quality['redundancy_level']}")
            else:
                # Usar evaluación básica
                quality = basic_quality
            
            if not quality['should_move']:
                logger.warning(f"  ⚠️  Documento no cumple criterios de calidad:")
                for reason in quality['reasons']:
                    logger.warning(f"     - {reason}")
                logger.info(f"  ❌ Omitido (no se moverá)")
                self.stats['skipped'] += 1
                continue
            
            if quality['score'] < 0.7:
                logger.warning(f"  ⚠️  Calidad baja (score: {quality['score']:.2f}):")
                for reason in quality['reasons']:
                    logger.warning(f"     - {reason}")
            
            # 4. Verificar redundancia (si no se hizo en análisis semántico)
            if quality.get('method') != 'semantic_llm' or quality.get('redundancy_level') == 'unknown':
                redundant = self.find_redundancy(temp_metadata, official_docs)
                if redundant:
                    logger.warning(f"  ⚠️  Redundancia detectada con: {[d['name'] for d in redundant]}")
                    # Si es muy redundante (>90% similitud), no mover
                    if len(redundant) > 0:
                        temp_content = temp_metadata['path'].read_text(encoding='utf-8').lower()
                        for red_doc in redundant:
                            red_content = red_doc.get('content', '').lower()
                            if red_content:
                                temp_words = set(temp_content.split())
                                red_words = set(red_content.split())
                                if len(temp_words) > 0:
                                    similarity = len(temp_words & red_words) / len(temp_words | red_words)
                                    if similarity > 0.9:
                                        logger.warning(f"  ❌ Muy redundante con {red_doc['name']} ({similarity*100:.1f}% similitud)")
                                        logger.info(f"  ❌ Omitido (redundancia alta)")
                                        if not file_skipped:
                                            self.stats['skipped'] += 1
                                            file_skipped = True
                                        continue
            else:
                # Usar resultado del análisis semántico
                redundancy_level = quality.get('redundancy_level', 'unknown')
                if redundancy_level in ['high']:
                    logger.warning(f"  ❌ Redundancia alta detectada por LLM")
                    logger.info(f"  ❌ Omitido (redundancia alta)")
                    if not file_skipped:
                        self.stats['skipped'] += 1
                        file_skipped = True
                    continue
            
            # 5. Verificar decisión final
            if not quality['should_move']:
                logger.warning(f"  ⚠️  Documento no cumple criterios de calidad:")
                for reason in quality['reasons']:
                    logger.warning(f"     - {reason}")
                logger.info(f"  ❌ Omitido (no se moverá)")
                if not file_skipped:
                    self.stats['skipped'] += 1
                    file_skipped = True
                continue
            
            destination_file = destination / temp_file.name
            
            # 6. Verificar si ya existe un archivo con el mismo nombre
            if destination_file.exists():
                # Comparar contenido
                existing_content = destination_file.read_text(encoding='utf-8')
                new_content = temp_metadata['path'].read_text(encoding='utf-8')
                
                if existing_content.strip() == new_content.strip():
                    logger.info(f"  ℹ️  Archivo idéntico ya existe en destino")
                    logger.info(f"  ❌ Omitido (sin cambios)")
                    # Solo contar si no fue ya contado por otra razón
                    if not file_skipped:
                        self.stats['skipped'] += 1
                        file_skipped = True
                    continue
                else:
                    # Renombrar con timestamp
                    timestamp = int(temp_metadata['last_modified'])
                    new_name = f"{temp_file.stem}_{timestamp}{temp_file.suffix}"
                    destination_file = destination / new_name
                    logger.info(f"  ℹ️  Archivo existe, renombrando a: {new_name}")
            
            # 5. Mover documento
            if not self.dry_run:
                destination.mkdir(parents=True, exist_ok=True)
                temp_file.rename(destination_file)
                logger.info(f"  ✅ Movido a: {destination_file.relative_to(self.project_root)}")
                if quality['score'] < 0.8:
                    logger.info(f"     ⚠️  Calidad: {quality['score']:.2f} - Revisar contenido")
                self.stats['moved'] += 1
            else:
                logger.info(f"  [DRY-RUN] Se movería a: {destination_file.relative_to(self.project_root)}")
                logger.info(f"     Calidad: {quality['score']:.2f}")
    
    def generate_report(self) -> Dict:
        """Generar reporte del procesamiento."""
        return self.stats


class CronManager:
    """Gestor de cron jobs para procesamiento de documentación."""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.script_path = self.project_root / 'scripts' / 'process_docs.py'
        self.cron_log = self.project_root / 'logs' / 'docs_processing.log'
        self.cron_identifier = f"{self.project_root.name}_docs_processing"
    
    def check_status(self) -> Dict:
        """Verificar estado del cron job."""
        try:
            crontab_output = subprocess.run(
                ['crontab', '-l'],
                capture_output=True,
                text=True,
                stderr=subprocess.DEVNULL
            )
            
            if self.cron_identifier in crontab_output.stdout:
                # Encontrar la línea del cron job
                for line in crontab_output.stdout.split('\n'):
                    if self.cron_identifier in line or str(self.script_path) in line:
                        return {
                            'installed': True,
                            'line': line.strip(),
                            'identifier': self.cron_identifier
                        }
            
            return {'installed': False}
        except subprocess.CalledProcessError:
            return {'installed': False}
        except Exception as e:
            logger.error(f"Error verificando cron: {e}")
            return {'installed': False, 'error': str(e)}
    
    def install(self, interval_hours: int = 6) -> bool:
        """Instalar cron job."""
        try:
            # Verificar si ya existe
            status = self.check_status()
            if status.get('installed'):
                logger.warning("Cron job ya está instalado")
                return False
            
            # Crear directorio de logs
            self.cron_log.parent.mkdir(parents=True, exist_ok=True)
            
            # Crear entrada de cron
            cron_comment = f"# {self.cron_identifier} - Procesamiento de documentación {self.project_root.name}"
            cron_schedule = f"0 */{interval_hours} * * *"
            cron_command = f"cd {self.project_root} && python3 {self.script_path} --verbose >> {self.cron_log} 2>&1"
            cron_job = f"{cron_comment}\n{cron_schedule} {cron_command}"
            
            # Obtener crontab actual
            try:
                current_crontab = subprocess.run(
                    ['crontab', '-l'],
                    capture_output=True,
                    text=True
                ).stdout
            except subprocess.CalledProcessError:
                current_crontab = ""
            
            # Agregar nuevo cron job
            new_crontab = current_crontab.rstrip() + "\n" + cron_job + "\n"
            
            # Instalar
            process = subprocess.Popen(
                ['crontab', '-'],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                logger.info("Cron job instalado exitosamente")
                return True
            else:
                logger.error("Error al instalar cron job")
                return False
                
        except Exception as e:
            logger.error(f"Error instalando cron: {e}")
            return False
    
    def remove(self) -> bool:
        """Eliminar cron job."""
        try:
            status = self.check_status()
            if not status.get('installed'):
                logger.warning("Cron job no está instalado")
                return False
            
            # Obtener crontab actual
            current_crontab = subprocess.run(
                ['crontab', '-l'],
                capture_output=True,
                text=True
            ).stdout
            
            # Eliminar líneas con el identificador
            new_lines = [
                line for line in current_crontab.split('\n')
                if self.cron_identifier not in line and str(self.script_path) not in line
            ]
            
            new_crontab = '\n'.join(new_lines) + '\n'
            
            # Instalar crontab actualizado
            process = subprocess.Popen(
                ['crontab', '-'],
                stdin=subprocess.PIPE,
                text=True
            )
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                logger.info("Cron job eliminado exitosamente")
                return True
            else:
                logger.error("Error al eliminar cron job")
                return False
                
        except Exception as e:
            logger.error(f"Error eliminando cron: {e}")
            return False

