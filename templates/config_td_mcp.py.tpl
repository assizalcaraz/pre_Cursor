# Configuración del Proyecto $NOMBRE_PROYECTO
# $DESCRIPCION_PROYECTO

# Configuración del servidor MCP
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8000

# Configuración de TouchDesigner
TOUCHDESIGNER_HOST = "localhost"
TOUCHDESIGNER_PORT = 8080

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de archivos
TOX_FILES_PATH = "./examples/tox_files"
TEMP_PATH = "./temp"

# Configuración de seguridad
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_FILE_EXTENSIONS = [".tox", ".toe"]

# Configuración de timeouts
CONNECTION_TIMEOUT = 30  # segundos
OPERATION_TIMEOUT = 60   # segundos

# Configuración específica del proyecto
PROJECT_NAME = "$NOMBRE_PROYECTO"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "$DESCRIPCION_PROYECTO"
PROJECT_AUTHOR = "$AUTOR"
PROJECT_EMAIL = "$EMAIL_CONTACTO"
PROJECT_GITHUB = "$GITHUB_USER"

# Configuración de entorno
ENVIRONMENT = "development"  # development, testing, staging, production

# Configuración de TouchEngine SDK
TOUCHENGINE_SDK_URL_MACOS = "https://github.com/TouchDesigner/TouchEngine-macOS"
TOUCHENGINE_SDK_URL_WINDOWS = "https://github.com/TouchDesigner/TouchEngine-Windows"

# Configuración de desarrollo
DEBUG = True
VERBOSE_LOGGING = False

# Configuración de deployment
DEPLOYMENT_CONFIG = {
    "docker": True,
    "kubernetes": True,
    "health_monitoring": True
}
