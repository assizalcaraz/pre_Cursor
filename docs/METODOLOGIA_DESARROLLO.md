# Metodología de Desarrollo con Cursor - Mejores Prácticas

**Fecha**: 2024-12-19  
**Proyecto**: Metodología Universal de Desarrollo  
**Objetivo**: Plantilla de metodología de desarrollo establecida para aplicar a cualquier proyecto

---

## 🚀 Guía Rápida (TL;DR)

### Principios Clave
1. **Documentación Continua**: BITACORA.md actualizada en tiempo real
2. **Testing Proactivo**: Evaluar tests existentes antes de crear nuevos
3. **Tutoriales Estructurados**: Fecha, lección, resumen
4. **Organización Modular**: Estructura clara de directorios

### Checklist Rápido
- [ ] Bitácora actualizada
- [ ] Tests evaluados antes de crear nuevos
- [ ] Documentación actualizada
- [ ] Commits descriptivos
- [ ] Estructura organizada

### Convenciones de Commits
- **WIP**: Trabajo en progreso
- **FIX**: Corrección de bugs (requiere supervisión)
- **FEAT**: Nueva funcionalidad (requiere supervisión)
- **POINT**: Versión estable para rollback

### Flujo de Desarrollo
```bash
# Para cada cambio significativo:
# 1. Implementar funcionalidad
# 2. Actualizar BITACORA.md
# 3. Evaluar tests existentes
# 4. Crear/actualizar tests si es necesario
# 5. Actualizar documentación
# 6. Commit descriptivo
git add . && git commit -m "WIP: Descripción del cambio"
```

---

## 📋 Resumen Ejecutivo

Este documento establece las mejores prácticas de desarrollo universales que pueden aplicarse a cualquier proyecto, incluyendo gestión de bitácora, sistema de testing, documentación de tutoriales y organización de código. Estas prácticas han demostrado ser efectivas para mantener proyectos organizados, documentados y mantenibles independientemente del tipo de proyecto.

---

## 🎯 Principios Fundamentales

### 1. **Documentación Continua**
- Documentar cada cambio importante en tiempo real
- Mantener bitácora actualizada con progreso diario
- Crear tutoriales estructurados con fecha, lección y resumen

### 2. **Testing Proactivo**
- Evaluar tests existentes antes de crear nuevos
- Mantener estructura organizada de pruebas
- Documentar convenciones de testing

### 3. **Organización Modular**
- Separar funcionalidades en módulos específicos
- Mantener estructura de directorios clara
- Usar convenciones de nomenclatura consistentes

---

## 📚 Gestión de Bitácora (BITACORA.md)

### Estructura Recomendada

```markdown
# BITACORA - [NOMBRE_PROYECTO]

## Log de desarrollo del [DESCRIPCIÓN_PROYECTO]

### YYYY-MM-DD
- **INICIO**: Descripción del inicio del proyecto
- **OBJETIVO**: Objetivo principal del proyecto
- **ESTADO**: Estado actual del proyecto
- **PRÓXIMOS PASOS**: Pasos siguientes identificados

### YYYY-MM-DD (Continuación)
- **CAMBIOS REALIZADOS**: Lista de cambios específicos
- **ARCHIVOS CREADOS**: Archivos nuevos añadidos
- **FUNCIONALIDADES**: Funcionalidades implementadas
- **PRÓXIMO PASO**: Siguiente acción planificada
```

### Mejores Prácticas

1. **Actualización Continua**: Actualizar la bitácora después de cada cambio significativo
2. **Detalle Específico**: Incluir nombres de archivos, funciones y cambios específicos
3. **Progreso Claro**: Marcar claramente qué está completado y qué está pendiente
4. **Referencias**: Incluir referencias a archivos, commits y decisiones importantes

### Ejemplo de Entrada

```markdown
### 2024-12-19 (Fase 4 - Funcionalidades Core)
- **SISTEMA DE EVENTOS IMPLEMENTADO**:
  - `event_system.py`: Sistema completo de eventos asíncronos
  - Tipos de eventos: conexión, operadores, parámetros, archivos .tox, errores
  - Gestión de listeners y callbacks
  - Cola de eventos con procesamiento asíncrono
- **MANEJO DE ERRORES ROBUSTO**:
  - `error_handler.py`: Sistema completo de manejo de errores
  - Categorización de errores (conexión, archivos, TouchDesigner, etc.)
  - Severidad de errores (low, medium, high, critical)
  - Recuperación automática y reintentos
- **FASE 4 COMPLETADA**: Todas las funcionalidades core implementadas y probadas
```

---

## 🧪 Sistema de Testing

### Estructura de Directorios

```
tests/
├── README.md                    # Instrucciones detalladas
├── test_system.py              # Pruebas del sistema completo
├── test_[modulo].py            # Pruebas específicas por módulo
└── conftest.py                 # Configuración común de pytest
```

### Instrucciones para Cursos y LLMs

#### ⚠️ OBLIGATORIO: Evaluación de Tests Existentes

**ANTES de crear cualquier test nuevo, SIEMPRE:**

1. **Revisar carpeta `tests/`** para tests existentes
2. **Evaluar si el test actual** cubre la funcionalidad requerida
3. **Decidir la acción apropiada**:
   - ✅ **Usar test existente** si cubre completamente la necesidad
   - 🔄 **Extender test existente** si necesita funcionalidad adicional
   - ➕ **Crear nuevo test** solo si no existe test adecuado

#### Proceso de Testing

```bash
# Paso 1: Evaluación
ls tests/
cat tests/test_*.py

# Paso 2: Decisión
# - Test existe y es completo → Usar test existente
# - Test existe pero es parcial → Añadir nueva sección
# - Test no existe → Crear nuevo test

# Paso 3: Implementación
# Seguir convenciones establecidas
```

#### Convenciones de Testing

- **Nomenclatura**: `test_<modulo>.py`, `test_<funcionalidad>()`
- **Documentación**: Docstring obligatorio en cada función
- **Cobertura**: Éxito, error, límites, casos edge
- **Estructura**: Arrange, Act, Assert

#### Plantilla para Nuevos Tests

```python
"""
Test para [Módulo/Funcionalidad].

Este módulo contiene tests para [descripción del módulo].
"""

import pytest
import asyncio
from unittest.mock import Mock, patch

class TestNuevoModulo:
    """Tests para NuevoModulo."""
    
    def test_funcionalidad_basica(self):
        """
        Test de funcionalidad básica.
        
        Casos cubiertos:
        - Éxito: Funcionalidad normal
        - Error: Manejo de excepciones
        """
        # Arrange
        # Act
        # Assert
        pass
    
    @pytest.mark.asyncio
    async def test_funcionalidad_async(self):
        """
        Test de funcionalidad asíncrona.
        
        Casos cubiertos:
        - Éxito: Operación async exitosa
        - Timeout: Manejo de timeouts
        """
        # Arrange
        # Act
        # Assert
        pass
```

---

## 📖 Sistema de Tutoriales

### Estructura de Tutoriales

```markdown
# Tutorial de [NOMBRE] - [PROYECTO]

**Fecha**: YYYY-MM-DD  
**Lección**: [NOMBRE_DESCRIPTIVO_DE_LA_LECCION]  
**Resumen**: [RESUMEN_COMPLETO_DE_LO_QUE_CUBRE_EL_TUTORIAL]

---

## [CONTENIDO_DEL_TUTORIAL]
```

### Mejores Prácticas

1. **Formato Estructurado**: Siempre incluir fecha, lección y resumen
2. **Ubicación Organizada**: Colocar tutoriales en carpeta `docs/`
3. **Referencias Actualizadas**: Mantener todas las referencias actualizadas
4. **Instrucciones Claras**: Proporcionar comandos específicos y ejemplos

### Ejemplo de Tutorial

```markdown
# Tutorial de Inicio - TD_MCP

**Fecha**: 2024-12-19  
**Lección**: Configuración e Inicio del Middleware MCP para TouchDesigner  
**Resumen**: Guía completa paso a paso para configurar y usar el middleware TD_MCP que permite a los modelos de IA interactuar con TouchDesigner a través del Model Context Protocol.

---

## Bienvenido al Middleware MCP para TouchDesigner

Este tutorial te guiará paso a paso para configurar y usar el middleware TD_MCP...
```

---

## 🏗️ Organización de Código

### Estructura de Proyecto Recomendada

```
PROYECTO/
├── README.md                    # Documentación principal
├── BITACORA.md                 # Log de desarrollo
├── roadmap_v1.md               # Plan de desarrollo
├── investigacion.md            # Documentación de investigación
├── requirements.txt            # Dependencias
├── config.py                   # Configuración
├── iniciar.sh                  # Script de inicio rápido
├── ejemplos_basicos.py         # Ejemplos de uso
├── src/                        # Código fuente
│   ├── [modulo_principal].py   # Módulo principal
│   ├── [modulo_especifico]/    # Módulos específicos
│   └── utils/                  # Utilidades
├── tests/                      # Pruebas
│   ├── README.md              # Instrucciones de testing
│   ├── test_system.py         # Pruebas del sistema
│   └── test_[modulo].py       # Pruebas específicas
├── docs/                       # Documentación
│   ├── TUTORIAL.md            # Tutorial principal
│   └── [otros_docs].md        # Documentación adicional
├── examples/                   # Ejemplos
└── logs/                       # Logs (si aplica)
```

### Convenciones de Nomenclatura

- **Archivos Python**: `snake_case.py`
- **Clases**: `PascalCase`
- **Funciones**: `snake_case()`
- **Constantes**: `UPPER_CASE`
- **Tests**: `test_<funcionalidad>.py`

---

## 🔄 Flujo de Desarrollo Recomendado

### 1. Inicio de Proyecto
```bash
# Crear estructura básica
mkdir proyecto && cd proyecto
git init

# Crear archivos fundamentales
touch README.md BITACORA.md roadmap_v1.md requirements.txt
mkdir -p src tests docs examples
```

### 2. Desarrollo Iterativo
```bash
# Para cada cambio significativo:
# 1. Implementar funcionalidad
# 2. Actualizar BITACORA.md
# 3. Crear/actualizar tests
# 4. Actualizar documentación
# 5. Commit con mensaje descriptivo
git add . && git commit -m "WIP: Descripción del cambio"
```

### 3. Gestión de Tests
```bash
# Antes de crear nuevo test:
ls tests/
cat tests/test_*.py

# Evaluar si existe test adecuado
# Si no existe, crear nuevo test siguiendo plantilla
```

### 4. Documentación Continua
```bash
# Actualizar tutoriales cuando sea necesario
# Mantener referencias actualizadas
# Documentar decisiones importantes en BITACORA.md
```

---

## 📝 Convenciones de Commits

### Formato de Mensajes

```bash
# Para trabajo en progreso
git commit -m "WIP: Descripción del cambio implementado"

# Para correcciones (solo con supervisión)
git commit -m "FIX: Descripción del bug y enfoque de solución"

# Para características estables (requiere supervisión)
git commit -m "FEAT: Descripción de nueva funcionalidad"
```

### Tags de Versión

- **WIP**: Trabajo en progreso
- **FIX**: Corrección de bugs (requiere supervisión)
- **FEAT**: Nueva funcionalidad (requiere supervisión)
- **POINT**: Versión estable para rollback

---

## 🎯 Checklist de Mejores Prácticas

### Para Cada Sesión de Desarrollo

- [ ] **Bitácora Actualizada**: Cambios documentados en BITACORA.md
- [ ] **Tests Evaluados**: Revisar tests existentes antes de crear nuevos
- [ ] **Documentación Actualizada**: Referencias y tutoriales actualizados
- [ ] **Commits Descriptivos**: Mensajes claros con tags apropiados
- [ ] **Estructura Organizada**: Archivos en ubicaciones correctas

### Para Cada Nueva Funcionalidad

- [ ] **Módulo Separado**: Funcionalidad en módulo específico
- [ ] **Tests Creados**: Pruebas para casos exitosos y de error
- [ ] **Documentación**: Docstrings y documentación actualizada
- [ ] **Logging**: Logging apropiado implementado
- [ ] **Manejo de Errores**: Errores manejados correctamente

### Para Cada Fase del Proyecto

- [ ] **Roadmap Actualizado**: Progreso marcado en roadmap
- [ ] **Tutorial Creado**: Guía paso a paso si es necesario
- [ ] **Ejemplos Proporcionados**: Ejemplos de uso implementados
- [ ] **Pruebas Completas**: Suite de tests ejecutada exitosamente
- [ ] **Documentación Completa**: Todo documentado apropiadamente

---

## 🚀 Aplicación en Otros Proyectos

### Pasos para Implementar esta Metodología

1. **Crear Estructura Base**:
   ```bash
   mkdir nuevo_proyecto && cd nuevo_proyecto
   git init
   # Crear estructura de directorios recomendada
   ```

2. **Configurar Archivos Fundamentales**:
   - Copiar plantilla de BITACORA.md
   - Crear README.md con estructura recomendada
   - Configurar tests/README.md con instrucciones

3. **Establecer Convenciones**:
   - Definir convenciones de nomenclatura
   - Configurar formato de commits
   - Establecer proceso de testing

4. **Implementar Flujo de Desarrollo**:
   - Seguir checklist de mejores prácticas
   - Mantener documentación actualizada
   - Evaluar tests antes de crear nuevos

### Adaptaciones por Tipo de Proyecto

- **Proyectos Web**: Añadir carpeta `static/`, `templates/`
- **Proyectos de IA**: Incluir `models/`, `data/`, `notebooks/`
- **Proyectos de API**: Añadir `endpoints/`, `schemas/`
- **Proyectos de CLI**: Incluir `commands/`, `cli.py`

---

## 📊 Métricas de Éxito

### Indicadores de Calidad

- **Cobertura de Tests**: >80% de código cubierto
- **Documentación**: Todos los módulos documentados
- **Commits Descriptivos**: 100% de commits con mensajes claros
- **Estructura Organizada**: Archivos en ubicaciones lógicas
- **Bitácora Actualizada**: Cambios documentados en tiempo real

### Beneficios Observados

- **Mantenibilidad**: Código fácil de mantener y extender
- **Colaboración**: Otros desarrolladores pueden entender el proyecto
- **Debugging**: Errores fáciles de localizar y corregir
- **Escalabilidad**: Estructura preparada para crecimiento
- **Calidad**: Código robusto y bien probado

---

## 🔗 Referencias y Recursos

### Archivos de Referencia de Ejemplo

- `BITACORA.md`: Ejemplo completo de gestión de bitácora
- `tests/README.md`: Instrucciones detalladas de testing
- `docs/TUTORIAL.md`: Ejemplo de tutorial estructurado
- `roadmap_v1.md`: Plan de desarrollo por fases

### Herramientas Recomendadas

- **Testing**: pytest, unittest
- **Documentación**: Markdown, Sphinx
- **Control de Versiones**: Git con convenciones establecidas
- **Logging**: Python logging, loguru
- **Manejo de Errores**: Excepciones personalizadas, decoradores

---

## 📋 Conclusión

Esta metodología de desarrollo ha demostrado ser efectiva para mantener proyectos organizados, documentados y mantenibles. Las mejores prácticas identificadas incluyen:

1. **Documentación Continua** con bitácora actualizada
2. **Testing Proactivo** con evaluación de tests existentes
3. **Organización Modular** con estructura clara
4. **Tutoriales Estructurados** con formato consistente
5. **Convenciones Establecidas** para nomenclatura y commits

Al aplicar estas prácticas en otros proyectos, se puede lograr un desarrollo más eficiente, mantenible y colaborativo.

---

**Nota**: Este documento debe ser actualizado con nuevas mejores prácticas identificadas en futuros proyectos.
