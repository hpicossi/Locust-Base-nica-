# Datos de prueba para persona física
body_insertar_persona_fisica = {
    "p_cuil": "24492837632",
    "p_nombre": "PRUEBA KUNAN",
    "p_apellido": "PRUEBA KUNAN",
    "p_fecha_nacimiento": "1990-01-15",
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos para insertar persona física por DNI
body_insertar_persona_fisica_by_dni = {
    "p_dni": "49283763",  # DNI sin dígito verificador
    "p_sexo": "04",        
    "p_nombre": "PRUEBA KUNAN",
    "p_apellido": "PRUEBA KUNAN",
    "p_fecha_nacimiento": "1990-01-15",
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos para insertar persona física simplificada
body_insertar_persona_fisica_simplificada = {
  "p_cuil": "20151230300",
  "p_id_tipo_documento": 4,
  "p_dni": "15123030",
  "p_id_pais_origen_docto": 19,
  "p_sexo": "01",
  "p_nombre": "string",
  "p_apellido": "string",
  "p_fecha_nacimiento": "1992-05-27",
  "p_usuario_aplicacion": "string"
}

# Parámetros para consultar persona física
parametros_consulta_persona_fisica = [
    {"p_cuil": "24492837632"},  # Consulta por CUIL
    {"p_dni": "49283763", "p_sexo": "04"},  # Consulta por DNI y sexo
    {"p_dni": "49283763", "p_sexo": "04", "p_id_pais_nacionalidad": 1}  # Consulta completa
]


# Datos para insertar domicilio de persona física
body_insertar_domicilio_persona_fisica = {
  "p_tipo_domicilio": "LEGAL",
  "p_id_persona_fisica": 9233499,
  "p_id_localidad": 1,
  "p_id_barrio": 250,
  "p_id_calle": "866",
  "p_barrio": "ASDF",
  "p_calle": "Hola",
  "p_altura": "1440",
  "p_piso": "279",
  "p_codigo_postal": "5000",
  "p_dpto": "stri",
  "p_manzana": "stri",
  "p_lote": "stri",
  "p_torre": "string",
  "p_oficina_local": "stri",
  "p_usuario_aplicacion": "PRUEBA"
}

# Parámetros para consultar comunicaciones de personas
parametros_consulta_comunicaciones = [
    {"p_cuil_cuit": "24492837632"},  # Consulta por CUIL (persona física)
    {"p_cuil_cuit": "30372159614"},  # Consulta por CUIT (persona jurídica)
    {"p_telefono": "3512345678"},    # Consulta por teléfono
    {"p_correo_electronico": "prueba@example.com"}  # Consulta por correo electrónico
]

# Datos para insertar comunicaciones de personas
body_insertar_comunicaciones_personas = [
    {
        # Persona física
        "p_cuil_cuit": "24492837632",
        "p_nombre": "PRUEBA KUNAN",
        "p_tipo_persona": "PF",
        "p_telefono": "3512345678",
        "p_correo_electronico": "prueba.pf@example.com",
        "p_usuario_aplicacion": "PRUEBA KUNAN"
    },
    {
        # Persona jurídica
        "p_cuil_cuit": "30372159614",
        "p_nombre": "EMPRESA DE PRUEBA",
        "p_tipo_persona": "PJ",
        "p_telefono": "3514567890",
        "p_correo_electronico": "prueba.pj@example.com",
        "p_usuario_aplicacion": "PRUEBA KUNAN"
    }
]
