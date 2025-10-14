#!/bin/bash
# Autocompletado para Pre-Cursor CLI
# Instalar con: source <(pre-cursor --completion)

_pre_cursor_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Comandos principales
    local commands="create template generate list-types info"
    
    # Opciones globales
    local global_opts="--verbose --version --help --config"
    
    # Tipos de proyecto
    local project_types="Python-Library Python-CLI-Tool Python-Web-App-Flask Python-Web-App-Django Python-Web-App-FastAPI Python-Data-Science Python-ML-AI C++-Project Node.js-Project TD_MCP-Project Otro"
    
    case "${prev}" in
        pre-cursor)
            COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            return 0
            ;;
        create)
            if [[ ${cur} == -* ]]; then
                COMPREPLY=( $(compgen -W "--path --type --interactive --help" -- ${cur}) )
            else
                # Sugerir nombres de proyecto basados en directorio actual
                COMPREPLY=( $(compgen -f -- ${cur}) )
            fi
            return 0
            ;;
        --type|-t)
            COMPREPLY=( $(compgen -W "${project_types}" -- ${cur}) )
            return 0
            ;;
        template)
            COMPREPLY=( $(compgen -W "--type --output --format --help" -- ${cur}) )
            return 0
            ;;
        generate)
            COMPREPLY=( $(compgen -W "--dry-run --help" -- ${cur}) )
            return 0
            ;;
        list-types|info)
            COMPREPLY=( $(compgen -W "--examples --help" -- ${cur}) )
            return 0
            ;;
        --format)
            COMPREPLY=( $(compgen -W "json yaml" -- ${cur}) )
            return 0
            ;;
        --output|-o)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
        --path|-p)
            COMPREPLY=( $(compgen -d -- ${cur}) )
            return 0
            ;;
        --config|-c)
            COMPREPLY=( $(compgen -f -X "!*.{json,yaml,yml}" -- ${cur}) )
            return 0
            ;;
    esac
    
    # Si no hay contexto específico, mostrar comandos y opciones globales
    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "${global_opts}" -- ${cur}) )
    else
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
    fi
}

complete -F _pre_cursor_completion pre-cursor

# Función de ayuda para mostrar ejemplos
_pre_cursor_help() {
    echo "🚀 Pre-Cursor CLI - Ejemplos de uso:"
    echo ""
    echo "Comandos básicos:"
    echo "  pre-cursor create mi-proyecto"
    echo "  pre-cursor create mi-api --type 'Python Web App (FastAPI)'"
    echo "  pre-cursor template --type 'Python Library'"
    echo "  pre-cursor generate mi_config.json"
    echo ""
    echo "Comandos informativos:"
    echo "  pre-cursor list-types"
    echo "  pre-cursor info --examples"
    echo ""
    echo "Opciones avanzadas:"
    echo "  pre-cursor create mi-proyecto --interactive"
    echo "  pre-cursor generate config.yaml --dry-run"
    echo "  pre-cursor --verbose create mi-proyecto"
}

# Alias para ayuda rápida
alias pre-cursor-help='_pre_cursor_help'
