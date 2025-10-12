# Instrucciones de Testing para Agentes de IA

## ⚠️ OBLIGATORIO: Evaluación de Tests Existentes

**ANTES de crear cualquier test nuevo, SIEMPRE:**

1. **Revisar carpeta `tests/`** para tests existentes
2. **Evaluar si el test actual** cubre la funcionalidad requerida
3. **Decidir la acción apropiada**:
   - ✅ **Usar test existente** si cubre completamente la necesidad
   - 🔄 **Extender test existente** si necesita funcionalidad adicional
   - ➕ **Crear nuevo test** solo si no existe test adecuado

## Proceso de Testing para Agentes

### Paso 1: Evaluación
```bash
# Listar archivos de test existentes
ls tests/
cat tests/test_*.py
```

### Paso 2: Decisión
- **Test existe y es completo** → Usar test existente
- **Test existe pero es parcial** → Añadir nueva sección
- **Test no existe** → Crear nuevo test siguiendo plantilla

### Paso 3: Implementación
Seguir convenciones establecidas en la metodología.

## Convenciones de Testing

### Nomenclatura
- **Archivos**: `test_<modulo>.py`, `test_<funcionalidad>.py`
- **Funciones**: `test_<funcionalidad>()`
- **Clases**: `Test<Modulo>`

### Documentación
- **Docstring obligatorio** en cada función de test
- **Casos cubiertos** claramente especificados
- **Estructura**: Arrange, Act, Assert

### Cobertura Requerida
- ✅ **Éxito**: Casos de uso normal
- ❌ **Error**: Manejo de excepciones
- 🔍 **Límites**: Casos edge y boundary
- ⚡ **Performance**: Tests de rendimiento si aplica

## Plantilla para Nuevos Tests

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

## Comandos de Testing

### Ejecutar Tests
```bash
# Todos los tests
pytest

# Test específico
pytest tests/test_modulo.py

# Con verbose
pytest -v

# Con coverage
pytest --cov=src
```

### Debugging
```bash
# Con debug
pytest --pdb

# Solo fallos
pytest -x
```

## Estructura de Directorios

```
tests/
├── README.md                    # Este archivo
├── test_system.py              # Pruebas del sistema completo
├── test_[modulo].py            # Pruebas específicas por módulo
└── conftest.py                 # Configuración común de pytest
```

## Mejores Prácticas para Agentes

1. **Siempre evaluar tests existentes** antes de crear nuevos
2. **Usar nombres descriptivos** para funciones y archivos
3. **Documentar casos cubiertos** en docstrings
4. **Mantener tests simples** y enfocados
5. **Usar mocks** para dependencias externas
6. **Seguir estructura AAA** (Arrange, Act, Assert)

## Casos Especiales

### Testing de Generación de Proyectos
- Testear creación de directorios
- Testear procesamiento de plantillas
- Testear inicialización de Git
- Testear validación de parámetros

### Testing de Plantillas
- Testear reemplazo de placeholders
- Testear validación de archivos generados
- Testear estructura de directorios creada

### Testing de Scripts
- Testear argumentos de línea de comandos
- Testear manejo de errores
- Testear flujos de trabajo completos

## Recursos Adicionales

- [Documentación de pytest](https://docs.pytest.org/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
