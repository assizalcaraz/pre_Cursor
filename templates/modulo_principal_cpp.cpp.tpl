#include "$MODULO_PRINCIPAL.hpp"
#include "utils/logger.hpp"
#include <iostream>
#include <stdexcept>

namespace $NOMBRE_PROYECTO {

$CLASE_PRINCIPAL::$CLASE_PRINCIPAL() {
    logger::info("$CLASE_PRINCIPAL inicializada");
}

$CLASE_PRINCIPAL::~$CLASE_PRINCIPAL() {
    logger::info("$CLASE_PRINCIPAL destruida");
}

void $CLASE_PRINCIPAL::ejecutar() {
    try {
        logger::info("Ejecutando $CLASE_PRINCIPAL");
        {{IMPLEMENTACION_METODO_PRINCIPAL}}
        logger::info("$CLASE_PRINCIPAL ejecutada exitosamente");
    } catch (const std::exception& e) {
        logger::error("Error en $CLASE_PRINCIPAL: " + std::string(e.what()));
        throw;
    }
}

{{METODO_SECUNDARIO_RETORNO}} $CLASE_PRINCIPAL::{{METODO_SECUNDARIO}}({{PARAMETROS_METODO_SECUNDARIO}}) {
    logger::info("Ejecutando {{METODO_SECUNDARIO}}");
    {{IMPLEMENTACION_METODO_SECUNDARIO}}
    return {{RETORNO_METODO_SECUNDARIO}};
}

} // namespace $NOMBRE_PROYECTO
