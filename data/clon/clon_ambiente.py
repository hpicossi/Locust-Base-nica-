# Placeholder para futuros datos de ambiente si se necesitan
ambiente_config = {
    "descripcion": "Datos de configuración para pruebas del módulo ambiente",
    "version": "1.0"
}

# Datos de prueba para consulta de campanas PET
campanas_pet_config = {
    "descripcion": "Configuración para consulta de campanas PET de Córdoba",
    "tipos_esperados": ["Campana PET", "Eco Punto", "Centro Verde"],
    "campos_esperados": ["id", "nombre", "tipo", "ubicacion", "direccion", "barrio", "coordenadas"]
}

# Datos de prueba para consulta de recolección diferenciada de residuos
recoleccion_residuos_config = {
    "descripcion": "Configuración para consulta de recolección diferenciada de residuos",
    "tipos_residuos": ["Orgánicos", "Reciclables", "Especiales", "Voluminosos"],
    "dias_semana": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
}

# Parámetros de consulta para recolección de residuos
parametros_recoleccion_residuos = [
    {},
    #Falta de agregar los query params correspondientes a cada consulta
]
