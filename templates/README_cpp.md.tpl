# {{NOMBRE_PROYECTO}}

{{DESCRIPCION_PROYECTO}}

## 🚀 Inicio Rápido

### Requisitos
- CMake 3.16+
- Compilador C++17 compatible (GCC, Clang, MSVC)
- Git

### Instalación
```bash
# Clonar el repositorio
git clone {{REPOSITORIO_URL}}
cd {{NOMBRE_PROYECTO}}

# Crear directorio de build
mkdir build && cd build

# Configurar con CMake
cmake ..

# Compilar
make  # o ninja, o usar el IDE

# Ejecutar tests
ctest
```

### Uso Básico
```cpp
#include "{{MODULO_PRINCIPAL}}.hpp"

int main() {
    {{CLASE_PRINCIPAL}} proyecto;
    proyecto.ejecutar();
    return 0;
}
```

## 📁 Estructura del Proyecto

```
{{NOMBRE_PROYECTO}}/
├── README.md                    # Este archivo
├── BITACORA.md                 # Log de desarrollo
├── roadmap_v1.md               # Plan de desarrollo
├── CMakeLists.txt              # Configuración de CMake
├── src/                        # Código fuente
│   ├── {{MODULO_PRINCIPAL}}.cpp
│   ├── {{MODULO_PRINCIPAL}}.hpp
│   └── utils/                  # Utilidades
├── tests/                      # Pruebas
│   ├── README.md              # Instrucciones de testing
│   ├── test_{{MODULO_PRINCIPAL}}.cpp
│   └── CMakeLists.txt
├── docs/                       # Documentación
├── examples/                   # Ejemplos
└── build/                      # Directorio de compilación
```

## 🧪 Testing

Seguir las instrucciones en `tests/README.md` para ejecutar las pruebas.

```bash
# Compilar tests
cd build
make tests

# Ejecutar tests
./tests/test_{{MODULO_PRINCIPAL}}
```

## 📚 Documentación

- [Tutorial de Inicio](docs/TUTORIAL.md)
- [API Reference](docs/API.md)
- [Contributing](CONTRIBUTING.md)

## 🔧 Compilación

### CMake
```bash
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)
```

### Configuraciones Disponibles
- **Debug**: `-DCMAKE_BUILD_TYPE=Debug`
- **Release**: `-DCMAKE_BUILD_TYPE=Release`
- **RelWithDebInfo**: `-DCMAKE_BUILD_TYPE=RelWithDebInfo`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'WIP: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia {{LICENCIA}} - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**{{AUTOR}}**
- GitHub: [@{{GITHUB_USER}}](https://github.com/{{GITHUB_USER}})

## 📞 Contacto

{{EMAIL_CONTACTO}}

---

**Fecha de Creación**: {{FECHA_CREACION}}  
**Última Actualización**: {{FECHA_ACTUALIZACION}}
