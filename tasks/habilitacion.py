import random
from typing import Dict, Any

def get_comercios(client, logger, environment, data_module):
    """Prueba el endpoint de obtener comercios e industrias de Córdoba"""
    
    logger.info("Ejecutando get_comercios")
    
    # Primero intentar sin parámetros para ver la estructura esperada
    query_params = {}
    
    # Si hay parámetros específicos en data_module, usarlos
    if hasattr(data_module, 'parametros_comercios'):
        query_params.update(data_module.parametros_comercios)
    
    try:
        with client.get(
            "/habilitaciones/comercios", 
            params=query_params if query_params else None,
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/comercios [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    # Para respuesta paginada, verificar si tiene estructura de paginación
                    if "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} comercios encontrados")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} comercios encontrados")
                    else:
                        logger.info(f"Respuesta recibida: {response.text[:100]}...")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info("=== RESUMEN DE LA RESPUESTA (COMERCIOS) ===")
                    if query_params:
                        logger.info(f"Parámetros utilizados: {query_params}")
                    else:
                        logger.info("Sin parámetros de consulta")
                    
                    # Validar estructura de datos esperada para respuesta paginada
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura CommercesGetPaginatedResponseSchema
                        items = response_data["items"]
                        total = response_data.get("total", len(items))
                        page = response_data.get("page", 1)
                        size = response_data.get("size", len(items))
                        
                        logger.info(f"Página: {page}, Tamaño: {size}, Total: {total}")
                        logger.info(f"Se encontraron {len(items)} comercios en esta página")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de comercios
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "razon_social", "comercio_id", "establecimiento", "cuit", "actividad"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de comercios exitosa")
                                
                                # Mostrar información de algunos comercios (hasta 5)
                                for idx, comercio in enumerate(items[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in comercio:
                                        logger.info(f"Comercio {idx+1}: {comercio.get('nombre')}")
                                    elif "razon_social" in comercio:
                                        logger.info(f"Comercio {idx+1}: {comercio.get('razon_social')}")
                                    elif "establecimiento" in comercio:
                                        logger.info(f"Comercio {idx+1}: {comercio.get('establecimiento')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in comercio.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Comercio {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "cuit" in comercio and comercio.get("cuit"):
                                        logger.info(f"  CUIT: {comercio.get('cuit')}")
                                    if "actividad" in comercio and comercio.get("actividad"):
                                        logger.info(f"  Actividad: {comercio.get('actividad')}")
                                    if "direccion" in comercio and comercio.get("direccion"):
                                        logger.info(f"  Dirección: {comercio.get('direccion')}")
                                
                                # Si hay más de 5 comercios, indicar cuántos más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} comercios más en esta página")
                                
                                # Información de paginación
                                if total > len(items):
                                    logger.info(f"Total de comercios disponibles: {total}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.comercios = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de comercios")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron comercios
                            logger.warning("No se encontraron comercios en esta página")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_comercios = len(response_data)
                        logger.info(f"Se encontraron {cantidad_comercios} comercios")
                        
                        if cantidad_comercios > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "razon_social", "comercio_id", "establecimiento", "cuit"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de comercios exitosa")
                                
                                # Mostrar algunos comercios
                                for idx, comercio in enumerate(response_data[:5]):
                                    if "nombre" in comercio:
                                        logger.info(f"Comercio {idx+1}: {comercio.get('nombre')}")
                                    elif "razon_social" in comercio:
                                        logger.info(f"Comercio {idx+1}: {comercio.get('razon_social')}")
                                
                                if cantidad_comercios > 5:
                                    logger.info(f"... y {cantidad_comercios - 5} comercios más")
                                
                                data_module.comercios = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de comercios")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            logger.warning("No se encontraron comercios")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de comercios exitosa")
                        data_module.comercios = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros - intentar sin parámetros
                logger.warning("Error de validación en parámetros de consulta de comercios")
                logger.info("Reintentando sin parámetros...")
                
                # Reintentar sin parámetros
                with client.get(
                    "/habilitaciones/comercios", 
                    catch_response=True,
                    name="(HABILITACIONES) - /habilitaciones/comercios [GET sin parámetros]"
                ) as retry_response:
                    if retry_response.status_code == 200:
                        try:
                            retry_data = retry_response.json()
                            logger.info("Consulta exitosa sin parámetros")
                            logger.info(f"Estructura de respuesta: {type(retry_data)}")
                            if isinstance(retry_data, list):
                                logger.info(f"Cantidad de comercios: {len(retry_data)}")
                            elif isinstance(retry_data, dict):
                                logger.info(f"Claves en respuesta: {list(retry_data.keys())}")
                            
                            response.success()
                            data_module.comercios = retry_data
                        except ValueError:
                            response.failure("Error al procesar respuesta sin parámetros")
                    else:
                        response.failure(f"Error incluso sin parámetros: {retry_response.status_code}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de comercios")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de comercios no encontrado")
                response.failure("Endpoint no encontrado")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de comercios: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de comercios: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/habilitaciones/comercios",
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/comercios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_geriatricos_privados(client, logger, environment, data_module):
    """Prueba el endpoint de obtener geriátricos privados habilitados de Córdoba"""
    
    logger.info("Ejecutando get_geriatricos_privados")
    
    try:
        with client.get(
            "/habilitaciones/geriatricos-privados", 
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/geriatricos-privados [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} geriátricos encontrados")
                    else:
                        logger.info(f"Respuesta recibida: {response.text[:100]}...")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info("=== RESUMEN DE LA RESPUESTA (GERIÁTRICOS PRIVADOS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_geriatricos = len(response_data)
                        logger.info(f"Se encontraron {cantidad_geriatricos} geriátricos privados")
                        
                        if cantidad_geriatricos > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de geriátricos
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "razon_social", "cuit", "direccion", "telefono", "email", "establecimiento"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de geriátricos privados exitosa")
                                
                                # Mostrar información de algunos geriátricos (hasta 5)
                                for idx, geriatrico in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in geriatrico:
                                        logger.info(f"Geriátrico {idx+1}: {geriatrico.get('nombre')}")
                                    elif "razon_social" in geriatrico:
                                        logger.info(f"Geriátrico {idx+1}: {geriatrico.get('razon_social')}")
                                    elif "establecimiento" in geriatrico:
                                        logger.info(f"Geriátrico {idx+1}: {geriatrico.get('establecimiento')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in geriatrico.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Geriátrico {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "cuit" in geriatrico and geriatrico.get("cuit"):
                                        logger.info(f"  CUIT: {geriatrico.get('cuit')}")
                                    if "direccion" in geriatrico and geriatrico.get("direccion"):
                                        logger.info(f"  Dirección: {geriatrico.get('direccion')}")
                                    if "telefono" in geriatrico and geriatrico.get("telefono"):
                                        logger.info(f"  Teléfono: {geriatrico.get('telefono')}")
                                    if "email" in geriatrico and geriatrico.get("email"):
                                        logger.info(f"  Email: {geriatrico.get('email')}")
                                
                                # Si hay más de 5 geriátricos, indicar cuántos más hay
                                if cantidad_geriatricos > 5:
                                    logger.info(f"... y {cantidad_geriatricos - 5} geriátricos más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.geriatricos_privados = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de geriátricos")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron geriátricos
                            logger.warning("No se encontraron geriátricos privados")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} geriátricos en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos geriátricos
                                for idx, geriatrico in enumerate(items[:5]):
                                    if "nombre" in geriatrico:
                                        logger.info(f"Geriátrico {idx+1}: {geriatrico.get('nombre')}")
                                    elif "razon_social" in geriatrico:
                                        logger.info(f"Geriátrico {idx+1}: {geriatrico.get('razon_social')}")
                                
                                data_module.geriatricos_privados = response_data
                        
                        response.success()
                        logger.info("Consulta de geriátricos privados exitosa")
                        data_module.geriatricos_privados = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de geriátricos privados")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de geriátricos privados no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de geriátricos privados")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de geriátricos privados: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de geriátricos privados: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/habilitaciones/geriatricos-privados",
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/geriatricos-privados [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_jardines_maternales_privados(client, logger, environment, data_module):
    """Prueba el endpoint de obtener jardines maternales privados habilitados de Córdoba"""
    
    logger.info("Ejecutando get_jardines_maternales_privados")
    
    try:
        with client.get(
            "/habilitaciones/jardines-maternales-privados", 
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/jardines-maternales-privados [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} jardines maternales encontrados")
                    else:
                        logger.info(f"Respuesta recibida: {response.text[:100]}...")
                except:
                    logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
            else:
                logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar un resumen de los datos obtenidos en el log
                    logger.info("=== RESUMEN DE LA RESPUESTA (JARDINES MATERNALES PRIVADOS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_jardines = len(response_data)
                        logger.info(f"Se encontraron {cantidad_jardines} jardines maternales privados")
                        
                        if cantidad_jardines > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de jardines maternales
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "razon_social", "cuit", "direccion", "telefono", "email", "establecimiento", "jardin"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de jardines maternales privados exitosa")
                                
                                # Mostrar información de algunos jardines (hasta 5)
                                for idx, jardin in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('nombre')}")
                                    elif "razon_social" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('razon_social')}")
                                    elif "establecimiento" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('establecimiento')}")
                                    elif "jardin" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('jardin')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in jardin.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Jardín Maternal {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "cuit" in jardin and jardin.get("cuit"):
                                        logger.info(f"  CUIT: {jardin.get('cuit')}")
                                    if "direccion" in jardin and jardin.get("direccion"):
                                        logger.info(f"  Dirección: {jardin.get('direccion')}")
                                    if "telefono" in jardin and jardin.get("telefono"):
                                        logger.info(f"  Teléfono: {jardin.get('telefono')}")
                                    if "email" in jardin and jardin.get("email"):
                                        logger.info(f"  Email: {jardin.get('email')}")
                                
                                # Si hay más de 5 jardines, indicar cuántos más hay
                                if cantidad_jardines > 5:
                                    logger.info(f"... y {cantidad_jardines - 5} jardines maternales más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.jardines_maternales_privados = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de jardines maternales")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron jardines maternales
                            logger.warning("No se encontraron jardines maternales privados")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} jardines maternales en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos jardines maternales
                                for idx, jardin in enumerate(items[:5]):
                                    if "nombre" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('nombre')}")
                                    elif "razon_social" in jardin:
                                        logger.info(f"Jardín Maternal {idx+1}: {jardin.get('razon_social')}")
                                
                                data_module.jardines_maternales_privados = response_data
                        
                        response.success()
                        logger.info("Consulta de jardines maternales privados exitosa")
                        data_module.jardines_maternales_privados = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de jardines maternales privados")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de jardines maternales privados no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de jardines maternales privados")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de jardines maternales privados: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de jardines maternales privados: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/habilitaciones/jardines-maternales-privados",
            catch_response=True,
            name="(HABILITACIONES) - /habilitaciones/jardines-maternales-privados [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")
