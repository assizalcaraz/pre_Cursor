#!/usr/bin/env bash
# Script de inicio rápido para el Generador de Proyectos

echo "🚀 Generador de Proyectos Optimizado para Agentes de IA"
echo "=================================================="
echo ""

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar que Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git no está instalado. Por favor instala Git."
    exit 1
fi

echo "✅ Python y Git están disponibles"
echo ""

# Ejecutar el generador
python3 init_project.py "$@"
