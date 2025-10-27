# Autocompletado para Pre-Cursor CLI en Fish Shell
# Instalar con: source ~/.config/fish/completions/pre-cursor.fish

# Comandos principales
complete -c pre-cursor -n "not __fish_seen_subcommand_from create template generate list-types info" -a "create" -d "Crear un nuevo proyecto"
complete -c pre-cursor -n "not __fish_seen_subcommand_from create template generate list-types info" -a "template" -d "Generar plantilla de configuración"
complete -c pre-cursor -n "not __fish_seen_subcommand_from create template generate list-types info" -a "generate" -d "Generar proyecto desde configuración"
complete -c pre-cursor -n "not __fish_seen_subcommand_from create template generate list-types info" -a "list-types" -d "Listar tipos de proyecto disponibles"
complete -c pre-cursor -n "not __fish_seen_subcommand_from create template generate list-types info" -a "info" -d "Mostrar información del proyecto"

# Opciones globales
complete -c pre-cursor -s v -l verbose -d "Activar modo verbose"
complete -c pre-cursor -l version -d "Mostrar versión"
complete -c pre-cursor -s h -l help -d "Mostrar ayuda"
complete -c pre-cursor -s c -l config -r -d "Archivo de configuración"

# Comando create
complete -c pre-cursor -n "__fish_seen_subcommand_from create" -s p -l path -r -d "Ruta donde crear el proyecto"
complete -c pre-cursor -n "__fish_seen_subcommand_from create" -s t -l type -d "Tipo de proyecto"
complete -c pre-cursor -n "__fish_seen_subcommand_from create" -l interactive -d "Modo interactivo"
complete -c pre-cursor -n "__fish_seen_subcommand_from create" -s h -l help -d "Mostrar ayuda"

# Tipos de proyecto para --type
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-Library" -d "Biblioteca de Python"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-CLI-Tool" -d "Herramienta CLI de Python"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-Web-App-Flask" -d "Aplicación web Flask"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-Web-App-Django" -d "Aplicación web Django"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-Web-App-FastAPI" -d "Aplicación web FastAPI"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-Data-Science" -d "Proyecto de ciencia de datos"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Python-ML-AI" -d "Proyecto de ML/AI"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "C++-Project" -d "Proyecto C++"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Node.js-Project" -d "Proyecto Node.js"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "TD_MCP-Project" -d "Proyecto TD_MCP"
complete -c pre-cursor -n "__fish_seen_subcommand_from create; and __fish_seen_argument_from -s t --type" -a "Otro" -d "Otro tipo de proyecto"

# Comando template
complete -c pre-cursor -n "__fish_seen_subcommand_from template" -s t -l type -d "Tipo de proyecto"
complete -c pre-cursor -n "__fish_seen_subcommand_from template" -s o -l output -r -d "Archivo de salida"
complete -c pre-cursor -n "__fish_seen_subcommand_from template" -l format -a "json yaml" -d "Formato de salida"
complete -c pre-cursor -n "__fish_seen_subcommand_from template" -s h -l help -d "Mostrar ayuda"

# Comando generate
complete -c pre-cursor -n "__fish_seen_subcommand_from generate" -l dry-run -d "Simular generación sin crear archivos"
complete -c pre-cursor -n "__fish_seen_subcommand_from generate" -s h -l help -d "Mostrar ayuda"

# Comando list-types
complete -c pre-cursor -n "__fish_seen_subcommand_from list-types" -l examples -d "Mostrar ejemplos"
complete -c pre-cursor -n "__fish_seen_subcommand_from list-types" -s h -l help -d "Mostrar ayuda"

# Comando info
complete -c pre-cursor -n "__fish_seen_subcommand_from info" -l examples -d "Mostrar ejemplos"
complete -c pre-cursor -n "__fish_seen_subcommand_from info" -s h -l help -d "Mostrar ayuda"

# Función de ayuda para Fish
function pre-cursor-help
    echo "🚀 Pre-Cursor CLI - Ejemplos de uso:"
    echo ""
    echo "Comandos básicos:"
    echo "  pre-cursor create mi-proyecto"
    echo "  pre-cursor create mi-api --type 'Python-Web-App-FastAPI'"
    echo "  pre-cursor template --type 'Python-Library'"
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
end
