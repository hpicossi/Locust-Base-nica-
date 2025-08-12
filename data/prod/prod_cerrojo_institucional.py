p_nivel=[4]

p_id_dependencia = [71]

body_ids_dependencias = [17, 71, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 9231, 9233, 9235, 9237, 9239, 9241, 9242, 9243, 9245, 9246, 9255, 9256, 9262, 9270, 9271, 9278, 9282, 9312, 9457, 9458, 9459, 9460, 9461, 9462, 9463, 9464, 9465, 9466, 9467, 9642, 9643, 9644, 9645, 9646, 9713, 9714, 9715, 9716, 9717, 9743, 9762, 9785, 9787, 9788, 9789, 9811, 9818, 9827, 9833, 9834, 9852, 9857, 9859, 9877, 9883, 9889, 9929, 9931, 10005, 10009, 10010, 10011, 10098, 10099, 10179, 10180, 10268, 10271, 10284, 10351, 10375, 10594, 10600, 10609, 10624, 10639, 10694, 10702, 10744, 10791, 10805]

lista_id_dependencia = [71]

# Fechas para consultar días no hábiles (formato DD/MM/YYYY)
# Aclaracion se tiene que poner una fecha maxima de 100 dias y por otro lado tiene que estar sujeto al año actual si estas en 2025 lo deberias de usar en 2025 unicamente
fechas_consulta = {
    "desde": "01/10/2025",
    "hasta": "31/12/2025"
}

# Datos de prueba para actualizar visibilidad de dependencias
body_update_visibilidad_dependencia = {
    "p_id_dependencia": 9624,  # ID de dependencia a actualizar
    "p_visible": 'S',  # Cambiar visibilidad (True o False)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Lista de IDs de dependencias para probar actualización de visibilidad
lista_ids_update_visibilidad = [9624]

# Parámetros de consulta para actualizar visibilidad
query_params_update_visibilidad = {
    "p_id_dependencia": 9624,
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