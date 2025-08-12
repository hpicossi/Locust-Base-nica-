p_nivel=[4]

p_id_dependencia = [9226]

body_ids_dependencias = [9226, 8182]

lista_id_dependencia = [9226, 8182]

# Fechas para consultar días no hábiles (formato DD/MM/YYYY)
# Aclaracion se tiene que poner una fecha maxima de 100 dias y por otro lado tiene que estar sujeto al año actual si estas en 2025 lo deberias de usar en 2025 unicamente
fechas_consulta = {
    "desde": "01/10/2025",
    "hasta": "31/12/2025"
}

# Datos de prueba para actualizar visibilidad de dependencias
body_update_visibilidad_dependencia = {
    "p_id_dependencia": 9226,  # ID de dependencia a actualizar
    "p_visible": 'N',  # Cambiar visibilidad (True o False)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Lista de IDs de dependencias para probar actualización de visibilidad
lista_ids_update_visibilidad = [9226]

# Parámetros de consulta para actualizar visibilidad
query_params_update_visibilidad = {
    "p_id_dependencia": 9226,
    "p_visible": 'S',
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Fechas para consultar días no hábiles (formato DD/MM/YYYY)
# Aclaración: se tiene que poner una fecha máxima de 100 días y por otro lado tiene que estar sujeto al año actual
# Si estás en 2025 lo deberías de usar en 2025 únicamente
fechas_consulta = {
    "desde": "01/10/2025",
    "hasta": "31/12/2025"
}

# Múltiples rangos de fechas para probar diferentes escenarios
rangos_fechas_no_habiles = [
    {
        "p_fecha_desde": "01/01/2025",
        "p_fecha_hasta": "31/01/2025"
    },
    {
        "p_fecha_desde": "01/05/2025",
        "p_fecha_hasta": "31/05/2025"
    },
    {
        "p_fecha_desde": "01/12/2025",
        "p_fecha_hasta": "31/12/2025"
    },
    {
        "p_fecha_desde": "15/07/2025",
        "p_fecha_hasta": "15/08/2025"
    }
]

# Datos para organizaciones sociales
organizaciones_sociales_params = {
    "p_tipo_org_social": "IGLESIAS",
    "p_id_tipo_org_social": 3
}

# Lista de tipos de organizaciones sociales para probar
tipos_organizaciones_sociales = [
    {"nombre": "IGLESIAS", "id": 3}
]