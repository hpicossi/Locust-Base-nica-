# Lista de IDs de localidades para consultar barrios
ids_localidades = [
    1    # Córdoba Capital
    #650  # Otra localidad de ejemplo
]

# Datos para consulta de domicilios
datos_domicilio = {
    "id_provincia": 22,     # Córdoba
    "id_departamento": 3,   # Capital
    "id_localidad": 1,      # Córdoba Capital
    "id_barrio": 21,        # Barrio de ejemplo
    "id_calle": 8           # Calle de ejemplo
}

# Lista de textos para búsqueda de calles por nombre
busquedas_calles = [
    "SAN",     # Para encontrar calles como "SAN MARTIN", "SAN JERÓNIMO", etc.
    "AV",      # Para encontrar avenidas
    "COLON",   # Para encontrar calles relacionadas con Colón
    "GENERAL", # Para encontrar calles como "GENERAL PAZ", etc.
    ""         # Para obtener todas las calles (sin filtro)
]

# Datos para consulta de domicilios
datos_domicilio = {
    "id_provincia": 22,     # Córdoba
    "id_departamento": 3,   # Capital
    "id_localidad": 1,      # Córdoba Capital
    "id_barrio": 21,        # Barrio de ejemplo
    "id_calle": 8           # Calle de ejemplo
}

# Datos esperados para países (algunos ejemplos para validación)
paises_esperados = [
    {"id_pais": 19, "nombre": "ARGENTINA"},
    {"id_pais": 20, "nombre": "ARMENIA"}
]

# Campos esperados en la respuesta de países
campos_esperados_paises = ["id_pais", "nombre"]

# Países de interés para logging (opcional)
paises_interes = ["ARGENTINA", "BRASIL", "CHILE", "URUGUAY", "PARAGUAY", "BOLIVIA"]

# Mapeo de países conocidos con sus IDs (se actualizará dinámicamente)
paises_conocidos = {
    "ARGENTINA": None,  # Se llenará dinámicamente
    "BRASIL": None,
    "CHILE": None,
    "URUGUAY": None
}

# IDs de provincias para consultar departamentos
ids_provincias = [
    22,  # Córdoba
    1,   # Buenos Aires (probablemente)
    2,   # Catamarca (probablemente)
    # Agregar más IDs según sea necesario
]

# Datos esperados para departamentos (algunos ejemplos para validación)
departamentos_esperados = [
    {"id_departamento": 1, "nombre": "CAPITAL"},
    {"id_departamento": 26, "nombre": "UNION"},
    {"id_departamento": 3, "nombre": "CAPITAL"}  # Capital de Córdoba
]

# Campos esperados en la respuesta de departamentos
campos_esperados_departamentos = ["id_departamento", "nombre"]

# Departamentos de interés para logging (opcional)
departamentos_interes = ["CAPITAL", "UNION", "COLON", "PUNILLA", "SANTA MARIA"]

# Mapeo de provincias conocidas con sus IDs (se actualizará dinámicamente)
provincias_conocidas = {
    "CÓRDOBA": 22,  # ID conocido
    "BUENOS AIRES": None,  # Se llenará dinámicamente
    "SANTA FE": None,
    "MENDOZA": None
}

# Mapeo de departamentos conocidos con sus IDs (se actualizará dinámicamente)
departamentos_conocidos = {
    "CAPITAL": None,  # Se llenará dinámicamente
    "UNION": 26,      # ID conocido
    "COLON": None,
    "PUNILLA": None
}

# Datos de prueba para insertar domicilios

# Domicilio en Córdoba Capital (con IDs de barrio y calle)
body_insertar_domicilio_cordoba = {
    "p_id_localidad": 1,  
    "p_id_barrio": 21,    
    "p_id_calle": 8,     
    "p_barrio": None,     
    "p_calle": None,      
    "p_altura": "1234",   
    "p_piso": "2",        
    "p_dpto": "A",        
    "p_manzana": None,    
    "p_lote": None,       
    "p_torre": None,     
    "p_oficina_local": None,  
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Domicilio fuera de Córdoba Capital (con nombres de barrio y calle)
body_insertar_domicilio_interior = {
    "p_id_localidad": 650,  # Otra localidad (no Córdoba Capital)
    "p_id_barrio": None,    # No se usa fuera de Córdoba Capital
    "p_id_calle": None,     # No se usa fuera de Córdoba Capital
    "p_barrio": "CENTRO",   # Nombre del barrio
    "p_calle": "AVENIDA SAN MARTIN",  # Nombre de la calle
    "p_altura": "567",      # Número de puerta
    "p_piso": None,         # Sin piso
    "p_dpto": None,         # Sin departamento
    "p_manzana": "12",      # Manzana
    "p_lote": "5",          # Lote
    "p_torre": None,        # Sin torre
    "p_oficina_local": None,  # Sin oficina
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Domicilio sin número (SN)
body_insertar_domicilio_sin_numero = {
    "p_id_localidad": 1,    # Córdoba Capital
    "p_id_barrio": 21,      # ID del barrio en Córdoba
    "p_id_calle": 8,        # ID de la calle en Córdoba
    "p_barrio": None,       # No se usa cuando se tiene ID
    "p_calle": None,        # No se usa cuando se tiene ID
    "p_altura": "SN",       # Sin número
    "p_piso": None,         # Sin piso
    "p_dpto": None,         # Sin departamento
    "p_manzana": None,      # Sin manzana
    "p_lote": None,         # Sin lote
    "p_torre": None,        # Sin torre
    "p_oficina_local": None,  # Sin oficina
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Domicilio comercial con oficina/local

# Datos de prueba para insertar domicilio comercial (caso único)
body_insertar_domicilio_comercial = {
    "p_id_localidad": 1,
    "p_id_barrio": 250,
    "p_id_calle": 866,
    "p_barrio": "PATRICIOS",
    "p_calle": "string",
    "p_altura": "2905",
    "p_piso": "string",
    "p_dpto": "4",
    "p_manzana": "stri",
    "p_lote": "stri",
    "p_torre": "string",
    "p_oficina_local": "stri",
    "p_usuario_aplicacion": "Prueba Kunan"
}

# Datos de prueba para insertar domicilio ampliado
body_insertar_domicilio_ampliado = {
    "p_id_localidad": 1,
    "p_id_barrio": 250,
    "p_id_calle": 866,
    "p_barrio": "PATRICIOS",
    "p_calle": None,
    "p_altura": "2950",
    "p_piso": "string",
    "p_dpto": "strin",
    "p_manzana": "stri",
    "p_lote": "stri",
    "p_torre": "string",
    "p_oficina_local": "stri",
    "p_usuario_aplicacion": "PRUEBA",
    "id_calle_perp1": None,
    "id_calle_perp2": None,
    "p_observaciones": "string",
    "p_latitud": -31.376654,
    "p_longitud": -64.139906
}

# Datos de prueba para insertar domicilio geo
body_insertar_domicilio_geo = {
    "p_id_localidad": 1,
    "p_id_calle": "866",
    "p_calle": "string",
    "p_altura": "2905",
    "p_piso": "string",
    "p_dpto": "strin",
    "p_manzana": "stri",
    "p_lote": "stri",
    "p_torre": "string",
    "p_oficina_local": "stri",
    "p_id_calle_perp1": "3064", 
    "p_id_calle_perp2":"4125", 
    "p_observaciones": "stringss",
    "p_usuario_aplicacion": "prueba"
}

# Datos de prueba para consultar domicilio geo
query_params_domicilio_geo = {
    "p_id_localidad": 1,  # Solo acepta Córdoba Capital
    "p_id_calle": 866,    # ID de calle válido en Córdoba
    "p_altura": "2950"    # Altura/número de puerta
}

# Lista de parámetros para múltiples consultas geo
lista_consultas_domicilio_geo = [
    {"p_id_localidad": 1, "p_id_calle": 866, "p_altura": "2950"}
]

# Datos de prueba para consultar domicilio por ID
lista_ids_domicilios = [15]  # IDs de domicilios para consultar

# ID específico para consulta individual
id_domicilio_consulta = 1

# Datos de prueba para insertar/actualizar incidentes
body_insertar_incidente = {
    "p_id_domicilio": 15,  # ID de domicilio válido (se actualizará dinámicamente)
    "p_numero_incidente": "INC-2024-001",
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Lista de incidentes para pruebas múltiples
lista_incidentes = [
    {
        "p_id_domicilio": 15,
        "p_numero_incidente": "INC-2024-001",
        "p_usuario_aplicacion": "PRUEBA KUNAN"
    }
]

# Parámetros para consultar domicilio con CPC por ID
parametros_domicilio_cpc = {
    "p_id_domicilio": 43  # ID del domicilio en base única (path parameter)
}

# Comentarios sobre el endpoint de domicilio con CPC
parametros_domicilio_cpc_comentados = {
    # Este endpoint consulta un domicilio por su ID en base única con información del CPC
    # Usa p_id_domicilio como PATH PARAMETER (no query parameter)
    # Formato de URL: /domicilios/cpc/{p_id_domicilio}
    # Retorna DomicilioCPCResponseSchema con información completa:
    # - Datos básicos del domicilio (id, país, provincia, departamento, localidad)
    # - Información de ubicación (barrio, calle, altura, piso, dpto, etc.)
    # - Coordenadas geográficas (latitud, longitud)
    # - Información del CPC correspondiente (p_id_cpc, p_cpc)
    # - Calles perpendiculares (p_id_calle_perp1/2, p_calle_perp1/2)
    # - Metadatos (fecha_creacion, fecha_modifica, usuario_aplicacion)
    # - Validación (p_valido: "S" si se pudo validar altura y edificio)
    #
    # El endpoint requiere permisos específicos (servicio_context 145)
    # URL: /domicilios/cpc/{p_id_domicilio}
    # Método: GET
    # Response: DomicilioCPCResponseSchema
    #
    # NOTA: p_id_domicilio debe ser un ID válido existente en base única
    # Si el ID no existe, retornará error 404
}
