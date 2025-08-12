import random
from typing import Dict, Any

def get_barrios_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener barrios por localidad"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    # Seleccionar un ID de localidad aleatorio
    id_localidad = random.choice(ids_localidades)
    
    logger.info(f"Ejecutando get_barrios_por_localidad con ID de localidad: {id_localidad}")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/barrios", 
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [GET]"
        ) as response:
            # Guardar un resumen de la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info(f"Cantidad de barrios encontrados: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_barrios = len(response_data)
                        logger.info(f"Se encontraron {cantidad_barrios} barrios para la localidad con ID {id_localidad}")
                        
                        if cantidad_barrios > 0:
                            campos_esperados = ["id_barrio", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de barrios por localidad exitosa")
                                
                                # Mostrar información de algunos barrios (hasta 5)
                                for idx, barrio in enumerate(response_data[:5]):
                                    logger.info(f"Barrio {idx+1}: ID={barrio.get('id_barrio')}, Nombre={barrio.get('nombre')}")
                                
                                if cantidad_barrios > 5:
                                    logger.info(f"... y {cantidad_barrios - 5} barrios más")
                                
                                data_module.ids_barrios = [barrio.get('id_barrio') for barrio in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron barrios para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de barrios por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/barrios",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_calles_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener calles por localidad"""
    
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        ids_localidades = [1]
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    id_localidad = random.choice(ids_localidades)
    usar_busqueda = random.choice([True, False])
    
    if usar_busqueda and hasattr(data_module, 'busquedas_calles') and data_module.busquedas_calles:
        texto_busqueda = random.choice(data_module.busquedas_calles)
        params = {"calle": texto_busqueda} if texto_busqueda else {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} y búsqueda: '{texto_busqueda}'")
    else:
        params = {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} (sin filtro de búsqueda)")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/calles", 
            params=params,
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [GET]"
        ) as response:
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    response_data = response.json()
                    logger.info(f"Cantidad de calles encontradas: {len(response_data)}")
                    
                    if isinstance(response_data, list):
                        cantidad_calles = len(response_data)
                        logger.info(f"Se encontraron {cantidad_calles} calles para la localidad con ID {id_localidad}")
                        
                        if cantidad_calles > 0:
                            campos_esperados = ["id_calle", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de calles por localidad exitosa")
                                
                                for idx, calle in enumerate(response_data[:5]):
                                    logger.info(f"Calle {idx+1}: ID={calle.get('id_calle')}, Nombre={calle.get('nombre')}")
                                
                                if cantidad_calles > 5:
                                    logger.info(f"... y {cantidad_calles - 5} calles más")
                                
                                data_module.ids_calles = [calle.get('id_calle') for calle in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron calles para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de calles por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/calles",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
from typing import Dict, Any

def get_barrios_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener barrios por localidad"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    # Seleccionar un ID de localidad aleatorio
    id_localidad = random.choice(ids_localidades)
    
    logger.info(f"Ejecutando get_barrios_por_localidad con ID de localidad: {id_localidad}")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/barrios", 
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [GET]"
        ) as response:
            # Guardar un resumen de la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info(f"Cantidad de barrios encontrados: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_barrios = len(response_data)
                        logger.info(f"Se encontraron {cantidad_barrios} barrios para la localidad con ID {id_localidad}")
                        
                        if cantidad_barrios > 0:
                            campos_esperados = ["id_barrio", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de barrios por localidad exitosa")
                                
                                # Mostrar información de algunos barrios (hasta 5)
                                for idx, barrio in enumerate(response_data[:5]):
                                    logger.info(f"Barrio {idx+1}: ID={barrio.get('id_barrio')}, Nombre={barrio.get('nombre')}")
                                
                                if cantidad_barrios > 5:
                                    logger.info(f"... y {cantidad_barrios - 5} barrios más")
                                
                                data_module.ids_barrios = [barrio.get('id_barrio') for barrio in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron barrios para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de barrios por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/barrios",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_calles_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener calles por localidad"""
    
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        ids_localidades = [1]
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    id_localidad = random.choice(ids_localidades)
    usar_busqueda = random.choice([True, False])
    
    if usar_busqueda and hasattr(data_module, 'busquedas_calles') and data_module.busquedas_calles:
        texto_busqueda = random.choice(data_module.busquedas_calles)
        params = {"calle": texto_busqueda} if texto_busqueda else {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} y búsqueda: '{texto_busqueda}'")
    else:
        params = {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} (sin filtro de búsqueda)")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/calles", 
            params=params,
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [GET]"
        ) as response:
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    response_data = response.json()
                    logger.info(f"Cantidad de calles encontradas: {len(response_data)}")
                    
                    if isinstance(response_data, list):
                        cantidad_calles = len(response_data)
                        logger.info(f"Se encontraron {cantidad_calles} calles para la localidad con ID {id_localidad}")
                        
                        if cantidad_calles > 0:
                            campos_esperados = ["id_calle", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de calles por localidad exitosa")
                                
                                for idx, calle in enumerate(response_data[:5]):
                                    logger.info(f"Calle {idx+1}: ID={calle.get('id_calle')}, Nombre={calle.get('nombre')}")
                                
                                if cantidad_calles > 5:
                                    logger.info(f"... y {cantidad_calles - 5} calles más")
                                
                                data_module.ids_calles = [calle.get('id_calle') for calle in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron calles para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de calles por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/calles",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_paises(client, logger, environment, data_module):
    """Prueba el endpoint de obtener todos los países"""
    
    logger.info("Ejecutando get_paises - obteniendo lista completa de países")
    
    try:
        with client.get(
            "/paises", 
            catch_response=True,
            name="(DOMICILIOS) - /paises [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PAÍSES) ===")
                    logger.info(f"Cantidad de países obtenidos: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_paises = len(response_data)
                        logger.info(f"Se encontraron {cantidad_paises} países en total")
                        
                        if cantidad_paises > 0:
                            # Verificar campos esperados
                            campos_esperados = getattr(data_module, 'campos_esperados_paises', ["id_pais", "nombre"])
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de países exitosa")
                                
                                # Mostrar información de algunos países (hasta 10)
                                for idx, pais in enumerate(response_data[:10]):
                                    logger.info(f"País {idx+1}: ID={pais.get('id_pais')}, Nombre={pais.get('nombre')}")
                                
                                if cantidad_paises > 10:
                                    logger.info(f"... y {cantidad_paises - 10} países más")
                                
                                # Buscar países de interés si están definidos
                                if hasattr(data_module, 'paises_interes'):
                                    paises_encontrados = []
                                    for pais in response_data:
                                        if pais.get('nombre') in data_module.paises_interes:
                                            paises_encontrados.append(pais)
                                    
                                    if paises_encontrados:
                                        logger.info("=== PAÍSES DE INTERÉS ENCONTRADOS ===")
                                        for pais in paises_encontrados:
                                            logger.info(f"- {pais.get('nombre')} (ID: {pais.get('id_pais')})")
                                
                                # Guardar datos para posibles pruebas futuras
                                data_module.paises_disponibles = response_data
                                data_module.ids_paises = [pais.get('id_pais') for pais in response_data]
                                data_module.nombres_paises = [pais.get('nombre') for pais in response_data]
                                
                                # Validar algunos países esperados si están definidos
                                if hasattr(data_module, 'paises_esperados'):
                                    for pais_esperado in data_module.paises_esperados:
                                        encontrado = any(
                                            p.get('id_pais') == pais_esperado.get('id_pais') and 
                                            p.get('nombre') == pais_esperado.get('nombre')
                                            for p in response_data
                                        )
                                        if encontrado:
                                            logger.info(f"✓ País esperado encontrado: {pais_esperado.get('nombre')}")
                                        else:
                                            logger.warning(f"✗ País esperado NO encontrado: {pais_esperado.get('nombre')}")
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = []
                                for item in response_data[:5]:  # Revisar solo los primeros 5 elementos
                                    faltantes = [campo for campo in campos_esperados if campo not in item]
                                    if faltantes:
                                        campos_faltantes.extend(faltantes)
                                
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en algunos elementos: {set(campos_faltantes)}")
                                    response.failure("Algunos elementos no tienen los campos esperados")
                                else:
                                    response.success()
                                    logger.info("Consulta de países exitosa (validación parcial)")
                        else:
                            logger.warning("La lista de países está vacía")
                            response.failure("No se encontraron países en la base de datos")
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en países: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en países: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener países")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener países")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener países")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de países: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de países: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            "/paises",
            catch_response=True,
            name="(DOMICILIOS) - /paises [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
from typing import Dict, Any

def get_barrios_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener barrios por localidad"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        ids_localidades = [1]
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    # Seleccionar un ID de localidad aleatorio
    id_localidad = random.choice(ids_localidades)
    
    logger.info(f"Ejecutando get_barrios_por_localidad con ID de localidad: {id_localidad}")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/barrios", 
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [GET]"
        ) as response:
            # Guardar un resumen de la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info(f"Cantidad de barrios encontrados: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_barrios = len(response_data)
                        logger.info(f"Se encontraron {cantidad_barrios} barrios para la localidad con ID {id_localidad}")
                        
                        if cantidad_barrios > 0:
                            campos_esperados = ["id_barrio", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de barrios por localidad exitosa")
                                
                                # Mostrar información de algunos barrios (hasta 5)
                                for idx, barrio in enumerate(response_data[:5]):
                                    logger.info(f"Barrio {idx+1}: ID={barrio.get('id_barrio')}, Nombre={barrio.get('nombre')}")
                                
                                if cantidad_barrios > 5:
                                    logger.info(f"... y {cantidad_barrios - 5} barrios más")
                                
                                data_module.ids_barrios = [barrio.get('id_barrio') for barrio in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron barrios para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de barrios por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/barrios",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/barrios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_calles_por_localidad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener calles por localidad"""
    
    if not hasattr(data_module, 'ids_localidades') or not data_module.ids_localidades:
        ids_localidades = [1]
        logger.warning("No se encontraron IDs de localidades en el módulo de datos. Usando valor predeterminado: 1 (Córdoba Capital)")
    else:
        ids_localidades = data_module.ids_localidades
    
    id_localidad = random.choice(ids_localidades)
    usar_busqueda = random.choice([True, False])
    
    if usar_busqueda and hasattr(data_module, 'busquedas_calles') and data_module.busquedas_calles:
        texto_busqueda = random.choice(data_module.busquedas_calles)
        params = {"calle": texto_busqueda} if texto_busqueda else {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} y búsqueda: '{texto_busqueda}'")
    else:
        params = {}
        logger.info(f"Ejecutando get_calles_por_localidad con ID de localidad: {id_localidad} (sin filtro de búsqueda)")
    
    try:
        with client.get(
            f"/localidades/{id_localidad}/calles", 
            params=params,
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [GET]"
        ) as response:
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    response_data = response.json()
                    logger.info(f"Cantidad de calles encontradas: {len(response_data)}")
                    
                    if isinstance(response_data, list):
                        cantidad_calles = len(response_data)
                        logger.info(f"Se encontraron {cantidad_calles} calles para la localidad con ID {id_localidad}")
                        
                        if cantidad_calles > 0:
                            campos_esperados = ["id_calle", "nombre"]
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de calles por localidad exitosa")
                                
                                for idx, calle in enumerate(response_data[:5]):
                                    logger.info(f"Calle {idx+1}: ID={calle.get('id_calle')}, Nombre={calle.get('nombre')}")
                                
                                if cantidad_calles > 5:
                                    logger.info(f"... y {cantidad_calles - 5} calles más")
                                
                                data_module.ids_calles = [calle.get('id_calle') for calle in response_data]
                            else:
                                response.failure("Algunos elementos no tienen los campos esperados")
                        else:
                            logger.warning(f"No se encontraron calles para la localidad con ID {id_localidad}")
                            response.success()
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
            elif response.status_code == 404:
                logger.warning(f"No se encontró la localidad con ID {id_localidad}")
                response.success()
            else:
                response.failure(f"Error: {response.status_code}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de calles por localidad: {str(e)}")
        with client.get(
            f"/localidades/{id_localidad}/calles",
            catch_response=True,
            name=f"(DOMICILIOS) - /localidades/{id_localidad}/calles [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_paises(client, logger, environment, data_module):
    """Prueba el endpoint de obtener todos los países"""
    
    logger.info("Ejecutando get_paises - obteniendo lista completa de países")
    
    try:
        with client.get(
            "/paises", 
            catch_response=True,
            name="(DOMICILIOS) - /paises [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PAÍSES) ===")
                    logger.info(f"Cantidad de países obtenidos: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_paises = len(response_data)
                        logger.info(f"Se encontraron {cantidad_paises} países en total")
                        
                        if cantidad_paises > 0:
                            # Verificar campos esperados
                            campos_esperados = getattr(data_module, 'campos_esperados_paises', ["id_pais", "nombre"])
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de países exitosa")
                                
                                # Mostrar información de algunos países (hasta 10)
                                for idx, pais in enumerate(response_data[:10]):
                                    logger.info(f"País {idx+1}: ID={pais.get('id_pais')}, Nombre={pais.get('nombre')}")
                                
                                if cantidad_paises > 10:
                                    logger.info(f"... y {cantidad_paises - 10} países más")
                                
                                # Buscar países de interés si están definidos
                                if hasattr(data_module, 'paises_interes'):
                                    paises_encontrados = []
                                    for pais in response_data:
                                        if pais.get('nombre') in data_module.paises_interes:
                                            paises_encontrados.append(pais)
                                    
                                    if paises_encontrados:
                                        logger.info("=== PAÍSES DE INTERÉS ENCONTRADOS ===")
                                        for pais in paises_encontrados:
                                            logger.info(f"- {pais.get('nombre')} (ID: {pais.get('id_pais')})")
                                
                                # Guardar datos para posibles pruebas futuras
                                data_module.paises_disponibles = response_data
                                data_module.ids_paises = [pais.get('id_pais') for pais in response_data]
                                data_module.nombres_paises = [pais.get('nombre') for pais in response_data]
                                
                                # Actualizar mapeo de países conocidos
                                if hasattr(data_module, 'paises_conocidos'):
                                    for pais in response_data:
                                        nombre_pais = pais.get('nombre')
                                        if nombre_pais in data_module.paises_conocidos:
                                            data_module.paises_conocidos[nombre_pais] = pais.get('id_pais')
                                            logger.info(f"País conocido actualizado: {nombre_pais} -> ID {pais.get('id_pais')}")
                                
                                # Validar algunos países esperados si están definidos
                                if hasattr(data_module, 'paises_esperados'):
                                    for pais_esperado in data_module.paises_esperados:
                                        encontrado = any(
                                            p.get('id_pais') == pais_esperado.get('id_pais') and 
                                            p.get('nombre') == pais_esperado.get('nombre')
                                            for p in response_data
                                        )
                                        if encontrado:
                                            logger.info(f"✓ País esperado encontrado: {pais_esperado.get('nombre')}")
                                        else:
                                            logger.warning(f"✗ País esperado NO encontrado: {pais_esperado.get('nombre')}")
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = []
                                for item in response_data[:5]:  # Revisar solo los primeros 5 elementos
                                    faltantes = [campo for campo in campos_esperados if campo not in item]
                                    if faltantes:
                                        campos_faltantes.extend(faltantes)
                                
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en algunos elementos: {set(campos_faltantes)}")
                                    response.failure("Algunos elementos no tienen los campos esperados")
                                else:
                                    response.success()
                                    logger.info("Consulta de países exitosa (validación parcial)")
                        else:
                            logger.warning("La lista de países está vacía")
                            response.failure("No se encontraron países en la base de datos")
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en países: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en países: {response.text[:200]}")
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener países")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener países")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener países")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de países: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de países: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            "/paises",
            catch_response=True,
            name="(DOMICILIOS) - /paises [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_provincias_por_pais(client, logger, environment, data_module):
    """Prueba el endpoint de obtener provincias por país"""
    
    # Intentar usar IDs de países obtenidos dinámicamente de la consulta anterior
    ids_paises_disponibles = []
    
    # Primero intentar usar los IDs obtenidos dinámicamente
    if hasattr(data_module, 'ids_paises') and data_module.ids_paises:
        ids_paises_disponibles = data_module.ids_paises[:5]  # Usar solo los primeros 5
        logger.info(f"Usando IDs de países obtenidos dinámicamente: {ids_paises_disponibles}")
    
    # Si no hay IDs dinámicos, usar los predefinidos
    if not ids_paises_disponibles:
        if hasattr(data_module, 'ids_paises') and data_module.ids_paises:
            ids_paises_disponibles = data_module.ids_paises
        else:
            ids_paises_disponibles = [1, 2, 3]  # IDs por defecto
            logger.warning("No se encontraron IDs de países. Usando valores predeterminados: [1, 2, 3]")
    
    # Seleccionar un ID de país aleatorio
    id_pais = random.choice(ids_paises_disponibles)
    
    logger.info(f"Ejecutando get_provincias_por_pais con ID de país: {id_pais}")
    
    try:
        with client.get(
            f"/paises/{id_pais}/provincias", 
            catch_response=True,
            name=f"(DOMICILIOS) - /paises/{id_pais}/provincias [GET]"
        ) as response:
            # Guardar la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PROVINCIAS) ===")
                    logger.info(f"Cantidad de provincias obtenidas: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_provincias = len(response_data)
                        logger.info(f"Se encontraron {cantidad_provincias} provincias para el país con ID {id_pais}")
                        
                        if cantidad_provincias > 0:
                            # Verificar campos esperados
                            campos_esperados = getattr(data_module, 'campos_esperados_provincias', ["id_provincia", "nombre"])
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de provincias exitosa")
                                
                                # Mostrar información de algunas provincias (hasta 10)
                                for idx, provincia in enumerate(response_data[:10]):
                                    logger.info(f"Provincia {idx+1}: ID={provincia.get('id_provincia')}, Nombre={provincia.get('nombre')}")
                                
                                if cantidad_provincias > 10:
                                    logger.info(f"... y {cantidad_provincias - 10} provincias más")
                                
                                # Buscar provincias de interés si están definidas
                                if hasattr(data_module, 'provincias_interes'):
                                    provincias_encontradas = []
                                    for provincia in response_data:
                                        if provincia.get('nombre') in data_module.provincias_interes:
                                            provincias_encontradas.append(provincia)
                                    
                                    if provincias_encontradas:
                                        logger.info("=== PROVINCIAS DE INTERÉS ENCONTRADAS ===")
                                        for provincia in provincias_encontradas:
                                            logger.info(f"- {provincia.get('nombre')} (ID: {provincia.get('id_provincia')})")
                                
                                # Guardar datos para posibles pruebas futuras
                                if not hasattr(data_module, 'provincias_disponibles'):
                                    data_module.provincias_disponibles = {}
                                data_module.provincias_disponibles[id_pais] = response_data
                                
                                if not hasattr(data_module, 'ids_provincias'):
                                    data_module.ids_provincias = []
                                data_module.ids_provincias.extend([provincia.get('id_provincia') for provincia in response_data])
                                
                                if not hasattr(data_module, 'nombres_provincias'):
                                    data_module.nombres_provincias = []
                                data_module.nombres_provincias.extend([provincia.get('nombre') for provincia in response_data])
                                
                                # Validar algunas provincias esperadas si están definidas
                                if hasattr(data_module, 'provincias_esperadas'):
                                    for provincia_esperada in data_module.provincias_esperadas:
                                        encontrado = any(
                                            p.get('id_provincia') == provincia_esperada.get('id_provincia') and 
                                            p.get('nombre') == provincia_esperada.get('nombre')
                                            for p in response_data
                                        )
                                        if encontrado:
                                            logger.info(f"✓ Provincia esperada encontrada: {provincia_esperada.get('nombre')}")
                                        else:
                                            logger.debug(f"✗ Provincia esperada NO encontrada en este país: {provincia_esperada.get('nombre')}")
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = []
                                for item in response_data[:5]:  # Revisar solo los primeros 5 elementos
                                    faltantes = [campo for campo in campos_esperados if campo not in item]
                                    if faltantes:
                                        campos_faltantes.extend(faltantes)
                                
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en algunos elementos: {set(campos_faltantes)}")
                                    response.failure("Algunos elementos no tienen los campos esperados")
                                else:
                                    response.success()
                                    logger.info("Consulta de provincias exitosa (validación parcial)")
                        else:
                            logger.info(f"No se encontraron provincias para el país con ID {id_pais}")
                            response.success()  # Esto es válido, algunos países pueden no tener provincias
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en provincias: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en provincias: {response.text[:200]}")
            elif response.status_code == 400:
                # Error de validación del ID de país
                logger.warning(f"ID de país inválido: {id_pais}")
                response.failure("ID de país inválido")
            elif response.status_code == 404:
                # País no encontrado
                logger.warning(f"No se encontró el país con ID {id_pais}")
                response.success()  # Esto puede ser un comportamiento esperado
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener provincias")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener provincias")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener provincias")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de provincias: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de provincias: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            f"/paises/{id_pais}/provincias",
            catch_response=True,
            name=f"(DOMICILIOS) - /paises/{id_pais}/provincias [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_departamentos_por_provincia(client, logger, environment, data_module):
    """Prueba el endpoint de obtener departamentos por provincia"""
    
    # Intentar usar IDs de provincias obtenidos dinámicamente de la consulta anterior
    ids_provincias_disponibles = []
    
    # Primero intentar usar los IDs obtenidos dinámicamente
    if hasattr(data_module, 'ids_provincias') and data_module.ids_provincias:
        ids_provincias_disponibles = data_module.ids_provincias[:5]  # Usar solo los primeros 5
        logger.info(f"Usando IDs de provincias obtenidos dinámicamente: {ids_provincias_disponibles}")
    
    # Si no hay IDs dinámicos, usar los predefinidos
    if not ids_provincias_disponibles:
        if hasattr(data_module, 'ids_provincias') and data_module.ids_provincias:
            ids_provincias_disponibles = data_module.ids_provincias
        else:
            ids_provincias_disponibles = [22, 1, 2]  # IDs por defecto (Córdoba, Buenos Aires, etc.)
            logger.warning("No se encontraron IDs de provincias. Usando valores predeterminados: [22, 1, 2]")
    
    # Seleccionar un ID de provincia aleatorio
    id_provincia = random.choice(ids_provincias_disponibles)
    
    logger.info(f"Ejecutando get_departamentos_por_provincia con ID de provincia: {id_provincia}")
    
    try:
        with client.get(
            f"/provincias/{id_provincia}/departamentos", 
            catch_response=True,
            name=f"(DOMICILIOS) - /provincias/{id_provincia}/departamentos [GET]"
        ) as response:
            # Guardar la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DEPARTAMENTOS) ===")
                    logger.info(f"Cantidad de departamentos obtenidos: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_departamentos = len(response_data)
                        logger.info(f"Se encontraron {cantidad_departamentos} departamentos para la provincia con ID {id_provincia}")
                        
                        if cantidad_departamentos > 0:
                            # Verificar campos esperados
                            campos_esperados = getattr(data_module, 'campos_esperados_departamentos', ["id_departamento", "nombre"])
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de departamentos exitosa")
                                
                                # Mostrar información de algunos departamentos (hasta 10)
                                for idx, departamento in enumerate(response_data[:10]):
                                    logger.info(f"Departamento {idx+1}: ID={departamento.get('id_departamento')}, Nombre={departamento.get('nombre')}")
                                
                                if cantidad_departamentos > 10:
                                    logger.info(f"... y {cantidad_departamentos - 10} departamentos más")
                                
                                # Buscar departamentos de interés si están definidos
                                if hasattr(data_module, 'departamentos_interes'):
                                    departamentos_encontrados = []
                                    for departamento in response_data:
                                        if departamento.get('nombre') in data_module.departamentos_interes:
                                            departamentos_encontrados.append(departamento)
                                    
                                    if departamentos_encontrados:
                                        logger.info("=== DEPARTAMENTOS DE INTERÉS ENCONTRADOS ===")
                                        for departamento in departamentos_encontrados:
                                            logger.info(f"- {departamento.get('nombre')} (ID: {departamento.get('id_departamento')})")
                                
                                # Guardar datos para posibles pruebas futuras
                                if not hasattr(data_module, 'departamentos_disponibles'):
                                    data_module.departamentos_disponibles = {}
                                data_module.departamentos_disponibles[id_provincia] = response_data
                                
                                if not hasattr(data_module, 'ids_departamentos'):
                                    data_module.ids_departamentos = []
                                data_module.ids_departamentos.extend([depto.get('id_departamento') for depto in response_data])
                                
                                if not hasattr(data_module, 'nombres_departamentos'):
                                    data_module.nombres_departamentos = []
                                data_module.nombres_departamentos.extend([depto.get('nombre') for depto in response_data])
                                
                                # Validar algunos departamentos esperados si están definidos
                                if hasattr(data_module, 'departamentos_esperados'):
                                    for departamento_esperado in data_module.departamentos_esperados:
                                        encontrado = any(
                                            d.get('id_departamento') == departamento_esperado.get('id_departamento') and 
                                            d.get('nombre') == departamento_esperado.get('nombre')
                                            for d in response_data
                                        )
                                        if encontrado:
                                            logger.info(f"✓ Departamento esperado encontrado: {departamento_esperado.get('nombre')}")
                                        else:
                                            logger.debug(f"✗ Departamento esperado NO encontrado en esta provincia: {departamento_esperado.get('nombre')}")
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = []
                                for item in response_data[:5]:  # Revisar solo los primeros 5 elementos
                                    faltantes = [campo for campo in campos_esperados if campo not in item]
                                    if faltantes:
                                        campos_faltantes.extend(faltantes)
                                
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en algunos elementos: {set(campos_faltantes)}")
                                    response.failure("Algunos elementos no tienen los campos esperados")
                                else:
                                    response.success()
                                    logger.info("Consulta de departamentos exitosa (validación parcial)")
                        else:
                            logger.info(f"No se encontraron departamentos para la provincia con ID {id_provincia}")
                            response.success()  # Esto es válido, algunas provincias pueden no tener departamentos
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en departamentos: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en departamentos: {response.text[:200]}")
            elif response.status_code == 400:
                # Error de validación del ID de provincia
                logger.warning(f"ID de provincia inválido: {id_provincia}")
                response.failure("ID de provincia inválido")
            elif response.status_code == 404:
                # Provincia no encontrada
                logger.warning(f"No se encontró la provincia con ID {id_provincia}")
                response.success()  # Esto puede ser un comportamiento esperado
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener departamentos")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener departamentos")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener departamentos")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de departamentos: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de departamentos: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            f"/provincias/{id_provincia}/departamentos",
            catch_response=True,
            name=f"(DOMICILIOS) - /provincias/{id_provincia}/departamentos [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_localidades_por_departamento(client, logger, environment, data_module):
    """Prueba el endpoint de obtener localidades por departamento"""
    
    # Intentar usar IDs de departamentos obtenidos dinámicamente de la consulta anterior
    ids_departamentos_disponibles = []
    
    # Primero intentar usar los IDs obtenidos dinámicamente
    if hasattr(data_module, 'ids_departamentos') and data_module.ids_departamentos:
        ids_departamentos_disponibles = data_module.ids_departamentos[:5]  # Usar solo los primeros 5
        logger.info(f"Usando IDs de departamentos obtenidos dinámicamente: {ids_departamentos_disponibles}")
    
    # Si no hay IDs dinámicos, usar los predefinidos
    if not ids_departamentos_disponibles:
        if hasattr(data_module, 'ids_departamentos') and data_module.ids_departamentos:
            ids_departamentos_disponibles = data_module.ids_departamentos
        else:
            ids_departamentos_disponibles = [3, 1, 26]  # IDs por defecto (Capital Córdoba, Capital BA, Unión)
            logger.warning("No se encontraron IDs de departamentos. Usando valores predeterminados: [3, 1, 26]")
    
    # Seleccionar un ID de departamento aleatorio
    id_departamento = random.choice(ids_departamentos_disponibles)
    
    logger.info(f"Ejecutando get_localidades_por_departamento con ID de departamento: {id_departamento}")
    
    try:
        with client.get(
            f"/departamentos/{id_departamento}/localidades", 
            catch_response=True,
            name=f"(DOMICILIOS) - /departamentos/{id_departamento}/localidades [GET]"
        ) as response:
            # Guardar la respuesta en el log
            logger.info(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (LOCALIDADES) ===")
                    logger.info(f"Cantidad de localidades obtenidas: {len(response_data)}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        cantidad_localidades = len(response_data)
                        logger.info(f"Se encontraron {cantidad_localidades} localidades para el departamento con ID {id_departamento}")
                        
                        if cantidad_localidades > 0:
                            # Verificar campos esperados
                            campos_esperados = getattr(data_module, 'campos_esperados_localidades', ["id_localidad", "nombre"])
                            todos_validos = all(
                                all(campo in item for campo in campos_esperados)
                                for item in response_data
                            )
                            
                            if todos_validos:
                                response.success()
                                logger.info("Consulta de localidades exitosa")
                                
                                # Mostrar información de algunas localidades (hasta 10)
                                for idx, localidad in enumerate(response_data[:10]):
                                    logger.info(f"Localidad {idx+1}: ID={localidad.get('id_localidad')}, Nombre={localidad.get('nombre')}")
                                
                                if cantidad_localidades > 10:
                                    logger.info(f"... y {cantidad_localidades - 10} localidades más")
                                
                                # Buscar localidades de interés si están definidas
                                if hasattr(data_module, 'localidades_interes'):
                                    localidades_encontradas = []
                                    for localidad in response_data:
                                        if localidad.get('nombre') in data_module.localidades_interes:
                                            localidades_encontradas.append(localidad)
                                    
                                    if localidades_encontradas:
                                        logger.info("=== LOCALIDADES DE INTERÉS ENCONTRADAS ===")
                                        for localidad in localidades_encontradas:
                                            logger.info(f"- {localidad.get('nombre')} (ID: {localidad.get('id_localidad')})")
                                
                                # Guardar datos para posibles pruebas futuras
                                if not hasattr(data_module, 'localidades_disponibles'):
                                    data_module.localidades_disponibles = {}
                                data_module.localidades_disponibles[id_departamento] = response_data
                                
                                if not hasattr(data_module, 'ids_localidades'):
                                    data_module.ids_localidades = []
                                data_module.ids_localidades.extend([loc.get('id_localidad') for loc in response_data])
                                
                                if not hasattr(data_module, 'nombres_localidades'):
                                    data_module.nombres_localidades = []
                                data_module.nombres_localidades.extend([loc.get('nombre') for loc in response_data])
                                
                                # Validar algunas localidades esperadas si están definidas
                                if hasattr(data_module, 'localidades_esperadas'):
                                    for localidad_esperada in data_module.localidades_esperadas:
                                        encontrado = any(
                                            l.get('id_localidad') == localidad_esperada.get('id_localidad') and 
                                            l.get('nombre') == localidad_esperada.get('nombre')
                                            for l in response_data
                                        )
                                        if encontrado:
                                            logger.info(f"✓ Localidad esperada encontrada: {localidad_esperada.get('nombre')}")
                                        else:
                                            logger.debug(f"✗ Localidad esperada NO encontrada en este departamento: {localidad_esperada.get('nombre')}")
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = []
                                for item in response_data[:5]:  # Revisar solo los primeros 5 elementos
                                    faltantes = [campo for campo in campos_esperados if campo not in item]
                                    if faltantes:
                                        campos_faltantes.extend(faltantes)
                                
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en algunos elementos: {set(campos_faltantes)}")
                                    response.failure("Algunos elementos no tienen los campos esperados")
                                else:
                                    response.success()
                                    logger.info("Consulta de localidades exitosa (validación parcial)")
                        else:
                            logger.info(f"No se encontraron localidades para el departamento con ID {id_departamento}")
                            response.success()  # Esto es válido, algunos departamentos pueden no tener localidades
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en localidades: {response.text[:200]}")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en localidades: {response.text[:200]}")
            elif response.status_code == 400:
                # Error de validación del ID de departamento
                logger.warning(f"ID de departamento inválido: {id_departamento}")
                response.failure("ID de departamento inválido")
            elif response.status_code == 404:
                # Departamento no encontrado
                logger.warning(f"No se encontró el departamento con ID {id_departamento}")
                response.success()  # Esto puede ser un comportamiento esperado
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al obtener localidades")
                response.failure("Error de autenticación")
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al obtener localidades")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al obtener localidades")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de localidades: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante obtención de localidades: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            f"/departamentos/{id_departamento}/localidades",
            catch_response=True,
            name=f"(DOMICILIOS) - /departamentos/{id_departamento}/localidades [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
import copy
from typing import Dict, Any

# ... (funciones existentes) ...

def insert_domicilio(client, logger, environment, data_module):
    """Prueba el endpoint de insertar domicilios"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_domicilio_comercial'):
        logger.error("No hay datos para insertar domicilios en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/domicilios", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para domicilios")
        return
    
    # Usar el cuerpo de domicilio comercial
    body_insertar = copy.deepcopy(data_module.body_insertar_domicilio_comercial)
    
    # Agregar variación aleatoria a la altura para evitar duplicados
    try:
        altura_base = int(body_insertar["p_altura"])
        variacion = random.randint(1, 999)
        body_insertar["p_altura"] = str(altura_base + variacion)
    except ValueError:
        # Si no se puede convertir a entero, agregar sufijo
        body_insertar["p_altura"] = f"{body_insertar['p_altura']}-{random.randint(1, 99)}"
    
    # Intentar usar IDs válidos obtenidos dinámicamente
    ids_usados = {"barrio": None, "calle": None}
    
    # Si hay IDs de barrios obtenidos dinámicamente, usar uno de ellos
    if hasattr(data_module, 'ids_barrios') and data_module.ids_barrios:
        body_insertar["p_id_barrio"] = random.choice(data_module.ids_barrios)
        ids_usados["barrio"] = body_insertar["p_id_barrio"]
        logger.info(f"Usando ID de barrio obtenido dinámicamente: {body_insertar['p_id_barrio']}")
    
    # Si hay IDs de calles obtenidos dinámicamente, usar uno de ellos
    if hasattr(data_module, 'ids_calles') and data_module.ids_calles:
        body_insertar["p_id_calle"] = random.choice(data_module.ids_calles)
        ids_usados["calle"] = body_insertar["p_id_calle"]
        logger.info(f"Usando ID de calle obtenido dinámicamente: {body_insertar['p_id_calle']}")
    
    logger.info(f"Ejecutando insert_domicilio con datos: {body_insertar}")
    
    try:
        with client.post(
            "/domicilios", 
            json=body_insertar,
            catch_response=True,
            name="(DOMICILIOS) - /domicilios [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "p_id_domicilio", "p_id_localidad", "p_altura",
                        "fecha_creacion", "fecha_modifica", "p_usuario_aplicacion"
                    ]
                    
                    # Verificar campos obligatorios
                    campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                    
                    if not campos_faltantes:
                        response.success()
                        logger.info(f"Inserción de domicilio exitosa")
                        logger.info(f"ID domicilio generado: {response_data.get('p_id_domicilio')}")
                        logger.info(f"Validación del domicilio: {response_data.get('p_valido', 'No especificado')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.ultimo_id_domicilio = response_data.get('p_id_domicilio')
                        
                        # Mostrar información relevante del domicilio creado
                        logger.info(f"Domicilio comercial creado:")
                        logger.info(f"- Localidad ID: {response_data.get('p_id_localidad')}")
                        logger.info(f"- Barrio ID: {response_data.get('p_id_barrio')}")
                        logger.info(f"- Calle ID: {response_data.get('p_id_calle')}")
                        logger.info(f"- Altura: {response_data.get('p_altura')}")
                        logger.info(f"- Piso: {response_data.get('p_piso')}")
                        logger.info(f"- Departamento: {response_data.get('p_dpto')}")
                        logger.info(f"- Oficina/Local: {response_data.get('p_oficina_local')}")
                        
                    else:
                        logger.warning(f"Faltan campos obligatorios en la respuesta: {campos_faltantes}")
                        response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos obligatorios")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 422:  # Unprocessable Entity - Error de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 422: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list):
                            # Revisar tipos de errores específicos
                            for error_item in detail:
                                error_type = error_item.get("type", "")
                                error_msg = error_item.get("msg", "")
                                error_loc = error_item.get("loc", [])
                                
                                if "p_id_barrio" in error_loc and "id of neighborhood for Córdoba" in error_msg:
                                    logger.warning(f"ID de barrio inválido para Córdoba: {ids_usados['barrio']}")
                                    response.failure(f"ID de barrio {ids_usados['barrio']} no es válido para Córdoba")
                                elif "p_id_calle" in error_loc:
                                    logger.warning(f"ID de calle inválido: {ids_usados['calle']}")
                                    response.failure(f"ID de calle {ids_usados['calle']} no es válido")
                                elif "p_id_localidad" in error_loc:
                                    logger.warning(f"ID de localidad inválido: {body_insertar['p_id_localidad']}")
                                    response.failure(f"ID de localidad {body_insertar['p_id_localidad']} no es válido")
                                else:
                                    logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                    response.failure(f"Error de validación: {error_msg}")
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 422 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
                    
            elif response.status_code == 400:
                # Otros errores de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    
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
                    
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al insertar domicilio")
                response.failure("Error de autenticación")
                
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al insertar domicilio")
                response.failure("Error de permisos")
                
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al insertar domicilio")
                response.failure("Error interno del servidor")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción de domicilio: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/domicilios",
            json={"error": "exception"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
import copy
from typing import Dict, Any

# ... (funciones existentes) ...

def insert_domicilio_ampliado(client, logger, environment, data_module):
    """Prueba el endpoint de insertar domicilios ampliado"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_domicilio_ampliado'):
        logger.error("No hay datos para insertar domicilios ampliados en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/domicilios/ampliado", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/ampliado [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para domicilios ampliados")
        return
    
    # Usar el cuerpo de domicilio ampliado
    body_insertar = copy.deepcopy(data_module.body_insertar_domicilio_ampliado)
    
    # Agregar variación aleatoria a la altura para evitar duplicados
    try:
        altura_base = int(body_insertar["p_altura"])
        variacion = random.randint(1, 999)
        body_insertar["p_altura"] = str(altura_base + variacion)
    except ValueError:
        # Si no se puede convertir a entero, agregar sufijo
        body_insertar["p_altura"] = f"{body_insertar['p_altura']}-{random.randint(1, 99)}"
    
    # Agregar pequeña variación a las coordenadas para evitar duplicados
    if body_insertar["p_latitud"] is not None:
        variacion_lat = random.uniform(-0.001, 0.001)  # Variación pequeña en latitud
        body_insertar["p_latitud"] = round(body_insertar["p_latitud"] + variacion_lat, 6)
    
    if body_insertar["p_longitud"] is not None:
        variacion_lng = random.uniform(-0.001, 0.001)  # Variación pequeña en longitud
        body_insertar["p_longitud"] = round(body_insertar["p_longitud"] + variacion_lng, 6)
    
    # Intentar usar IDs válidos obtenidos dinámicamente
    ids_usados = {"barrio": None, "calle": None, "calle_perp1": None, "calle_perp2": None}
    
    # Si hay IDs de barrios obtenidos dinámicamente, usar uno de ellos
    if hasattr(data_module, 'ids_barrios') and data_module.ids_barrios:
        body_insertar["p_id_barrio"] = random.choice(data_module.ids_barrios)
        ids_usados["barrio"] = body_insertar["p_id_barrio"]
        logger.info(f"Usando ID de barrio obtenido dinámicamente: {body_insertar['p_id_barrio']}")
    
    # Si hay IDs de calles obtenidos dinámicamente, usar uno de ellos
    if hasattr(data_module, 'ids_calles') and data_module.ids_calles:
        body_insertar["p_id_calle"] = random.choice(data_module.ids_calles)
        ids_usados["calle"] = body_insertar["p_id_calle"]
        logger.info(f"Usando ID de calle obtenido dinámicamente: {body_insertar['p_id_calle']}")
        
        # Opcionalmente, agregar calles perpendiculares si hay suficientes IDs
        if len(data_module.ids_calles) >= 3:
            calles_disponibles = [c for c in data_module.ids_calles if c != body_insertar["p_id_calle"]]
            
            # Agregar calle perpendicular 1 aleatoriamente (50% de probabilidad)
            if random.choice([True, False]) and calles_disponibles:
                body_insertar["id_calle_perp1"] = random.choice(calles_disponibles)
                ids_usados["calle_perp1"] = body_insertar["id_calle_perp1"]
                logger.info(f"Usando ID de calle perpendicular 1: {body_insertar['id_calle_perp1']}")
                
                # Agregar calle perpendicular 2 si ya hay perpendicular 1 (30% de probabilidad)
                calles_restantes = [c for c in calles_disponibles if c != body_insertar["id_calle_perp1"]]
                if random.random() < 0.3 and calles_restantes:
                    body_insertar["id_calle_perp2"] = random.choice(calles_restantes)
                    ids_usados["calle_perp2"] = body_insertar["id_calle_perp2"]
                    logger.info(f"Usando ID de calle perpendicular 2: {body_insertar['id_calle_perp2']}")
    
    # Agregar variación a las observaciones
    if body_insertar["p_observaciones"]:
        timestamp = random.randint(1000, 9999)
        body_insertar["p_observaciones"] = f"{body_insertar['p_observaciones']} - Test {timestamp}"
    
    logger.info(f"Ejecutando insert_domicilio_ampliado con datos: {body_insertar}")
    
    try:
        with client.post(
            "/domicilios/ampliado", 
            json=body_insertar,
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/ampliado [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO AMPLIADO) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "p_id_domicilio", "p_id_localidad", "p_altura",
                        "fecha_creacion", "fecha_modifica", "p_usuario_aplicacion"
                    ]
                    
                    # Campos específicos del domicilio ampliado
                    campos_ampliados = [
                        "p_latitud", "p_longitud", "p_observaciones",
                        "id_calle_perp1", "id_calle_perp2"
                    ]
                    
                    # Verificar campos obligatorios
                    campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                    
                    if not campos_faltantes:
                        response.success()
                        logger.info(f"Inserción de domicilio ampliado exitosa")
                        logger.info(f"ID domicilio generado: {response_data.get('p_id_domicilio')}")
                        logger.info(f"Validación del domicilio: {response_data.get('p_valido', 'No especificado')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.ultimo_id_domicilio_ampliado = response_data.get('p_id_domicilio')
                        
                        # Mostrar información relevante del domicilio ampliado creado
                        logger.info(f"Domicilio ampliado creado:")
                        logger.info(f"- Localidad ID: {response_data.get('p_id_localidad')}")
                        logger.info(f"- Barrio ID: {response_data.get('p_id_barrio')}")
                        logger.info(f"- Calle ID: {response_data.get('p_id_calle')}")
                        logger.info(f"- Altura: {response_data.get('p_altura')}")
                        logger.info(f"- Piso: {response_data.get('p_piso')}")
                        logger.info(f"- Departamento: {response_data.get('p_dpto')}")
                        logger.info(f"- Oficina/Local: {response_data.get('p_oficina_local')}")
                        
                        # Información específica del domicilio ampliado
                        if response_data.get('p_latitud') is not None:
                            logger.info(f"- Latitud: {response_data.get('p_latitud')}")
                        if response_data.get('p_longitud') is not None:
                            logger.info(f"- Longitud: {response_data.get('p_longitud')}")
                        if response_data.get('p_observaciones'):
                            logger.info(f"- Observaciones: {response_data.get('p_observaciones')}")
                        if response_data.get('id_calle_perp1'):
                            logger.info(f"- Calle perpendicular 1 ID: {response_data.get('id_calle_perp1')}")
                        if response_data.get('id_calle_perp2'):
                            logger.info(f"- Calle perpendicular 2 ID: {response_data.get('id_calle_perp2')}")
                        
                        # Validar campos ampliados presentes
                        campos_ampliados_presentes = [campo for campo in campos_ampliados if campo in response_data and response_data[campo] is not None]
                        if campos_ampliados_presentes:
                            logger.info(f"Campos ampliados presentes: {campos_ampliados_presentes}")
                        
                    else:
                        logger.warning(f"Faltan campos obligatorios en la respuesta: {campos_faltantes}")
                        response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos obligatorios")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 422:  # Unprocessable Entity - Error de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 422: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list):
                            # Revisar tipos de errores específicos
                            for error_item in detail:
                                error_type = error_item.get("type", "")
                                error_msg = error_item.get("msg", "")
                                error_loc = error_item.get("loc", [])
                                
                                if "p_id_barrio" in error_loc and "id of neighborhood for Córdoba" in error_msg:
                                    logger.warning(f"ID de barrio inválido para Córdoba: {ids_usados['barrio']}")
                                    response.failure(f"ID de barrio {ids_usados['barrio']} no es válido para Córdoba")
                                elif "p_id_calle" in error_loc:
                                    logger.warning(f"ID de calle inválido: {ids_usados['calle']}")
                                    response.failure(f"ID de calle {ids_usados['calle']} no es válido")
                                elif "id_calle_perp1" in error_loc:
                                    logger.warning(f"ID de calle perpendicular 1 inválido: {ids_usados['calle_perp1']}")
                                    response.failure(f"ID de calle perpendicular 1 {ids_usados['calle_perp1']} no es válido")
                                elif "id_calle_perp2" in error_loc:
                                    logger.warning(f"ID de calle perpendicular 2 inválido: {ids_usados['calle_perp2']}")
                                    response.failure(f"ID de calle perpendicular 2 {ids_usados['calle_perp2']} no es válido")
                                elif "p_id_localidad" in error_loc:
                                    logger.warning(f"ID de localidad inválido: {body_insertar['p_id_localidad']}")
                                    response.failure(f"ID de localidad {body_insertar['p_id_localidad']} no es válido")
                                elif "p_latitud" in error_loc or "p_longitud" in error_loc:
                                    logger.warning(f"Coordenadas inválidas: lat={body_insertar.get('p_latitud')}, lng={body_insertar.get('p_longitud')}")
                                    response.failure(f"Coordenadas geográficas inválidas")
                                else:
                                    logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                    response.failure(f"Error de validación: {error_msg}")
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 422 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
                    
            elif response.status_code == 400:
                # Otros errores de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("El domicilio ampliado ya existe - respuesta 400 esperada")
                            response.success()
                        elif isinstance(detail, list) and any("low_data_quality" in str(item.get("type", "")) for item in detail):
                            logger.info("Calidad de datos baja - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
                    
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al insertar domicilio ampliado")
                response.failure("Error de autenticación")
                
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al insertar domicilio ampliado")
                response.failure("Error de permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al insertar domicilio ampliado")
                response.failure("Error interno del servidor")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción de domicilio ampliado: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio ampliado: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/domicilios/ampliado",
            json={"error": "exception"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/ampliado [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def insert_domicilio_geo(client, logger, environment, data_module):
    """Prueba el endpoint de insertar domicilios con información geográfica"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_domicilio_geo'):
        logger.error("No hay datos para insertar domicilios geo en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/domicilios/geo", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/geo [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para domicilios geo")
        return
    
    # Usar el cuerpo de domicilio geo
    body_insertar = copy.deepcopy(data_module.body_insertar_domicilio_geo)
    
    # Agregar variación aleatoria a la altura para evitar duplicados
    try:
        altura_base = int(body_insertar["p_altura"])
        variacion = random.randint(1, 999)
        body_insertar["p_altura"] = str(altura_base + variacion)
    except ValueError:
        # Si no se puede convertir a entero, agregar sufijo
        body_insertar["p_altura"] = f"{body_insertar['p_altura']}-{random.randint(1, 99)}"
    
    # Intentar usar IDs válidos obtenidos dinámicamente
    ids_usados = {"calle": None, "calle_perp1": None, "calle_perp2": None}
    
    # Si hay IDs de calles obtenidos dinámicamente, usar uno de ellos
    if hasattr(data_module, 'ids_calles') and data_module.ids_calles:
        body_insertar["p_id_calle"] = random.choice(data_module.ids_calles)
        ids_usados["calle"] = body_insertar["p_id_calle"]
        logger.info(f"Usando ID de calle obtenido dinámicamente: {body_insertar['p_id_calle']}")
        
        # Decidir aleatoriamente el tipo de ubicación a usar
        tipo_ubicacion = random.choice(["altura", "esquina_simple", "esquina_doble"])
        
        if tipo_ubicacion == "altura":
            # Usar calle + altura (comportamiento por defecto)
            body_insertar["p_id_calle_perp1"] = None
            body_insertar["p_id_calle_perp2"] = None
            logger.info(f"Usando ubicación por calle + altura: {body_insertar['p_altura']}")
            
        elif tipo_ubicacion == "esquina_simple" and len(data_module.ids_calles) >= 2:
            # Usar calle + una calle perpendicular (esquina)
            calles_disponibles = [c for c in data_module.ids_calles if c != body_insertar["p_id_calle"]]
            body_insertar["p_id_calle_perp1"] = random.choice(calles_disponibles)
            body_insertar["p_id_calle_perp2"] = None
            body_insertar["p_altura"] = "SN"  # Sin número para esquinas
            ids_usados["calle_perp1"] = body_insertar["p_id_calle_perp1"]
            logger.info(f"Usando ubicación por esquina simple: calle {body_insertar['p_id_calle']} y {body_insertar['p_id_calle_perp1']}")
            
        elif tipo_ubicacion == "esquina_doble" and len(data_module.ids_calles) >= 3:
            # Usar calle + dos calles perpendiculares
            calles_disponibles = [c for c in data_module.ids_calles if c != body_insertar["p_id_calle"]]
            calles_seleccionadas = random.sample(calles_disponibles, 2)
            body_insertar["p_id_calle_perp1"] = calles_seleccionadas[0]
            body_insertar["p_id_calle_perp2"] = calles_seleccionadas[1]
            body_insertar["p_altura"] = "SN"  # Sin número para esquinas
            ids_usados["calle_perp1"] = body_insertar["p_id_calle_perp1"]
            ids_usados["calle_perp2"] = body_insertar["p_id_calle_perp2"]
            logger.info(f"Usando ubicación por esquina doble: calle {body_insertar['p_id_calle']}, {body_insertar['p_id_calle_perp1']} y {body_insertar['p_id_calle_perp2']}")
    
    # Agregar variación a las observaciones
    if body_insertar["p_observaciones"]:
        timestamp = random.randint(1000, 9999)
        body_insertar["p_observaciones"] = f"{body_insertar['p_observaciones']} - Geo Test {timestamp}"
    
    logger.info(f"Ejecutando insert_domicilio_geo con datos: {body_insertar}")
    
    try:
        with client.post(
            "/domicilios/geo", 
            json=body_insertar,
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/geo [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO GEO) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "p_id_domicilio", "p_id_localidad", "p_altura",
                        "fecha_creacion", "fecha_modifica", "p_usuario_aplicacion"
                    ]
                    
                    # Campos específicos del domicilio geo
                    campos_geo = [
                        "p_id_pais", "p_id_provincia", "p_id_departamento",
                        "p_latitud", "p_longitud", "p_zona", "p_id_cpc", "p_cpc"
                    ]
                    
                    # Verificar campos obligatorios
                    campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                    
                    if not campos_faltantes:
                        response.success()
                        logger.info(f"Inserción de domicilio geo exitosa")
                        logger.info(f"ID domicilio generado: {response_data.get('p_id_domicilio')}")
                        logger.info(f"Validación del domicilio: {response_data.get('p_valido', 'No especificado')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.ultimo_id_domicilio_geo = response_data.get('p_id_domicilio')
                        
                        # Mostrar información relevante del domicilio geo creado
                        logger.info(f"Domicilio geo creado:")
                        logger.info(f"- País ID: {response_data.get('p_id_pais')}")
                        logger.info(f"- Provincia ID: {response_data.get('p_id_provincia')}")
                        logger.info(f"- Departamento ID: {response_data.get('p_id_departamento')}")
                        logger.info(f"- Localidad ID: {response_data.get('p_id_localidad')}")
                        logger.info(f"- Barrio ID: {response_data.get('p_id_barrio')}")
                        logger.info(f"- Calle ID: {response_data.get('p_id_calle')}")
                        logger.info(f"- Altura: {response_data.get('p_altura')}")
                        
                        # Información geográfica específica
                        if response_data.get('p_latitud') is not None:
                            logger.info(f"- Latitud: {response_data.get('p_latitud')}")
                        if response_data.get('p_longitud') is not None:
                            logger.info(f"- Longitud: {response_data.get('p_longitud')}")
                        if response_data.get('p_zona'):
                            logger.info(f"- Zona catastral: {response_data.get('p_zona')}")
                        if response_data.get('p_id_cpc'):
                            logger.info(f"- CPC ID: {response_data.get('p_id_cpc')}")
                        if response_data.get('p_cpc'):
                            logger.info(f"- CPC: {response_data.get('p_cpc')}")
                        if response_data.get('p_id_calle_perp1'):
                            logger.info(f"- Calle perpendicular 1 ID: {response_data.get('p_id_calle_perp1')}")
                        if response_data.get('p_id_calle_perp2'):
                            logger.info(f"- Calle perpendicular 2 ID: {response_data.get('p_id_calle_perp2')}")
                        
                        # Validar campos geo presentes
                        campos_geo_presentes = [campo for campo in campos_geo if campo in response_data and response_data[campo] is not None]
                        if campos_geo_presentes:
                            logger.info(f"Campos geográficos presentes: {campos_geo_presentes}")
                        
                    else:
                        logger.warning(f"Faltan campos obligatorios en la respuesta: {campos_faltantes}")
                        response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos obligatorios")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 422:  # Unprocessable Entity - Error de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 422: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list):
                            # Revisar tipos de errores específicos
                            for error_item in detail:
                                error_type = error_item.get("type", "")
                                error_msg = error_item.get("msg", "")
                                error_loc = error_item.get("loc", [])
                                
                                if "p_id_calle" in error_loc:
                                    logger.warning(f"ID de calle inválido: {ids_usados['calle']}")
                                    response.failure(f"ID de calle {ids_usados['calle']} no es válido")
                                elif "p_id_calle_perp1" in error_loc:
                                    logger.warning(f"ID de calle perpendicular 1 inválido: {ids_usados['calle_perp1']}")
                                    response.failure(f"ID de calle perpendicular 1 {ids_usados['calle_perp1']} no es válido")
                                elif "p_id_calle_perp2" in error_loc:
                                    logger.warning(f"ID de calle perpendicular 2 inválido: {ids_usados['calle_perp2']}")
                                    response.failure(f"ID de calle perpendicular 2 {ids_usados['calle_perp2']} no es válido")
                                elif "p_id_localidad" in error_loc:
                                    logger.warning(f"ID de localidad inválido: {body_insertar['p_id_localidad']}")
                                    response.failure(f"ID de localidad {body_insertar['p_id_localidad']} no es válido")
                                elif "insufficient_parameters" in error_msg.lower():
                                    logger.warning("Parámetros insuficientes para determinar ubicación")
                                    response.failure("Parámetros insuficientes o inválidos para ubicación")
                                else:
                                    logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                    response.failure(f"Error de validación: {error_msg}")
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 422 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
                    
            elif response.status_code == 400:
                # Otros errores de validación
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("already_exists" in str(item.get("type", "")) for item in detail):
                            logger.info("El domicilio geo ya existe - respuesta 400 esperada")
                            response.success()
                        elif isinstance(detail, list) and any("low_data_quality" in str(item.get("type", "")) for item in detail):
                            logger.info("Calidad de datos baja - respuesta 400 esperada")
                            response.success()
                        elif isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info("No se encontró ubicación válida - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
                    
            elif response.status_code == 404:
                # Error de ubicación no encontrada
                try:
                    error_data = response.json()
                    logger.warning(f"Ubicación no encontrada 404: {error_data}")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info("No se encontró ubicación válida para los parámetros dados - respuesta 404 esperada")
                            response.success()
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.failure(f"Error 404 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
                    
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al insertar domicilio geo")
                response.failure("Error de autenticación")
                
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al insertar domicilio geo")
                response.failure("Error de permisos")
                
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al insertar domicilio geo")
                response.failure("Error interno del servidor")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción de domicilio geo: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante inserción de domicilio geo: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/domicilios/geo",
            json={"error": "exception"},
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/geo [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_domicilio_geo(client, logger, environment, data_module):
    """Prueba el endpoint de obtener coordenadas de domicilio por calle y altura"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'query_params_domicilio_geo') and not hasattr(data_module, 'lista_consultas_domicilio_geo'):
        logger.error("No hay datos para consultar domicilios geo en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/domicilios/geo?p_id_localidad=1&p_id_calle=1&p_altura=1", 
            catch_response=True,
            name="(DOMICILIOS) - /domicilios/geo [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para consultar domicilios geo")
        return
    
    # Determinar qué datos usar para las consultas
    consultas_a_realizar = []
    
    logger.info(f"Ejecutando get_domicilio_geo con {len(consultas_a_realizar)} consultas")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "no_encontrados": 0,
        "errores": 0
    }
    
    # Realizar cada consulta
    for idx, params in enumerate(consultas_a_realizar):
        p_id_localidad = params.get("p_id_localidad", 1)
        p_id_calle = params.get("p_id_calle")
        p_altura = params.get("p_altura")
        
        # Construir la URL con parámetros de consulta
        url = f"/domicilios/geo?p_id_localidad={p_id_localidad}&p_id_calle={p_id_calle}&p_altura={p_altura}"
        
        logger.info(f"Consulta {idx + 1}: Localidad={p_id_localidad}, Calle={p_id_calle}, Altura={p_altura}")
        
        try:
            with client.get(
                url, 
                catch_response=True,
                name=f"(DOMICILIOS) - /domicilios/geo [GET {p_id_calle}-{p_altura}]"
            ) as response:
                # Guardar la respuesta en el log (versión resumida para no saturar)
                logger.info(f"Respuesta para consulta {idx + 1}: Código {response.status_code}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar los datos completos obtenidos en el log
                        logger.info(f"=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO GEO {idx + 1}) ===")
                        logger.info(f"Respuesta: {response_data}")
                        
                        # Validar estructura de datos esperada
                        campos_esperados = [
                            "p_id_localidad", "p_id_barrio", "p_id_calle", 
                            "p_barrio", "p_calle", "p_altura", 
                            "p_latitud", "p_longitud"
                        ]
                        
                        if all(campo in response_data for campo in campos_esperados):
                            response.success()
                            logger.info(f"Consulta geo exitosa para calle {p_id_calle}, altura {p_altura}")
                            logger.info(f"Coordenadas: Lat={response_data.get('p_latitud')}, Lng={response_data.get('p_longitud')}")
                            logger.info(f"Ubicación: {response_data.get('p_calle')} {response_data.get('p_altura')}, {response_data.get('p_barrio')}")
                            
                            # Guardar datos para posibles pruebas futuras
                            data_module.ultima_consulta_geo = response_data
                            resultados["exitosos"] += 1
                            
                            # Validar que las coordenadas sean válidas para Córdoba
                            latitud = response_data.get('p_latitud')
                            longitud = response_data.get('p_longitud')
                            
                            if latitud and longitud:
                                # Córdoba está aproximadamente entre -31.2 y -31.5 de latitud, -64.0 y -64.3 de longitud
                                if -31.6 <= latitud <= -31.0 and -64.5 <= longitud <= -63.8:
                                    logger.info("✓ Coordenadas válidas para la ciudad de Córdoba")
                                else:
                                    logger.warning(f"⚠ Coordenadas fuera del rango esperado para Córdoba: {latitud}, {longitud}")
                        else:
                            # Verificar qué campos faltan
                            campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                            logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                            resultados["errores"] += 1
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en respuesta: {response.text[:100]}...")
                        resultados["errores"] += 1
                        
                elif response.status_code == 404:
                    # No se encontró ubicación válida (comportamiento esperado)
                    try:
                        error_data = response.json()
                        logger.info(f"No se encontró ubicación para calle {p_id_calle}, altura {p_altura}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                                logger.info("No se encontró ubicación válida - respuesta 404 esperada")
                                response.success()  # Marcamos como éxito porque es comportamiento esperado
                            else:
                                response.failure(f"Error 404: {detail}")
                        else:
                            response.success()  # Marcamos como éxito porque es comportamiento esperado
                        
                        resultados["no_encontrados"] += 1
                    except ValueError:
                        response.failure(f"Error 404 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 400:
                    # Error de validación de parámetros
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 400: {error_data}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list):
                                for error_item in detail:
                                    error_msg = error_item.get("msg", "")
                                    error_loc = error_item.get("loc", [])
                                    
                                    if "p_id_localidad" in error_loc:
                                        logger.warning(f"ID de localidad inválido: {p_id_localidad}")
                                        response.failure(f"Solo se acepta localidad de Córdoba (ID=1)")
                                    elif "p_id_calle" in error_loc:
                                        logger.warning(f"ID de calle inválido: {p_id_calle}")
                                        response.failure(f"ID de calle {p_id_calle} no es válido")
                                    elif "p_altura" in error_loc:
                                        logger.warning(f"Altura inválida: {p_altura}")
                                        response.failure(f"Altura {p_altura} no es válida")
                                    else:
                                        logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                        response.failure(f"Error de validación: {error_msg}")
                            else:
                                response.failure(f"Error de validación: {detail}")
                        else:
                            response.failure(f"Error 400 sin detalle: {error_data}")
                        
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 400 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 422:
                    # Error de validación de esquema
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 422: {error_data}")
                        response.failure(f"Error de validación de parámetros: {error_data}")
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 422 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 401:
                    # Error de autenticación
                    logger.error("Error de autenticación al consultar domicilio geo")
                    response.failure("Error de autenticación")
                    resultados["errores"] += 1
                    
                elif response.status_code == 403:
                    # Error de permisos
                    logger.error("Error de permisos al consultar domicilio geo")
                    response.failure("Error de permisos")
                    resultados["errores"] += 1
                    
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error("Error interno del servidor al consultar domicilio geo")
                    response.failure("Error interno del servidor")
                    resultados["errores"] += 1
                    
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de domicilio geo: {response.status_code} - {response.text}")
                    resultados["errores"] += 1
                    
        except Exception as e:
            logger.error(f"Excepción durante consulta de domicilio geo {idx + 1}: {str(e)}")
            resultados["errores"] += 1
            
            # Registrar el error como una respuesta fallida
            with client.get(
                url,
                catch_response=True,
                name=f"(DOMICILIOS) - /domicilios/geo [Exception {p_id_calle}-{p_altura}]"
            ) as response:
                response.failure(f"Excepción: {str(e)}")


def get_domicilio_by_id(client, logger, environment, data_module):
    """Prueba el endpoint de obtener domicilio por ID"""
    
    # Verificar si tenemos datos para probar
    ids_para_consultar = []
    
    # Priorizar IDs obtenidos dinámicamente de inserciones previas
    if hasattr(data_module, 'ultimo_id_domicilio') and data_module.ultimo_id_domicilio:
        ids_para_consultar.append(data_module.ultimo_id_domicilio)
        logger.info(f"Usando ID de domicilio obtenido dinámicamente: {data_module.ultimo_id_domicilio}")
    
    if hasattr(data_module, 'ultimo_id_domicilio_ampliado') and data_module.ultimo_id_domicilio_ampliado:
        ids_para_consultar.append(data_module.ultimo_id_domicilio_ampliado)
        logger.info(f"Usando ID de domicilio ampliado obtenido dinámicamente: {data_module.ultimo_id_domicilio_ampliado}")
    
    if hasattr(data_module, 'ultimo_id_domicilio_geo') and data_module.ultimo_id_domicilio_geo:
        ids_para_consultar.append(data_module.ultimo_id_domicilio_geo)
        logger.info(f"Usando ID de domicilio geo obtenido dinámicamente: {data_module.ultimo_id_domicilio_geo}")
    
    # Si no hay IDs dinámicos, usar los predefinidos
    if not ids_para_consultar:
        if hasattr(data_module, 'lista_ids_domicilios') and data_module.lista_ids_domicilios:
            ids_para_consultar = data_module.lista_ids_domicilios[:3]  # Usar solo los primeros 3
        elif hasattr(data_module, 'id_domicilio_consulta'):
            ids_para_consultar = [data_module.id_domicilio_consulta]
        else:
            ids_para_consultar = [1, 2, 3]  # IDs por defecto
            logger.warning("No se encontraron IDs de domicilios. Usando valores predeterminados: [1, 2, 3]")
    
    logger.info(f"Ejecutando get_domicilio_by_id con {len(ids_para_consultar)} IDs")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "no_encontrados": 0,
        "errores": 0
    }
    
    # Realizar consulta para cada ID
    for idx, id_domicilio in enumerate(ids_para_consultar):
        logger.info(f"Consulta {idx + 1}: Domicilio ID={id_domicilio}")
        
        try:
            with client.get(
                f"/domicilios/{id_domicilio}", 
                catch_response=True,
                name=f"(DOMICILIOS) - /domicilios/{{id}} [GET {id_domicilio}]"
            ) as response:
                # Guardar la respuesta en el log (versión resumida para no saturar)
                logger.info(f"Respuesta para domicilio {id_domicilio}: Código {response.status_code}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar los datos completos obtenidos en el log
                        logger.info(f"=== DATOS COMPLETOS DE LA RESPUESTA (DOMICILIO {id_domicilio}) ===")
                        logger.info(f"Respuesta: {response_data}")
                        
                        # Validar estructura de datos esperada
                        campos_esperados = [
                            "p_id_domicilio", "p_id_localidad", "p_altura",
                            "fecha_creacion", "fecha_modifica", "p_valido"
                        ]
                        
                        # Campos opcionales que pueden estar presentes
                        campos_opcionales = [
                            "p_id_barrio", "p_id_calle", "p_barrio", "p_calle",
                            "p_piso", "p_dpto", "p_manzana", "p_lote", "p_torre",
                            "p_oficina_local", "p_id_pais", "p_id_provincia", 
                            "p_id_departamento", "p_id_calle_perp1", "p_id_calle_perp2",
                            "p_observaciones", "p_latitud", "p_longitud"
                        ]
                        
                        if all(campo in response_data for campo in campos_esperados):
                            response.success()
                            logger.info(f"Consulta de domicilio exitosa para ID: {id_domicilio}")
                            logger.info(f"Domicilio válido: {response_data.get('p_valido')}")
                            
                            # Mostrar información relevante del domicilio
                            logger.info(f"Información del domicilio {id_domicilio}:")
                            logger.info(f"- Localidad ID: {response_data.get('p_id_localidad')}")
                            
                            if response_data.get('p_id_barrio'):
                                logger.info(f"- Barrio ID: {response_data.get('p_id_barrio')}")
                            if response_data.get('p_barrio'):
                                logger.info(f"- Barrio: {response_data.get('p_barrio')}")
                            
                            if response_data.get('p_id_calle'):
                                logger.info(f"- Calle ID: {response_data.get('p_id_calle')}")
                            if response_data.get('p_calle'):
                                logger.info(f"- Calle: {response_data.get('p_calle')}")
                            
                            logger.info(f"- Altura: {response_data.get('p_altura')}")
                            
                            if response_data.get('p_piso'):
                                logger.info(f"- Piso: {response_data.get('p_piso')}")
                            if response_data.get('p_dpto'):
                                logger.info(f"- Departamento: {response_data.get('p_dpto')}")
                            if response_data.get('p_torre'):
                                logger.info(f"- Torre: {response_data.get('p_torre')}")
                            if response_data.get('p_oficina_local'):
                                logger.info(f"- Oficina/Local: {response_data.get('p_oficina_local')}")
                            
                            # Información geográfica si está disponible
                            if response_data.get('p_latitud') is not None and response_data.get('p_longitud') is not None:
                                logger.info(f"- Coordenadas: Lat={response_data.get('p_latitud')}, Lng={response_data.get('p_longitud')}")
                            
                            if response_data.get('p_observaciones'):
                                logger.info(f"- Observaciones: {response_data.get('p_observaciones')}")
                            
                            # Información jerárquica
                            if response_data.get('p_id_pais'):
                                logger.info(f"- País ID: {response_data.get('p_id_pais')}")
                            if response_data.get('p_id_provincia'):
                                logger.info(f"- Provincia ID: {response_data.get('p_id_provincia')}")
                            if response_data.get('p_id_departamento'):
                                logger.info(f"- Departamento ID: {response_data.get('p_id_departamento')}")
                            
                            # Calles perpendiculares si existen
                            if response_data.get('p_id_calle_perp1'):
                                logger.info(f"- Calle perpendicular 1 ID: {response_data.get('p_id_calle_perp1')}")
                            if response_data.get('p_id_calle_perp2'):
                                logger.info(f"- Calle perpendicular 2 ID: {response_data.get('p_id_calle_perp2')}")
                            
                            # Guardar datos para posibles pruebas futuras
                            data_module.ultimo_domicilio_consultado = response_data
                            resultados["exitosos"] += 1
                            
                            # Contar campos opcionales presentes
                            campos_presentes = [campo for campo in campos_opcionales if campo in response_data and response_data[campo] is not None]
                            if campos_presentes:
                                logger.info(f"Campos opcionales presentes: {len(campos_presentes)}/{len(campos_opcionales)}")
                        else:
                            # Verificar qué campos obligatorios faltan
                            campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                            logger.warning(f"Faltan campos obligatorios en la respuesta: {campos_faltantes}")
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos obligatorios")
                            resultados["errores"] += 1
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en respuesta: {response.text[:100]}...")
                        resultados["errores"] += 1
                        
                elif response.status_code == 404:
                    # Domicilio no encontrado (comportamiento esperado)
                    try:
                        error_data = response.json()
                        logger.info(f"No se encontró domicilio con ID: {id_domicilio}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                                logger.info("Domicilio no encontrado - respuesta 404 esperada")
                                response.success()  # Marcamos como éxito porque es comportamiento esperado
                            else:
                                response.failure(f"Error 404: {detail}")
                        else:
                            response.success()  # Marcamos como éxito porque es comportamiento esperado
                        
                        resultados["no_encontrados"] += 1
                    except ValueError:
                        response.failure(f"Error 404 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 400:
                    # Error de validación de parámetros
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 400: {error_data}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list):
                                for error_item in detail:
                                    error_msg = error_item.get("msg", "")
                                    error_loc = error_item.get("loc", [])
                                    
                                    if "p_id_domicilio" in error_loc:
                                        logger.warning(f"ID de domicilio inválido: {id_domicilio}")
                                        response.failure(f"ID de domicilio {id_domicilio} no es válido")
                                    else:
                                        logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                        response.failure(f"Error de validación: {error_msg}")
                            else:
                                response.failure(f"Error de validación: {detail}")
                        else:
                            response.failure(f"Error 400 sin detalle: {error_data}")
                        
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 400 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 422:
                    # Error de validación de esquema
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 422: {error_data}")
                        response.failure(f"Error de validación de parámetros: {error_data}")
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 422 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 401:
                    # Error de autenticación
                    logger.error("Error de autenticación al consultar domicilio")
                    response.failure("Error de autenticación")
                    resultados["errores"] += 1
                    
                elif response.status_code == 403:
                    # Error de permisos
                    logger.error("Error de permisos al consultar domicilio")
                    response.failure("Error de permisos")
                    resultados["errores"] += 1
                    
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error("Error interno del servidor al consultar domicilio")
                    response.failure("Error interno del servidor")
                    resultados["errores"] += 1
                    
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de domicilio: {response.status_code} - {response.text}")
                    resultados["errores"] += 1
                    
        except Exception as e:
            logger.error(f"Excepción durante consulta de domicilio {id_domicilio}: {str(e)}")
            resultados["errores"] += 1
            
            # Registrar el error como una respuesta fallida
            with client.get(
                f"/domicilios/{id_domicilio}",
                catch_response=True,
                name=f"(DOMICILIOS) - /domicilios/{{id}} [Exception {id_domicilio}]"
            ) as response:
                response.failure(f"Excepción: {str(e)}")
    
def insert_incidente(client, logger, environment, data_module):
    """Prueba el endpoint de insertar/actualizar incidentes"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_incidente') and not hasattr(data_module, 'lista_incidentes'):
        logger.error("No hay datos para insertar incidentes en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/incidente", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(DOMICILIOS) - /incidente [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para incidentes")
        return
    
    # Determinar qué datos usar
    incidentes_a_insertar = []
    
    if hasattr(data_module, 'lista_incidentes') and data_module.lista_incidentes:
        incidentes_a_insertar = data_module.lista_incidentes
    elif hasattr(data_module, 'body_insertar_incidente'):
        incidentes_a_insertar = [data_module.body_insertar_incidente]
    
    logger.info(f"Ejecutando insert_incidente con {len(incidentes_a_insertar)} incidentes")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "actualizados": 0,
        "errores": 0
    }
    
    # Procesar cada incidente
    for idx, incidente_data in enumerate(incidentes_a_insertar):
        # Crear una copia profunda para evitar modificar el original
        body_insertar = copy.deepcopy(incidente_data)
        
        # Intentar usar IDs de domicilios obtenidos dinámicamente
        if hasattr(data_module, 'ultimo_id_domicilio') and data_module.ultimo_id_domicilio:
            body_insertar["p_id_domicilio"] = data_module.ultimo_id_domicilio
            logger.info(f"Usando ID de domicilio obtenido dinámicamente: {data_module.ultimo_id_domicilio}")
        elif hasattr(data_module, 'ultimo_id_domicilio_ampliado') and data_module.ultimo_id_domicilio_ampliado:
            body_insertar["p_id_domicilio"] = data_module.ultimo_id_domicilio_ampliado
            logger.info(f"Usando ID de domicilio ampliado obtenido dinámicamente: {data_module.ultimo_id_domicilio_ampliado}")
        elif hasattr(data_module, 'ultimo_id_domicilio_geo') and data_module.ultimo_id_domicilio_geo:
            body_insertar["p_id_domicilio"] = data_module.ultimo_id_domicilio_geo
            logger.info(f"Usando ID de domicilio geo obtenido dinámicamente: {data_module.ultimo_id_domicilio_geo}")
        
        # Agregar variación al número de incidente para evitar duplicados
        timestamp = random.randint(1000, 9999)
        numero_base = body_insertar["p_numero_incidente"]
        body_insertar["p_numero_incidente"] = f"{numero_base}-{timestamp}"
        
        logger.info(f"Incidente {idx + 1}: {body_insertar}")
        
        try:
            with client.post(
                "/incidente", 
                json=body_insertar,
                catch_response=True,
                name="(DOMICILIO) - /incidente [POST]"
            ) as response:
                # Guardar la respuesta completa en el log
                logger.info(f"Respuesta completa para incidente {idx + 1}: {response.text}")
                
                if response.status_code == 201:  # HTTP 201 Created
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar los datos completos obtenidos en el log
                        logger.info(f"=== DATOS COMPLETOS DE LA RESPUESTA (INCIDENTE {idx + 1}) ===")
                        logger.info(f"Respuesta: {response_data}")
                        
                        # Validar estructura de datos esperada
                        campos_esperados = [
                            "id_incidente", "id_domicilio", "numero_incidente",
                            "fecha_creacion", "fecha_modificacion", 
                            "usuario_creacion", "usuario_modificacion"
                        ]
                        
                        if all(campo in response_data for campo in campos_esperados):
                            response.success()
                            logger.info(f"Inserción/actualización de incidente exitosa")
                            logger.info(f"ID incidente: {response_data.get('id_incidente')}")
                            logger.info(f"Número incidente: {response_data.get('numero_incidente')}")
                            logger.info(f"ID domicilio asociado: {response_data.get('id_domicilio')}")
                            
                            # Guardar el ID para posibles pruebas futuras
                            data_module.ultimo_id_incidente = response_data.get('id_incidente')
                            data_module.ultimo_numero_incidente = response_data.get('numero_incidente')
                            
                            # Verificar si es inserción o actualización
                            if response_data.get('fecha_creacion') == response_data.get('fecha_modificacion'):
                                resultados["exitosos"] += 1
                                logger.info("✓ Nuevo incidente creado")
                            else:
                                resultados["actualizados"] += 1
                                logger.info("✓ Incidente existente actualizado")
                            
                            # Mostrar información adicional si está disponible
                            if response_data.get('calidad_dato'):
                                logger.info(f"Calidad del dato: {response_data.get('calidad_dato')}")
                            
                        else:
                            # Verificar qué campos faltan
                            campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                            logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                            response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                            resultados["errores"] += 1
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 400:
                    # Error de validación (comportamiento esperado en algunos casos)
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 400: {error_data}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list):
                                for error_item in detail:
                                    error_type = error_item.get("type", "")
                                    error_msg = error_item.get("msg", "")
                                    error_loc = error_item.get("loc", [])
                                    
                                    if "p_id_domicilio" in error_loc:
                                        logger.warning(f"ID de domicilio inválido: {body_insertar['p_id_domicilio']}")
                                        response.failure(f"ID de domicilio {body_insertar['p_id_domicilio']} no es válido")
                                    elif "p_numero_incidente" in error_loc:
                                        logger.warning(f"Número de incidente inválido: {body_insertar['p_numero_incidente']}")
                                        response.failure(f"Número de incidente {body_insertar['p_numero_incidente']} no es válido")
                                    elif "already_exists" in error_type:
                                        logger.info("El incidente ya existe - respuesta 400 esperada")
                                        response.success()
                                        resultados["actualizados"] += 1
                                    elif "low_data_quality" in error_type:
                                        logger.info("Calidad de datos baja - respuesta 400 esperada")
                                        response.success()
                                        resultados["errores"] += 1
                                    else:
                                        logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                        response.failure(f"Error de validación: {error_msg}")
                                        resultados["errores"] += 1
                            else:
                                response.failure(f"Error de validación: {detail}")
                                resultados["errores"] += 1
                        else:
                            response.failure(f"Error 400 sin detalle: {error_data}")
                            resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 400 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 422:
                    # Error de validación de esquema
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 422: {error_data}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list):
                                for error_item in detail:
                                    error_msg = error_item.get("msg", "")
                                    error_loc = error_item.get("loc", [])
                                    logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                
                                response.failure(f"Error de validación de esquema: {detail}")
                            else:
                                response.failure(f"Error de validación: {detail}")
                        else:
                            response.failure(f"Error 422 sin detalle: {error_data}")
                        
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 422 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 401:
                    # Error de autenticación
                    logger.error("Error de autenticación al insertar incidente")
                    response.failure("Error de autenticación")
                    resultados["errores"] += 1
                    
                elif response.status_code == 403:
                    # Error de permisos
                    logger.error("Error de permisos al insertar incidente")
                    response.failure("Error de permisos")
                    resultados["errores"] += 1
                    
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error("Error interno del servidor al insertar incidente")
                    response.failure("Error interno del servidor")
                    resultados["errores"] += 1
                    
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en inserción de incidente: {response.status_code} - {response.text}")
                    resultados["errores"] += 1
                    
        except Exception as e:
            logger.error(f"Excepción durante inserción de incidente {idx + 1}: {str(e)}")
            resultados["errores"] += 1
            
            # Registrar el error como una respuesta fallida
            with client.post(
                "/incidente",
                json={"error": "exception"},
                catch_response=True,
                name="(DOMICILIOS) - /incidente [Exception]"
            ) as response:
                response.failure(f"Excepción: {str(e)}")

def get_domicilio_cpc_by_id(client, logger, environment, data_module):
    """Consultar domicilio con CPC por ID"""
    try:
        logger.info("=== CONSULTANDO DOMICILIO CON CPC POR ID ===")
        
        # Obtener ID del domicilio del módulo de datos
        id_domicilio = data_module.parametros_domicilio_cpc["p_id_domicilio"]
        
        response = client.get(
            f"/domicilios/cpc/{id_domicilio}",
            name="(DOMICILIOS) - /domicilios/cpc/{id}"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info("EXITO: Domicilio con CPC consultado exitosamente")
            logger.info(f"ID Domicilio: {data.get('p_id_domicilio', 'N/A')}")
            logger.info(f"Direccion: {data.get('p_n_calle', data.get('p_calle', 'N/A'))} {data.get('p_altura', 'N/A')}")
            logger.info(f"Barrio: {data.get('p_n_barrio', data.get('p_barrio', 'N/A'))}")
            logger.info(f"Localidad: {data.get('p_localidad', 'N/A')}")
            logger.info(f"CPC: {data.get('p_cpc', 'N/A')} (ID: {data.get('p_id_cpc', 'N/A')})")
            
            # Información adicional
            if data.get('p_latitud') and data.get('p_longitud'):
                logger.info(f"Coordenadas: {data.get('p_latitud')}, {data.get('p_longitud')}")
            
            if data.get('p_calle_perp1') or data.get('p_calle_perp2'):
                perp1 = data.get('p_calle_perp1', 'N/A')
                perp2 = data.get('p_calle_perp2', 'N/A')
                logger.info(f"Calles perpendiculares: {perp1} / {perp2}")
            
            valido = data.get('p_valido', 'N/A')
            logger.info(f"Domicilio validado: {valido}")
                
        elif response.status_code == 404:
            logger.error(f"ERROR 404: Domicilio no encontrado para ID {id_domicilio}")
        elif response.status_code == 403:
            logger.error("ERROR 403: Sin permisos para consultar domicilio con CPC")
        else:
            logger.error(f"ERROR: Error al consultar domicilio con CPC: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"EXCEPCION: Error al consultar domicilio con CPC: {str(e)}")
