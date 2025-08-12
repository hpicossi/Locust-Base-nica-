# Parámetros básicos para consultar chapas (solo paginación)
parametros_chapas = {
    "p_page_number": 1,
    "p_page_size": 20
}

# Parámetros opcionales para chapas (comentados - se pueden activar cuando se conozca la estructura exacta)
parametros_chapas_comentados = {
    # "p_numero_chapa": "ABC123",      # Posible parámetro de número de chapa
    # "p_tipo_vehiculo": "AUTO",       # Posible parámetro de tipo de vehículo
    # "p_estado": "ACTIVO",            # Posible parámetro de estado
    # "p_situacion": 1,                # Posible parámetro de situación
    # "p_fecha_desde": "2024-01-01",   # Posible parámetro de fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Posible parámetro de fecha hasta
    # "p_propietario": "Juan Perez",   # Posible parámetro de propietario
    # "p_cuit_cuil": "20123456789",    # Posible parámetro de CUIT/CUIL
}

# Parámetros para consultar leasing de chapas
parametros_leasing = {
    "p_page_number": 1,
    "p_page_size": 1
}

# Parámetros opcionales para leasing (comentados hasta conocer la estructura exacta)
parametros_leasing_comentados = {
    # "p_numero_chapa": "ABC123",          # Posible parámetro de número de chapa
    # "p_apellido_arrendatario": "PEREZ",  # Posible parámetro de apellido del arrendatario
    # "p_nombre_arrendatario": "JUAN",     # Posible parámetro de nombre del arrendatario
    # "p_dni_arrendatario": "12345678",    # Posible parámetro de DNI del arrendatario
    # "p_cuil_arrendatario": "20123456789", # Posible parámetro de CUIL del arrendatario
    # "p_estado": "ACTIVO",                # Posible parámetro de estado del leasing
    # "p_fecha_desde": "2024-01-01",       # Posible parámetro de fecha desde
    # "p_fecha_hasta": "2024-12-31",       # Posible parámetro de fecha hasta
    # "p_vencimiento_desde": "2024-01-01", # Posible parámetro de vencimiento desde
    # "p_vencimiento_hasta": "2024-12-31", # Posible parámetro de vencimiento hasta
    # "p_tipo_servicio": "TAXI",           # Posible parámetro de tipo de servicio
}

# Parámetros para consultar centrales agencias por CUIT
parametros_centrales_agencias = {
    "p_page_number": 1,
    "p_page_size": 20
}

# Parámetros opcionales para centrales agencias (comentados hasta conocer la estructura exacta)
parametros_centrales_agencias_comentados = {
    # "p_cuit": "20123456789",         # Posible parámetro de CUIT de la central/agencia
    # "p_nombre": "CENTRAL TAXI",      # Posible parámetro de nombre de la central
    # "p_razon_social": "EMPRESA SA",  # Posible parámetro de razón social
    # "p_estado": "ACTIVO",            # Posible parámetro de estado
    # "p_tipo": "CENTRAL",             # Posible parámetro de tipo (CENTRAL/AGENCIA)
    # "p_fecha_desde": "2024-01-01",   # Posible parámetro de fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Posible parámetro de fecha hasta
    # "p_localidad": "CORDOBA",        # Posible parámetro de localidad
    # "p_barrio": "CENTRO",            # Posible parámetro de barrio
}

# Parámetros para consultar persona física por número de chapa (REQUERIDOS)
parametros_persona_fisica_chapa = {
    "p_numero_interno": "3138",  # Número interno de chapa (ejemplo basado en datos anteriores)
    "p_id_tipo_servicio": 6      # ID del tipo de servicio (ejemplo: 3 para taxi)
}

# Parámetros alternativos para probar diferentes chapas
parametros_persona_fisica_chapa_alternativos = {
    "p_numero_interno": "2740",  # Otro número de chapa para probar
    "p_id_tipo_servicio": 3      # Otro tipo de servicio
}

# Parámetros opcionales para persona física por chapa (comentados hasta conocer la estructura exacta)
parametros_persona_fisica_chapa_comentados = {
    # Estos son los parámetros REQUERIDOS que ya están arriba
    # "p_numero_interno": "1234",      # REQUERIDO - Número interno de chapa
    # "p_id_tipo_servicio": 1,         # REQUERIDO - ID tipo servicio (1=taxi, 2=remis, etc.)
    # "p_tipo_servicio": "TAXI",       # Posible parámetro adicional de tipo de servicio como string
    # "p_estado": "ACTIVO",            # Posible parámetro adicional de estado
}

# Parámetros para consultar chapas por CUIL (usando CUIL como path parameter)
parametros_chapas_por_cuil = {
    "p_cuil": "20227952661"  # CUIL real que funciona según la URL proporcionada
}

# Parámetros alternativos para chapas por CUIL (otros CUILs para probar)
parametros_chapas_por_cuil_alternativos = [
    {"p_cuil": "20227952661"},  # CUIL que sabemos que funciona
    {"p_cuil": "20299682545"}
]

# Comentarios sobre el endpoint de chapas por CUIL
parametros_chapas_por_cuil_comentados = {
    # Este endpoint usa el CUIL como PATH PARAMETER, NO como query parameter
    # Formato correcto: /chapas/{cuil}
    # NO: /chapas?p_cuil={cuil}
    # 
    # Ejemplo de URL correcta:
    # https://datos.cordoba.gob.ar/api/base-unica/v3/chapas/20227952661
    #
    # El CUIL debe ser un número válido de 11 dígitos con dígito verificador correcto
    # El endpoint retorna una lista de ChapasPermisionadosSchema
    # Si no encuentra chapas para el CUIL, retorna una lista vacía []
    # Si el CUIL es inválido, retorna error 422 (Unprocessable Entity)
}

# Parámetros para consultar permisionarios por DNI y CUIL
parametros_permisionarios = {
    "p_page_number": 1,
    "p_page_size": 20
}

# Parámetros opcionales para permisionarios (se pueden activar según necesidad)
parametros_permisionarios_con_filtros = {
    "p_page_number": 1,
    "p_page_size": 20,
    # "p_dni": "12345678",             # Filtrar por DNI específico
    # "p_cuil": "20123456789",         # Filtrar por CUIL específico
    # "p_apellido": "PEREZ",           # Filtrar por apellido
    # "p_nombre": "JUAN",              # Filtrar por nombre
    # "p_estado": "ACTIVO",            # Filtrar por estado del permisionario
    # "p_tipo_servicio": "TAXI",       # Filtrar por tipo de servicio
    # "p_fecha_desde": "2024-01-01",   # Filtrar por fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Filtrar por fecha hasta
}

# Parámetros alternativos para probar diferentes filtros de permisionarios
parametros_permisionarios_alternativos = [
    {
        "p_page_number": 1,
        "p_page_size": 10
    }
]

# Comentarios sobre el endpoint de permisionarios
parametros_permisionarios_comentados = {
    # Este endpoint consulta permisionarios por DNI y CUIL
    # Usa paginación obligatoria con p_page_number y p_page_size
    # Retorna PaginationResponseSchema con:
    # - page_number: número de página actual
    # - page_size: tamaño de página
    # - total_items: total de elementos
    # - items: lista de permisionarios
    #
    # Posibles filtros (a confirmar con la API):
    # - p_dni: filtrar por DNI
    # - p_cuil: filtrar por CUIL  
    # - p_apellido: filtrar por apellido
    # - p_nombre: filtrar por nombre
    # - p_estado: filtrar por estado
    # - p_tipo_servicio: filtrar por tipo de servicio
    # - p_fecha_desde/p_fecha_hasta: filtrar por rango de fechas
    #
    # El endpoint requiere permisos específicos (servicio_context 43)
}

# Parámetros para consultar licencias de conducir por DNI y CUIL
parametros_licencias = {
    "p_page_number": 1,
    "p_page_size": 20
}

# Parámetros opcionales para licencias (se pueden activar según necesidad)
parametros_licencias_con_filtros = {
    "p_page_number": 1,
    "p_page_size": 20,
    # "p_dni": "12345678",             # Filtrar por DNI específico
    # "p_cuil": "20123456789",         # Filtrar por CUIL específico
    # "p_apellido": "PEREZ",           # Filtrar por apellido
    # "p_nombre": "JUAN",              # Filtrar por nombre
    # "p_numero_licencia": "123456",   # Filtrar por número de licencia
    # "p_clase": "B1",                 # Filtrar por clase de licencia
    # "p_estado": "VIGENTE",           # Filtrar por estado de la licencia
    # "p_fecha_desde": "2024-01-01",   # Filtrar por fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Filtrar por fecha hasta
    # "p_vencimiento_desde": "2024-01-01", # Filtrar por vencimiento desde
    # "p_vencimiento_hasta": "2024-12-31", # Filtrar por vencimiento hasta
}

# Parámetros alternativos para probar diferentes filtros de licencias
parametros_licencias_alternativos = [
    {
        "p_page_number": 1,
        "p_page_size": 10
    }
    # Se pueden agregar más combinaciones cuando se conozcan los filtros exactos
]

# Comentarios sobre el endpoint de licencias
parametros_licencias_comentados = {
    # Este endpoint consulta licencias de conducir por DNI y CUIL
    # Usa paginación obligatoria con p_page_number y p_page_size
    # Retorna PaginationResponseSchema con:
    # - page_number: número de página actual
    # - page_size: tamaño de página
    # - total_items: total de elementos
    # - items: lista de licencias
    #
    # Posibles filtros (a confirmar con la API):
    # - p_dni: filtrar por DNI del titular
    # - p_cuil: filtrar por CUIL del titular
    # - p_apellido: filtrar por apellido del titular
    # - p_nombre: filtrar por nombre del titular
    # - p_numero_licencia: filtrar por número de licencia
    # - p_clase: filtrar por clase de licencia (A, B1, B2, C, D, etc.)
    # - p_estado: filtrar por estado (VIGENTE, VENCIDA, SUSPENDIDA, etc.)
    # - p_fecha_desde/p_fecha_hasta: filtrar por rango de fechas de emisión
    # - p_vencimiento_desde/p_vencimiento_hasta: filtrar por rango de vencimiento
    #
    # El endpoint requiere permisos específicos (servicio_context 51)
    # URL: /licencias
}

# Parámetros para consultar ciclovías
parametros_ciclovias = {
    # "p_programa_conectar": "S",
    # "p_peatonal": "S"
}

# Parámetros opcionales para ciclovías (se pueden activar según necesidad)
parametros_ciclovias_con_filtros = {
    # "p_nombre": "CICLOVIA CENTRO",       # Filtrar por nombre de ciclovía
    # "p_barrio": "CENTRO",                # Filtrar por barrio
    # "p_zona": "NORTE",                   # Filtrar por zona
    # "p_estado": "ACTIVA",                # Filtrar por estado (ACTIVA, INACTIVA, EN_CONSTRUCCION)
    # "p_tipo": "BIDIRECCIONAL",           # Filtrar por tipo de ciclovía
    # "p_longitud_min": "100",             # Filtrar por longitud mínima en metros
    # "p_longitud_max": "5000",            # Filtrar por longitud máxima en metros
    # "p_fecha_desde": "2024-01-01",       # Filtrar por fecha de construcción desde
    # "p_fecha_hasta": "2024-12-31",       # Filtrar por fecha de construcción hasta
}

# Parámetros alternativos para probar diferentes filtros de ciclovías
parametros_ciclovias_alternativos = [
    # Sin filtros (todas las ciclovías)
    {},
    # Con filtros específicos (cuando se conozcan los valores válidos)
    # {
    #     "p_estado": "ACTIVA"
    # },
    # {
    #     "p_zona": "CENTRO"
    # },
    # {
    #     "p_tipo": "BIDIRECCIONAL"
    # }
]

# Comentarios sobre el endpoint de ciclovías
parametros_ciclovias_comentados = {
    # Este endpoint consulta información sobre ciclovías de la ciudad
    # NO usa paginación - retorna directamente list[CicloviasGetResponseSchema]
    # Retorna una lista de ciclovías con información como:
    # - id: identificador único de la ciclovía
    # - nombre: nombre de la ciclovía
    # - descripcion: descripción detallada
    # - barrio: barrio donde se encuentra
    # - zona: zona de la ciudad
    # - estado: estado actual (activa, inactiva, en construcción)
    # - tipo: tipo de ciclovía (bidireccional, unidireccional, etc.)
    # - longitud: longitud en metros
    # - coordenadas: información geográfica
    # - fecha_construccion: fecha de construcción
    # - observaciones: observaciones adicionales
    #
    # Posibles filtros (a confirmar con la API):
    # - p_nombre: filtrar por nombre de ciclovía
    # - p_barrio: filtrar por barrio
    # - p_zona: filtrar por zona de la ciudad
    # - p_estado: filtrar por estado
    # - p_tipo: filtrar por tipo de ciclovía
    # - p_longitud_min/p_longitud_max: filtrar por rango de longitud
    # - p_fecha_desde/p_fecha_hasta: filtrar por rango de fechas
    #
    # El endpoint requiere permisos específicos (servicio_context 113)
    # URL: /ciclovias
    # Método: GET
    # Response: list[CicloviasGetResponseSchema] (lista directa, sin paginación)
}

# Parámetros para consultar personal por empresa
parametros_personal = {
    "p_page_number": 1,
    "p_page_size": 20,
    "p_id_trp_empresa": 1  # ID de empresa de transporte (requerido según la lógica)
}

# Parámetros opcionales para personal (comentados hasta conocer la estructura exacta)
parametros_personal_comentados = {
    # "p_id_trp_empresa": 1,           # REQUERIDO - ID de la empresa de transporte
    # "p_page_number": 1,              # REQUERIDO - Número de página para paginación
    # "p_page_size": 20,               # REQUERIDO - Tamaño de página para paginación
    # "p_dni": "12345678",             # Posible parámetro de DNI del personal
    # "p_cuil": "20123456789",         # Posible parámetro de CUIL del personal
    # "p_apellido": "PEREZ",           # Posible parámetro de apellido
    # "p_nombre": "JUAN",              # Posible parámetro de nombre
    # "p_estado": "ACTIVO",            # Posible parámetro de estado del personal
    # "p_cargo": "CONDUCTOR",          # Posible parámetro de cargo
    # "p_fecha_desde": "2024-01-01",   # Posible parámetro de fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Posible parámetro de fecha hasta
    # "p_situacion": 1,                # Posible parámetro de situación
}

# Comentarios sobre el endpoint de personal
parametros_personal_comentarios = {
    # Este endpoint consulta personal asociado a empresas de transporte
    # Usa paginación obligatoria con p_page_number y p_page_size
    # Requiere p_id_trp_empresa como parámetro obligatorio
    # Retorna PaginationResponseSchema con:
    # - page_number: número de página actual
    # - page_size: tamaño de página
    # - total_items: total de elementos
    # - items: lista de personal
    #
    # El endpoint valida que el ID de empresa exista antes de procesar la consulta
    # El endpoint requiere permisos específicos (servicio_context 138)
    # URL: /personal
    # Método: GET
    # Response: PaginationResponseSchema con lista de PersonalSchema
    #
    # Posibles filtros adicionales (a confirmar con la API):
    # - p_dni: filtrar por DNI del personal
    # - p_cuil: filtrar por CUIL del personal
    # - p_apellido: filtrar por apellido
    # - p_nombre: filtrar por nombre
    # - p_estado: filtrar por estado (ACTIVO, INACTIVO, etc.)
    # - p_cargo: filtrar por cargo del personal
    # - p_fecha_desde/p_fecha_hasta: filtrar por rango de fechas
    # - p_situacion: filtrar por situación específica
}

# Parámetros para consultar empresas de transporte
parametros_empresas = {
    # Este endpoint no requiere parámetros obligatorios según el código
}

# Comentarios sobre el endpoint de empresas
parametros_empresas_comentados = {
    # Este endpoint consulta todas las empresas de transporte
    # NO usa paginación - retorna directamente list[CompanySchema]
    # NO requiere parámetros obligatorios
    # Retorna una lista de empresas con información como:
    # - id_trp_empresa: identificador único de la empresa
    # - id_transporte: identificador de transporte
    # - nombre_alt: nombre alternativo de la empresa
    # - cuit: CUIT de la empresa
    # - razon_social: razón social de la empresa
    # - domicilio: información completa del domicilio incluyendo:
    #   * id_domicilio, id_localidad, id_barrio, id_calle
    #   * barrio, calle, altura, piso, dpto, manzana, lote
    #   * torre, oficina_local, localidad, codigo_postal
    #   * latitud, longitud
    #
    # El endpoint requiere permisos específicos (servicio_context 140)
    # URL: /empresas
    # Método: GET
    # Response: list[CompanySchema] (lista directa, sin paginación)
    #
    # Posibles filtros adicionales (a confirmar con la API):
    # - p_cuit: filtrar por CUIT específico
    # - p_razon_social: filtrar por razón social
    # - p_nombre_alt: filtrar por nombre alternativo
    # - p_estado: filtrar por estado de la empresa
    # - p_localidad: filtrar por localidad
    # - p_tipo_transporte: filtrar por tipo de transporte
}

# Parámetros para consultar recorridos de líneas
parametros_recorridos_lineas = {
    "p_id_trp_empresa": 1  # ID de empresa de transporte (opcional pero recomendado)
}

# Parámetros opcionales para recorridos de líneas (comentados hasta conocer la estructura exacta)
parametros_recorridos_lineas_comentados = {
    # "p_id_trp_empresa": 1,           # Filtrar por ID de empresa de transporte
    # "p_id_trp_linea": 1,             # Filtrar por ID de línea específica
    # "p_id_transporte": 1,            # Posible parámetro de ID transporte
    # "p_id_trp_corredor": 1,          # Posible parámetro de ID corredor
    # "p_nombre": "LINEA A",           # Posible parámetro de nombre de línea
    # "p_estado": "ACTIVO",            # Posible parámetro de estado
    # "p_sentido": "IDA",              # Posible parámetro de sentido (IDA/VUELTA)
}

# Comentarios sobre el endpoint de recorridos de líneas
parametros_recorridos_lineas_comentarios = {
    # Este endpoint consulta recorridos de líneas de transporte por empresa y/o línea
    # NO usa paginación - retorna directamente list[LineasRecorridoResponseSchema]
    # Los parámetros p_id_trp_empresa y p_id_trp_linea son opcionales pero se validan si se proporcionan
    # Retorna una lista de recorridos con información como:
    # - id_trp_empresa: identificador de la empresa
    # - id_trp_linea: identificador de la línea
    # - id_transporte: identificador de transporte
    # - id_trp_corredor: identificador del corredor
    # - nombre: nombre de la línea
    # - desc_cartel: descripción del cartel
    # - color: color de la línea
    # - descripcion: descripción de la línea
    # - paradas: lista de paradas con información detallada:
    #   * sentido: sentido del recorrido (IDA/VUELTA)
    #   * id_trp_parada: identificador de la parada
    #   * codigo: código de la parada
    #   * nombre_parada: nombre de la parada
    #   * ubicacion: ubicación de la parada
    #   * id_barrio: identificador del barrio
    #   * barrio: nombre del barrio
    #   * latitud: coordenada latitud
    #   * longitud: coordenada longitud
    #
    # El endpoint requiere permisos específicos (servicio_context 141)
    # URL: /lineas/recorrido
    # Método: GET
    # Response: list[LineasRecorridoResponseSchema] (lista directa, sin paginación)
    #
    # El endpoint valida que existan los IDs de empresa y línea si se proporcionan
    # Agrupa las paradas por línea en el resultado final
}

# Parámetros para consultar vehículos por empresa y/o dominio
parametros_vehiculos = {
    "p_page_number": 1,
    "p_page_size": 20,
    "p_id_trp_empresa": 3  # ID de empresa de transporte (opcional pero recomendado)
}

# Parámetros opcionales para vehículos (comentados hasta conocer la estructura exacta)
parametros_vehiculos_comentados = {
    # "p_id_trp_empresa": 1,           # Filtrar por ID de empresa de transporte
    # "p_page_number": 1,              # REQUERIDO - Número de página para paginación
    # "p_page_size": 20,               # REQUERIDO - Tamaño de página para paginación
    # "p_dominio": "ABC123",           # Filtrar por dominio del vehículo
    # "p_marca": "MERCEDES",           # Posible parámetro de marca del vehículo
    # "p_modelo": "SPRINTER",          # Posible parámetro de modelo del vehículo
    # "p_año": "2020",                 # Posible parámetro de año del vehículo
    # "p_estado": "ACTIVO",            # Posible parámetro de estado del vehículo
    # "p_tipo_vehiculo": "COLECTIVO",  # Posible parámetro de tipo de vehículo
    # "p_numero_interno": "001",       # Posible parámetro de número interno
    # "p_fecha_desde": "2024-01-01",   # Posible parámetro de fecha desde
    # "p_fecha_hasta": "2024-12-31",   # Posible parámetro de fecha hasta
}

# Comentarios sobre el endpoint de vehículos
parametros_vehiculos_comentarios = {
    # Este endpoint consulta vehículos por empresa y/o dominio
    # Usa paginación obligatoria con p_page_number y p_page_size
    # El parámetro p_id_trp_empresa es opcional pero se valida si se proporciona
    # Retorna PaginationResponseSchema con:
    # - page_number: número de página actual
    # - page_size: tamaño de página
    # - total_items: total de elementos
    # - items: lista de vehículos
    #
    # El endpoint valida que el ID de empresa exista antes de procesar la consulta
    # El endpoint requiere permisos específicos (servicio_context 139)
    # URL: /vehiculos
    # Método: GET
    # Response: PaginationResponseSchema con lista de VehiculosSchema
    #
    # Posibles filtros adicionales (a confirmar con la API):
    # - p_dominio: filtrar por dominio específico del vehículo
    # - p_marca: filtrar por marca del vehículo
    # - p_modelo: filtrar por modelo del vehículo
    # - p_año: filtrar por año del vehículo
    # - p_estado: filtrar por estado (ACTIVO, INACTIVO, etc.)
    # - p_tipo_vehiculo: filtrar por tipo de vehículo
    # - p_numero_interno: filtrar por número interno
    # - p_fecha_desde/p_fecha_hasta: filtrar por rango de fechas
}

# Parámetros para consultar paradas por línea
parametros_paradas_linea = {
    "p_id_trp_linea": 669  # ID de línea de transporte (requerido según la lógica)
}
