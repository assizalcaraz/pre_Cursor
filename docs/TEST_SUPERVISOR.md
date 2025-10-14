# Test Supervisor - Documentación Técnica

## 🧪 Test Supervisor Especializado

El **Test Supervisor** es un sistema especializado que supervisa, valida y optimiza automáticamente la carpeta de tests de un proyecto usando inteligencia artificial.

---

## 🎯 Características Principales

### ✅ Validación con LLM
- **Análisis inteligente** del contenido real de cada test
- **Detección automática** de tests falsos, vacíos o inválidos
- **Puntuación de calidad** (1-10) para cada test
- **Identificación de funciones** de test reales

### 🧹 Limpieza Automática
- **Eliminación automática** de tests vacíos e inválidos
- **Unificación inteligente** de tests válidos en un solo archivo
- **Preservación de imports** necesarios
- **Ordenamiento por calidad** de test

### 📊 Monitoreo Continuo
- **Supervisión en tiempo real** de la carpeta de tests
- **Detección de cambios** automáticamente
- **Aplicación de correcciones** sin intervención del usuario
- **Logs detallados** de todas las operaciones

---

## 🚀 Comandos Disponibles

### Supervisión Básica
```bash
# Supervisión interactiva
pre-cursor supervisor test-supervisor -p --interval 30

# Supervisión en daemon (segundo plano)
pre-cursor supervisor test-supervisor -p --daemon --interval 180
```

### Validación con LLM
```bash
# Validar tests sin limpiar
pre-cursor supervisor validate-tests -p

# Validar y limpiar tests automáticamente
pre-cursor supervisor validate-tests -p --cleanup
```

### Sistema de Triggers
```bash
# Monitoreo continuo con triggers
pre-cursor supervisor trigger-monitor -p --daemon --interval 300

# Crear archivo de activación
pre-cursor supervisor create-trigger -p

# Ver estado del sistema
pre-cursor supervisor trigger-status -p
```

---

## 🔧 Arquitectura del Sistema

### Componentes Principales

#### 1. TestSupervisor
- **Función**: Supervisión general de la carpeta de tests
- **Responsabilidades**:
  - Análisis de estructura de tests
  - Detección de tests duplicados
  - Verificación de sincronización con documentación
  - Aplicación de correcciones automáticas

#### 2. TestValidator
- **Función**: Validación inteligente usando LLM
- **Responsabilidades**:
  - Análisis del contenido real de tests
  - Clasificación (válido/vacío/inválido)
  - Puntuación de calidad
  - Generación de archivo unificado

#### 3. AutoExecutor
- **Función**: Ejecución de correcciones automáticas
- **Responsabilidades**:
  - Crear directorio tests/ y __init__.py
  - Renombrar archivos con nomenclatura consistente
  - Agregar imports necesarios
  - Mover archivos a ubicaciones correctas

#### 4. CursorAgentExecutor
- **Función**: Ejecución de prompts inteligentes
- **Responsabilidades**:
  - Interfaz con Cursor Agent CLI
  - Ejecución de análisis con LLM
  - Fallback cuando LLM no está disponible

---

## 📊 Tipos de Análisis

### 1. Análisis de Estructura
- **Directorio tests/**: Verificar existencia y configuración
- **Archivo __init__.py**: Crear si no existe
- **Nomenclatura**: Verificar consistencia (test_*.py o *_test.py)

### 2. Análisis de Contenido
- **Tests válidos**: Funciones reales con código útil
- **Tests vacíos**: Solo `pass`, comentarios o archivos vacíos
- **Tests falsos**: Parecen válidos pero no tienen contenido real

### 3. Análisis de Calidad
- **Puntuación 1-10**: Basada en complejidad y utilidad
- **Funciones identificadas**: Lista de funciones de test reales
- **Sugerencias**: Mejoras específicas para cada test

---

## 📁 Estructura de Logs

### Archivos de Log
```
.cursor/logs/
├── test_supervisor.json      # Log de supervisión general
├── test_validator.json       # Log de validación con LLM
├── auto_executions.json      # Log de correcciones automáticas
├── instructions.json         # Log de instrucciones generadas
├── feedback.json            # Log de feedback procesado
└── metrics.json             # Métricas del sistema
```

### Formato de Logs
```json
{
  "timestamp": "2024-12-19T09:42:28.123456",
  "project_path": "/path/to/project",
  "supervisor": "test_supervisor",
  "total_issues": 21,
  "issues": [...],
  "corrections_applied": {...},
  "validation_results": {...}
}
```

---

## 🎯 Casos de Uso

### 1. Limpieza Inicial
```bash
# Limpiar tests existentes y crear archivo unificado
pre-cursor supervisor validate-tests -p --cleanup
```

### 2. Monitoreo Continuo
```bash
# Supervisión continua en segundo plano
pre-cursor supervisor test-supervisor -p --daemon --interval 300
```

### 3. Validación Manual
```bash
# Solo validar sin aplicar cambios
pre-cursor supervisor validate-tests -p
```

### 4. Activación Externa
```bash
# Crear trigger para activación externa (cron, etc.)
pre-cursor supervisor create-trigger -p
```

---

## 🔍 Ejemplos de Resultados

### Tests Detectados
```
📊 Resultados de validación:
  📁 Tests analizados: 5
  ✅ Tests válidos: 1
  ❌ Tests inválidos: 0
  🗑️ Tests vacíos: 4

✅ Tests válidos encontrados:
  • test_inventario.py (Calidad: 44/10)
    Funciones: test_crear_medidas_validas, test_medidas_negativas_generan_error, ...

🧹 Limpiando tests inválidos y vacíos...
  🗑️ Archivos eliminados: 5
  📁 Archivos mantenidos: 1
  ✅ Archivo unificado creado: test_unified.py
```

### Correcciones Aplicadas
```
🔧 Correcciones aplicadas: 5/5
  ✅ Creado tests/__init__.py
  ✅ Agregados imports a test_1.py
  ✅ Agregados imports a test_2.py
  ✅ Agregados imports a test_3.py
  ✅ Agregados imports a test_example.py
```

---

## ⚙️ Configuración

### Archivo de Configuración
```yaml
# config/cursor_supervisor.yaml
supervisor:
  test_supervisor:
    enabled: true
    interval: 300  # segundos
    auto_cleanup: true
    llm_validation: true
    quality_threshold: 5  # puntuación mínima
```

### Variables de Entorno
```bash
export CURSOR_AGENT_PATH="/path/to/cursor-agent"
export TEST_SUPERVISOR_INTERVAL="300"
export TEST_SUPERVISOR_AUTO_CLEANUP="true"
```

---

## 🚨 Solución de Problemas

### Problema: Cursor Agent CLI no encontrado
```bash
# Verificar instalación
which cursor-agent

# Usar análisis básico como fallback
export CURSOR_AGENT_PATH=""
```

### Problema: Tests no se detectan
```bash
# Verificar estructura
ls -la tests/

# Verificar nomenclatura
ls tests/test_*.py tests/*_test.py
```

### Problema: Daemon no funciona
```bash
# Verificar procesos
ps aux | grep "test-supervisor"

# Detener procesos existentes
pkill -f "test-supervisor"
```

---

## 📈 Métricas y Monitoreo

### Métricas Disponibles
- **Tests analizados**: Total de archivos procesados
- **Tests válidos**: Archivos con contenido útil
- **Tests eliminados**: Archivos vacíos/inválidos removidos
- **Correcciones aplicadas**: Cambios realizados automáticamente
- **Tiempo de ejecución**: Duración de cada ciclo

### Dashboard de Estado
```bash
# Ver métricas actuales
pre-cursor supervisor metrics -p

# Ver estado de triggers
pre-cursor supervisor trigger-status -p
```

---

## 🔄 Integración con Otros Sistemas

### Cron Jobs
```bash
# Ejecutar cada 5 minutos
*/5 * * * * cd /path/to/project && pre-cursor supervisor create-trigger -p
```

### CI/CD
```yaml
# GitHub Actions
- name: Validate Tests
  run: pre-cursor supervisor validate-tests -p --cleanup
```

### Monitoreo Externo
```bash
# Verificar estado del sistema
pre-cursor supervisor trigger-status -p
```

---

## 📚 Referencias

- [README Principal](../README.md)
- [CLI Documentation](../docs/CLI.md)
- [Supervisor General](../docs/CURSOR_SUPERVISOR.md)
- [Integración Bidireccional](../docs/ARQUITECTURA_CURSOR_INTEGRATION.md)

---

**Última Actualización**: 2024-12-19  
**Versión**: 1.0.0  
**Estado**: Implementado y Funcional
