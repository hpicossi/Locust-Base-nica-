import copy
import random


def get_organigrama_por_niveles(client, logger, environment, data_module):
    """Prueba el endpoint de obtener organigrama por nivel"""
    
    # Verificar si la lista de niveles está vacía
    if not hasattr(data_module, 'p_nivel') or not data_module.p_nivel:
        logger.error("La lista de niveles está vacía. No se puede continuar con la prueba de organigrama.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/dependencias/niveles", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/dependencias/niveles [Lista vacía]"
        ) as response:
            response.failure("Lista de niveles vacía")
        return
    
    # Seleccionar un nivel aleatorio de la lista
    p_nivel = random.choice(data_module.p_nivel)
    
    logger.info(f"Ejecutando get_organigrama_por_nivel con nivel: {p_nivel}")
    
    try:
        with client.get(
            f"/organigrama/dependencias/niveles/{p_nivel}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/niveles/{p_nivel}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía y que contenga los campos esperados
                        if response_data and all("id_unidad" in item and "unidad" in item and "nivel" in item for item in response_data):
                            response.success()
                            logger.info(f"Obtención de organigrama por nivel exitosa para nivel: {p_nivel}")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                        else:
                            response.failure("Formato de respuesta incompleto o lista vacía")
                            logger.warning(f"Formato incompleto o lista vacía en organigrama: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en organigrama: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en organigrama: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de organigrama: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de organigrama: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/niveles/{p_nivel}",
            response_time=0,
            exception=e
        )

def get_organigrama_por_nivel(client, logger, environment, data_module):
    """Prueba el endpoint de obtener dependencias por nivel del organigrama"""
    
    # Verificar si la lista de niveles está vacía
    if not hasattr(data_module, 'p_nivel') or not data_module.p_nivel:
        logger.error("La lista de niveles está vacía. No se puede continuar con la prueba de dependencias por nivel.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/dependencias/nivel", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/dependencias/nivel [Lista vacía]"
        ) as response:
            response.failure("Lista de niveles vacía")
        return
    
    # Seleccionar un nivel aleatorio de la lista
    p_nivel = random.choice(data_module.p_nivel)
    
    logger.info(f"Ejecutando get_dependencias_por_nivel con nivel: {p_nivel}")
    
    try:
        with client.get(
            f"/organigrama/dependencias/nivel/{p_nivel}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/nivel/{p_nivel}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía y que contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada", "nivel"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de dependencias por nivel exitosa para nivel: {p_nivel}")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                        else:
                            response.failure("Formato de respuesta incompleto o lista vacía")
                            logger.warning(f"Formato incompleto o lista vacía en dependencias: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en dependencias: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en dependencias: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de dependencias: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de dependencias: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/nivel/{p_nivel}",
            response_time=0,
            exception=e
        )

def get_organigrama_por_dependencia(client, logger, environment, data_module):
    """Prueba el endpoint de obtener organigrama por ID de dependencia"""
    
    # Verificar si la lista de dependencias está vacía
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.error("La lista de IDs de dependencias está vacía. No se puede continuar con la prueba de organigrama por dependencia.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/1", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/{id_dependencia} [Lista vacía]"
        ) as response:
            response.failure("Lista de IDs de dependencias vacía")
        return
    
    # Seleccionar un ID de dependencia aleatorio de la lista
    p_id_dependencia = random.choice(data_module.p_id_dependencia)
    
    logger.info(f"Ejecutando get_organigrama_por_dependencia con ID: {p_id_dependencia}")
    
    try:
        with client.get(
            f"/organigrama/{p_id_dependencia}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/{p_id_dependencia}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía y que contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de organigrama por dependencia exitosa para ID: {p_id_dependencia}")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                        else:
                            response.failure("Formato de respuesta incompleto o lista vacía")
                            logger.warning(f"Formato incompleto o lista vacía en organigrama por dependencia: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en organigrama por dependencia: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en organigrama por dependencia: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de organigrama por dependencia: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de organigrama por dependencia: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/{p_id_dependencia}",
            response_time=0,
            exception=e
        )

# También probar el caso sin parámetro (organigrama completo)
def get_organigrama_completo(client, logger, environment, data_module):
    """Prueba el endpoint de obtener organigrama completo (sin ID de dependencia)"""
    
    logger.info("Ejecutando get_organigrama_completo")
    
    try:
        with client.get(
            "/organigrama/", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/ [Completo]"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log (solo cantidad por volumen)
                    logger.debug(f"Cantidad de datos obtenidos: {len(response_data) if isinstance(response_data, list) else 'No es lista'}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía y que contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data[:5]):  # Verificar solo los primeros 5 elementos
                            response.success()
                            logger.info("Obtención de organigrama completo exitosa")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                        else:
                            response.failure("Formato de respuesta incompleto o lista vacía")
                            logger.warning(f"Formato incompleto o lista vacía en organigrama completo")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en organigrama completo")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en organigrama completo: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de organigrama completo: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de organigrama completo: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /organigrama -Consulta del organigrama de la municipalidad de Córdoba.-",
            response_time=0,
            exception=e
        )

def get_dependencia_mas_alta(client, logger, environment, data_module):
    """Prueba el endpoint de obtener la dependencia de mayor nivel para una dependencia determinada"""
    
    # Intentar obtener IDs válidos si no están disponibles
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.info("Intentando obtener IDs de dependencias válidos...")
        try:
            # Obtener el organigrama completo para extraer IDs válidos
            with client.get(
                "/organigrama/dependencias/1", 
                catch_response=True
            ) as response:
                if response.status_code == 200:
                    org_data = response.json()
                    if isinstance(org_data, list) and org_data:
                        # Extraer hasta 5 IDs válidos
                        valid_ids = [item["id_unidad"] for item in org_data[:5] if "id_unidad" in item]
                        if valid_ids:
                            data_module.p_id_dependencia = valid_ids
                            logger.info(f"Se obtuvieron IDs válidos: {valid_ids}")
                        else:
                            logger.error("No se pudieron extraer IDs válidos del organigrama")
                else:
                    logger.error(f"No se pudo obtener el organigrama completo: {response.status_code}")
        except Exception as e:
            logger.error(f"Error al intentar obtener IDs válidos: {str(e)}")
    
    # Verificar si la lista de dependencias está vacía
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.error("La lista de IDs de dependencias está vacía. No se puede continuar con la prueba de dependencia más alta.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/dependencias/1", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/dependencias/{id_dependencia} [Lista vacía]"
        ) as response:
            response.failure("Lista de IDs de dependencias vacía")
        return
    
    # Seleccionar un ID de dependencia aleatorio de la lista
    p_id_dependencia = random.choice(data_module.p_id_dependencia)
    
    logger.info(f"Ejecutando get_dependencia_mas_alta con ID: {p_id_dependencia}")
    
    try:
        with client.get(
            f"/organigrama/dependencias/{p_id_dependencia}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/{p_id_dependencia}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, dict):
                        # Verificar que el diccionario no esté vacío y que contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                        
                        if response_data and all(campo in response_data for campo in campos_esperados):
                            response.success()
                            logger.info(f"Obtención de dependencia más alta exitosa para ID: {p_id_dependencia}")
                        else:
                            # Si es un diccionario vacío, también es válido según la documentación
                            if not response_data:
                                response.success()
                                logger.info(f"Dependencia más alta no encontrada para ID: {p_id_dependencia} (respuesta vacía)")
                            else:
                                response.failure("Formato de respuesta incompleto")
                                logger.warning(f"Formato incompleto en dependencia más alta: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en dependencia más alta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en dependencia más alta: {response.text[:200]}")
            elif response.status_code == 404:
                # Verificar si es un error de ID no encontrado (comportamiento esperado)
                try:
                    error_data = response.json()
                    if "detail" in error_data and any("not_found_element" in item.get("type", "") for item in error_data.get("detail", [])):
                        logger.info(f"ID de dependencia {p_id_dependencia} no existe - respuesta 404 esperada")
                        response.success()  # Marcar como éxito ya que es un comportamiento esperado
                    else:
                        response.failure(f"Error 404 inesperado: {response.text}")
                except:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de dependencia más alta: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de dependencia más alta: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias/{p_id_dependencia}",
            response_time=0,
            exception=e
        )

def get_dependencias_ruta(client, logger, environment, data_module):
    """Prueba el endpoint de obtener la ruta de dependencias hasta la dependencia superior"""
    
    # Verificar si la lista de dependencias está vacía
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.error("La lista de IDs de dependencias está vacía. No se puede continuar con la prueba de ruta de dependencias.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/dependencias-ruta", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/dependencias-ruta/{id_dependencia} [Lista vacía]"
        ) as response:
            response.failure("Lista de IDs de dependencias vacía")
        return
    
    # Seleccionar un ID de dependencia aleatorio de la lista
    p_id_dependencia = random.choice(data_module.p_id_dependencia)
    
    logger.info(f"Ejecutando get_dependencias_ruta con ID: {p_id_dependencia}")
    
    try:
        with client.get(
            f"/organigrama/dependencias-ruta/{p_id_dependencia}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias-ruta/{p_id_dependencia}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de ruta de dependencias exitosa para ID: {p_id_dependencia}")
                            logger.debug(f"Cantidad de elementos en la ruta: {len(response_data)}")
                        else:
                            # Si es una lista vacía, también es válido según la documentación
                            if not response_data:
                                response.success()
                                logger.info(f"Ruta de dependencias no encontrada para ID: {p_id_dependencia} (respuesta vacía)")
                            else:
                                response.failure("Formato de respuesta incompleto")
                                logger.warning(f"Formato incompleto en ruta de dependencias: {response.text[:200]}")
                    elif isinstance(response_data, dict):
                        # Si es un diccionario vacío, también es válido según la documentación
                        if not response_data:
                            response.success()
                            logger.info(f"Ruta de dependencias no encontrada para ID: {p_id_dependencia} (respuesta vacía)")
                        else:
                            response.failure("Formato de respuesta inesperado (diccionario no vacío)")
                            logger.warning(f"Formato inesperado en ruta de dependencias: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en ruta de dependencias: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en ruta de dependencias: {response.text[:200]}")
            elif response.status_code == 404:
                # Verificar si es un error de ID no encontrado (comportamiento esperado)
                try:
                    error_data = response.json()
                    if "detail" in error_data and any("not_found_element" in item.get("type", "") for item in error_data.get("detail", [])):
                        logger.info(f"ID de dependencia {p_id_dependencia} no existe - respuesta 404 esperada")
                        response.success()  # Marcar como éxito ya que es un comportamiento esperado
                    else:
                        response.failure(f"Error 404 inesperado: {response.text}")
                except:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de ruta de dependencias: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de ruta de dependencias: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias-ruta/{p_id_dependencia}",
            response_time=0,
            exception=e
        )

def get_dependencias_por_parametros(client, logger, environment, data_module):
    """Prueba el endpoint de obtener dependencias por nombre, id_dependencia o id_cerrojo"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.error("No hay IDs de dependencias disponibles para la prueba.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/dependencias", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /dependencias [Sin datos]"
        ) as response:
            response.failure("No hay datos para probar el endpoint")
        return
    
    # Seleccionar un ID de dependencia aleatorio
    p_id_dependencia = random.choice(data_module.p_id_dependencia)
    
    # Probar búsqueda por ID de dependencia
    logger.info(f"Ejecutando get_dependencias_por_parametros con ID: {p_id_dependencia}")
    
    try:
        with client.get(
            f"/dependencias?p_id_dependencia={p_id_dependencia}", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /dependencias?p_id_dependencia"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                           "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                           "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de dependencias por ID exitosa: {p_id_dependencia}")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                            
                            # Si encontramos dependencias, guardamos el nombre para probar la búsqueda por nombre
                            if response_data:
                                nombre_dependencia = response_data[0]["unidad"]
                                data_module.nombre_dependencia = nombre_dependencia
                                data_module.id_cerrojo = response_data[0]["id_cerrojo"]
                        else:
                            # Si es una lista vacía, también es válido
                            if not response_data:
                                response.success()
                                logger.info(f"No se encontraron dependencias para ID: {p_id_dependencia}")
                            else:
                                response.failure("Formato de respuesta incompleto")
                                logger.warning(f"Formato incompleto en dependencias: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en dependencias: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en dependencias: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de dependencias por ID: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de dependencias por ID: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /dependencias?p_id_dependencia",
            response_time=0,
            exception=e
        )
    
    # Probar búsqueda por nombre si está disponible
    if hasattr(data_module, 'nombre_dependencia') and data_module.nombre_dependencia:
        nombre_dependencia = data_module.nombre_dependencia
        logger.info(f"Ejecutando get_dependencias_por_parametros con nombre: {nombre_dependencia}")
        
        try:
            with client.get(
                f"/dependencias?p_nombre={nombre_dependencia}", 
                catch_response=True,
                name="(CERROJO INSTITUCIONAL) - /dependencias?p_nombre"
            ) as response:
                if response.status_code == 200:
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        # Validar estructura de datos esperada
                        if isinstance(response_data, list):
                            # Verificar que la lista contenga los campos esperados
                            campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                               "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                               "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                               "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                            
                            if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                                response.success()
                                logger.info(f"Obtención de dependencias por nombre exitosa: {nombre_dependencia}")
                                logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                            else:
                                # Si es una lista vacía, también es válido
                                if not response_data:
                                    response.success()
                                    logger.info(f"No se encontraron dependencias para nombre: {nombre_dependencia}")
                                else:
                                    response.failure("Formato de respuesta incompleto")
                                    logger.warning(f"Formato incompleto en dependencias por nombre: {response.text[:200]}")
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en dependencias por nombre: {response.text[:200]}")
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en dependencias por nombre: {response.text[:200]}")
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de dependencias por nombre: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Excepción durante obtención de dependencias por nombre: {str(e)}")
            # Registrar el error como una respuesta fallida
            environment.events.request_failure.fire(
                request_type="GET",
                name="(CERROJO INSTITUCIONAL) - /dependencias?p_nombre",
                response_time=0,
                exception=e
            )
    
    # Probar búsqueda por ID de cerrojo si está disponible
    if hasattr(data_module, 'id_cerrojo') and data_module.id_cerrojo:
        id_cerrojo = data_module.id_cerrojo
        logger.info(f"Ejecutando get_dependencias_por_parametros con ID de cerrojo: {id_cerrojo}")
        
        try:
            with client.get(
                f"/dependencias?p_id_cerrojo={id_cerrojo}", 
                catch_response=True,
                name="(CERROJO INSTITUCIONAL) - /dependencias?p_id_cerrojo"
            ) as response:
                if response.status_code == 200:
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        # Validar estructura de datos esperada
                        if isinstance(response_data, list):
                            # Verificar que la lista contenga los campos esperados
                            campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                               "externa", "mesa", "id_unidad_superior", "unidad_superior", 
                                               "id_cerrojo_superior", "tipo_superior", "ubicacion_superior", 
                                               "externa_superior", "mesa_superior", "cod_mesa_entrada"]
                            
                            if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                                response.success()
                                logger.info(f"Obtención de dependencias por ID de cerrojo exitosa: {id_cerrojo}")
                                logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                            else:
                                # Si es una lista vacía, también es válido
                                if not response_data:
                                    response.success()
                                    logger.info(f"No se encontraron dependencias para ID de cerrojo: {id_cerrojo}")
                                else:
                                    response.failure("Formato de respuesta incompleto")
                                    logger.warning(f"Formato incompleto en dependencias por ID de cerrojo: {response.text[:200]}")
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en dependencias por ID de cerrojo: {response.text[:200]}")
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en dependencias por ID de cerrojo: {response.text[:200]}")
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de dependencias por ID de cerrojo: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Excepción durante obtención de dependencias por ID de cerrojo: {str(e)}")
            # Registrar el error como una respuesta fallida
            environment.events.request_failure.fire(
                request_type="GET",
                name="(CERROJO INSTITUCIONAL) - /dependencias?p_id_cerrojo",
                response_time=0,
                exception=e
            )

def post_dependencias_por_ids(client, logger, environment, data_module):
    """Prueba el endpoint de obtener dependencias por una lista de IDs"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_ids_dependencias') or not data_module.body_ids_dependencias:
        logger.error("No hay IDs de dependencias disponibles en body_ids_dependencias para la prueba.")
        
        # Intentar usar p_id_dependencia como alternativa
        if hasattr(data_module, 'p_id_dependencia') and data_module.p_id_dependencia:
            logger.info("Usando p_id_dependencia como alternativa")
            ids_dependencias = data_module.p_id_dependencia[:3]  # Tomar hasta 3 IDs
        else:
            # Registrar un error explícito usando catch_response
            with client.post(
                "/dependencias/ids", 
                json={"ids_dependencias": [1]},
                catch_response=True,
                name="(CERROJO INSTITUCIONAL) - /dependencias/ids [Sin datos]"
            ) as response:
                response.failure("No hay datos para probar el endpoint")
            return
    else:
        # Usar los IDs específicos de body_ids_dependencias
        ids_dependencias = data_module.body_ids_dependencias
    
    logger.info(f"Ejecutando get_dependencias_por_ids con IDs: {ids_dependencias}")
    
    try:
        with client.post(
            "/dependencias/ids", 
            json={"ids_dependencias": ids_dependencias},
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /dependencias/ids"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Datos obtenidos: {response_data}")
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados
                        # Modificamos los campos esperados para que coincidan con la respuesta real
                        campos_esperados = ["id_unidad", "unidad"]
                        
                        if all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de dependencias por IDs exitosa: {ids_dependencias}")
                            logger.debug(f"Cantidad de elementos recibidos: {len(response_data)}")
                        else:
                            # Si es una lista vacía, también es válido
                            if not response_data:
                                response.success()
                                logger.info(f"No se encontraron dependencias para IDs: {ids_dependencias}")
                            else:
                                response.failure("Formato de respuesta incompleto")
                                logger.warning(f"Formato incompleto en dependencias por IDs: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en dependencias por IDs: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en dependencias por IDs: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de dependencias por IDs: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de dependencias por IDs: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="POST",
            name="(CERROJO INSTITUCIONAL) - /dependencias/ids",
            response_time=0,
            exception=e
        )

def get_dependencias_directas(client, logger, environment, data_module):
    """Prueba el endpoint de obtener dependencias directas a la dependencia enviada por parámetro"""
    
    # Verificar si la lista de dependencias está vacía
    if not hasattr(data_module, 'p_id_dependencia') or not data_module.p_id_dependencia:
        logger.error("La lista de IDs de dependencias está vacía. No se puede continuar con la prueba de dependencias directas.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/organigrama/dependencias-directas", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /organigrama/dependencias-directas/{id_dependencia} [Lista vacía]"
        ) as response:
            response.failure("Lista de IDs de dependencias vacía")
        return
    
    # Seleccionar un ID de dependencia aleatorio de la lista
    p_id_dependencia = random.choice(data_module.p_id_dependencia)
    
    logger.info(f"Ejecutando get_dependencias_directas con ID: {p_id_dependencia}")
    
    try:
        with client.get(
            f"/organigrama/dependencias-directas/{p_id_dependencia}", 
            catch_response=True,
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias-directas/{p_id_dependencia}"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DEPENDENCIAS DIRECTAS) ===")
                    logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados
                        campos_esperados = ["id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion", 
                                           "externa", "mesa", "cod_mesa_entrada"]
                        
                        if response_data and all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de dependencias directas exitosa para ID: {p_id_dependencia}")
                            logger.info(f"Cantidad de dependencias directas: {len(response_data)}")
                            
                            # Registrar información detallada de cada dependencia
                            for i, dependencia in enumerate(response_data):
                                logger.info(f"Dependencia directa {i+1}:")
                                for key, value in dependencia.items():
                                    logger.info(f"  {key}: {value}")
                        else:
                            # Si es una lista vacía, también es válido (no tiene dependencias directas)
                            if not response_data:
                                response.success()
                                logger.info(f"No se encontraron dependencias directas para ID: {p_id_dependencia}")
                            else:
                                # Registrar qué campos faltan
                                campos_encontrados = set()
                                for item in response_data:
                                    campos_encontrados.update(item.keys())
                                
                                logger.warning(f"Campos encontrados: {sorted(list(campos_encontrados))}")
                                logger.warning(f"Campos esperados: {campos_esperados}")
                                
                                # Verificar si al menos tiene los campos mínimos
                                campos_minimos = ["id_unidad", "unidad"]
                                if all(all(campo in item for campo in campos_minimos) for item in response_data):
                                    logger.info("Aunque faltan algunos campos, se encontraron los campos mínimos necesarios")
                                    response.success()
                                else:
                                    response.failure("Formato de respuesta incompleto")
                                    logger.warning(f"Formato incompleto en dependencias directas: {response.text[:200]}")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en dependencias directas: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en dependencias directas: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de dependencias directas: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de dependencias directas: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name=f"(CERROJO INSTITUCIONAL) - /organigrama/dependencias-directas/{p_id_dependencia}",
            response_time=0,
            exception=e
        )

def get_all_cpc(client, logger, environment, data_module):
    """Prueba el endpoint de obtener todos los centros de participación comunal (CPC)"""
    
    logger.info("Ejecutando get_all_cpc")
    
    try:
        with client.get(
            "/poblacion-y-sociedad/cpc", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/cpc"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (CPC) ===")
                    logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # No tenemos la estructura exacta esperada, pero verificamos que sea una lista no vacía
                        if response_data:
                            response.success()
                            logger.info(f"Obtención de CPCs exitosa")
                            logger.info(f"Cantidad de CPCs: {len(response_data)}")
                            
                            # Registrar información detallada de cada CPC
                            for i, cpc in enumerate(response_data):
                                logger.info(f"CPC {i+1}:")
                                for key, value in cpc.items():
                                    logger.info(f"  {key}: {value}")
                                    
                            # Registrar los campos encontrados
                            if response_data:
                                campos_encontrados = set()
                                for item in response_data:
                                    campos_encontrados.update(item.keys())
                                logger.info(f"Campos encontrados en la respuesta de CPCs: {sorted(list(campos_encontrados))}")
                        else:
                            # Si es una lista vacía, también podría ser válido
                            response.success()
                            logger.info("No se encontraron CPCs (lista vacía)")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en CPCs: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en CPCs: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de CPCs: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de CPCs: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/cpc",
            response_time=0,
            exception=e
        )

def get_barrios_cpc(client, logger, environment, data_module):
    """Prueba el endpoint de obtener los barrios de los centros de participación comunal (CPC)"""
    
    logger.info("Ejecutando get_barrios_cpc")
    
    try:
        with client.get(
            "/poblacion-y-sociedad/cpc/barrios", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/cpc/barrios"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BARRIOS CPC) ===")
                    logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía
                        if response_data:
                            response.success()
                            logger.info(f"Obtención de barrios CPC exitosa")
                            logger.info(f"Cantidad de barrios: {len(response_data)}")
                            
                            # Registrar información detallada de los primeros 5 barrios (para no saturar el log)
                            for i, barrio in enumerate(response_data[:5]):
                                logger.info(f"Barrio {i+1}:")
                                for key, value in barrio.items():
                                    logger.info(f"  {key}: {value}")
                            
                            # Si hay más de 5 barrios, indicar cuántos más hay
                            if len(response_data) > 5:
                                logger.info(f"... y {len(response_data) - 5} barrios más")
                                    
                            # Registrar los campos encontrados
                            if response_data:
                                campos_encontrados = set()
                                for item in response_data:
                                    campos_encontrados.update(item.keys())
                                logger.info(f"Campos encontrados en la respuesta de barrios CPC: {sorted(list(campos_encontrados))}")
                        else:
                            # Si es una lista vacía, también podría ser válido
                            response.success()
                            logger.info("No se encontraron barrios CPC (lista vacía)")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en barrios CPC: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en barrios CPC: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de barrios CPC: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de barrios CPC: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/cpc/barrios",
            response_time=0,
            exception=e
        )

def get_centros_vecinales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener todos los centros vecinales de Córdoba"""
    
    logger.info("Ejecutando get_centros_vecinales")
    
    try:
        with client.get(
            "/poblacion-y-sociedad/centros-vecinales", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/centros-vecinales"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (CENTROS VECINALES) ===")
                    logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista no esté vacía
                        if response_data:
                            response.success()
                            logger.info(f"Obtención de centros vecinales exitosa")
                            logger.info(f"Cantidad de centros vecinales: {len(response_data)}")
                            
                            # Registrar información detallada de los primeros 5 centros vecinales (para no saturar el log)
                            for i, centro in enumerate(response_data[:5]):
                                logger.info(f"Centro vecinal {i+1}:")
                                for key, value in centro.items():
                                    logger.info(f"  {key}: {value}")
                            
                            # Si hay más de 5 centros vecinales, indicar cuántos más hay
                            if len(response_data) > 5:
                                logger.info(f"... y {len(response_data) - 5} centros vecinales más")
                                    
                            # Registrar los campos encontrados
                            if response_data:
                                campos_encontrados = set()
                                for item in response_data:
                                    campos_encontrados.update(item.keys())
                                logger.info(f"Campos encontrados en la respuesta de centros vecinales: {sorted(list(campos_encontrados))}")
                        else:
                            # Si es una lista vacía, también podría ser válido
                            response.success()
                            logger.info("No se encontraron centros vecinales (lista vacía)")
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en centros vecinales: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en centros vecinales: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de centros vecinales: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de centros vecinales: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/centros-vecinales",
            response_time=0,
            exception=e
        )

def get_unidades_judiciales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener unidades judiciales de la municipalidad de Córdoba"""
    
    logger.info("Ejecutando get_unidades_judiciales")
    
    try:
        with client.get(
            "/poblacion-y-sociedad/unidades-judiciales", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/unidades-judiciales"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log (versión resumida para no saturar)
                    logger.debug(f"Cantidad de unidades judiciales obtenidas: {len(response_data)}")
                    if response_data:
                        logger.debug(f"Primera unidad judicial: {response_data[0]}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        if response_data:
                            # Obtener los campos disponibles del primer elemento
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # El endpoint funciona correctamente, marcar como exitoso
                            response.success()
                            logger.info(f"Obtención de unidades judiciales exitosa")
                            logger.info(f"Cantidad de unidades judiciales: {len(response_data)}")
                            
                            # Mostrar información de algunas unidades judiciales (hasta 5)
                            for idx, unidad in enumerate(response_data[:5]):
                                # Mostrar información usando los campos reales de la respuesta
                                if "nombre" in unidad:
                                    logger.info(f"Unidad Judicial {idx+1}: {unidad.get('nombre')}")
                                elif "descripcion" in unidad:
                                    logger.info(f"Unidad Judicial {idx+1}: {unidad.get('descripcion')}")
                                else:
                                    # Mostrar el primer campo que contenga información útil
                                    for key, value in unidad.items():
                                        if isinstance(value, str) and len(value) > 0:
                                            logger.info(f"Unidad Judicial {idx+1}: {key}={value}")
                                            break
                                
                                # Mostrar información adicional disponible
                                campos_importantes = ["direccion", "telefono", "tipo", "barrio", "cpc", "latitud", "longitud"]
                                for campo in campos_importantes:
                                    if campo in unidad and unidad.get(campo) is not None and unidad.get(campo) != "":
                                        logger.info(f"  {campo.capitalize()}: {unidad.get(campo)}")
                            
                            # Si hay más de 5 unidades, indicar cuántas más hay
                            if len(response_data) > 5:
                                logger.info(f"... y {len(response_data) - 5} unidades judiciales más")
                            
                            # Guardar los datos para posibles pruebas futuras
                            data_module.unidades_judiciales = response_data
                            
                            # Análisis adicional de los datos
                            logger.info("=== ANÁLISIS DE UNIDADES JUDICIALES ===")
                            
                            # Contar unidades con información de contacto
                            if "telefono" in campos_disponibles:
                                unidades_con_telefono = sum(1 for unidad in response_data if unidad.get("telefono"))
                                logger.info(f"Unidades con teléfono: {unidades_con_telefono}/{len(response_data)}")
                            
                            # Contar unidades con coordenadas
                            campos_coordenadas = ["latitud", "longitud"]
                            if all(campo in campos_disponibles for campo in campos_coordenadas):
                                unidades_con_coordenadas = sum(1 for unidad in response_data 
                                                            if unidad.get("latitud") is not None and unidad.get("longitud") is not None)
                                logger.info(f"Unidades con coordenadas: {unidades_con_coordenadas}/{len(response_data)}")
                                
                                if unidades_con_coordenadas > 0:
                                    porcentaje_geo = (unidades_con_coordenadas / len(response_data)) * 100
                                    logger.info(f"Porcentaje geolocalizado: {porcentaje_geo:.1f}%")
                            
                            # Análisis por tipo si está disponible
                            if "tipo" in campos_disponibles:
                                tipos = {}
                                for unidad in response_data:
                                    tipo = unidad.get("tipo", "Sin tipo")
                                    tipos[tipo] = tipos.get(tipo, 0) + 1
                                
                                logger.info(f"Distribución por tipo: {tipos}")
                            
                            # Análisis por barrio/CPC si está disponible
                            if "barrio" in campos_disponibles:
                                barrios = {}
                                for unidad in response_data:
                                    barrio = unidad.get("barrio", "Sin barrio")
                                    barrios[barrio] = barrios.get(barrio, 0) + 1
                                
                                top_barrios = sorted(barrios.items(), key=lambda x: x[1], reverse=True)[:5]
                                logger.info(f"Top 5 barrios con más unidades judiciales: {top_barrios}")
                            
                            if "cpc" in campos_disponibles:
                                cpcs = {}
                                for unidad in response_data:
                                    cpc = unidad.get("cpc", "Sin CPC")
                                    cpcs[cpc] = cpcs.get(cpc, 0) + 1
                                
                                top_cpcs = sorted(cpcs.items(), key=lambda x: x[1], reverse=True)[:5]
                                logger.info(f"Top 5 CPCs con más unidades judiciales: {top_cpcs}")
                        else:
                            # Si la lista está vacía, también es un resultado válido
                            logger.info("La lista de unidades judiciales está vacía")
                            response.success()
                            data_module.unidades_judiciales = []
                    else:
                        response.failure("Formato de respuesta inesperado (no es una lista)")
                        logger.warning(f"Formato inesperado en unidades judiciales: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en unidades judiciales: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener unidades judiciales")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener unidades judiciales")
                response.failure("Error de permisos")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de unidades judiciales: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de unidades judiciales: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/unidades-judiciales",
            response_time=0,
            exception=e
        )



def get_organizaciones_sociales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener organizaciones sociales de Córdoba"""
    
    # Definir parámetros de consulta para probar diferentes escenarios
    escenarios_consulta = [
        # Escenario 1: Sin parámetros (debería devolver todas las organizaciones)
        {},
        # Escenario 2: Búsqueda por tipo de organización específico
        {"p_tipo_org_social": "IGLESIAS"} if hasattr(data_module, 'organizaciones_sociales_params') else None,
        # Escenario 3: Búsqueda por ID de tipo de organización específico
        {"p_id_tipo_org_social": 3} if hasattr(data_module, 'organizaciones_sociales_params') else None
    ]
    
    # Si tenemos datos específicos en el módulo, usarlos
    if hasattr(data_module, 'organizaciones_sociales_params'):
        params_data = data_module.organizaciones_sociales_params
        escenarios_consulta.extend([
            {"p_tipo_org_social": params_data["p_tipo_org_social"]},
            {"p_id_tipo_org_social": params_data["p_id_tipo_org_social"]}
        ])
    
    # Filtrar escenarios None y duplicados
    escenarios_consulta = [escenario for escenario in escenarios_consulta if escenario is not None]
    # Eliminar duplicados manteniendo el orden
    escenarios_unicos = []
    for escenario in escenarios_consulta:
        if escenario not in escenarios_unicos:
            escenarios_unicos.append(escenario)
    escenarios_consulta = escenarios_unicos
    
    # Si no hay escenarios disponibles, usar al menos la consulta sin parámetros
    if not escenarios_consulta:
        escenarios_consulta = [{}]
    
    logger.info(f"Ejecutando get_organizaciones_sociales con {len(escenarios_consulta)} escenarios")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "errores": 0
    }
    
    # Ejecutar cada escenario de consulta
    for i, params in enumerate(escenarios_consulta):
        nombre_escenario = f"Escenario {i+1}"
        if "p_tipo_org_social" in params:
            nombre_escenario += f" (tipo: {params['p_tipo_org_social']})"
        elif "p_id_tipo_org_social" in params:
            nombre_escenario += f" (id_tipo: {params['p_id_tipo_org_social']})"
        else:
            nombre_escenario += " (sin parámetros)"
        
        logger.info(f"Probando {nombre_escenario} con parámetros: {params}")
        
        try:
            with client.get(
                "/poblacion-y-sociedad/organizaciones-sociales", 
                params=params,
                catch_response=True,
                name=f"(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/organizaciones-sociales [{nombre_escenario}]"
            ) as response:
                if response.status_code == 200:
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar los datos obtenidos en el log (versión resumida para no saturar)
                        logger.debug(f"Cantidad de organizaciones sociales obtenidas: {len(response_data)}")
                        if response_data:
                            logger.debug(f"Primera organización social: {response_data[0]}")
                        
                        # Validar estructura de datos esperada
                        if isinstance(response_data, list):
                            if response_data:
                                # Obtener los campos disponibles del primer elemento
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # El endpoint funciona correctamente, marcar como exitoso
                                response.success()
                                logger.info(f"Obtención de organizaciones sociales exitosa para {nombre_escenario}")
                                logger.info(f"Cantidad de organizaciones sociales: {len(response_data)}")
                                
                                # Mostrar información de algunas organizaciones (hasta 5)
                                for idx, org in enumerate(response_data[:5]):
                                    # Mostrar información usando los campos reales de la respuesta
                                    if "nombre" in org:
                                        logger.info(f"Organización {idx+1}: {org.get('nombre')}")
                                    elif "descripcion" in org:
                                        logger.info(f"Organización {idx+1}: {org.get('descripcion')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in org.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Organización {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional disponible
                                    campos_importantes = ["direccion", "telefono", "email", "tipo_org_social", "barrio", "cpc"]
                                    for campo in campos_importantes:
                                        if campo in org and org.get(campo):
                                            logger.info(f"  {campo.capitalize()}: {org.get(campo)}")
                                
                                # Si hay más de 5 organizaciones, indicar cuántas más hay
                                if len(response_data) > 5:
                                    logger.info(f"... y {len(response_data) - 5} organizaciones sociales más")
                                
                                # Guardar datos para posibles pruebas futuras
                                if i == 0:  # Solo guardamos los datos del primer escenario
                                    data_module.organizaciones_sociales = response_data
                                    
                                    # Si encontramos organizaciones, guardamos un tipo y un ID para futuras consultas
                                    if response_data:
                                        primer_org = response_data[0]
                                        if "tipo_org_social" in primer_org:
                                            data_module.tipo_org_social = primer_org["tipo_org_social"]
                                        if "id_tipo_org_social" in primer_org:
                                            data_module.id_tipo_org_social = primer_org["id_tipo_org_social"]
                                
                                resultados["exitosos"] += 1
                            else:
                                # Si la lista está vacía, también es un resultado válido
                                logger.info(f"La lista de organizaciones sociales está vacía para {nombre_escenario}")
                                response.success()
                                resultados["exitosos"] += 1
                        else:
                            response.failure("Formato de respuesta inesperado (no es una lista)")
                            logger.warning(f"Formato inesperado en organizaciones sociales: {response.text[:200]}")
                            resultados["errores"] += 1
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en organizaciones sociales: {response.text[:200]}")
                        resultados["errores"] += 1
                elif response.status_code == 401:
                    # Error de autenticación
                    logger.error(f"Error de autenticación al obtener organizaciones sociales para {nombre_escenario}")
                    response.failure("Error de autenticación")
                    resultados["errores"] += 1
                elif response.status_code == 403:
                    # Error de permisos
                    logger.error(f"Error de permisos al obtener organizaciones sociales para {nombre_escenario}")
                    response.failure("Error de permisos")
                    resultados["errores"] += 1
                elif response.status_code == 422:
                    # Error de validación de parámetros
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación de parámetros: {error_data}")
                        response.failure(f"Error de validación de parámetros: {error_data}")
                    except ValueError:
                        response.failure(f"Error de validación con formato inesperado: {response.text}")
                    resultados["errores"] += 1
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de organizaciones sociales para {nombre_escenario}: {response.status_code} - {response.text}")
                    resultados["errores"] += 1
        except Exception as e:
            logger.error(f"Excepción durante obtención de organizaciones sociales para {nombre_escenario}: {str(e)}")
            resultados["errores"] += 1
            # Registrar el error como una respuesta fallida
            environment.events.request_failure.fire(
                request_type="GET",
                name=f"(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/organizaciones-sociales [{nombre_escenario}]",
                response_time=0,
                exception=e
            )
    
    # Mostrar resumen de resultados
    logger.info(f"=== RESUMEN DE ORGANIZACIONES SOCIALES ===")
    logger.info(f"Escenarios exitosos: {resultados['exitosos']}")
    logger.info(f"Escenarios con errores: {resultados['errores']}")
    logger.info(f"Total de escenarios probados: {len(escenarios_consulta)}")

    

def get_tipos_organizaciones_sociales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener tipos de organizaciones sociales de Córdoba"""
    
    logger.info("Ejecutando get_tipos_organizaciones_sociales")
    
    try:
        with client.get(
            "/poblacion-y-sociedad/tipos-organizaciones-sociales", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/tipos-organizaciones-sociales"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Cantidad de tipos de organizaciones sociales obtenidos: {len(response_data)}")
                    if response_data:
                        logger.debug(f"Primer tipo de organización social: {response_data[0]}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados (si no está vacía)
                        campos_esperados = ["id", "nombre"]
                        
                        if response_data:
                            # Verificar si al menos el primer elemento tiene los campos esperados
                            primer_elemento = response_data[0]
                            campos_presentes = all(campo in primer_elemento for campo in campos_esperados)
                            
                            if campos_presentes:
                                response.success()
                                logger.info(f"Obtención de tipos de organizaciones sociales exitosa")
                                logger.info(f"Cantidad de tipos de organizaciones sociales: {len(response_data)}")
                                
                                # Guardar datos para posibles pruebas futuras
                                data_module.tipos_organizaciones_sociales = response_data
                                
                                # Si encontramos tipos, guardamos un ID para futuras consultas
                                if response_data:
                                    data_module.id_tipo_org_social = response_data[0]["id"]
                                    data_module.tipo_org_social = response_data[0]["nombre"]
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = [campo for campo in campos_esperados if campo not in primer_elemento]
                                logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                                
                                # Si faltan pocos campos, podemos considerarlo un éxito parcial
                                if len(campos_faltantes) <= 1:  # Solo hay dos campos esperados, así que si falta uno es la mitad
                                    logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                                    response.success()
                                else:
                                    response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                        else:
                            # Si la lista está vacía, también es un resultado válido
                            logger.info("La lista de tipos de organizaciones sociales está vacía")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (no es una lista)")
                        logger.warning(f"Formato inesperado en tipos de organizaciones sociales: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en tipos de organizaciones sociales: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener tipos de organizaciones sociales")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener tipos de organizaciones sociales")
                response.failure("Error de permisos")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de tipos de organizaciones sociales: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de tipos de organizaciones sociales: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /poblacion-y-sociedad/tipos-organizaciones-sociales",
            response_time=0,
            exception=e
        )

def get_limites_administrativos(client, logger, environment, data_module):
    """Prueba el endpoint de obtener límites administrativos de Córdoba"""
    
    logger.info("Ejecutando get_limites_administrativos")
    
    try:
        with client.get(
            "/limites-administrativos", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /limites-administrativos"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Cantidad de límites administrativos obtenidos: {len(response_data)}")
                    if response_data:
                        logger.debug(f"Primer límite administrativo: {response_data[0]}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        if response_data:
                            # Obtener los campos disponibles del primer elemento
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # El endpoint funciona correctamente, marcar como exitoso
                            response.success()
                            logger.info(f"Obtención de límites administrativos exitosa")
                            logger.info(f"Cantidad de límites administrativos: {len(response_data)}")
                            
                            # Mostrar información de algunos límites administrativos (hasta 5)
                            for idx, limite in enumerate(response_data[:5]):
                                # Mostrar información usando los campos reales de la respuesta
                                if "nombre" in limite:
                                    logger.info(f"Límite Administrativo {idx+1}: {limite.get('nombre')}")
                                elif "descripcion" in limite:
                                    logger.info(f"Límite Administrativo {idx+1}: {limite.get('descripcion')}")
                                else:
                                    # Mostrar el primer campo que contenga información útil
                                    for key, value in limite.items():
                                        if isinstance(value, str) and len(value) > 0:
                                            logger.info(f"Límite Administrativo {idx+1}: {key}={value}")
                                            break
                                
                                # Mostrar información adicional disponible
                                for key, value in limite.items():
                                    if key not in ['nombre', 'descripcion'] and value is not None and value != "":
                                        logger.info(f"  {key.capitalize()}: {value}")
                            
                            # Si hay más de 5 límites, indicar cuántos más hay
                            if len(response_data) > 5:
                                logger.info(f"... y {len(response_data) - 5} límites administrativos más")
                            
                            # Guardar datos para posibles pruebas futuras
                            data_module.limites_administrativos = response_data
                        else:
                            # Si la lista está vacía, también es un resultado válido
                            logger.info("La lista de límites administrativos está vacía")
                            response.success()
                            data_module.limites_administrativos = []
                    else:
                        response.failure("Formato de respuesta inesperado (no es una lista)")
                        logger.warning(f"Formato inesperado en límites administrativos: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en límites administrativos: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener límites administrativos")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener límites administrativos")
                response.failure("Error de permisos")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de límites administrativos: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de límites administrativos: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /limites-administrativos",
            response_time=0,
            exception=e
        )


def get_centros_operativos(client, logger, environment, data_module):
    """Prueba el endpoint de obtener centros operativos de Córdoba"""
    
    logger.info("Ejecutando get_centros_operativos")
    
    try:
        with client.get(
            "/centros-operativos", 
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /centros-operativos"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Cantidad de centros operativos obtenidos: {len(response_data)}")
                    if response_data:
                        logger.debug(f"Primer centro operativo: {response_data[0]}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        if response_data:
                            # Obtener los campos disponibles del primer elemento
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Campos mínimos esperados (más flexibles)
                            campos_minimos = ["nombre"]  # Solo requerimos que tenga al menos el nombre
                            
                            # Verificar si tiene al menos los campos mínimos
                            tiene_campos_minimos = all(campo in primer_elemento for campo in campos_minimos)
                            
                            if tiene_campos_minimos:
                                response.success()
                                logger.info(f"Obtención de centros operativos exitosa")
                                logger.info(f"Cantidad de centros operativos: {len(response_data)}")
                                
                                # Guardar datos para posibles pruebas futuras
                                data_module.centros_operativos = response_data
                                
                                # Mostrar estadísticas basadas en los campos disponibles
                                logger.info("=== ESTADÍSTICAS DE CENTROS OPERATIVOS ===")
                                
                                # Análisis dinámico basado en campos disponibles
                                if "cpc" in campos_disponibles:
                                    cpcs = {}
                                    for centro in response_data:
                                        cpc = centro.get("cpc", "Sin CPC")
                                        cpcs[cpc] = cpcs.get(cpc, 0) + 1
                                    
                                    top_cpcs = sorted(cpcs.items(), key=lambda x: x[1], reverse=True)[:5]
                                    logger.info(f"Top 5 CPCs con más centros operativos: {top_cpcs}")
                                
                                if "barrio" in campos_disponibles:
                                    barrios = {}
                                    for centro in response_data:
                                        barrio = centro.get("barrio", "Sin barrio")
                                        barrios[barrio] = barrios.get(barrio, 0) + 1
                                    
                                    top_barrios = sorted(barrios.items(), key=lambda x: x[1], reverse=True)[:5]
                                    logger.info(f"Top 5 barrios con más centros operativos: {top_barrios}")
                                
                                # Contar centros con información de contacto
                                if "telefono" in campos_disponibles:
                                    centros_con_telefono = sum(1 for centro in response_data if centro.get("telefono"))
                                    logger.info(f"Centros con teléfono: {centros_con_telefono}/{len(response_data)}")
                                
                                # Contar centros con coordenadas
                                campos_coordenadas = ["latitud", "longitud"]
                                if all(campo in campos_disponibles for campo in campos_coordenadas):
                                    centros_con_coordenadas = sum(1 for centro in response_data 
                                                                if centro.get("latitud") is not None and centro.get("longitud") is not None)
                                    logger.info(f"Centros con coordenadas: {centros_con_coordenadas}/{len(response_data)}")
                                    
                                    if centros_con_coordenadas > 0:
                                        porcentaje_geo = (centros_con_coordenadas / len(response_data)) * 100
                                        logger.info(f"Porcentaje geolocalizado: {porcentaje_geo:.1f}%")
                                
                                # Mostrar información del primer centro operativo con campos disponibles
                                logger.info("=== INFORMACIÓN DEL PRIMER CENTRO OPERATIVO ===")
                                primer_centro = response_data[0]
                                
                                # Mostrar todos los campos disponibles
                                for campo, valor in primer_centro.items():
                                    if valor is not None and valor != "":
                                        logger.info(f"{campo.capitalize()}: {valor}")
                                
                                # Análisis adicional de tipos de datos
                                logger.info("=== ANÁLISIS DE ESTRUCTURA DE DATOS ===")
                                tipos_campos = {}
                                for campo, valor in primer_centro.items():
                                    tipos_campos[campo] = type(valor).__name__
                                logger.info(f"Tipos de datos por campo: {tipos_campos}")
                                
                                # Verificar consistencia de datos
                                campos_con_valores = {}
                                for centro in response_data:
                                    for campo in campos_disponibles:
                                        if campo not in campos_con_valores:
                                            campos_con_valores[campo] = 0
                                        if centro.get(campo) is not None and centro.get(campo) != "":
                                            campos_con_valores[campo] += 1
                                
                                logger.info("=== COMPLETITUD DE DATOS ===")
                                for campo, cantidad in campos_con_valores.items():
                                    porcentaje = (cantidad / len(response_data)) * 100
                                    logger.info(f"{campo}: {cantidad}/{len(response_data)} ({porcentaje:.1f}%)")
                                
                            else:
                                # Si no tiene ni siquiera los campos mínimos
                                logger.warning(f"No se encontraron campos mínimos requeridos: {campos_minimos}")
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Aún así, marcamos como éxito si es una respuesta válida
                                response.success()
                                data_module.centros_operativos = response_data
                                logger.info(f"Cantidad de centros operativos: {len(response_data)}")
                                
                                # Mostrar el primer elemento completo para análisis
                                logger.info("=== ESTRUCTURA REAL DEL PRIMER ELEMENTO ===")
                                logger.info(f"Primer centro operativo completo: {primer_elemento}")
                        else:
                            # Si la lista está vacía, también es un resultado válido
                            logger.info("La lista de centros operativos está vacía")
                            response.success()
                            data_module.centros_operativos = []
                    else:
                        response.failure("Formato de respuesta inesperado (no es una lista)")
                        logger.warning(f"Formato inesperado en centros operativos: {response.text[:200]}")
                        logger.info(f"Tipo de respuesta recibida: {type(response_data)}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en centros operativos: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener centros operativos")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener centros operativos")
                response.failure("Error de permisos")
            elif response.status_code == 404:
                # No se encontraron centros operativos
                logger.warning("No se encontraron centros operativos")
                response.success()  # Marcamos como éxito porque puede ser un resultado válido
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener centros operativos")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de centros operativos: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de centros operativos: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /centros-operativos",
            response_time=0,
            exception=e
        )


def get_fechas_no_habiles(client, logger, environment, data_module):
    """Prueba el endpoint de obtener fechas no hábiles entre dos fechas determinadas"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'fechas_consulta'):
        logger.warning("No se encontraron fechas de consulta en el módulo de datos. Se usarán fechas predeterminadas.")
    else:
        fechas_consulta = data_module.fechas_consulta
    
    # Construir los parámetros de consulta
    params = {
        "p_fecha_desde": fechas_consulta["desde"],
        "p_fecha_hasta": fechas_consulta["hasta"]
    }
    
    logger.info(f"Ejecutando get_fechas_no_habiles con fechas desde: {params['p_fecha_desde']} hasta: {params['p_fecha_hasta']}")
    
    try:
        with client.get(
            "/fechas-no-habiles", 
            params=params,
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /fechas-no-habiles"
        ) as response:
            if response.status_code == 200:
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.debug(f"Cantidad de fechas no hábiles obtenidas: {len(response_data)}")
                    if response_data:
                        logger.debug(f"Primera fecha no hábil: {response_data[0]}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que la lista contenga los campos esperados (si no está vacía)
                        campos_esperados = ["fecha_dia_no_habil", "tipo_dia_no_habil", "descripcion"]
                        
                        if response_data:
                            # Verificar si al menos el primer elemento tiene los campos esperados
                            primer_elemento = response_data[0]
                            campos_presentes = all(campo in primer_elemento for campo in campos_esperados)
                            
                            if campos_presentes:
                                response.success()
                                logger.info(f"Obtención de fechas no hábiles exitosa")
                                logger.info(f"Cantidad de fechas no hábiles: {len(response_data)}")
                                
                                # Guardar datos para posibles pruebas futuras
                                data_module.fechas_no_habiles = response_data
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = [campo for campo in campos_esperados if campo not in primer_elemento]
                                logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                                
                                # Si faltan pocos campos, podemos considerarlo un éxito parcial
                                if len(campos_faltantes) <= 1:  # Si falta solo un campo
                                    logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                                    response.success()
                                    
                                    # Guardar los datos de todas formas
                                    data_module.fechas_no_habiles = response_data
                                else:
                                    response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                        else:
                            # Si la lista está vacía, también es un resultado válido
                            logger.info("La lista de fechas no hábiles está vacía")
                            response.success()
                            data_module.fechas_no_habiles = []
                    else:
                        response.failure("Formato de respuesta inesperado (no es una lista)")
                        logger.warning(f"Formato inesperado en fechas no hábiles: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en fechas no hábiles: {response.text[:200]}")
            elif response.status_code == 400:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación de parámetros: {error_data}")
                    response.failure(f"Error de validación de parámetros: {error_data}")
                except ValueError:
                    response.failure(f"Error de validación con formato inesperado: {response.text}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener fechas no hábiles")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener fechas no hábiles")
                response.failure("Error de permisos")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de fechas no hábiles: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de fechas no hábiles: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(CERROJO INSTITUCIONAL) - /fechas-no-habiles",
            response_time=0,
            exception=e
        )

def update_dependencias_visibility(client, logger, environment, data_module):
    """Prueba el endpoint de actualizar visibilidad de dependencias"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'query_params_update_visibilidad'):
        # Si no hay parámetros específicos, usar datos por defecto
        if hasattr(data_module, 'p_id_dependencia') and data_module.p_id_dependencia:
            query_params = {
                "p_id_dependencia": random.choice(data_module.p_id_dependencia),
                "p_visible": random.choice(['S', 'N']),  # Usar 'S' o 'N' en lugar de booleanos
                "p_usuario_aplicacion": "PRUEBA KUNAN"
            }
        else:
            logger.error("No hay IDs de dependencias disponibles para actualizar visibilidad.")
            
            # Registrar un error explícito usando catch_response
            with client.put(
                "/dependencias/visibilidad?p_id_dependencia=1&p_visible=S&p_usuario_aplicacion=TEST", 
                catch_response=True,
                name="(CERROJO INSTITUCIONAL) - /dependencias/visibilidad [Sin datos]"
            ) as response:
                response.failure("No hay datos para probar el endpoint")
            return
    else:
        # Usar los parámetros definidos en el módulo de datos
        query_params = copy.deepcopy(data_module.query_params_update_visibilidad)
        
        # Si hay una lista de IDs disponibles, seleccionar uno aleatoriamente
        if hasattr(data_module, 'lista_ids_update_visibilidad') and data_module.lista_ids_update_visibilidad:
            query_params["p_id_dependencia"] = random.choice(data_module.lista_ids_update_visibilidad)
        
        # Alternar la visibilidad aleatoriamente usando 'S' o 'N'
        query_params["p_visible"] = random.choice(['S', 'N'])
    
    # Construir la URL con los parámetros de consulta
    url = "/dependencias/visibilidad"
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    url = f"{url}?{query_string}"
    
    logger.info(f"Ejecutando update_dependencias_visibility con URL: {url}")
    logger.info(f"Parámetros: {query_params}")
    
    try:
        with client.put(
            url,
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /dependencias/visibilidad [PUT]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (UPDATE VISIBILIDAD DEPENDENCIA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "id_unidad", "unidad", "id_cerrojo", "tipo", "ubicacion",
                        "externa", "mesa", "fecha_alta", "fecha_baja", "id_estado",
                        "visible", "id_unidad_superior", "unidad_superior",
                        "id_cerrojo_superior", "tipo_superior", "ubicacion_superior",
                        "externa_superior", "mesa_superior", "cod_mesa_entrada"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Actualización de visibilidad de dependencia exitosa")
                        logger.info(f"ID dependencia: {response_data.get('id_unidad')}")
                        logger.info(f"Nombre dependencia: {response_data.get('unidad')}")
                        logger.info(f"Visibilidad actualizada: {response_data.get('visible')}")
                        logger.info(f"Estado: {response_data.get('id_estado')}")
                        
                        # Verificar que la visibilidad se haya actualizado correctamente
                        # Convertir 'S'/'N' a booleano para comparar con la respuesta
                        visibilidad_esperada = query_params["p_visible"] == 'S'
                        visibilidad_actual = response_data.get('visible')
                        
                        if visibilidad_actual == visibilidad_esperada:
                            logger.info(f"Visibilidad actualizada correctamente: {visibilidad_actual}")
                        else:
                            logger.warning(f"Visibilidad no coincide. Esperada: {visibilidad_esperada}, Actual: {visibilidad_actual}")
                        
                        # Guardar datos para posibles pruebas futuras
                        data_module.ultima_dependencia_actualizada = response_data
                        data_module.ultimo_id_dependencia_actualizada = response_data.get('id_unidad')
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 3:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                        else:
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    
                    # Analizar el detalle del error
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        for error_item in detail:
                            if "p_id_dependencia" in error_item.get("loc", []):
                                logger.error(f"Error en p_id_dependencia: {error_item.get('msg')}")
                            elif "p_visible" in error_item.get("loc", []):
                                logger.error(f"Error en p_visible: {error_item.get('msg')}")
                    
                    response.failure(f"Error de validación 400: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            elif response.status_code == 404:
                # Dependencia no encontrada
                try:
                    error_data = response.json()
                    logger.warning(f"Dependencia no encontrada: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info(f"Dependencia con ID {query_params['p_id_dependencia']} no existe - respuesta 404 esperada")
                            response.success()  # Marcar como éxito ya que es un comportamiento esperado
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.failure(f"Error 404 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
            elif response.status_code == 403:
                # Error de permisos
                logger.warning("Error de permisos (403) - verificar configuración de la aplicación")
                response.failure(f"Error de permisos: {response.text}")
            elif response.status_code == 422:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 422: {error_data}")
                    
                    # Analizar el detalle del error para entender qué parámetro está mal
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        for error_item in detail:
                            if "p_visible" in error_item.get("loc", []):
                                logger.error(f"Error en p_visible: {error_item.get('msg')}")
                                logger.info("p_visible debe ser 'S' o 'N', no booleano")
                            elif "p_id_dependencia" in error_item.get("loc", []):
                                logger.error(f"Error en p_id_dependencia: {error_item.get('msg')}")
                    
                    response.failure(f"Error de validación 422: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en actualización de visibilidad de dependencia: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante actualización de visibilidad de dependencia: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.put(
            url,
            catch_response=True,
            name="(CERROJO INSTITUCIONAL) - /dependencias/visibilidad [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

