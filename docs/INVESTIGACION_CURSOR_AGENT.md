# Investigación: cursor-agent API

**Fecha**: 2025-12-06  
**Objetivo**: Entender cómo usar `cursor-agent` correctamente para análisis semántico de documentación

---

## 🔍 Descubrimientos

### 1. cursor-agent es un Wrapper

`cursor-agent` es un **wrapper bash** ubicado en `pre_cursor/cursor-agent` que actúa como interfaz para `agent-cli`.

### 2. Comandos Disponibles

Según el wrapper, `cursor-agent` tiene estos comandos:

```bash
cursor-agent [OPTIONS] COMMAND [ARGS]...

Commands:
  analyze_test    Analyze test files using LLM
  fix_code        Fix code issues using LLM
  refactor        Refactor code using LLM
  --version       Show version
  --help          Show this help
```

### 3. Implementación del Wrapper

El wrapper usa `agent-cli chat` bajo el capó:

```bash
# analyze_test
agent-cli chat "Please analyze this test file and provide feedback..."

# fix_code
agent-cli chat "Please review and fix any issues in this code file..."

# refactor
agent-cli chat "Please refactor this code to improve..."
```

### 4. Problema Identificado

**El código actual intenta usar**:
```python
cmd = ['cursor-agent', '-p', prompt_file, '--output-format', 'json']
```

**Pero `cursor-agent` NO acepta**:
- `-p` como flag
- `--output-format` como flag
- Archivos de prompt directamente

**Solo acepta**:
- Comandos específicos: `analyze_test`, `fix_code`, `refactor`
- Cada comando requiere un archivo como argumento
- Usa `agent-cli chat` internamente

---

## 💡 Soluciones Posibles

### Opción 1: Crear Nuevo Comando en el Wrapper

Agregar un comando `analyze_documentation` al wrapper:

```bash
analyze_documentation() {
    local file_path="$1"
    if [ -z "$file_path" ]; then
        echo "Error: File path required for analyze_documentation"
        exit 1
    fi
    
    echo "Analyzing documentation: $file_path"
    # Leer el prompt del archivo y enviarlo a agent-cli
    agent-cli chat "$(cat "$file_path")"
}
```

**Ventajas**:
- ✅ Mantiene consistencia con otros comandos
- ✅ Fácil de implementar
- ✅ Reutiliza infraestructura existente

**Desventajas**:
- ⚠️ Requiere modificar el wrapper
- ⚠️ Depende de `agent-cli` estar disponible

### Opción 2: Usar `analyze_test` como Fallback

Usar el comando existente `analyze_test` pero adaptar el prompt:

```python
# Crear archivo temporal con el contenido del documento
temp_file = temp_dir / f"{doc_name}.md"
temp_file.write_text(doc_content)

# Usar analyze_test
cmd = ['cursor-agent', 'analyze_test', str(temp_file)]
```

**Ventajas**:
- ✅ No requiere modificar el wrapper
- ✅ Funciona inmediatamente

**Desventajas**:
- ⚠️ El comando está diseñado para tests, no documentación
- ⚠️ Puede no dar los mejores resultados

### Opción 3: Usar `agent-cli` Directamente

Si `agent-cli` está disponible, usarlo directamente:

```python
# Leer el prompt
prompt = prompt_file.read_text()

# Ejecutar agent-cli directamente
cmd = ['agent-cli', 'chat', prompt]
```

**Ventajas**:
- ✅ Más control sobre el formato
- ✅ No depende del wrapper

**Desventajas**:
- ⚠️ Requiere que `agent-cli` esté en PATH
- ⚠️ Bypassa el wrapper (puede ser inconsistente)

### Opción 4: Usar CursorAgentExecutor

El código ya tiene `CursorAgentExecutor` que intenta usar `cursor-agent`:

```python
result = self.cursor_agent._run_cursor_agent_command(prompt, instruction)
```

Pero este también intenta usar `-p` que no funciona.

---

## 🔧 Recomendación

### Solución Recomendada: Opción 1 + Opción 3 (Híbrida)

1. **Agregar comando `analyze_documentation` al wrapper**:
   - Mantiene consistencia
   - Fácil de usar desde Python

2. **Fallback a `agent-cli` directo**:
   - Si el wrapper no tiene el comando, usar `agent-cli` directamente
   - Más robusto

3. **Implementación**:

```python
def _execute_semantic_analysis(self, prompt: str) -> Dict:
    """Ejecutar análisis semántico usando Cursor Agent CLI."""
    try:
        # Crear archivo temporal con el prompt
        temp_prompt_file = self.project_root / '.cursor' / 'temp_analysis_prompt.md'
        temp_prompt_file.parent.mkdir(parents=True, exist_ok=True)
        temp_prompt_file.write_text(prompt)
        
        # Intentar 1: cursor-agent analyze_documentation (si existe)
        # Intentar 2: agent-cli chat (directo)
        # Intentar 3: cursor-agent analyze_test (fallback)
        
        for attempt in [
            (['cursor-agent', 'analyze_documentation', str(temp_prompt_file)], 'analyze_documentation'),
            (['agent-cli', 'chat', prompt], 'agent-cli direct'),
            (['cursor-agent', 'analyze_test', str(temp_prompt_file)], 'analyze_test fallback')
        ]:
            cmd, method = attempt
            try:
                result = subprocess.run(
                    cmd,
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    return {
                        'success': True,
                        'raw_output': result.stdout,
                        'method': method
                    }
            except FileNotFoundError:
                continue
        
        return {'success': False, 'error': 'No method available'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

---

## 📋 Pasos de Implementación

### Paso 1: Agregar Comando al Wrapper

Modificar `pre_cursor/cursor-agent`:

```bash
analyze_documentation)
    analyze_documentation "$2"
    ;;
```

Y agregar la función:

```bash
analyze_documentation() {
    local file_path="$1"
    if [ -z "$file_path" ]; then
        echo "Error: File path required for analyze_documentation"
        exit 1
    fi
    
    # Leer el prompt del archivo
    local prompt=$(cat "$file_path")
    
    # Enviar a agent-cli
    agent-cli chat "$prompt"
}
```

### Paso 2: Actualizar Código Python

Modificar `_execute_semantic_analysis` para usar el nuevo comando o fallbacks.

### Paso 3: Probar

Probar con documentos reales para verificar que funciona.

---

## 🔍 Verificaciones Necesarias

1. **¿Está `agent-cli` disponible?**
   ```bash
   which agent-cli
   ```

2. **¿Está `cursor-agent` en PATH?**
   ```bash
   which cursor-agent
   ```

3. **¿Funciona `agent-cli chat`?**
   ```bash
   agent-cli chat "test prompt"
   ```

---

## 📝 Notas

- El wrapper actual está en `pre_cursor/cursor-agent` (script bash)
- Usa `agent-cli` bajo el capó
- Los comandos actuales están diseñados para código/tests, no documentación
- Necesitamos un comando específico para análisis de documentación

---

## 🔗 Referencias

- [Wrapper cursor-agent](../../pre_cursor/cursor-agent)
- [CursorAgentExecutor](../../pre_cursor/src/pre_cursor/cursor_agent_executor.py)
- [Test Validator](../../pre_cursor/src/pre_cursor/test_validator.py)

---

**Última actualización**: 2025-12-06

---

## ✅ Commit Realizado

**Repositorio**: `pre_cursor`  
**Branch**: `master`  
**Commit Hash**: `a111661`  
**Mensaje**: `FEAT: Sistema de gestión de documentación con análisis semántico LLM`

**Estado**: ✅ Pusheado a `origin/master`

