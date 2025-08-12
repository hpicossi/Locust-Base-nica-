# Parámetros para consultar medios de pago
parametros_medios_pagos = {}

# Parámetros con filtro por nombre (opcional)
parametros_medios_pagos_con_filtro = {
    "p_nombre": "Getnet"  # Filtrar por nombre específico (min 3, max 150 caracteres)
}

# Parámetros alternativos para probar diferentes filtros de medios de pago
parametros_medios_pagos_alternativos = [
    # Sin filtros (todos los medios de pago)
    {}
]

# IDs de banco para probar el endpoint de consulta por ID
ids_banco = [1]  # IDs de bancos existentes en producción

# IDs de profesión para probar el endpoint de consulta por ID
ids_profesion = [1]  # IDs de profesiones existentes en producción

# Bodies para crear/actualizar medios de pago
body_medios_pagos = [
    {
        "p_nombre": "EFECTIVO_TEST",
        "p_usuario_aplicacion": "usuario_test"
    },
    {
        "p_nombre": "TARJETA_CREDITO_TEST", 
        "p_usuario_aplicacion": "usuario_test"
    }
]

# Parámetros para consultar actividades
parametros_actividades = [
    {"p_nombre": "FABRICACIÓN DE HILADOS TEXTILES DE ALGODÓN Y SUS MEZCLAS"},
    {"p_codigo_afip": "131132"},
    {"p_id_actividad": 779}
]
