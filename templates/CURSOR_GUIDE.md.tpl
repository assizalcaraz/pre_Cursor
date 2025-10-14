# 🤖 Guía para Cursor AI - $NOMBRE_PROYECTO

**IMPORTANTE**: Este es un proyecto generado con Pre-Cursor. Este archivo contiene instrucciones específicas para agentes de IA en Cursor.

---

## 📋 Contexto del Proyecto

### Objetivo Principal
**$DESCRIPCION_PROYECTO**

### Tipo de Proyecto
**$TIPO_PROYECTO** - {{DESCRIPCION_TIPO_PROYECTO}}

### Metodología
Este proyecto sigue la metodología establecida de Pre-Cursor, optimizada para desarrollo con agentes de IA.

---

## 🎯 Instrucciones para Cursor AI

### 1. **Usar este template como GUÍA, no como código final**
- ✅ **SÍ**: Adaptar el código a los objetivos específicos del proyecto
- ✅ **SÍ**: Modificar funciones según las necesidades reales
- ✅ **SÍ**: Añadir funcionalidades que cumplan la descripción del proyecto
- ❌ **NO**: Copiar literalmente sin adaptar al contexto
- ❌ **NO**: Dejar placeholders sin procesar

### 2. **Alinear TODO al objetivo del proyecto**
- Revisar `$DESCRIPCION_PROYECTO` antes de cada cambio
- Cada función debe contribuir al objetivo principal
- Priorizar funcionalidades que cumplan la descripción

### 3. **Estructura base a seguir**
```
$NOMBRE_PROYECTO/
├── README.md              # Documentación principal
├── TUTORIAL.md            # Guía de uso
├── BITACORA.md            # Log de desarrollo
├── CURSOR_GUIDE.md        # Este archivo (para IA)
├── requirements.txt       # Dependencias
├── src/                   # Código fuente
│   ├── $MODULO_PRINCIPAL.py
│   └── utils/
├── tests/                 # Pruebas
└── docs/                  # Documentación adicional
```

---

## 🔧 Comandos Útiles para Cursor

### Verificar estado del proyecto
```bash
# Ver estructura actual
ls -la

# Verificar dependencias
pip list | grep $NOMBRE_PROYECTO

# Ejecutar tests
pytest tests/
```

### Desarrollo iterativo
```bash
# Instalar en modo desarrollo
pip install -e .

# Ejecutar proyecto
python -m $MODULO_PRINCIPAL

# Verificar sintaxis
python -m py_compile src/$MODULO_PRINCIPAL.py
```

---

## 📝 Checklist de Desarrollo

### ✅ Fase 1: Configuración
- [ ] Revisar `requirements.txt` y instalar dependencias
- [ ] Verificar que el código base compila sin errores
- [ ] Leer `README.md` para entender el objetivo
- [ ] Revisar `TUTORIAL.md` para ejemplos de uso

### ✅ Fase 2: Adaptación
- [ ] Identificar qué funcionalidades faltan según la descripción
- [ ] Modificar `$MODULO_PRINCIPAL.py` para cumplir objetivos
- [ ] Actualizar documentación según cambios realizados
- [ ] Añadir tests para nuevas funcionalidades

### ✅ Fase 3: Validación
- [ ] Ejecutar todos los tests: `pytest`
- [ ] Verificar que el proyecto cumple su descripción
- [ ] Actualizar `BITACORA.md` con cambios realizados
- [ ] Revisar que no quedan placeholders sin procesar

---

## 🚨 Errores Comunes a Evitar

### ❌ NO hacer esto:
1. **Dejar placeholders**: `{{VARIABLE}}` o `$VARIABLE` sin reemplazar
2. **Copiar literalmente**: Sin adaptar al contexto del proyecto
3. **Ignorar la descripción**: No alinear funcionalidades al objetivo
4. **Saltarse tests**: No verificar que el código funciona

### ✅ SÍ hacer esto:
1. **Adaptar al contexto**: Modificar código según necesidades reales
2. **Cumplir objetivos**: Cada función debe servir al propósito del proyecto
3. **Documentar cambios**: Actualizar README y comentarios
4. **Probar funcionalidad**: Ejecutar tests y verificar funcionamiento

---

## 📚 Archivos de Referencia

### Documentación Principal
- `README.md` - Información general del proyecto
- `TUTORIAL.md` - Guía paso a paso de uso
- `BITACORA.md` - Historial de cambios y decisiones

### Código Fuente
- `src/$MODULO_PRINCIPAL.py` - Módulo principal (ADAPTAR SEGÚN OBJETIVOS)
- `src/utils/` - Utilidades auxiliares
- `tests/` - Pruebas unitarias e integración

### Configuración
- `requirements.txt` - Dependencias Python
- `pyproject.toml` - Configuración del proyecto
- `.gitignore` - Archivos ignorados por Git

---

## 🎯 Objetivos Específicos de $NOMBRE_PROYECTO

### Funcionalidad Principal
**$DESCRIPCION_PROYECTO**

### Características Esperadas
- {{CARACTERISTICA_1}}
- {{CARACTERISTICA_2}}
- {{CARACTERISTICA_3}}

### Casos de Uso
1. {{CASO_USO_1}}
2. {{CASO_USO_2}}
3. {{CASO_USO_3}}

---

## 🔄 Flujo de Trabajo Recomendado

1. **Leer contexto**: Revisar descripción y objetivos
2. **Analizar template**: Entender estructura base
3. **Adaptar código**: Modificar según necesidades reales
4. **Implementar funcionalidades**: Añadir características específicas
5. **Probar y validar**: Ejecutar tests y verificar funcionamiento
6. **Documentar cambios**: Actualizar README y comentarios

---

## 📞 Información de Contacto

- **Autor**: $AUTOR
- **Email**: $EMAIL_CONTACTO
- **GitHub**: [@$GITHUB_USER](https://github.com/$GITHUB_USER)
- **Proyecto**: [{{REPOSITORIO_URL}}]({{REPOSITORIO_URL}})

---

**Fecha de Creación**: {{FECHA_CREACION}}  
**Última Actualización**: {{FECHA_ACTUALIZACION}}  
**Versión**: {{VERSION_PROYECTO}}

---

> **💡 Tip para Cursor**: Este archivo es tu guía principal. Léelo completo antes de empezar a trabajar en el proyecto y consulta la descripción del proyecto para mantener el foco en los objetivos reales.
