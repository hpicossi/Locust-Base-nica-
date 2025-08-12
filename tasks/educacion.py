import random
from typing import Dict, Any

def get_parques_educativos(client, logger, environment, data_module):
    """Prueba el endpoint de obtener parques educativos de Córdoba"""
    
    logger.info("Ejecutando get_parques_educativos")
    
    try:
        with client.get(
            "/educacion/parques-educativos", 
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/parques-educativos [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info(f"Respuesta recibida: {len(response_data)} parques educativos encontrados")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info("=== RESUMEN DE LA RESPUESTA (PARQUES EDUCATIVOS) ===")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Contar cuántos parques educativos se encontraron
                        cantidad_parques = len(response_data)
                        logger.info(f"Se encontraron {cantidad_parques} parques educativos")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if cantidad_parques > 0:
                            # Campos esperados basados en el schema EducationalParksGetResponseSchema
                            # Nota: Como no se proporciona el schema completo, usamos campos comunes
                            campos_esperados = [
                                "id", "nombre"  # Campos básicos esperados
                            ]
                            
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "denominacion", "parque_id"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de parques educativos exitosa")
                                
                                # Mostrar información de algunos parques (hasta 5)
                                for idx, parque in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in parque:
                                        logger.info(f"Parque {idx+1}: {parque.get('nombre')}")
                                    elif "denominacion" in parque:
                                        logger.info(f"Parque {idx+1}: {parque.get('denominacion')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in parque.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Parque {idx+1}: {key}={value}")
                                                break
                                
                                # Si hay más de 5 parques, indicar cuántos más hay
                                if cantidad_parques > 5:
                                    logger.info(f"... y {cantidad_parques - 5} parques más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.parques_educativos = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron parques educativos
                            logger.warning("No se encontraron parques educativos")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de parques educativos")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de parques educativos no encontrado")
                response.failure("Endpoint no encontrado")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de parques educativos: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de parques educativos: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/educacion/parques-educativos",
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/parques-educativos [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
from typing import Dict, Any

def get_escuelas_municipales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener escuelas primarias municipales de Córdoba"""
    
    logger.info("Ejecutando get_escuelas_municipales")
    
    try:
        with client.get(
            "/educacion/escuelas-municipales", 
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/escuelas-municipales [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info(f"Respuesta recibida: {len(response_data)} escuelas municipales encontradas")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info("=== RESUMEN DE LA RESPUESTA (ESCUELAS MUNICIPALES) ===")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Contar cuántas escuelas municipales se encontraron
                        cantidad_escuelas = len(response_data)
                        logger.info(f"Se encontraron {cantidad_escuelas} escuelas municipales")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if cantidad_escuelas > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de escuelas
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "denominacion", "escuela_id", "establecimiento", "cue"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de escuelas municipales exitosa")
                                
                                # Mostrar información de algunas escuelas (hasta 5)
                                for idx, escuela in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in escuela:
                                        logger.info(f"Escuela {idx+1}: {escuela.get('nombre')}")
                                    elif "denominacion" in escuela:
                                        logger.info(f"Escuela {idx+1}: {escuela.get('denominacion')}")
                                    elif "establecimiento" in escuela:
                                        logger.info(f"Escuela {idx+1}: {escuela.get('establecimiento')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in escuela.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Escuela {idx+1}: {key}={value}")
                                                break
                                
                                # Si hay más de 5 escuelas, indicar cuántas más hay
                                if cantidad_escuelas > 5:
                                    logger.info(f"... y {cantidad_escuelas - 5} escuelas más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.escuelas_municipales = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de escuelas")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron escuelas municipales
                            logger.warning("No se encontraron escuelas municipales")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de escuelas municipales")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de escuelas municipales no encontrado")
                response.failure("Endpoint no encontrado")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de escuelas municipales: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de escuelas municipales: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/educacion/escuelas-municipales",
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/escuelas-municipales [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_jardines_municipales(client, logger, environment, data_module):
    """Prueba el endpoint de obtener jardines municipales de Córdoba"""
    
    logger.info("Ejecutando get_jardines_municipales")
    
    try:
        with client.get(
            "/educacion/jardines-municipales", 
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/jardines-municipales [GET]"
        ) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info(f"Respuesta recibida: {len(response_data)} jardines municipales encontrados")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info("=== RESUMEN DE LA RESPUESTA (JARDINES MUNICIPALES) ===")
                    
                    if isinstance(response_data, list):
                        cantidad_jardines = len(response_data)
                        logger.info(f"Se encontraron {cantidad_jardines} jardines municipales")
                        
                        if cantidad_jardines > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "denominacion", "jardin_id", "establecimiento", "cue"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de jardines municipales exitosa")
                                
                                for idx, jardin in enumerate(response_data[:5]):
                                    if "nombre" in jardin:
                                        logger.info(f"Jardín {idx+1}: {jardin.get('nombre')}")
                                    elif "denominacion" in jardin:
                                        logger.info(f"Jardín {idx+1}: {jardin.get('denominacion')}")
                                    elif "establecimiento" in jardin:
                                        logger.info(f"Jardín {idx+1}: {jardin.get('establecimiento')}")
                                
                                if cantidad_jardines > 5:
                                    logger.info(f"... y {cantidad_jardines - 5} jardines más")
                                
                                data_module.jardines_municipales = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de jardines")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            logger.warning("No se encontraron jardines municipales")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                logger.warning("Acceso denegado al endpoint de jardines municipales")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                logger.warning("Endpoint de jardines municipales no encontrado")
                response.failure("Endpoint no encontrado")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de jardines municipales: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de jardines municipales: {str(e)}")
        with client.get(
            "/educacion/jardines-municipales",
            catch_response=True,
            name="(EDUCACIÓN) - /educacion/jardines-municipales [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")
