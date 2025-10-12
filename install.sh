#!/bin/bash
# 🚀 Instalador Automático de Pre-Cursor
# Este script instala Pre-Cursor automáticamente

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Banner de bienvenida
echo -e "${BLUE}"
echo "🚀 Pre-Cursor - Instalador Automático"
echo "====================================="
echo -e "${NC}"

# Paso 1: Verificar Python
print_status "Verificando Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python encontrado: $PYTHON_VERSION"
    
    # Verificar versión mínima
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        print_success "Versión de Python compatible (>=3.8)"
    else
        print_error "Python 3.8+ requerido. Versión actual: $PYTHON_VERSION"
        print_status "Instalando Python 3.8..."
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command_exists brew; then
                brew install python@3.8
            else
                print_error "Homebrew no encontrado. Instala Python manualmente desde python.org"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            sudo apt update
            sudo apt install -y python3.8 python3.8-pip
        else
            print_error "Sistema operativo no soportado. Instala Python manualmente."
            exit 1
        fi
    fi
else
    print_error "Python3 no encontrado. Instalando..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install python@3.8
        else
            print_error "Instala Homebrew primero: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt update
        sudo apt install -y python3.8 python3.8-pip
    else
        print_error "Sistema operativo no soportado. Instala Python manualmente desde python.org"
        exit 1
    fi
fi

# Paso 2: Verificar pip
print_status "Verificando pip..."
if command_exists pip3; then
    print_success "pip3 encontrado"
else
    print_status "Instalando pip..."
    python3 -m ensurepip --upgrade
fi

# Paso 3: Verificar Git
print_status "Verificando Git..."
if command_exists git; then
    GIT_VERSION=$(git --version)
    print_success "Git encontrado: $GIT_VERSION"
else
    print_error "Git no encontrado. Instalando..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install git
        else
            print_error "Instala Git manualmente desde git-scm.com"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt install -y git
    else
        print_error "Instala Git manualmente desde git-scm.com"
        exit 1
    fi
fi

# Paso 4: Clonar repositorio
print_status "Descargando Pre-Cursor..."
if [ -d "pre_Cursor" ]; then
    print_warning "Directorio pre_Cursor ya existe. Actualizando..."
    cd pre_Cursor
    git pull
else
    git clone https://github.com/assizalcaraz/pre_Cursor.git
    cd pre_Cursor
fi

# Paso 5: Instalar dependencias
print_status "Instalando Pre-Cursor..."
if pip3 install -e ".[dev]" 2>/dev/null; then
    print_success "Pre-Cursor instalado exitosamente"
else
    print_warning "Instalación con permisos de usuario..."
    pip3 install --user -e ".[dev]"
    print_success "Pre-Cursor instalado exitosamente (modo usuario)"
fi

# Paso 6: Verificar instalación
print_status "Verificando instalación..."
if command_exists pre-cursor; then
    print_success "Comando 'pre-cursor' disponible"
elif python3 cli.py --help >/dev/null 2>&1; then
    print_success "Pre-Cursor instalado (usar: python3 cli.py)"
else
    print_error "Error en la instalación"
    exit 1
fi

# Paso 7: Configurar autocompletado
print_status "Configurando autocompletado..."
if [ -f "completion.sh" ]; then
    echo "source $(pwd)/completion.sh" >> ~/.bashrc 2>/dev/null || true
    echo "source $(pwd)/completion.sh" >> ~/.zshrc 2>/dev/null || true
    print_success "Autocompletado configurado"
fi

# Paso 8: Crear proyecto de prueba
print_status "Creando proyecto de prueba..."
if command_exists pre-cursor; then
    pre-cursor create test_pre_cursor --type "Python Library" >/dev/null 2>&1
elif python3 cli.py create test_pre_cursor --type "Python Library" >/dev/null 2>&1; then
    print_success "Proyecto de prueba creado exitosamente"
else
    print_warning "No se pudo crear proyecto de prueba automáticamente"
fi

# Limpiar proyecto de prueba
if [ -d "test_pre_cursor" ]; then
    rm -rf test_pre_cursor
fi

# Mensaje final
echo -e "${GREEN}"
echo "🎉 ¡Pre-Cursor instalado exitosamente!"
echo "====================================="
echo -e "${NC}"

echo "📚 Comandos útiles:"
echo "  pre-cursor --help              # Ver ayuda"
echo "  pre-cursor list-types          # Ver tipos de proyecto"
echo "  pre-cursor create mi_proyecto  # Crear proyecto"
echo "  pre-cursor info --examples     # Ver ejemplos"

echo ""
echo "📖 Guías disponibles:"
echo "  cat GUIA_SUPER_SIMPLE.md       # Guía súper simple"
echo "  cat GUIA_PASO_A_PASO.md        # Guía detallada"
echo "  cat QUICKSTART.md              # Guía rápida"

echo ""
echo "🚀 ¡Empieza a crear proyectos!"
echo "   pre-cursor create mi_primer_proyecto"

# Configurar PATH si es necesario
if ! command_exists pre-cursor; then
    echo ""
    echo -e "${YELLOW}Nota:${NC} Para usar 'pre-cursor' directamente, ejecuta:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
fi
