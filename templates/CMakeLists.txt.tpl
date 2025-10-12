cmake_minimum_required(VERSION 3.16)
project($NOMBRE_PROYECTO VERSION 1.0.0 LANGUAGES CXX)

# Configuración del compilador
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Opciones de compilación
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)

# Directorios de inclusión
include_directories(src)

# Archivos fuente principales
set(SOURCES
    src/$MODULO_PRINCIPAL.cpp
    src/utils/logger.cpp
)

set(HEADERS
    src/$MODULO_PRINCIPAL.hpp
    src/utils/logger.hpp
)

# Crear biblioteca principal
add_library($MODULO_PRINCIPAL STATIC ${SOURCES} ${HEADERS})

# Configurar propiedades de la biblioteca
set_target_properties($MODULO_PRINCIPAL PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
)

# Ejecutable principal
add_executable($NOMBRE_PROYECTO src/main.cpp)
target_link_libraries($NOMBRE_PROYECTO $MODULO_PRINCIPAL)

# Tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Ejemplos
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Instalación
install(TARGETS $MODULO_PRINCIPAL $NOMBRE_PROYECTO
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES ${HEADERS} DESTINATION include/$MODULO_PRINCIPAL)
