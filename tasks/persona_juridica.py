import random
import copy

def get_persona_juridica(client, logger, environment, sample_cuits):
    """Prueba el endpoint de obtener persona jurídica por CUIT"""

    
    # Seleccionar un CUIT aleatorio de la lista de muestra (si no está vacía)
    p_cuit = random.choice(sample_cuits)
    
    logger.info(f"Ejecutando get_persona_juridica con CUIT: {p_cuit}")
    
    try:
        with client.get(f"/personas-juridicas?p_cuit={p_cuit}", catch_response=True, name="(PERSONAS JURIDICAS) - /personas-juridicas") as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        response.success()
                        logger.info(f"Obtención de persona jurídica exitosa para CUIT: {p_cuit}")
                        logger.debug(f"Datos recibidos: {response_data}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en persona jurídica: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en persona jurídica: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de persona jurídica: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de persona jurídica: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            f"/personas-juridicas?p_cuit={p_cuit}",
            catch_response=True, 
            name="(PERSONAS JURIDICAS) - /personas-juridicas [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_sedes_pj(client, logger, environment, data_module):
    """Prueba el endpoint de obtener sedes de persona jurídica"""

    # Verificar si la lista de CUITs está vacía
    if not hasattr(data_module, 'p_cuit') or not data_module.p_cuit:
        logger.error("La lista de CUITs está vacía. No se puede continuar con la prueba de sedes.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/personas-juridicas/sedes_pj", 
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj [Lista vacía]"
        ) as response:
            response.failure("Lista de CUITs vacía para sedes")
        return
    
    # Seleccionar un CUIT aleatorio
    p_cuit = random.choice(data_module.p_cuit)
    
    # Crear parámetros de consulta
    query_params = {
        "p_cuit": p_cuit,
        "p_sede_principal": data_module.p_sede_principal
    }
    
    # Comprobar si tenemos datos para los parámetros opcionales
    try:
        if hasattr(data_module, 'p_id_sede_pj') and data_module.p_id_sede_pj:
            query_params["p_id_sede_pj"] = random.choice(data_module.p_id_sede_pj)
    except (AttributeError, IndexError):
        pass
    
    try:
        if hasattr(data_module, 'p_nombre_sede') and data_module.p_nombre_sede:
            query_params["p_nombre_sede"] = random.choice(data_module.p_nombre_sede)
    except (AttributeError, IndexError):
        pass
    
    logger.info(f"Ejecutando get_sedes_pj con parámetros: {query_params}")
    
    try:
        with client.get(
            "/personas-juridicas/sedes_pj", 
            params=query_params,
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj"

        ) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "p_cuit" in response_data and "p_razon_social" in response_data:
                        response.success()
                        logger.info(f"Obtención de sedes exitosa para CUIT: {p_cuit}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en sedes: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de sedes: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de sedes: {str(e)}")
        environment.events.request_failure.fire(
            request_type="GET",
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj",
            response_time=0,
            exception=e
        )

def insert_persona_juridica(client, logger, environment, body_insertar_persona_juridica):
    """Tarea para insertar una persona jurídica"""
    registro = copy.deepcopy(random.choice(body_insertar_persona_juridica))
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    logger.info(f"Enviando petición con CUIT: {registro['p_cuit']}")
    
    try:
        with client.post(
            "/personas-juridicas",
            json=registro,
            headers=headers,
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas"
        ) as response:
            if response.status_code in [200, 201]:
                logger.info(f"Persona jurídica insertada correctamente: {response.status_code}")
                response.success()
            else:
                logger.error(f"Error al insertar persona jurídica: {response.status_code} - {response.text}")
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante inserción de persona jurídica: {str(e)}")
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS JURIDICAS) - /personas-juridicas",
            response_time=0,
            exception=e
        )

def insert_domicilio_sede_pj(client, logger, environment, body_insertar_sede):
    """Tarea para insertar un domicilio para una sede de persona jurídica"""
    
    # Verificar que body_insertar_sede no esté vacío
    if not body_insertar_sede:
        logger.error("body_insertar_sede está vacío")
        with client.post(
            "/personas-juridicas/sedes_pj",
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj [Datos vacíos]"
        ) as response:
            response.failure("Datos de sede vacíos")
        return
    
    # Manejar tanto diccionario único como lista de diccionarios
    if isinstance(body_insertar_sede, dict):
        # Si es un diccionario único, usarlo directamente
        registro = copy.deepcopy(body_insertar_sede)
        logger.debug("Usando diccionario único para insertar domicilio de sede")
    elif isinstance(body_insertar_sede, list) and len(body_insertar_sede) > 0:
        # Si es una lista, seleccionar uno aleatoriamente
        registro = copy.deepcopy(random.choice(body_insertar_sede))
        logger.debug(f"Seleccionando de lista con {len(body_insertar_sede)} elementos")
    else:
        logger.error(f"Tipo de datos inesperado para body_insertar_sede: {type(body_insertar_sede)}")
        logger.error(f"Contenido: {body_insertar_sede}")
        with client.post(
            "/personas-juridicas/sedes_pj",
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj [Tipo incorrecto]"
        ) as response:
            response.failure("Tipo de datos incorrecto para sede")
        return
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


    logger.info(f"Enviando petición para insertar domicilio sede con CUIT: {registro['p_cuit']}, ID Sede: {registro.get('p_id_sede_pj', 'N/A')}")
    logger.debug(f"Datos completos a enviar: {registro}")
    
    try:
        with client.post(
            "/personas-juridicas/sedes_pj",
            json=registro,
            headers=headers,
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj"
        ) as response:
            logger.info(f"Respuesta recibida - Status: {response.status_code}")
            logger.debug(f"Headers de respuesta: {dict(response.headers)}")
            logger.debug(f"Contenido de respuesta: {response.text}")
            
            # Solo considerar exitoso el código 201 (Created)
            if response.status_code == 201:
                try:
                    response_data = response.json()
                    logger.debug(f"JSON parseado correctamente: {response_data}")
                    
                    # Verificar que la respuesta contenga el ID de la sede creada
                    if isinstance(response_data, dict) and "id_sede_pj" in response_data:
                        response.success()
                        logger.info(f"Domicilio de sede insertado correctamente: {response.status_code}")
                        logger.info(f"ID de sede creada: {response_data['id_sede_pj']}")
                        logger.debug(f"Datos completos de respuesta: {response_data}")
                    else:
                        response.failure("Formato de respuesta inesperado - falta 'id_sede_pj'")
                        logger.warning(f"Respuesta sin 'id_sede_pj': {response.text}")
                        
                except ValueError as e:
                    logger.error(f"Error al parsear JSON: {str(e)}")
                    logger.error(f"Contenido que causó el error: {response.text}")
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    
            elif response.status_code == 200:
                logger.warning(f"Código 200 recibido pero se esperaba 201 para creación: {response.text}")
                response.failure("Se esperaba código 201 para creación, recibido 200")
                
            elif response.status_code == 400:
                logger.error(f"Error de validación (400): {response.text}")
                response.failure(f"Error de validación: {response.status_code}")
                
            elif response.status_code == 404:
                logger.error(f"Endpoint no encontrado (404): {response.text}")
                response.failure(f"Endpoint no encontrado: {response.status_code}")
                
            elif response.status_code == 409:
                logger.warning(f"Conflicto - posiblemente ya existe (409): {response.text}")
                response.failure(f"Conflicto: {response.status_code}")
                
            elif response.status_code == 500:
                logger.error(f"Error interno del servidor (500): {response.text}")
                response.failure(f"Error interno del servidor: {response.status_code}")
                
            else:
                logger.error(f"Error al insertar domicilio de sede: {response.status_code} - {response.text}")
                response.failure(f"Error: {response.status_code}")
                
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio de sede: {str(e)}")
        logger.error(f"Tipo de excepción: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback completo: {traceback.format_exc()}")
        
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj",
            response_time=0,
            response_length=0,
            exception=e
        )



# def get_sedes_pj(client, logger, environment, data_module):
#     """Prueba el endpoint de obtener sedes de persona jurídica"""

#     # Verificar si la lista de CUITs está vacía
#     if not hasattr(data_module, 'p_cuit') or not data_module.p_cuit:
#         logger.error("La lista de CUITs está vacía. No se puede continuar con la prueba de sedes.")
        
#         # Registrar un error explícito usando catch_response
#         with client.get(
#             "/personas-juridicas/sedes_pj", 
#             catch_response=True,
#             name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj [Lista vacía]"
#         ) as response:
#             response.failure("Lista de CUITs vacía para sedes")
#         return
    
#     # Seleccionar un CUIT aleatorio
#     p_cuit = random.choice(data_module.p_cuit)
    
#     # Crear parámetros de consulta
#     query_params = {
#         "p_cuit": p_cuit,
#         "p_sede_principal": getattr(data_module, 'p_sede_principal', 'S')
#     }
    
#     # Comprobar si tenemos datos para los parámetros opcionales
#     try:
#         if hasattr(data_module, 'p_id_sede_pj') and data_module.p_id_sede_pj:
#             query_params["p_id_sede_pj"] = random.choice(data_module.p_id_sede_pj)
#     except (AttributeError, IndexError):
#         pass
    
#     try:
#         if hasattr(data_module, 'p_nombre_sede') and data_module.p_nombre_sede:
#             query_params["p_nombre_sede"] = random.choice(data_module.p_nombre_sede)
#     except (AttributeError, IndexError):
#         pass
    
#     logger.info(f"Ejecutando get_sedes_pj con parámetros: {query_params}")
    
#     try:
#         with client.get(
#             "/personas-juridicas/sedes_pj", 
#             params=query_params,
#             catch_response=True
#         ) as response:
#             if response.status_code == 200:
#                 try:
#                     response_data = response.json()
#                     if "p_cuit" in response_data and "p_razon_social" in response_data:
#                         response.success()
#                         logger.info(f"Obtención de sedes exitosa para CUIT: {p_cuit}")
#                     else:
#                         response.failure("Formato de respuesta inesperado")
#                         logger.warning(f"Formato inesperado en sedes: {response.text[:200]}")
#                 except ValueError as e:
#                     response.failure(f"Respuesta no es JSON válido: {str(e)}")
#                     logger.error(f"JSON inválido: {response.text[:200]}")
#             else:
#                 response.failure(f"Error: {response.status_code}")
#                 logger.error(f"Error en consulta de sedes: {response.status_code}")
#     except Exception as e:
#         logger.error(f"Excepción durante obtención de sedes: {str(e)}")
#         environment.events.request_failure.fire(
#             request_type="GET",
#             name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes_pj",
#             response_time=0,
#             exception=e
#         )


def insert_domicilio_sede(client, logger, environment, body_insertar_domicilio_sede):
    """Tarea para insertar un domicilio para una sede de persona jurídica usando el nuevo endpoint"""
    
    # Verificar que body_insertar_domicilio_sede no esté vacío
    if not body_insertar_domicilio_sede:
        logger.error("body_insertar_domicilio_sede está vacío")
        with client.post(
            "/personas-juridicas/sedes/domicilios",
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes/domicilios [Datos vacíos]"
        ) as response:
            response.failure("Datos de domicilio vacíos")
        return
    
    # Crear una copia profunda para evitar modificar el original
    # Si body_insertar_domicilio_sede es un dict único, no usar random.choice
    if isinstance(body_insertar_domicilio_sede, dict):
        registro = copy.deepcopy(body_insertar_domicilio_sede)
    elif isinstance(body_insertar_domicilio_sede, list):
        registro = copy.deepcopy(random.choice(body_insertar_domicilio_sede))
    else:
        logger.error(f"Tipo de datos inesperado para body_insertar_domicilio_sede: {type(body_insertar_domicilio_sede)}")
        return
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Verificar campos obligatorios
    campos_obligatorios = ['p_cuit', 'p_id_sede_pj']
    for campo in campos_obligatorios:
        if campo not in registro:
            logger.error(f"Campo obligatorio '{campo}' no encontrado en los datos")
            with client.post(
                "/personas-juridicas/sedes/domicilios",
                catch_response=True,
                name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes/domicilios [Campo faltante]"
            ) as response:
                response.failure(f"Campo obligatorio '{campo}' faltante")
            return
    
    logger.info(f"Enviando petición para insertar domicilio a sede con CUIT: {registro['p_cuit']}, ID Sede: {registro.get('p_id_sede_pj', 'N/A')}")
    logger.debug(f"Datos completos a enviar: {registro}")
    
    try:
        with client.post(
            "/personas-juridicas/sedes/domicilios",
            json=registro,
            headers=headers,
            catch_response=True,
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes/domicilios"
        ) as response:
            logger.info(f"Respuesta recibida - Status: {response.status_code}")
            logger.debug(f"Headers de respuesta: {dict(response.headers)}")
            logger.debug(f"Contenido de respuesta: {response.text}")
            
            if response.status_code in [200, 201]:
                try:
                    response_data = response.json()
                    logger.debug(f"JSON parseado correctamente: {response_data}")
                    
                    # Verificar la estructura de la respuesta - ajustar según la respuesta real del API
                    if isinstance(response_data, dict) and len(response_data) > 0:
                        response.success()
                        logger.info(f"Domicilio de sede insertado correctamente: {response.status_code}")
                        logger.info(f"Datos de respuesta: {response_data}")
                    else:
                        response.failure("Formato de respuesta inesperado o vacío")
                        logger.warning(f"Formato inesperado en respuesta: {response.text}")
                        
                except ValueError as e:
                    logger.error(f"Error al parsear JSON: {str(e)}")
                    logger.error(f"Contenido de respuesta que causó el error: {response.text}")
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    
            elif response.status_code == 400:
                logger.error(f"Error de validación (400): {response.text}")
                response.failure(f"Error de validación: {response.status_code}")
                
            elif response.status_code == 404:
                logger.error(f"Endpoint no encontrado (404): {response.text}")
                response.failure(f"Endpoint no encontrado: {response.status_code}")
                
            elif response.status_code == 500:
                logger.error(f"Error interno del servidor (500): {response.text}")
                response.failure(f"Error interno del servidor: {response.status_code}")
                
            else:
                logger.error(f"Error al insertar domicilio de sede: {response.status_code} - {response.text}")
                response.failure(f"Error: {response.status_code}")
                
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio de sede: {str(e)}")
        logger.error(f"Tipo de excepción: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback completo: {traceback.format_exc()}")
        
        # Registrar el fallo en Locust
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS JURIDICAS) - /personas-juridicas/sedes/domicilios",
            response_time=0,
            response_length=0,
            exception=e
        )
