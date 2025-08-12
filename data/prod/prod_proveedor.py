# Datos de prueba para insertar/actualizar proveedores

body_insertar_proveedor_pf = {
  "p_tipo_proveedor": "PF",
  "p_modalidad": "CON CONTRATO",
  "p_cuit_cuil": "24492837632",
  "p_cuil_responsable": None,
  "p_razon_social": "PRUEBA KUNAN",
  "p_nombre_fantasia": "PRUEBA KUNAN",
  "p_forma_juridica": 1,
  "p_nro_ingresos_brutos": "567890003",
  "p_inscripcion_directorio": "2023-07-14",
  "p_plazo_mandato": "2025-01-01",
  "p_inicio_vigencia": "2024-02-01",
  "p_fin_vigencia": "2024-11-24",
  "p_contratista_obra_publica": "S",
  "p_bienes_servicios": "S",
  "p_actividades_afip": [
    {
      "codigo": "581100",
      "descripcion": "EDICIÓN DE LIBROS, FOLLETOS, Y OTRAS PUBLICACIONES",
      "periodo": None
    }
  ],
    "p_especialidades": [
    {
        "id_especialidad": 1
    }
  ],
  "p_nombre": "PRUEBA KUNAN",
  "p_apellido": "PRUEBA KUNAN",
  "p_condicion_fiscal": 1,
  "p_correo_electronico_1": "himenendezpicossi@cordoba.gov.ar",
  "p_correo_electronico_2": "himenendezpicossi@cordoba.gov.ar",
  "p_telefono": "3516123450",
  "p_telefono_fijo": None,
  "p_id_profesion": None,
  "p_id_banco": None,
  "p_CBU": "2600000000000000000026",
  "p_tipo_domicilio": "LEGAL",
  "p_id_provincia": 22,
  "p_id_departamento": 1,
  "p_id_localidad": 1,  
  "p_id_barrio":337,
  "p_id_calle": 1549,
  "p_barrio": "ASDF",
  "p_calle": "Hola", 
  "p_altura": "1440",
  "p_torre": "prwa 3",
  "p_piso": "279",
  "p_dpto": "279",
  "p_manzana": "as2d",
  "p_lote": None,
  "p_oficina_local": None,
  "p_codigo_postal": "6001",
  "p_usuario_aplicacion": "string"
}

# Datos de prueba para insertar/actualizar proveedores (persona jurídica)
body_insertar_proveedor_pj = {
  "p_tipo_proveedor": "PJ",
  "p_modalidad": "CON CONTRATO",
  "p_cuit_cuil": "30717105970",
  "p_cuil_responsable": None,
  "p_razon_social": "PRUEBA KUNAN",
  "p_nombre_fantasia": "PRUEBA KUNAN",
  "p_forma_juridica": 1,
  "p_nro_ingresos_brutos": "567890003",
  "p_inscripcion_directorio": "2023-07-14",
  "p_plazo_mandato": "2025-01-01",
  "p_inicio_vigencia": "2024-02-01",
  "p_fin_vigencia": "2024-11-24",
  "p_contratista_obra_publica": "S",
  "p_bienes_servicios": "S",
  "p_actividades_afip": [
    {
      "codigo": "581100",
      "descripcion": "EDICIÓN DE LIBROS, FOLLETOS, Y OTRAS PUBLICACIONES",
      "periodo": None
    }
  ],
    "p_especialidades": [
    {
        "id_especialidad": 1
    }
  ],
  "p_nombre": "PRUEBA KUNAN",
  "p_apellido": "PRUEBA KUNAN",
  "p_condicion_fiscal": 1,
  "p_correo_electronico_1": "himenendezpicossi@cordoba.gov.ar",
  "p_correo_electronico_2": "himenendezpicossi@cordoba.gov.ar",
  "p_telefono": "3516123450",
  "p_telefono_fijo": None,
  "p_id_profesion": None,
  "p_id_banco": None,
  "p_CBU": "2600000000000000000026",
  "p_tipo_domicilio": "LEGAL",
  "p_id_provincia": 22,
  "p_id_departamento": 1,
  "p_id_localidad": 1,  
  "p_id_barrio":337,
  "p_id_calle": 1549,
  "p_barrio": "ASDF",
  "p_calle": "Hola", 
  "p_altura": "1440",
  "p_torre": "prwa 3",
  "p_piso": "279",
  "p_dpto": "279",
  "p_manzana": "as2d",
  "p_lote": None,
  "p_oficina_local": None,
  "p_codigo_postal": "6001",
  "p_usuario_aplicacion": "string"
}

lista_cuit_cuil_proveedores = [
    "24492837632",  # CUIL persona física
    "30372159614",  # CUIT persona jurídica
    "30717105970"
]


body_busqueda_por_cuils_cuits = {
    "p_cuils_cuits": [
    "24492837632",
    "30372159614",
    "30717105970"
  ]
}

# Datos de prueba para alta simplificada de proveedores (persona física)
body_alta_proveedor_pf = {
    "p_tipo_persona": "PF",
    "p_cuit_cuil": "24492837632",
    "p_modalidad": "EVENTUAL",
    "p_nombre": "PRUEBA KUNAN",
    "p_apellido": "PRUEBA KUNAN",
    "p_razon_social": "PRUEBA KUNAN",
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para alta simplificada de proveedores (persona jurídica)
body_alta_proveedor_pj = {
    "p_tipo_persona": "PJ",
    "p_cuit_cuil": "30717105970",
    "p_modalidad": "EVENTUAL",
    "p_nombre": "PRUEBA KUNAN",
    "p_apellido": "PRUEBA KUNAN",
    "p_razon_social": "PRUEBA KUNAN",
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para alta de proveedores con CBU y banco (persona física)
body_alta_cbu_banco_proveedor_pf = {
    "p_tipo_persona": "PF",
    "p_modalidad": "EVENTUAL",
    "p_cuit_cuil": "24492837632",
    "p_nombre": "PRUEBA CBU",
    "p_apellido": "BANCO PF",
    "p_razon_social": None,
    "p_cbu": "0070181820000001234567",
    "p_id_banco": 7,  # ID del banco (ejemplo: Banco Galicia)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para alta de proveedores con CBU y banco (persona jurídica)
body_alta_cbu_banco_proveedor_pj = {
    "p_tipo_persona": "PJ",
    "p_modalidad": "EVENTUAL",
    "p_cuit_cuil": "30717105970",
    "p_nombre": None,
    "p_apellido": None,
    "p_razon_social": "PRUEBA CBU BANCO PJ",
    "p_cbu": "0720000720000000123456",
    "p_id_banco": 7,  # ID del banco (ejemplo: Banco Galicia)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para consulta de proveedores por ID de actividad AFIP
lista_id_actividad_afip = [9, 10, 11, 12, 13]  # IDs de actividades AFIP para pruebas

# Parámetros de consulta para proveedores por actividad
body_consulta_proveedor_actividad = {
    "p_id_actividad": 9  # ID de actividad AFIP (ejemplo: "EDICIÓN DE LIBROS, FOLLETOS, Y OTRAS PUBLICACIONES")
}

# Datos de prueba para búsqueda de proveedores por parámetros se tienen que modificar por el criterio que se busque
body_busqueda_proveedores = {
    "p_cuil_cuit": "30717105970"
}

# Datos de prueba para búsqueda de proveedores por IDs
body_busqueda_proveedores_por_ids = {
    "p_ids_proveedor": [1, 2, 3, 4, 5]  # Lista de IDs de proveedores para pruebas
}

# Datos de prueba para búsqueda de proveedores por IDs con parámetro de búsqueda
body_busqueda_proveedores_por_ids_search = {
    "p_ids_proveedor": [1, 2, 3, 4, 5]  # Lista de IDs de proveedores para pruebas
}

# Parámetros de consulta para búsqueda de proveedores por IDs con parámetro de búsqueda
query_params_busqueda_proveedores_por_ids_search = {
    "p_search_input": "prueba",  # Texto de búsqueda
    "p_page_size": 10,
    "p_page_number": 1
}

# Corregir los query params - p_criterio_orden debe ser número, no string
query_params_busqueda_proveedores = {
    "p_criterio_orden": 1,
    "p_orden": 1,
    "p_page_size": 1,
    "p_page_number": 1
}

# Simplificar el body de búsqueda - solo incluir campos que realmente queremos buscar
body_busqueda_proveedores = {
  "p_cuil_cuit": "24492837632"
}


# Datos de prueba para insertar/actualizar CBU de proveedor (persona física)
body_insertar_cbu_proveedor_pf = {
  "p_cuil_cuit": "24492837632",
  "p_cbu": "0070181820000001234567",
  "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para insertar/actualizar CBU de proveedor (persona jurídica)
body_insertar_cbu_proveedor_pj = {
  "p_cuil_cuit": "30717105970",
  "p_cbu": "0720000720000000123456",
  "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para insertar/actualizar CBU de proveedor (persona física)
body_insertar_cbu_proveedor_pf = {
  "p_cuil_cuit": "24492837632",
  "p_cbu": "0070181820000001234567",
  "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para insertar/actualizar CBU de proveedor (persona jurídica)
body_insertar_cbu_proveedor_pj = {
  "p_cuil_cuit": "30717105970",
  "p_cbu": "0720000720000000123456",
  "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para insertar/actualizar CBU y banco de proveedor (persona física)
body_insertar_cbu_banco_proveedor_pf = {
    "p_cuil_cuit": "24492837632",
    "p_cbu": "0070181820000001234567",
    "p_id_banco": 7,  # ID del banco (ejemplo: Banco Galicia)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# Datos de prueba para insertar/actualizar CBU y banco de proveedor (persona jurídica)
body_insertar_cbu_banco_proveedor_pj = {
    "p_cuil_cuit": "30717105970",
    "p_cbu": "0720000720000000123456",
    "p_id_banco": 7,  # ID del banco (ejemplo: Banco Galicia)
    "p_usuario_aplicacion": "PRUEBA KUNAN"
}

# En tu módulo de datos
parametros_busqueda_minimizada_query = {
    "p_page_size": 1,
    "p_page_number": 1
}

body_busqueda_minimizada = {
    #"p_denominacion": "",
    #"p_cuil_cuit": "",
    #"p_tipo_persona": ""
}

body_busqueda_minimizada_casos = [
    {"p_cuil_cuit": "24492837632"}
]


# Casos múltiples para búsqueda minimizada de proveedores
body_busqueda_minimizada_casos = [
    # Caso 1: Búsqueda por ID proveedor SAM
    {
        "p_id_proveedor_sam": 165260
    },
    
    # Caso 2: Búsqueda por CUIL/CUIT
    {
        "p_cuil_cuit": "24492837632"
    },
    
    # Caso 3: Búsqueda por RUPEM
    {
        "p_rupem": "S"
    },
    
    # Caso 4: Búsqueda por contratista obra pública
    {
        "p_contratista_obra_publica": "S"
    },
    
    # Caso 5: Búsqueda por rango de fechas inicio vigencia
    {
        "p_f_inicio_vigencia_d": "2025-07-15",
        "p_f_inicio_vigencia_h": "2026-07-20"
    },
    
    # Caso 6: Búsqueda por rango de fechas fin vigencia
    {
        "p_f_fin_vigencia_d": "2026-12-19",
        "p_f_fin_vigencia_h": "2026-12-31"
    },
    
    # Caso 7: Búsqueda por tipo persona
    {
        "p_tipo_persona": "PF"
    },
    
    # Caso 8: Búsqueda por denominación
    {
        "p_denominacion": "PRUEBA KUNAN PRUEBA KUNAN"
    },
    
    # Caso 9: Búsqueda por actividades
    {
        "p_id_actividades": [9]
    },
    
    # Caso 10: Búsqueda por especialidades
    {
        "p_id_especialidades": [1]
    },
    
    # Caso 11: Búsqueda combinada (todos los parámetros)
    {
        "p_id_proveedor_sam": 165260,
        "p_cuil_cuit": "24492837632",
        "p_rupem": "S",
        "p_contratista_obra_publica": "S",
        "p_modalidad": None,
        "p_f_inicio_vigencia_d": "2025-07-15",
        "p_f_inicio_vigencia_h": "2026-07-20",
        "p_f_fin_vigencia_d": "2026-12-19",
        "p_f_fin_vigencia_h": "2026-12-31",
        "p_tipo_persona": "PF",
        "p_denominacion": "PRUEBA KUNAN PRUEBA KUNAN",
        "p_id_actividades": [9],
        "p_id_especialidades": [1]
    }
]


