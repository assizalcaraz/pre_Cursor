# 🤖 Cursor Supervisor - Supervisión Automática de Código

**Versión**: 1.0.0  
**Fecha**: 2024-10-13  
**Estado**: 🔬 En Desarrollo

---

## 📋 Descripción

El **Cursor Supervisor** es un sistema de supervisión automática diseñado para resolver los problemas comunes en la generación de código con Cursor IDE:

- **Archivos fuera de lugar**: Tests en `/` en lugar de `/tests/`
- **Scripts repetitivos**: Funciones duplicadas que generan redundancias
- **Fallos de configuración**: Conflictos con archivos preexistentes
- **Interrupciones por conexión**: Generación se detiene por fallas de red
- **Intervención manual constante**: Requiere supervisión humana continua

---

## 🏗️ Arquitectura

### **Instancia 1 - Supervisor (Cron Job)**
- **Rol**: Supervisión y control de calidad
- **Frecuencia**: Revisión periódica (cada 5-10 minutos)
- **Responsabilidades**:
  - Verificar alineación con metodología del proyecto
  - Documentar cambios en BITACORA.md
  - Revisar logs de generación
  - Analizar estructura del proyecto (`tree`)
  - Detectar archivos fuera de lugar
  - Identificar redundancias y duplicados

### **Instancia 2 - Generador (Cursor CLI)**
- **Rol**: Generación de código siguiendo roadmap
- **Modo**: Instrucciones esporádicas del supervisor
- **Responsabilidades**:
  - Seguir roadmap definido
  - Generar código según especificaciones
  - Reportar progreso al supervisor
  - Detener generación si hay problemas

---

## 🚀 Instalación

### **Dependencias requeridas:**
```bash
pip install watchdog psutil
```

### **Instalación desde fuente:**
```bash
git checkout feature/cursor-cli-integration
pip install -e .
```

---

## 🔧 Uso

### **Supervisión básica:**
```python
from pre_cursor.cursor_supervisor import CursorSupervisor

# Crear supervisor
supervisor = CursorSupervisor('/path/to/project', check_interval=300)

# Iniciar supervisión continua
supervisor.start_supervision()
```

### **Verificación única:**
```python
# Ejecutar una verificación
report = supervisor.check_project_health()

print(f"Problemas encontrados: {len(report.issues_found)}")
for issue in report.issues_found:
    print(f"- {issue.severity.upper()}: {issue.description}")
```

### **Desde línea de comandos:**
```bash
# Verificación única
python -m pre_cursor.cursor_supervisor /path/to/project --once

# Supervisión continua
python -m pre_cursor.cursor_supervisor /path/to/project --interval 300
```

---

## 🔍 Tipos de Problemas Detectados

### **Estructura del Proyecto:**
- **Directorio faltante**: `tests/`, `docs/`, `src/`, etc.
- **Archivos fuera de lugar**: Tests en raíz, config en `src/`
- **Estructura incorrecta**: Directorios en ubicaciones incorrectas

### **Duplicados:**
- **Archivos duplicados**: Mismo contenido en diferentes ubicaciones
- **Funciones duplicadas**: Misma función en múltiples archivos
- **Código redundante**: Bloques de código repetidos

### **Configuración:**
- **Archivos de configuración mal ubicados**
- **Dependencias faltantes**
- **Configuración inconsistente**

---

## 📊 Métricas y Reportes

### **Reporte de Supervisión:**
```python
@dataclass
class SupervisionReport:
    timestamp: datetime
    issues_found: List[ProjectIssue]
    files_created: List[str]
    files_modified: List[str]
    structure_changes: List[str]
    recommendations: List[str]
```

### **Problema Individual:**
```python
@dataclass
class ProjectIssue:
    type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    file_path: Optional[str] = None
    suggestion: Optional[str] = None
    timestamp: datetime = None
```

---

## ⚙️ Configuración

### **Archivo de configuración:**
```yaml
# config/cursor_supervisor.yaml
supervisor:
  check_interval: 300  # segundos
  max_issues: 10
  auto_fix: true
  log_level: "INFO"

detection:
  check_misplaced_files: true
  check_duplicates: true
  check_structure: true

notifications:
  console: true
  file_logging: true
  log_file: "logs/supervisor.log"
```

---

## 🧪 Testing

### **Ejecutar pruebas:**
```bash
python test_cursor_supervisor.py
```

### **Pruebas incluidas:**
- ✅ Monitor de estructura
- ✅ Detector de duplicados
- ✅ Supervisor completo
- ✅ Actualización de bitácora
- ✅ Generación de recomendaciones

---

## 📈 Roadmap

### **Fase 1: Investigación y Prototipo** ✅
- [x] Documentar capacidades de Cursor CLI
- [x] Crear prototipo básico de supervisión
- [x] Probar integración con proyectos existentes

### **Fase 2: Desarrollo del Supervisor** 🔄
- [x] Implementar CursorSupervisor
- [x] Crear sistema de detección de problemas
- [x] Desarrollar actualización automática de bitácora
- [ ] Implementar corrección automática de problemas simples

### **Fase 3: Integración con Generador** 📋
- [ ] Modificar init_project.py para incluir supervisión
- [ ] Crear sistema de instrucciones para Cursor
- [ ] Implementar monitoreo de progreso

### **Fase 4: Testing y Optimización** 📋
- [ ] Probar con diferentes tipos de proyecto
- [ ] Optimizar frecuencia de supervisión
- [ ] Refinar detección de problemas

---

## 🎯 Objetivos de Éxito

### **Métricas Cuantitativas:**
- **Reducción de intervención manual**: 80%
- **Archivos fuera de lugar**: 0%
- **Redundancias detectadas**: 95%
- **Tiempo de corrección**: -70%

### **Métricas Cualitativas:**
- **Experiencia de usuario**: Sin intervención constante
- **Calidad de código**: Consistente y organizado
- **Mantenibilidad**: Proyectos bien estructurados
- **Automatización**: Proceso completamente automático

---

## 🔧 API Reference

### **CursorSupervisor**
```python
class CursorSupervisor:
    def __init__(self, project_path: str, check_interval: int = 300)
    def start_supervision(self) -> None
    def check_project_health(self) -> SupervisionReport
    def update_bitacora(self, report: SupervisionReport) -> None
```

### **ProjectStructureMonitor**
```python
class ProjectStructureMonitor:
    def __init__(self, project_path: str)
    def check_structure(self) -> List[ProjectIssue]
    def check_files_out_of_place(self) -> List[ProjectIssue]
```

### **DuplicateDetector**
```python
class DuplicateDetector:
    def __init__(self, project_path: str)
    def find_duplicate_files(self) -> List[ProjectIssue]
    def find_duplicate_functions(self) -> List[ProjectIssue]
```

---

## 🐛 Troubleshooting

### **Problemas comunes:**

#### **"Cursor CLI no encontrado"**
```bash
# Verificar instalación de Cursor
which cursor
# Instalar Cursor si es necesario
```

#### **"Bitácora no se actualiza"**
```bash
# Verificar permisos de escritura
ls -la BITACORA.md
# Verificar logs del supervisor
tail -f logs/supervisor.log
```

#### **"Problemas no detectados"**
```bash
# Verificar configuración
cat config/cursor_supervisor.yaml
# Ejecutar con verbose
python -m pre_cursor.cursor_supervisor --verbose
```

---

## 📝 Contribuir

1. **Fork** el repositorio
2. **Crear** rama para feature: `git checkout -b feature/nueva-funcionalidad`
3. **Commit** cambios: `git commit -m 'Añadir nueva funcionalidad'`
4. **Push** a la rama: `git push origin feature/nueva-funcionalidad`
5. **Crear** Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para más detalles.

---

**Desarrollado por**: Assiz Alcaraz Baxter  
**Contacto**: assiz@pre-cursor.dev  
**Repositorio**: https://github.com/assizalcaraz/pre_Cursor
