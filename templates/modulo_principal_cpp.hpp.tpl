#ifndef {{MODULO_PRINCIPAL_UPPER}}_HPP
#define {{MODULO_PRINCIPAL_UPPER}}_HPP

#include <string>
#include <vector>
#include <memory>

namespace $NOMBRE_PROYECTO {

/**
 * @class $CLASE_PRINCIPAL
 * @brief {{DESCRIPCION_CLASE_PRINCIPAL}}
 * 
 * Esta clase proporciona {{FUNCIONALIDAD_PRINCIPAL}}.
 */
class $CLASE_PRINCIPAL {
public:
    /**
     * @brief Constructor por defecto
     */
    $CLASE_PRINCIPAL();
    
    /**
     * @brief Destructor
     */
    ~$CLASE_PRINCIPAL();
    
    /**
     * @brief Ejecutar funcionalidad principal
     * @throws std::runtime_error Si ocurre un error durante la ejecución
     */
    void ejecutar();
    
    /**
     * @brief {{DESCRIPCION_METODO_SECUNDARIO}}
     * @param {{PARAMETROS_METODO_SECUNDARIO_DOC}}
     * @return {{DESCRIPCION_RETORNO_METODO_SECUNDARIO}}
     */
    {{METODO_SECUNDARIO_RETORNO}} {{METODO_SECUNDARIO}}({{PARAMETROS_METODO_SECUNDARIO}});

private:
    // Miembros privados
    std::string nombre_;
    bool inicializado_;
    
    /**
     * @brief Método privado auxiliar
     */
    void inicializar();
};

} // namespace $NOMBRE_PROYECTO

#endif // {{MODULO_PRINCIPAL_UPPER}}_HPP
