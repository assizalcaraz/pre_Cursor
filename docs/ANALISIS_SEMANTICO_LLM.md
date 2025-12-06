# Análisis Semántico con LLM

**Fecha**: 2025-12-06  
**Proyecto**: pre_cursor

---

## 🎯 Objetivo

El sistema de procesamiento de documentación ahora utiliza **análisis semántico con LLM** (a través de Cursor CLI) para evaluar si los documentos temporales realmente aportan valor antes de moverlos a la documentación oficial.

---

## 🤖 Cómo Funciona

### Flujo de Evaluación

1. **Filtro Básico** (primera capa):
   - Verificación rápida de tamaño, estructura básica
   - Detección de archivos de prueba/borradores obvios
   - Si falla este filtro, no se usa LLM (ahorro de recursos)

2. **Análisis Semántico con LLM** (segunda capa):
   - El documento pasa al LLM con contexto completo
   - Se incluye documentación existente en el destino
   - El LLM evalúa:
     - ¿Aporta información valiosa?
     - ¿Es redundante con documentación existente?
     - ¿Está completo y listo para ser oficial?

3. **Decisión Final**:
   - Basada en evaluación semántica del LLM
   - Solo se mueven documentos que realmente aportan valor

---

## 📋 Prompt del LLM

El sistema envía al LLM:

### Documento a Evaluar
- Nombre, título, líneas, secciones
- Contenido completo del documento

### Contexto
- Documentación existente en el destino propuesto
- Resúmenes de documentos relacionados (hasta 5 documentos)

### Instrucciones
1. Evaluar si aporta información valiosa
2. Verificar redundancia con documentación existente
3. Determinar si está completo y listo

### Respuesta Esperada (JSON)

```json
{
    "is_valuable": true/false,
    "score": 0.0-1.0,
    "should_move": true/false,
    "redundancy_level": "none" | "low" | "medium" | "high",
    "reasons": ["razón 1", "razón 2"],
    "suggestions": ["sugerencia 1", "sugerencia 2"],
    "summary": "Resumen breve del análisis"
}
```

---

## 🔧 Uso

### Habilitado por Defecto

```bash
# Análisis semántico habilitado automáticamente
pre-cursor docs process -p
```

### Deshabilitar Análisis LLM

```bash
# Usar solo evaluación básica (más rápido)
pre-cursor docs process -p --no-llm
```

### Modo Verbose

```bash
# Ver detalles del análisis semántico
pre-cursor docs process -p --verbose
```

---

## 📊 Ventajas del Análisis Semántico

### Antes (Solo Evaluación Básica)

❌ **Problemas**:
- Solo contaba líneas y caracteres
- Detectaba palabras clave simples
- No entendía el contexto real
- Movía documentos sin valor real

**Ejemplo**: `juce_wrapper.md` con solo "esto es un manual de juce" → Se movía incorrectamente

### Ahora (Con Análisis Semántico)

✅ **Mejoras**:
- Entiende el contenido real del documento
- Compara con documentación existente
- Detecta redundancia semántica (no solo textual)
- Evalúa si aporta información nueva
- Determina si está completo y listo

**Ejemplo**: `juce_wrapper.md` → LLM detecta que es solo un placeholder → Rechazado correctamente

---

## 🔍 Ejemplo de Análisis

### Documento: `juce_wrapper.md`

**Contenido**: "esto es un manual de juce"

**Análisis LLM**:
```json
{
    "is_valuable": false,
    "score": 0.1,
    "should_move": false,
    "redundancy_level": "none",
    "reasons": [
        "Contenido extremadamente breve, solo una frase",
        "Parece ser un placeholder o borrador",
        "No aporta información técnica sustancial",
        "No tiene estructura ni contenido útil"
    ],
    "suggestions": [
        "Expandir con información real sobre JUCE wrapper",
        "Agregar ejemplos de código",
        "Incluir documentación técnica completa"
    ],
    "summary": "Documento de prueba/placeholder sin contenido útil"
}
```

**Decisión**: ❌ **Rechazado** - No se mueve

---

## ⚙️ Requisitos

### Cursor Agent CLI

El análisis semántico requiere `cursor-agent` CLI disponible:

```bash
# Verificar disponibilidad
cursor-agent --version
```

Si no está disponible:
- El sistema usa automáticamente evaluación básica
- Se muestra advertencia en logs
- El procesamiento continúa normalmente

### Configuración

El análisis LLM se habilita automáticamente si:
- ✅ `cursor-agent` está disponible
- ✅ No se usa flag `--no-llm`
- ✅ El documento pasa el filtro básico

---

## 📈 Estadísticas

El sistema reporta:

- **Analizados**: Total de documentos procesados
- **Evaluados con LLM**: Documentos analizados semánticamente
- **Movidos**: Documentos que pasaron evaluación
- **Omitidos**: Documentos rechazados
- **Errores**: Errores durante procesamiento

---

## 🔄 Fallback Automático

Si el análisis LLM falla:

1. **Timeout**: Se usa evaluación básica
2. **Error de conexión**: Se usa evaluación básica
3. **Error de parsing**: Se usa evaluación básica
4. **cursor-agent no disponible**: Se usa evaluación básica

El sistema **siempre** puede procesar documentos, incluso sin LLM.

---

## 💡 Mejores Prácticas

### Para Desarrolladores

1. **Escribir documentación completa**:
   - Mínimo 10 líneas de contenido útil
   - Estructura clara con secciones
   - Información técnica sustancial

2. **Evitar placeholders**:
   - No crear documentos con solo "esto es un..."
   - Completar borradores antes de ponerlos en `temp/`
   - O eliminarlos si no son necesarios

3. **Revisar sugerencias del LLM**:
   - Si un documento es rechazado, revisar las sugerencias
   - Mejorar el documento según las recomendaciones
   - Reintentar después de mejoras

### Para Agentes de IA

1. **Crear documentación sustancial**:
   - Mínimo 200 caracteres de contenido útil
   - Incluir información técnica real
   - Estructurar con secciones apropiadas

2. **Evitar documentos de prueba**:
   - No crear documentos solo para probar el sistema
   - Completar documentación antes de ponerla en `temp/`
   - Usar nombres descriptivos, no "test", "prueba", etc.

---

## 🔗 Referencias

- [Sistema de Evaluación de Calidad](SISTEMA_EVALUACION_CALIDAD.md)
- [Evaluación de Clasificación](EVALUACION_CLASIFICACION.md)
- [Guía de pre_cursor](GUIA_PRE_CURSOR_DOCS.md)

---

**Última actualización**: 2025-12-06

