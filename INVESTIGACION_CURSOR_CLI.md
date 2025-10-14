# 🔬 Investigación: Integración Cursor CLI en Pre-Cursor

**Rama**: `feature/cursor-cli-integration`  
**Fecha**: 2024-10-13  
**Objetivo**: Investigar y diseñar integración del CLI de Cursor para supervisión automática de generación de código

---

## 📋 Problema Identificado

### **Síntomas observados:**
- **Archivos fuera de lugar**: Tests generados en `/` en lugar de `/tests/`
- **Scripts repetitivos**: Funciones duplicadas que generan redundancias
- **Fallos de configuración**: Conflictos con archivos preexistentes
- **Interrupciones por conexión**: Generación de código se detiene por fallas de red
- **Intervención manual constante**: Requiere supervisión humana continua

### **Impacto:**
- **Productividad reducida**: Tiempo perdido en corrección manual
- **Calidad inconsistente**: Código generado sin supervisión
- **Mantenimiento complejo**: Archivos desorganizados y duplicados
- **Experiencia de usuario**: Frustración por intervenciones constantes

---

## 🎯 Hipótesis de Solución

### **Arquitectura de Supervisión Dual:**

#### **Instancia 1 - Supervisor (Cron Job)**
- **Rol**: Supervisión y control de calidad
- **Frecuencia**: Revisión periódica (cada 5-10 minutos)
- **Responsabilidades**:
  - Verificar alineación con metodología del proyecto
  - Documentar cambios en BITACORA.md
  - Revisar logs de generación
  - Analizar estructura del proyecto (`tree`)
  - Detectar archivos fuera de lugar
  - Identificar redundancias y duplicados

#### **Instancia 2 - Generador (Cursor CLI)**
- **Rol**: Generación de código siguiendo roadmap
- **Modo**: Instrucciones esporádicas del supervisor
- **Responsabilidades**:
  - Seguir roadmap definido
  - Generar código según especificaciones
  - Reportar progreso al supervisor
  - Detener generación si hay problemas

---

## 🔍 Investigación Técnica

### **Cursor CLI - Capacidades Identificadas:**

#### **Comandos Básicos:**
```bash
# Abrir proyecto en Cursor
cursor <path>

# Abrir archivo específico
cursor <file>

# Abrir con configuración específica
cursor --config <config> <path>
```

#### **Integración Python:**
```python
import subprocess
import os

def open_cursor_project(project_path):
    """Abrir proyecto en Cursor desde Python"""
    try:
        subprocess.run(['cursor', project_path], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def cursor_command(command, project_path):
    """Ejecutar comando en Cursor CLI"""
    cmd = ['cursor', '--command', command, project_path]
    return subprocess.run(cmd, capture_output=True, text=True)
```

### **Limitaciones Identificadas:**
- **No hay API REST**: Solo comandos de línea
- **Sin control granular**: No se puede controlar generación paso a paso
- **Dependencia de conexión**: Requiere internet para IA
- **Sin supervisión automática**: No hay modo "supervisor"

---

## 🏗️ Arquitectura Propuesta

### **Componente 1: Cursor Supervisor**
```python
class CursorSupervisor:
    def __init__(self, project_path, check_interval=300):
        self.project_path = project_path
        self.check_interval = check_interval
        self.cursor_process = None
        self.bitacora_path = os.path.join(project_path, 'BITACORA.md')
        
    def start_supervision(self):
        """Iniciar supervisión continua"""
        while True:
            self.check_project_health()
            self.update_bitacora()
            time.sleep(self.check_interval)
    
    def check_project_health(self):
        """Verificar salud del proyecto"""
        # Verificar estructura de directorios
        # Detectar archivos fuera de lugar
        # Identificar redundancias
        # Revisar logs de Cursor
        pass
```

### **Componente 2: Cursor Generator**
```python
class CursorGenerator:
    def __init__(self, project_path, roadmap_path):
        self.project_path = project_path
        self.roadmap_path = roadmap_path
        self.current_task = None
        
    def generate_code(self, task_description):
        """Generar código según tarea específica"""
        # Abrir Cursor con contexto específico
        # Proporcionar instrucciones claras
        # Monitorear progreso
        pass
```

### **Componente 3: Project Monitor**
```python
class ProjectMonitor:
    def __init__(self, project_path):
        self.project_path = project_path
        self.last_check = None
        
    def detect_issues(self):
        """Detectar problemas en el proyecto"""
        issues = []
        
        # Verificar estructura
        if not os.path.exists('tests/'):
            issues.append("Directorio tests/ no encontrado")
            
        # Verificar archivos fuera de lugar
        root_files = [f for f in os.listdir('.') if f.endswith('_test.py')]
        if root_files:
            issues.append(f"Archivos de test en raíz: {root_files}")
            
        return issues
```

---

## 🚀 Plan de Implementación

### **Fase 1: Investigación y Prototipo**
- [ ] Documentar capacidades completas de Cursor CLI
- [ ] Crear prototipo básico de supervisión
- [ ] Probar integración con proyectos existentes

### **Fase 2: Desarrollo del Supervisor**
- [ ] Implementar CursorSupervisor
- [ ] Crear sistema de detección de problemas
- [ ] Desarrollar actualización automática de bitácora

### **Fase 3: Integración con Generador**
- [ ] Modificar init_project.py para incluir supervisión
- [ ] Crear sistema de instrucciones para Cursor
- [ ] Implementar monitoreo de progreso

### **Fase 4: Testing y Optimización**
- [ ] Probar con diferentes tipos de proyecto
- [ ] Optimizar frecuencia de supervisión
- [ ] Refinar detección de problemas

---

## 📊 Métricas de Éxito

### **Objetivos Cuantitativos:**
- **Reducción de intervención manual**: 80%
- **Archivos fuera de lugar**: 0%
- **Redundancias detectadas**: 95%
- **Tiempo de corrección**: -70%

### **Objetivos Cualitativos:**
- **Experiencia de usuario**: Sin intervención constante
- **Calidad de código**: Consistente y organizado
- **Mantenibilidad**: Proyectos bien estructurados
- **Automatización**: Proceso completamente automático

---

## 🔧 Consideraciones Técnicas

### **Dependencias:**
- `subprocess`: Para ejecutar comandos de Cursor
- `watchdog`: Para monitoreo de archivos
- `schedule`: Para tareas programadas
- `psutil`: Para monitoreo de procesos

### **Configuración:**
```yaml
cursor_supervisor:
  check_interval: 300  # segundos
  max_issues: 10
  auto_fix: true
  
cursor_generator:
  timeout: 3600  # segundos
  retry_attempts: 3
  backup_enabled: true
```

### **Logging:**
- **Supervisor**: `logs/supervisor.log`
- **Generator**: `logs/generator.log`
- **Issues**: `logs/issues.log`

---

## 🎯 Próximos Pasos

1. **Investigar más a fondo** las capacidades de Cursor CLI
2. **Crear prototipo básico** de supervisión
3. **Probar integración** con proyecto de ejemplo
4. **Iterar y mejorar** basado en resultados

---

**Estado**: 🔬 En Investigación  
**Prioridad**: 🔥 Alta  
**Complejidad**: ⚡ Media-Alta
