# Sistema de Evaluación de Calidad de Documentación

**Fecha**: 2025-12-06  
**Proyecto**: pre_cursor

---

## 🎯 Objetivo

El sistema de procesamiento de documentación ahora **evalúa la calidad y utilidad** de cada documento antes de moverlo, evitando mover archivos que no aportan valor real.

---

## 📊 Criterios de Evaluación

### 1. Tamaño y Contenido Mínimo

**Criterios**:
- ✅ Mínimo 10 líneas de contenido real
- ✅ Mínimo 200 caracteres de texto
- ❌ Menos de 5 líneas → Rechazado automáticamente
- ❌ Menos de 100 caracteres → Rechazado automáticamente

**Razón**: Documentos muy cortos generalmente no aportan información útil.

### 2. Estructura

**Criterios**:
- ✅ Documentos estructurados deben tener al menos 2 secciones
- ⚠️ Documentos sin secciones pero con contenido sustancial pueden pasar

**Razón**: La estructura indica que el documento está pensado y organizado.

### 3. Detección de Borradores/Pruebas

**Indicadores de archivo de prueba**:
- Contiene frases como: "esto es un", "test", "prueba", "borrador", "draft"
- Nombres temporales: "xxx", "zzz", "asdf", "temp"
- Contenido muy breve con indicadores de prueba

**Acción**: Rechazado automáticamente si es claramente un archivo de prueba.

### 4. Redundancia con Documentación Existente

**Verificaciones**:
- ✅ Comparación por nombre exacto
- ✅ Comparación por título
- ✅ Comparación de contenido (similitud de texto)
- ✅ Comparación de secciones

**Umbrales**:
- **>90% similitud**: Rechazado (muy redundante)
- **70-90% similitud**: Advertencia pero se mueve
- **<70% similitud**: Aprobado

### 5. Archivos Idénticos

**Verificación**: Si el archivo ya existe en el destino con contenido idéntico, se omite.

---

## 🔢 Sistema de Puntuación

Cada documento recibe un **score de 0.0 a 1.0**:

- **1.0**: Documento perfecto
- **0.8-0.9**: Buena calidad
- **0.5-0.7**: Calidad aceptable (con advertencias)
- **<0.5**: Rechazado

### Descuentos por Criterios

- **-0.3**: Menos de 10 líneas
- **-0.2**: Menos de 200 caracteres
- **-0.2**: Sin estructura de secciones
- **-1.0**: Archivo de prueba/borrador (rechazado)

---

## ✅ Decisiones del Sistema

### Documento Aprobado (se mueve)

**Criterios**:
- ✅ Score >= 0.5
- ✅ is_valuable = True
- ✅ No es muy redundante (<90% similitud)
- ✅ No es idéntico a archivo existente

**Acción**: Se mueve al destino correspondiente.

### Documento Rechazado (no se mueve)

**Criterios**:
- ❌ Score < 0.5
- ❌ is_valuable = False
- ❌ Muy redundante (>90% similitud)
- ❌ Archivo de prueba/borrador
- ❌ Contenido vacío o casi vacío
- ❌ Idéntico a archivo existente

**Acción**: Se omite, permanece en `docs/temp/` o se puede eliminar manualmente.

### Documento con Advertencias (se mueve con advertencia)

**Criterios**:
- ⚠️ Score 0.5-0.7
- ⚠️ Calidad baja pero aceptable

**Acción**: Se mueve pero se marca para revisión.

---

## 📋 Ejemplo de Evaluación

### Caso: `juce_wrapper.md`

**Contenido**: "esto es un manual de juce"

**Evaluación**:
- ❌ Líneas: 1 (< 10) → -0.3
- ❌ Caracteres: ~25 (< 200) → -0.2
- ❌ Contiene "esto es un" → Archivo de prueba → -1.0
- ❌ Score final: 0.0
- ❌ is_valuable: False

**Decisión**: ❌ **Rechazado** - No se mueve

**Razones registradas**:
- "Documento muy corto (1 líneas)"
- "Contenido muy breve (25 caracteres)"
- "Parece ser un archivo de prueba/borrador"

---

## 🔍 Logging y Transparencia

El sistema registra:

1. **Análisis inicial**: Nombre del archivo
2. **Evaluación de calidad**: Score y razones
3. **Verificación de redundancia**: Documentos similares encontrados
4. **Decisión final**: Aprobado/Rechazado/Omitido
5. **Acción tomada**: Movido/Omitido/Eliminado

**Ejemplo de log**:
```
Analizando: juce_wrapper.md
  ⚠️  Documento no cumple criterios de calidad:
     - Documento muy corto (1 líneas)
     - Contenido muy breve (25 caracteres)
     - Parece ser un archivo de prueba/borrador
  ❌ Omitido (no se moverá)
```

---

## 💡 Recomendaciones de Uso

### Para Desarrolladores

1. **Revisar documentos rechazados**:
   - Los documentos en `docs/temp/` que no se mueven pueden necesitar más contenido
   - O pueden ser borradores que deben eliminarse

2. **Mejorar documentos con advertencias**:
   - Si un documento se mueve con score bajo, revisarlo y mejorarlo
   - Agregar más contenido, estructura, o información

3. **Eliminar archivos de prueba**:
   - Los archivos claramente de prueba pueden eliminarse manualmente
   - O dejarlos en `temp/` para limpieza posterior

### Para Agentes de IA

1. **Al crear documentación temporal**:
   - Asegurar mínimo 10 líneas de contenido útil
   - Incluir estructura con secciones
   - Evitar frases de prueba como "esto es un..."

2. **Verificar antes de colocar en temp/**:
   - El documento debe tener contenido sustancial
   - Debe aportar información nueva
   - No debe ser solo un placeholder

---

## 🔧 Configuración

Los umbrales pueden ajustarse en `docs_manager.py`:

```python
# Umbrales configurables
MIN_LINES = 10
MIN_CHARACTERS = 200
MIN_SCORE_TO_MOVE = 0.5
REDUNDANCY_THRESHOLD = 0.9
```

---

## 📊 Estadísticas

El sistema reporta:

- **Analizados**: Total de documentos procesados
- **Movidos**: Documentos que pasaron evaluación y se movieron
- **Omitidos**: Documentos rechazados por calidad/redundancia
- **Errores**: Errores durante el procesamiento

---

## ✅ Beneficios

1. **Calidad garantizada**: Solo se mueven documentos útiles
2. **Redundancia evitada**: No se duplican documentos similares
3. **Limpieza automática**: Archivos de prueba no se mueven
4. **Transparencia**: Logs claros de decisiones
5. **Eficiencia**: Menos trabajo manual de limpieza

---

## 🔗 Referencias

- [Evaluación de Clasificación](EVALUACION_CLASIFICACION.md)
- [Estructura de Documentación](ESTRUCTURA_DOCUMENTACION.md)
- [Guía de pre_cursor](GUIA_PRE_CURSOR_DOCS.md)

---

**Última actualización**: 2025-12-06

