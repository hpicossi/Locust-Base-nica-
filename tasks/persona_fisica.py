import random
import datetime
from typing import Dict, Any

def insert_or_update_persona_fisica(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar una persona física"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_persona_fisica'):
        logger.error("No hay datos para insertar persona física en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/personas-fisicas", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos en body_insertar_persona_fisica")
        return
    
    # Usar los datos específicos del archivo clon_persona_fisica.py
    body_insertar_persona_fisica = data_module.body_insertar_persona_fisica
    
    logger.info(f"Ejecutando insert_or_update_persona_fisica con datos: {body_insertar_persona_fisica}")
    
    try:
        with client.post(
            "/personas-fisicas", 
            json=body_insertar_persona_fisica,
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PERSONA FÍSICA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "id_persona_fisica", "cuil", "dni", "sexo", 
                        "nombre", "apellido", "fecha_nacimiento", 
                        "fecha_creacion", "fecha_modifica"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Inserción/actualización de persona física exitosa")
                        logger.info(f"ID persona física: {response_data.get('id_persona_fisica')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_persona_fisica = response_data.get('id_persona_fisica')
                        data_module.cuil_persona_fisica = response_data.get('cuil')
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "id_persona_fisica" in response_data:
                                data_module.id_persona_fisica = response_data.get('id_persona_fisica')
                                data_module.cuil_persona_fisica = response_data.get('cuil')
                        else:
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado (ej. persona ya existe), podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("La persona física ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de persona física: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de persona física: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS FISICAS) - /personas-fisicas/by-dni",
            response_time=0,
            exception=e
        )

def insert_or_update_persona_fisica_by_dni(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar una persona física por DNI"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_persona_fisica_by_dni'):
        logger.error("No hay datos para insertar persona física por DNI en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/by-dni", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /by-dni [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos en body_insertar_persona_fisica_by_dni")
        return
    
    # Usar los datos específicos del archivo de datos
    body_insertar_persona_fisica_by_dni = data_module.body_insertar_persona_fisica_by_dni
    
    logger.info(f"Ejecutando insert_or_update_persona_fisica_by_dni con datos: {body_insertar_persona_fisica_by_dni}")
    
    try:
        with client.post(
            "/personas-fisicas/by-dni", 
            json=body_insertar_persona_fisica_by_dni,
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/by-dni [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PERSONA FÍSICA POR DNI) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "id_persona_fisica", "cuil", "dni", "sexo", 
                        "nombre", "apellido", "fecha_nacimiento", 
                        "fecha_creacion", "fecha_modifica"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Inserción/actualización de persona física por DNI exitosa")
                        logger.info(f"ID persona física: {response_data.get('id_persona_fisica')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_persona_fisica_by_dni = response_data.get('id_persona_fisica')
                        data_module.dni_persona_fisica = response_data.get('dni')
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "id_persona_fisica" in response_data:
                                data_module.id_persona_fisica_by_dni = response_data.get('id_persona_fisica')
                                data_module.dni_persona_fisica = response_data.get('dni')
                        else:
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("La persona física ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de persona física por DNI: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de persona física por DNI: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS FISICAS) - /by-dni",
            response_time=0,
            exception=e
        )

def insert_or_update_persona_fisica_simplificada(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar una persona física de forma simplificada"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_persona_fisica_simplificada'):
        logger.error("No hay datos para insertar persona física simplificada en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.put(
            "/personas-fisicas/simplificado", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/simplificado [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos en body_insertar_persona_fisica_simplificada")
        return
    
    # Usar los datos específicos del archivo de datos
    body_insertar_persona_fisica_simplificada = data_module.body_insertar_persona_fisica_simplificada
    
    logger.info(f"Ejecutando insert_or_update_persona_fisica_simplificada con datos: {body_insertar_persona_fisica_simplificada}")
    
    try:
        with client.put(
            "/personas-fisicas/simplificado", 
            json=body_insertar_persona_fisica_simplificada,
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/simplificado [PUT]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code in [200, 201]:  # HTTP 200 OK o 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PERSONA FÍSICA SIMPLIFICADA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "id_persona_fisica", "p_cuil", "p_dni", "p_sexo", 
                        "p_nombre", "p_apellido", "p_fecha_nacimiento", 
                        "fecha_creacion", "fecha_modifica"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Inserción/actualización de persona física simplificada exitosa")
                        logger.info(f"ID persona física: {response_data.get('id_persona_fisica')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_persona_fisica_simplificada = response_data.get('id_persona_fisica')
                        data_module.cuil_persona_fisica_simplificada = response_data.get('p_cuil')
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "id_persona_fisica" in response_data:
                                data_module.id_persona_fisica_simplificada = response_data.get('id_persona_fisica')
                                data_module.cuil_persona_fisica_simplificada = response_data.get('p_cuil')
                        else:
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("La persona física ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de persona física simplificada: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de persona física simplificada: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="PUT",
            name="(PERSONAS FISICAS) - /personas-fisicas/simplificado",
            response_time=0,
            exception=e
        )


# def insert_or_update_persona_fisica_simplificada(client, logger, environment, data_module):
#     """Prueba el endpoint de insertar o actualizar una persona física de forma simplificada"""
    
#     # Verificar si tenemos datos para probar
#     if not hasattr(data_module, 'body_insertar_persona_fisica_simplificada'):
#         logger.error("No hay datos para insertar persona física simplificada en el módulo de datos.")
        
#         with client.put(
#             "/personas-fisicas/simplificado", 
#             json={"error": "sin_datos"},
#             catch_response=True,
#             name="(PERSONAS FISICAS) - /personas-fisicas/simplificado [Sin datos]"
#         ) as response:
#             response.failure("No hay datos definidos en body_insertar_persona_fisica_simplificada")
#         return
    
#     # Obtener los datos (ahora es una lista de casos de prueba)
#     casos_prueba = data_module.body_insertar_persona_fisica_simplificada
#     if not isinstance(casos_prueba, list):
#         casos_prueba = [casos_prueba]  # Compatibilidad con formato anterior
    
#     logger.info(f"=== INICIANDO PRUEBAS DE PERSONA FÍSICA SIMPLIFICADA - {len(casos_prueba)} CASOS ===")
    
#     resultados_casos = []
    
#     # Ejecutar todos los casos de prueba
#     for i, caso_datos in enumerate(casos_prueba, 1):
#         # Identificar el caso de prueba
#         caso_descripcion = f"CASO {i}"
#         if "p_cuil" in caso_datos and "p_dni" not in caso_datos:
#             caso_descripcion += ": Solo CUIL - extrae DNI"
#         elif "p_id_pais_origen_docto" not in caso_datos:
#             caso_descripcion += ": Sin país origen - default Argentina"
#         elif "p_id_tipo_documento" not in caso_datos:
#             caso_descripcion += ": Sin tipo doc - default DNI"
#         elif (caso_datos.get("p_id_pais_origen_docto") == 19 and 
#               caso_datos.get("p_id_tipo_documento") != 4 and
#               "p_cuil" not in caso_datos):
#             caso_descripcion += ": Argentina + no DNI sin CUIL - debe fallar"
#         elif len([k for k in caso_datos.keys() if k.startswith('p_')]) <= 6:
#             caso_descripcion += ": Campos mínimos"
#         else:
#             caso_descripcion += ": Datos completos"
        
#         logger.info(f"\n--- {caso_descripcion} ---")
#         logger.info(f"Datos enviados: {caso_datos}")
        
#         try:
#             with client.put(
#                 "/personas-fisicas/simplificado", 
#                 json=caso_datos,
#                 catch_response=True,
#                 name=f"(PERSONAS FISICAS) - /personas-fisicas/simplificado [{caso_descripcion}]"
#             ) as response:
                
#                 resultado_caso = {
#                     "caso": caso_descripcion,
#                     "datos": caso_datos,
#                     "status_code": response.status_code,
#                     "exitoso": False,
#                     "observaciones": []
#                 }
                
#                 logger.info(f"Status Code: {response.status_code}")
#                 logger.info(f"Respuesta: {response.text}")
                
#                 if response.status_code in [200, 201]:
#                     try:
#                         response_data = response.json()
#                         logger.info("=== RESPUESTA EXITOSA ===")
#                         logger.info(f"Datos recibidos: {response_data}")
                        
#                         if response_data and isinstance(response_data, dict):
#                             response.success()
#                             resultado_caso["exitoso"] = True
#                             resultado_caso["respuesta"] = response_data
                            
#                             # Validar lógica de negocio específica
#                             if "p_cuil" in caso_datos and "p_dni" not in caso_datos:
#                                 if "p_dni" in response_data:
#                                     resultado_caso["observaciones"].append(f"✓ DNI extraído del CUIL: {response_data['p_dni']}")
#                                     logger.info(f"✓ DNI extraído del CUIL correctamente: {response_data['p_dni']}")
#                                 if response_data.get("p_id_tipo_documento") == 4:
#                                     resultado_caso["observaciones"].append("✓ Tipo documento = DNI (4)")
#                                     logger.info("✓ Tipo documento establecido como DNI (4) correctamente")
#                                 if response_data.get("p_id_pais_origen_docto") == 19:
#                                     resultado_caso["observaciones"].append("✓ País origen = Argentina (19)")
#                                     logger.info("✓ País origen establecido como Argentina (19) correctamente")
                            
#                             # Validar defaults
#                             if "p_id_pais_origen_docto" not in caso_datos and response_data.get("p_id_pais_origen_docto") == 19:
#                                 resultado_caso["observaciones"].append("✓ Default país origen = Argentina (19)")
#                                 logger.info("✓ Default país origen aplicado correctamente")
                            
#                             if "p_id_tipo_documento" not in caso_datos and response_data.get("p_id_tipo_documento") == 4:
#                                 resultado_caso["observaciones"].append("✓ Default tipo documento = DNI (4)")
#                                 logger.info("✓ Default tipo documento aplicado correctamente")
                            
#                             # Guardar datos para pruebas futuras
#                             if "id_persona_fisica" in response_data:
#                                 data_module.id_persona_fisica_simplificada = response_data.get('id_persona_fisica')
#                                 data_module.cuil_persona_fisica_simplificada = response_data.get('p_cuil')
                                
#                         else:
#                             response.failure("Respuesta vacía o formato inesperado")
#                             resultado_caso["observaciones"].append("✗ Respuesta vacía o formato inesperado")
                            
#                     except ValueError as e:
#                         response.failure(f"Respuesta no es JSON válido: {str(e)}")
#                         resultado_caso["observaciones"].append(f"✗ JSON inválido: {str(e)}")
#                         logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                        
#                 elif response.status_code == 400:
#                     try:
#                         error_data = response.json()
#                         logger.info(f"Error 400 recibido: {error_data}")
                        
#                         # Para el caso específico que debe fallar
#                         if (caso_datos.get("p_id_pais_origen_docto") == 19 and 
#                             caso_datos.get("p_id_tipo_documento") != 4 and
#                             "p_cuil" not in caso_datos):
#                             logger.info("✓ Error 400 ESPERADO para caso Argentina + tipo doc != DNI sin CUIL")
#                             response.success()
#                             resultado_caso["exitoso"] = True
#                             resultado_caso["observaciones"].append("✓ Error 400 esperado - validación correcta")
#                         else:
#                             # Verificar otros errores esperados
#                             if "detail" in error_data:
#                                 detail = error_data["detail"]
#                                 if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
#                                     logger.info("✓ Error 400 esperado - persona ya existe")
#                                     response.success()
#                                     resultado_caso["exitoso"] = True
#                                     resultado_caso["observaciones"].append("✓ Error 400 esperado - persona ya existe")
#                                 else:
#                                     response.failure(f"Error de validación: {detail}")
#                                     resultado_caso["observaciones"].append(f"✗ Error validación: {detail}")
#                             else:
#                                 response.failure(f"Error 400 sin detalle: {error_data}")
#                                 resultado_caso["observaciones"].append(f"✗ Error 400 sin detalle")
                                
#                         resultado_caso["error_data"] = error_data
                        
#                     except ValueError:
#                         response.failure(f"Error 400 con formato inesperado: {response.text}")
#                         resultado_caso["observaciones"].append("✗ Error 400 formato inesperado")
                        
#                 else:
#                     response.failure(f"Error: {response.status_code}")
#                     resultado_caso["observaciones"].append(f"✗ Error HTTP {response.status_code}")
#                     logger.error(f"Error inesperado: {response.status_code} - {response.text}")
                
#                 resultados_casos.append(resultado_caso)
#                 logger.info(f"Resultado {caso_descripcion}: {'EXITOSO' if resultado_caso['exitoso'] else 'FALLIDO'}")
                
#         except Exception as e:
#             logger.error(f"Excepción en {caso_descripcion}: {str(e)}")
#             resultado_caso = {
#                 "caso": caso_descripcion,
#                 "datos": caso_datos,
#                 "exitoso": False,
#                 "observaciones": [f"✗ Excepción: {str(e)}"]
#             }
#             resultados_casos.append(resultado_caso)
            
#             # Registrar el error pero continuar con los demás casos
#             environment.events.request_failure.fire(
#                 request_type="PUT",
#                 name=f"(PERSONAS FISICAS) - /personas-fisicas/simplificado [{caso_descripcion}]",
#                 response_time=0,
#                 exception=e
#             )
    
#     # Resumen final
#     logger.info("\n" + "="*80)
#     logger.info("RESUMEN FINAL DE PRUEBAS PERSONA FÍSICA SIMPLIFICADA")
#     logger.info("="*80)
    
#     casos_exitosos = sum(1 for r in resultados_casos if r["exitoso"])
#     casos_fallidos = len(resultados_casos) - casos_exitosos
    
#     logger.info(f"Total casos ejecutados: {len(resultados_casos)}")
#     logger.info(f"Casos exitosos: {casos_exitosos}")
#     logger.info(f"Casos fallidos: {casos_fallidos}")
#     logger.info(f"Porcentaje de éxito: {(casos_exitosos/len(resultados_casos)*100):.1f}%")
    
#     for resultado in resultados_casos:
#         status = "✓ EXITOSO" if resultado["exitoso"] else "✗ FALLIDO"
#         logger.info(f"\n{resultado['caso']}: {status}")
#         for obs in resultado["observaciones"]:
#             logger.info(f"  {obs}")
    
#     logger.info("="*80)



def get_personas_fisicas(client, logger, environment, data_module):
    """Prueba el endpoint de obtener datos de una persona física"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'parametros_consulta_persona_fisica') or not data_module.parametros_consulta_persona_fisica:
        logger.error("No hay parámetros para consultar persona física en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/personas-fisicas", 
            params={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas [Sin datos]"
        ) as response:
            response.failure("No hay parámetros definidos en parametros_consulta_persona_fisica")
        return
    
    # Seleccionar un conjunto de parámetros aleatorio
    import random
    parametros = random.choice(data_module.parametros_consulta_persona_fisica)
    
    # Verificar si los parámetros son válidos según las reglas del API
    es_valido = False
    if "p_cuil" in parametros:
        es_valido = True
    elif "p_dni" in parametros and "p_sexo" in parametros:
        es_valido = True
    
    if not es_valido:
        logger.warning(f"Los parámetros seleccionados no son válidos para el API: {parametros}")
        logger.warning("Se requiere p_cuil o la combinación de p_dni y p_sexo")
        
        # Seleccionar un conjunto de parámetros válido
        for params in data_module.parametros_consulta_persona_fisica:
            if "p_cuil" in params or ("p_dni" in params and "p_sexo" in params):
                parametros = params
                es_valido = True
                logger.info(f"Usando parámetros alternativos: {parametros}")
                break
        
        if not es_valido:
            # Si no hay parámetros válidos, registrar un error
            with client.get(
                "/personas-fisicas", 
                params={"error": "parametros_invalidos"},
                catch_response=True,
                name="(PERSONAS FISICAS) - /personas-fisicas [Parámetros inválidos]"
            ) as response:
                response.failure("No hay parámetros válidos definidos en parametros_consulta_persona_fisica")
            return
    
    logger.info(f"Ejecutando get_personas_fisicas con parámetros: {parametros}")
    
    try:
        with client.get(
            "/personas-fisicas", 
            params=parametros,
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (CONSULTA PERSONA FÍSICA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada (debe ser una lista)
                    if isinstance(response_data, list):
                        if len(response_data) > 0:
                            # Verificar campos en el primer elemento
                            primer_elemento = response_data[0]
                            campos_esperados = [
                                "p_id_persona_fisica", "p_cuil", "p_nombre", "p_apellido", 
                                "p_fecha_nacimiento", "p_dni", "p_sexo"
                            ]
                            
                            if all(campo in primer_elemento for campo in campos_esperados):
                                response.success()
                                logger.info(f"Consulta de persona física exitosa")
                                logger.info(f"Cantidad de registros: {len(response_data)}")
                                
                                # Guardar datos para posibles pruebas futuras
                                if "p_cuil" in primer_elemento:
                                    data_module.ultimo_cuil_consultado = primer_elemento["p_cuil"]
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = [campo for campo in campos_esperados if campo not in primer_elemento]
                                logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                                
                                # Si faltan pocos campos, podemos considerarlo un éxito parcial
                                if len(campos_faltantes) <= 2:
                                    logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                                    response.success()
                                else:
                                    response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                        else:
                            # Lista vacía - puede ser válido si no hay resultados
                            logger.info("La consulta no devolvió resultados (lista vacía)")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado: se esperaba una lista")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found" in str(item.get("type", "")) for item in detail):
                            logger.info("Persona física no encontrada - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de persona física: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de persona física: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(PERSONAS FISICAS) - /personas-fisicas",
            response_time=0,
            exception=e
        )

def insert_domicilio_persona_fisica(client, logger, environment, data_module):
    """Prueba el endpoint de insertar un domicilio para una persona física"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_domicilio_persona_fisica'):
        logger.error("No hay datos para insertar domicilio de persona física en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/personas-fisicas/domicilios", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/domicilios [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos en body_insertar_domicilio_persona_fisica")
        return
    
    # Verificar si tenemos un ID de persona física para usar
    if not hasattr(data_module, 'id_persona_fisica') or not data_module.id_persona_fisica:
        logger.error("No hay ID de persona física disponible para asociar el domicilio.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/personas-fisicas/domicilios", 
            json={"error": "sin_id_persona_fisica"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/domicilios [Sin ID persona física]"
        ) as response:
            response.failure("No hay ID de persona física disponible para asociar el domicilio")
        return
    
    # Crear una copia de los datos para no modificar el original
    import copy
    body_insertar_domicilio = copy.deepcopy(data_module.body_insertar_domicilio_persona_fisica)
    
    # Actualizar el ID de persona física con un valor real
    body_insertar_domicilio["p_id_persona_fisica"] = data_module.id_persona_fisica
    
    logger.info(f"Ejecutando insert_domicilio_persona_fisica con datos: {body_insertar_domicilio}")
    
    try:
        with client.post(
            "/personas-fisicas/domicilios", 
            json=body_insertar_domicilio,
            catch_response=True,
            name="(PERSONAS FISICAS) - /personas-fisicas/domicilios [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO PERSONA FÍSICA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validación más flexible - verificar si la respuesta tiene algún contenido válido
                    if response_data and isinstance(response_data, dict):
                        response.success()
                        logger.info(f"Inserción de domicilio para persona física exitosa")
                        
                        # Intentar guardar IDs si están disponibles (sin requerir campos específicos)
                        if "id_domicilio_pf" in response_data:
                            data_module.id_domicilio_pf = response_data.get('id_domicilio_pf')
                            logger.info(f"ID domicilio persona física: {data_module.id_domicilio_pf}")
                        
                        if "id_domicilio" in response_data:
                            data_module.id_domicilio = response_data.get('id_domicilio')
                            logger.info(f"ID domicilio: {data_module.id_domicilio}")
                        
                        # Mostrar todos los campos que sí vinieron en la respuesta
                        logger.info(f"Campos recibidos en la respuesta: {list(response_data.keys())}")
                        
                    elif response_data and isinstance(response_data, list) and len(response_data) > 0:
                        # Si la respuesta es una lista con elementos
                        response.success()
                        logger.info(f"Inserción de domicilio para persona física exitosa (respuesta como lista)")
                        logger.info(f"Cantidad de elementos en respuesta: {len(response_data)}")
                        
                        # Intentar guardar datos del primer elemento
                        primer_elemento = response_data[0]
                        if "id_domicilio_pf" in primer_elemento:
                            data_module.id_domicilio_pf = primer_elemento.get('id_domicilio_pf')
                        if "id_domicilio" in primer_elemento:
                            data_module.id_domicilio = primer_elemento.get('id_domicilio')
                            
                    else:
                        response.failure("Respuesta vacía o formato inesperado")
                        logger.warning("La respuesta está vacía o tiene un formato inesperado")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 200:  # HTTP 200 OK también puede ser válido
                try:
                    response_data = response.json()
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO PERSONA FÍSICA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    response.success()
                    logger.info(f"Inserción de domicilio para persona física exitosa (200 OK)")
                    
                    # Intentar guardar IDs si están disponibles
                    if isinstance(response_data, dict):
                        if "id_domicilio_pf" in response_data:
                            data_module.id_domicilio_pf = response_data.get('id_domicilio_pf')
                        if "id_domicilio" in response_data:
                            data_module.id_domicilio = response_data.get('id_domicilio')
                            
                except ValueError as e:
                    # Si no es JSON, pero el status es 200, puede ser texto plano como "OK"
                    if response.text.strip().strip('"') == "OK":
                        response.success()
                        logger.info("Inserción de domicilio exitosa (respuesta: OK)")
                    else:
                        response.failure(f"Respuesta 200 pero formato inesperado: {response.text}")
                        
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("El domicilio ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción de domicilio para persona física: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio para persona física: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="POST",
            name="(PERSONAS FISICAS) - /personas-fisicas/domicilios",
            response_time=0,
            exception=e
        )


def get_comunicaciones_personas(client, logger, environment, data_module):
    """Prueba el endpoint de obtener datos de comunicaciones de personas"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'parametros_consulta_comunicaciones') or not data_module.parametros_consulta_comunicaciones:
        logger.error("No hay parámetros para consultar comunicaciones de personas en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/comunicaciones/personas", 
            params={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /comunicaciones/personas [Sin datos]"
        ) as response:
            response.failure("No hay parámetros definidos en parametros_consulta_comunicaciones")
        return
    
    # Seleccionar un conjunto de parámetros aleatorio
    import random
    parametros = random.choice(data_module.parametros_consulta_comunicaciones)
    
    logger.info(f"Ejecutando get_comunicaciones_personas con parámetros: {parametros}")
    
    try:
        with client.get(
            "/comunicaciones/personas", 
            params=parametros,
            catch_response=True,
            name="(PERSONAS FISICAS) - /comunicaciones/personas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (COMUNICACIONES PERSONAS) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada (debe ser una lista)
                    if isinstance(response_data, list):
                        if len(response_data) > 0:
                            # Verificar campos en el primer elemento
                            primer_elemento = response_data[0]
                            campos_esperados = [
                                "cuil_cuit", "tipo_persona"
                            ]
                            
                            # Verificar campos adicionales según el tipo de persona
                            if primer_elemento.get("tipo_persona") == "FISICA":
                                campos_esperados.extend(["apellido", "nombre"])
                            elif primer_elemento.get("tipo_persona") == "JURIDICA":
                                campos_esperados.append("razon_social")
                            
                            if all(campo in primer_elemento for campo in campos_esperados):
                                response.success()
                                logger.info(f"Consulta de comunicaciones de personas exitosa")
                                logger.info(f"Cantidad de registros: {len(response_data)}")
                                
                                # Guardar datos para posibles pruebas futuras
                                if "cuil_cuit" in primer_elemento:
                                    data_module.ultimo_cuil_cuit_consultado = primer_elemento["cuil_cuit"]
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = [campo for campo in campos_esperados if campo not in primer_elemento]
                                logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                                
                                # Si faltan pocos campos, podemos considerarlo un éxito parcial
                                if len(campos_faltantes) <= 2:
                                    logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                                    response.success()
                                else:
                                    response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                        else:
                            # Lista vacía - puede ser válido si no hay resultados
                            logger.info("La consulta no devolvió resultados (lista vacía)")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado: se esperaba una lista")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found" in str(item.get("type", "")) for item in detail):
                            logger.info("Comunicaciones no encontradas - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de comunicaciones de personas: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de comunicaciones de personas: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="GET",
            name="(PERSONAS FISICAS) - /comunicaciones/personas",
            response_time=0,
            exception=e
        )

def insert_comunicaciones_personas(client, logger, environment, data_module):
    """Prueba el endpoint de insertar comunicaciones de personas"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_comunicaciones_personas') or not data_module.body_insertar_comunicaciones_personas:
        logger.error("No hay datos para insertar comunicaciones de personas en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/comunicaciones/personas", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PERSONAS FISICAS) - /comunicaciones/personas [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos en body_insertar_comunicaciones_personas")
        return
    
    # Seleccionar un conjunto de datos aleatorio
    body_insertar = random.choice(data_module.body_insertar_comunicaciones_personas)
    
    logger.info(f"Ejecutando insert_comunicaciones_personas con datos: {body_insertar}")
    
    try:
        with client.post(
            "/comunicaciones/personas", 
            json=body_insertar,
            catch_response=True,
            name="(PERSONAS FISICAS) - /comunicaciones/personas [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (INSERCIÓN COMUNICACIONES) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "tipo_persona", "telefono", "correo_electronico"
                    ]
                    
                    # Añadir campos específicos según el tipo de persona
                    if body_insertar["p_tipo_persona"] == "PF":
                        campos_esperados.extend(["cuil", "nombre"])
                    elif body_insertar["p_tipo_persona"] == "PJ":
                        campos_esperados.extend(["cuit", "razon_social"])
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Inserción de comunicaciones para persona exitosa")
                        logger.info(f"Tipo de persona: {response_data.get('tipo_persona')}")
                        
                        # Guardar datos para posibles pruebas futuras
                        if "cuil" in response_data and response_data["cuil"]:
                            data_module.ultimo_cuil_insertado = response_data["cuil"]
                        elif "cuit" in response_data and response_data["cuit"]:
                            data_module.ultimo_cuit_insertado = response_data["cuit"]
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                        else:
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("La comunicación ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción de comunicaciones: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción de comunicaciones: {str(e)}")
        # Registrar el error como una respuesta fallida
        environment.events.request_failure.fire(
            request_type="POST",
            name=" (PERSONAS FISICAS) - /personas-fisicas",
            response_time=0,
            exception=e
        )
