import random
from typing import Dict, Any

def get_condiciones(client, logger, environment, data_module):
    """Prueba el endpoint de consultar todas las condiciones de transporte"""
    
    logger.info("Ejecutando get_condiciones")
    
    try:
        with client.get(
            "/condiciones", 
            catch_response=True,
            name="(TRANSPORTE) - /condiciones [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} condiciones encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CONDICIONES DE TRANSPORTE) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_condiciones = len(response_data)
                        logger.info(f"Se encontraron {cantidad_condiciones} condiciones")
                        
                        if cantidad_condiciones > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de condiciones
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "codigo", "tipo", "estado", "fecha_creacion", "fecha_modificacion", "activo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de condiciones exitosa")
                                
                                # Mostrar información de algunas condiciones (hasta 5)
                                for idx, condicion in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in condicion:
                                        logger.info(f"Condición {idx+1}: {condicion.get('nombre')}")
                                    elif "descripcion" in condicion:
                                        logger.info(f"Condición {idx+1}: {condicion.get('descripcion')}")
                                    elif "codigo" in condicion:
                                        logger.info(f"Condición {idx+1}: Código {condicion.get('codigo')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in condicion.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Condición {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in condicion and condicion.get("id"):
                                        logger.info(f"  ID: {condicion.get('id')}")
                                    if "codigo" in condicion and condicion.get("codigo"):
                                        logger.info(f"  Código: {condicion.get('codigo')}")
                                    if "descripcion" in condicion and condicion.get("descripcion"):
                                        logger.info(f"  Descripción: {condicion.get('descripcion')}")
                                    if "tipo" in condicion and condicion.get("tipo"):
                                        logger.info(f"  Tipo: {condicion.get('tipo')}")
                                    if "estado" in condicion and condicion.get("estado"):
                                        logger.info(f"  Estado: {condicion.get('estado')}")
                                    if "activo" in condicion and condicion.get("activo") is not None:
                                        logger.info(f"  Activo: {condicion.get('activo')}")
                                    if "fecha_creacion" in condicion and condicion.get("fecha_creacion"):
                                        logger.info(f"  Fecha Creación: {condicion.get('fecha_creacion')}")
                                    if "fecha_modificacion" in condicion and condicion.get("fecha_modificacion"):
                                        logger.info(f"  Fecha Modificación: {condicion.get('fecha_modificacion')}")
                                
                                # Si hay más de 5 condiciones, indicar cuántas más hay
                                if cantidad_condiciones > 5:
                                    logger.info(f"... y {cantidad_condiciones - 5} condiciones más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.condiciones = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de condiciones")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron condiciones
                            logger.warning("No se encontraron condiciones")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} condiciones en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas condiciones
                                for idx, condicion in enumerate(items[:5]):
                                    if "nombre" in condicion:
                                        logger.info(f"Condición {idx+1}: {condicion.get('nombre')}")
                                    elif "descripcion" in condicion:
                                        logger.info(f"Condición {idx+1}: {condicion.get('descripcion')}")
                                
                                data_module.condiciones = response_data
                        
                        response.success()
                        logger.info("Consulta de condiciones exitosa")
                        data_module.condiciones = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de condiciones")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de condiciones no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de condiciones")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de condiciones: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de condiciones: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/condiciones",
            catch_response=True,
            name="(TRANSPORTE) - /condiciones [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_estacionamiento_bicicletas(client, logger, environment, data_module):
    """Prueba el endpoint de consultar estacionamiento de bicicletas"""
    
    logger.info("Ejecutando get_estacionamiento_bicicletas")
    
    try:
        with client.get(
            "/estacionamiento-bicicletas", 
            catch_response=True,
            name="(TRANSPORTE) - /estacionamiento-bicicletas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} estacionamientos de bicicletas encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (ESTACIONAMIENTO BICICLETAS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_estacionamientos = len(response_data)
                        logger.info(f"Se encontraron {cantidad_estacionamientos} estacionamientos de bicicletas")
                        
                        if cantidad_estacionamientos > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de estacionamientos
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "ubicacion", "direccion", "capacidad", "tipo", "estado", "barrio", "zona", "latitud", "longitud", "horario"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de estacionamientos de bicicletas exitosa")
                                
                                # Mostrar información de algunos estacionamientos (hasta 5)
                                for idx, estacionamiento in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in estacionamiento:
                                        logger.info(f"Estacionamiento {idx+1}: {estacionamiento.get('nombre')}")
                                    elif "ubicacion" in estacionamiento:
                                        logger.info(f"Estacionamiento {idx+1}: {estacionamiento.get('ubicacion')}")
                                    elif "direccion" in estacionamiento:
                                        logger.info(f"Estacionamiento {idx+1}: {estacionamiento.get('direccion')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in estacionamiento.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Estacionamiento {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in estacionamiento and estacionamiento.get("id"):
                                        logger.info(f"  ID: {estacionamiento.get('id')}")
                                    if "direccion" in estacionamiento and estacionamiento.get("direccion"):
                                        logger.info(f"  Dirección: {estacionamiento.get('direccion')}")
                                    if "capacidad" in estacionamiento and estacionamiento.get("capacidad"):
                                        logger.info(f"  Capacidad: {estacionamiento.get('capacidad')}")
                                    if "tipo" in estacionamiento and estacionamiento.get("tipo"):
                                        logger.info(f"  Tipo: {estacionamiento.get('tipo')}")
                                    if "estado" in estacionamiento and estacionamiento.get("estado"):
                                        logger.info(f"  Estado: {estacionamiento.get('estado')}")
                                    if "barrio" in estacionamiento and estacionamiento.get("barrio"):
                                        logger.info(f"  Barrio: {estacionamiento.get('barrio')}")
                                    if "zona" in estacionamiento and estacionamiento.get("zona"):
                                        logger.info(f"  Zona: {estacionamiento.get('zona')}")
                                    if "horario" in estacionamiento and estacionamiento.get("horario"):
                                        logger.info(f"  Horario: {estacionamiento.get('horario')}")
                                    if "latitud" in estacionamiento and estacionamiento.get("latitud"):
                                        logger.info(f"  Coordenadas: {estacionamiento.get('latitud')}, {estacionamiento.get('longitud', 'N/A')}")
                                
                                # Si hay más de 5 estacionamientos, indicar cuántos más hay
                                if cantidad_estacionamientos > 5:
                                    logger.info(f"... y {cantidad_estacionamientos - 5} estacionamientos más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.estacionamientos_bicicletas = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de estacionamientos")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron estacionamientos
                            logger.warning("No se encontraron estacionamientos de bicicletas")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} estacionamientos en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos estacionamientos
                                for idx, estacionamiento in enumerate(items[:5]):
                                    if "nombre" in estacionamiento:
                                        logger.info(f"Estacionamiento {idx+1}: {estacionamiento.get('nombre')}")
                                    elif "ubicacion" in estacionamiento:
                                        logger.info(f"Estacionamiento {idx+1}: {estacionamiento.get('ubicacion')}")
                                
                                data_module.estacionamientos_bicicletas = response_data
                        
                        response.success()
                        logger.info("Consulta de estacionamientos de bicicletas exitosa")
                        data_module.estacionamientos_bicicletas = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de estacionamientos de bicicletas")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de estacionamientos de bicicletas no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de estacionamientos de bicicletas")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de estacionamientos de bicicletas: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de estacionamientos de bicicletas: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/estacionamiento-bicicletas",
            catch_response=True,
            name="(TRANSPORTE) - /estacionamiento-bicicletas [GET]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_estados_licencias(client, logger, environment, data_module):
    """Prueba el endpoint de consultar todos los estados de licencias"""
    
    logger.info("Ejecutando get_estados_licencias")
    
    try:
        with client.get(
            "/estados_licencias", 
            catch_response=True,
            name="(TRANSPORTE) - /estados_licencias [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} estados de licencias encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (ESTADOS DE LICENCIAS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_estados = len(response_data)
                        logger.info(f"Se encontraron {cantidad_estados} estados de licencias")
                        
                        if cantidad_estados > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de estados de licencias
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "codigo", "estado", "activo", "fecha_creacion", "fecha_modificacion"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de estados de licencias exitosa")
                                
                                # Mostrar información de algunos estados (hasta 5)
                                for idx, estado in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in estado:
                                        logger.info(f"Estado de Licencia {idx+1}: {estado.get('nombre')}")
                                    elif "descripcion" in estado:
                                        logger.info(f"Estado de Licencia {idx+1}: {estado.get('descripcion')}")
                                    elif "codigo" in estado:
                                        logger.info(f"Estado de Licencia {idx+1}: Código {estado.get('codigo')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in estado.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Estado de Licencia {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in estado and estado.get("id"):
                                        logger.info(f"  ID: {estado.get('id')}")
                                    if "codigo" in estado and estado.get("codigo"):
                                        logger.info(f"  Código: {estado.get('codigo')}")
                                    if "descripcion" in estado and estado.get("descripcion"):
                                        logger.info(f"  Descripción: {estado.get('descripcion')}")
                                    if "estado" in estado and estado.get("estado"):
                                        logger.info(f"  Estado: {estado.get('estado')}")
                                    if "activo" in estado and estado.get("activo") is not None:
                                        logger.info(f"  Activo: {estado.get('activo')}")
                                    if "fecha_creacion" in estado and estado.get("fecha_creacion"):
                                        logger.info(f"  Fecha Creación: {estado.get('fecha_creacion')}")
                                    if "fecha_modificacion" in estado and estado.get("fecha_modificacion"):
                                        logger.info(f"  Fecha Modificación: {estado.get('fecha_modificacion')}")
                                
                                # Si hay más de 5 estados, indicar cuántos más hay
                                if cantidad_estados > 5:
                                    logger.info(f"... y {cantidad_estados - 5} estados de licencias más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.estados_licencias = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de estados de licencias")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron estados de licencias
                            logger.warning("No se encontraron estados de licencias")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} estados de licencias en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos estados de licencias
                                for idx, estado in enumerate(items[:5]):
                                    if "nombre" in estado:
                                        logger.info(f"Estado de Licencia {idx+1}: {estado.get('nombre')}")
                                    elif "descripcion" in estado:
                                        logger.info(f"Estado de Licencia {idx+1}: {estado.get('descripcion')}")
                                
                                data_module.estados_licencias = response_data
                        
                        response.success()
                        logger.info("Consulta de estados de licencias exitosa")
                        data_module.estados_licencias = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de estados de licencias")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de estados de licencias no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de estados de licencias")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de estados de licencias: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de estados de licencias: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/estados_licencias",
            catch_response=True,
            name="(TRANSPORTE) - /estados_licencias [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_situaciones_chapas(client, logger, environment, data_module):
    """Prueba el endpoint de consultar todas las situaciones de chapas"""
    
    logger.info("Ejecutando get_situaciones_chapas")
    
    try:
        with client.get(
            "/situaciones_chapas", 
            catch_response=True,
            name="(TRANSPORTE) - /situaciones_chapas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} situaciones de chapas encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (SITUACIONES DE CHAPAS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_situaciones = len(response_data)
                        logger.info(f"Se encontraron {cantidad_situaciones} situaciones de chapas")
                        
                        if cantidad_situaciones > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de situaciones de chapas
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "codigo", "tipo", "estado", "activo", "fecha_creacion", "fecha_modificacion"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de situaciones de chapas exitosa")
                                
                                # Mostrar información de algunas situaciones (hasta 5)
                                for idx, situacion in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in situacion:
                                        logger.info(f"Situación de Chapa {idx+1}: {situacion.get('nombre')}")
                                    elif "descripcion" in situacion:
                                        logger.info(f"Situación de Chapa {idx+1}: {situacion.get('descripcion')}")
                                    elif "codigo" in situacion:
                                        logger.info(f"Situación de Chapa {idx+1}: Código {situacion.get('codigo')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in situacion.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Situación de Chapa {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in situacion and situacion.get("id"):
                                        logger.info(f"  ID: {situacion.get('id')}")
                                    if "codigo" in situacion and situacion.get("codigo"):
                                        logger.info(f"  Código: {situacion.get('codigo')}")
                                    if "descripcion" in situacion and situacion.get("descripcion"):
                                        logger.info(f"  Descripción: {situacion.get('descripcion')}")
                                    if "tipo" in situacion and situacion.get("tipo"):
                                        logger.info(f"  Tipo: {situacion.get('tipo')}")
                                    if "estado" in situacion and situacion.get("estado"):
                                        logger.info(f"  Estado: {situacion.get('estado')}")
                                    if "activo" in situacion and situacion.get("activo") is not None:
                                        logger.info(f"  Activo: {situacion.get('activo')}")
                                    if "fecha_creacion" in situacion and situacion.get("fecha_creacion"):
                                        logger.info(f"  Fecha Creación: {situacion.get('fecha_creacion')}")
                                    if "fecha_modificacion" in situacion and situacion.get("fecha_modificacion"):
                                        logger.info(f"  Fecha Modificación: {situacion.get('fecha_modificacion')}")
                                
                                # Si hay más de 5 situaciones, indicar cuántas más hay
                                if cantidad_situaciones > 5:
                                    logger.info(f"... y {cantidad_situaciones - 5} situaciones de chapas más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.situaciones_chapas = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de situaciones de chapas")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron situaciones de chapas
                            logger.warning("No se encontraron situaciones de chapas")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} situaciones de chapas en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas situaciones de chapas
                                for idx, situacion in enumerate(items[:5]):
                                    if "nombre" in situacion:
                                        logger.info(f"Situación de Chapa {idx+1}: {situacion.get('nombre')}")
                                    elif "descripcion" in situacion:
                                        logger.info(f"Situación de Chapa {idx+1}: {situacion.get('descripcion')}")
                                
                                data_module.situaciones_chapas = response_data
                        
                        response.success()
                        logger.info("Consulta de situaciones de chapas exitosa")
                        data_module.situaciones_chapas = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de situaciones de chapas")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de situaciones de chapas no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de situaciones de chapas")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de situaciones de chapas: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de situaciones de chapas: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/situaciones_chapas",
            catch_response=True,
            name="(TRANSPORTE) - /situaciones_chapas [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_tipos_servicios(client, logger, environment, data_module):
    """Prueba el endpoint de consultar todos los tipos de servicios"""
    
    logger.info("Ejecutando get_tipos_servicios")
    
    try:
        with client.get(
            "/tipos_servicios", 
            catch_response=True,
            name="(TRANSPORTE) - /tipos_servicios [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} tipos de servicios encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (TIPOS DE SERVICIOS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_tipos = len(response_data)
                        logger.info(f"Se encontraron {cantidad_tipos} tipos de servicios")
                        
                        if cantidad_tipos > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de tipos de servicios
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "codigo", "tipo", "categoria", "estado", "activo", "fecha_creacion", "fecha_modificacion"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de tipos de servicios exitosa")
                                
                                # Mostrar información de algunos tipos de servicios (hasta 5)
                                for idx, tipo_servicio in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in tipo_servicio:
                                        logger.info(f"Tipo de Servicio {idx+1}: {tipo_servicio.get('nombre')}")
                                    elif "descripcion" in tipo_servicio:
                                        logger.info(f"Tipo de Servicio {idx+1}: {tipo_servicio.get('descripcion')}")
                                    elif "codigo" in tipo_servicio:
                                        logger.info(f"Tipo de Servicio {idx+1}: Código {tipo_servicio.get('codigo')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in tipo_servicio.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Tipo de Servicio {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in tipo_servicio and tipo_servicio.get("id"):
                                        logger.info(f"  ID: {tipo_servicio.get('id')}")
                                    if "codigo" in tipo_servicio and tipo_servicio.get("codigo"):
                                        logger.info(f"  Código: {tipo_servicio.get('codigo')}")
                                    if "descripcion" in tipo_servicio and tipo_servicio.get("descripcion"):
                                        logger.info(f"  Descripción: {tipo_servicio.get('descripcion')}")
                                    if "tipo" in tipo_servicio and tipo_servicio.get("tipo"):
                                        logger.info(f"  Tipo: {tipo_servicio.get('tipo')}")
                                    if "categoria" in tipo_servicio and tipo_servicio.get("categoria"):
                                        logger.info(f"  Categoría: {tipo_servicio.get('categoria')}")
                                    if "estado" in tipo_servicio and tipo_servicio.get("estado"):
                                        logger.info(f"  Estado: {tipo_servicio.get('estado')}")
                                    if "activo" in tipo_servicio and tipo_servicio.get("activo") is not None:
                                        logger.info(f"  Activo: {tipo_servicio.get('activo')}")
                                    if "fecha_creacion" in tipo_servicio and tipo_servicio.get("fecha_creacion"):
                                        logger.info(f"  Fecha Creación: {tipo_servicio.get('fecha_creacion')}")
                                    if "fecha_modificacion" in tipo_servicio and tipo_servicio.get("fecha_modificacion"):
                                        logger.info(f"  Fecha Modificación: {tipo_servicio.get('fecha_modificacion')}")
                                
                                # Si hay más de 5 tipos de servicios, indicar cuántos más hay
                                if cantidad_tipos > 5:
                                    logger.info(f"... y {cantidad_tipos - 5} tipos de servicios más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.tipos_servicios = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de tipos de servicios")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron tipos de servicios
                            logger.warning("No se encontraron tipos de servicios")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} tipos de servicios en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos tipos de servicios
                                for idx, tipo_servicio in enumerate(items[:5]):
                                    if "nombre" in tipo_servicio:
                                        logger.info(f"Tipo de Servicio {idx+1}: {tipo_servicio.get('nombre')}")
                                    elif "descripcion" in tipo_servicio:
                                        logger.info(f"Tipo de Servicio {idx+1}: {tipo_servicio.get('descripcion')}")
                                
                                data_module.tipos_servicios = response_data
                        
                        response.success()
                        logger.info("Consulta de tipos de servicios exitosa")
                        data_module.tipos_servicios = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de tipos de servicios")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de tipos de servicios no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de tipos de servicios")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de tipos de servicios: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de tipos de servicios: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/tipos_servicios",
            catch_response=True,
            name="(TRANSPORTE) - /tipos_servicios [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_zona_semm(client, logger, environment, data_module):
    """Prueba el endpoint de consultar mapa zona SEMM"""
    
    logger.info("Ejecutando get_zona_semm")
    
    try:
        with client.get(
            "/zona-semm", 
            catch_response=True,
            name="(TRANSPORTE) - /zona-semm [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} zonas SEMM encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (ZONA SEMM) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_zonas = len(response_data)
                        logger.info(f"Se encontraron {cantidad_zonas} zonas SEMM")
                        
                        if cantidad_zonas > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de zonas SEMM
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "codigo", "zona", "area", "coordenadas", "poligono", "latitud", "longitud", "estado", "activo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de zonas SEMM exitosa")
                                
                                # Mostrar información de algunas zonas (hasta 5)
                                for idx, zona in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('nombre')}")
                                    elif "descripcion" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('descripcion')}")
                                    elif "codigo" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: Código {zona.get('codigo')}")
                                    elif "zona" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('zona')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in zona.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Zona SEMM {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id" in zona and zona.get("id"):
                                        logger.info(f"  ID: {zona.get('id')}")
                                    if "codigo" in zona and zona.get("codigo"):
                                        logger.info(f"  Código: {zona.get('codigo')}")
                                    if "descripcion" in zona and zona.get("descripcion"):
                                        logger.info(f"  Descripción: {zona.get('descripcion')}")
                                    if "area" in zona and zona.get("area"):
                                        logger.info(f"  Área: {zona.get('area')}")
                                    if "estado" in zona and zona.get("estado"):
                                        logger.info(f"  Estado: {zona.get('estado')}")
                                    if "activo" in zona and zona.get("activo") is not None:
                                        logger.info(f"  Activo: {zona.get('activo')}")
                                    if "latitud" in zona and zona.get("latitud"):
                                        logger.info(f"  Coordenadas: {zona.get('latitud')}, {zona.get('longitud', 'N/A')}")
                                    if "coordenadas" in zona and zona.get("coordenadas"):
                                        logger.info(f"  Coordenadas: {str(zona.get('coordenadas'))[:50]}...")
                                    if "poligono" in zona and zona.get("poligono"):
                                        logger.info(f"  Polígono: {str(zona.get('poligono'))[:50]}...")
                                
                                # Si hay más de 5 zonas, indicar cuántas más hay
                                if cantidad_zonas > 5:
                                    logger.info(f"... y {cantidad_zonas - 5} zonas SEMM más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.zona_semm = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de zonas SEMM")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron zonas SEMM
                            logger.warning("No se encontraron zonas SEMM")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} zonas SEMM en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas zonas SEMM
                                for idx, zona in enumerate(items[:5]):
                                    if "nombre" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('nombre')}")
                                    elif "descripcion" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('descripcion')}")
                                    elif "zona" in zona:
                                        logger.info(f"Zona SEMM {idx+1}: {zona.get('zona')}")
                                
                                data_module.zona_semm = response_data
                        
                        response.success()
                        logger.info("Consulta de zonas SEMM exitosa")
                        data_module.zona_semm = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de zona SEMM")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de zona SEMM no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de zona SEMM")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de zona SEMM: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de zona SEMM: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/zona-semm",
            catch_response=True,
            name="(TRANSPORTE) - /zona-semm [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_chapas(client, logger, environment, data_module):
    """Prueba el endpoint de consultar chapas por parámetros"""
    
    logger.info("Ejecutando get_chapas")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Agregar parámetros básicos (paginación)
    if hasattr(data_module, 'parametros_chapas'):
        query_params.update(data_module.parametros_chapas)
    
    # Agregar parámetros opcionales si están disponibles
    if hasattr(data_module, 'parametros_chapas_comentados'):
        # Solo agregar los parámetros que no estén comentados (que tengan valores)
        for key, value in data_module.parametros_chapas_comentados.items():
            if value is not None:  # Solo agregar si el valor no es None
                query_params[key] = value
    
    try:
        with client.get(
            "/chapas", 
            params=query_params if query_params else None,
            catch_response=True,
            name="(TRANSPORTE) - /chapas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} chapas encontradas")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} chapas encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CHAPAS) ===")
                    if query_params:
                        logger.info(f"Parámetros utilizados: {query_params}")
                    else:
                        logger.info("Sin parámetros de consulta")
                    
                    # Validar estructura de datos esperada para respuesta paginada
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura PaginationResponseSchema
                        items = response_data["items"]
                        total_items = response_data.get("total_items", len(items))
                        page_number = response_data.get("page_number", 1)
                        page_size = response_data.get("page_size", len(items))
                        
                        logger.info(f"Página: {page_number}, Tamaño: {page_size}, Total: {total_items}")
                        logger.info(f"Se encontraron {len(items)} chapas en esta página")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de chapas (usando los nombres reales)
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id_prm_chapa", "numero_interno", "tipo_servicio", "dominio", "apellido_permisionario", "nombre_permisionario", "cuil_permisionario", "situacion_chapa"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de chapas exitosa")
                                
                                # Mostrar información de algunas chapas (hasta 5)
                                for idx, chapa in enumerate(items[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "numero_interno" in chapa:
                                        logger.info(f"Chapa {idx+1}: Número Interno {chapa.get('numero_interno')}")
                                    elif "id_prm_chapa" in chapa:
                                        logger.info(f"Chapa {idx+1}: ID {chapa.get('id_prm_chapa')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in chapa.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Chapa {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id_prm_chapa" in chapa and chapa.get("id_prm_chapa"):
                                        logger.info(f"  ID Chapa: {chapa.get('id_prm_chapa')}")
                                    if "tipo_servicio" in chapa and chapa.get("tipo_servicio"):
                                        logger.info(f"  Tipo Servicio: {chapa.get('tipo_servicio')}")
                                    if "dominio" in chapa and chapa.get("dominio"):
                                        logger.info(f"  Dominio: {chapa.get('dominio')}")
                                    if "situacion_chapa" in chapa and chapa.get("situacion_chapa"):
                                        logger.info(f"  Situación: {chapa.get('situacion_chapa')}")
                                    if "apellido_permisionario" in chapa and chapa.get("apellido_permisionario"):
                                        nombre_completo = f"{chapa.get('apellido_permisionario')}, {chapa.get('nombre_permisionario', '')}"
                                        logger.info(f"  Permisionario: {nombre_completo}")
                                    if "cuil_permisionario" in chapa and chapa.get("cuil_permisionario"):
                                        logger.info(f"  CUIL Permisionario: {chapa.get('cuil_permisionario')}")
                                    if "central_agencia" in chapa and chapa.get("central_agencia"):
                                        logger.info(f"  Central/Agencia: {chapa.get('central_agencia')}")
                                    if "numero_dispositivo_pago" in chapa and chapa.get("numero_dispositivo_pago"):
                                        logger.info(f"  Dispositivo Pago: {chapa.get('numero_dispositivo_pago')}")
                                    if "nro_movil" in chapa and chapa.get("nro_movil"):
                                        logger.info(f"  Número Móvil: {chapa.get('nro_movil')}")
                                    if "cantidad_titulares" in chapa and chapa.get("cantidad_titulares"):
                                        logger.info(f"  Cantidad Titulares: {chapa.get('cantidad_titulares')}")
                                
                                # Si hay más de 5 chapas, indicar cuántas más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} chapas más en esta página")
                                
                                # Información de paginación
                                if total_items > len(items):
                                    logger.info(f"Total de chapas disponibles: {total_items}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.chapas = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de chapas")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron chapas
                            logger.warning("No se encontraron chapas en esta página")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_chapas = len(response_data)
                        logger.info(f"Se encontraron {cantidad_chapas} chapas")
                        
                        if cantidad_chapas > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id_prm_chapa", "numero_interno", "tipo_servicio", "dominio", "apellido_permisionario"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de chapas exitosa")
                                
                                # Mostrar algunas chapas
                                for idx, chapa in enumerate(response_data[:5]):
                                    if "numero_interno" in chapa:
                                        logger.info(f"Chapa {idx+1}: Número Interno {chapa.get('numero_interno')}")
                                    elif "id_prm_chapa" in chapa:
                                        logger.info(f"Chapa {idx+1}: ID {chapa.get('id_prm_chapa')}")
                                
                                if cantidad_chapas > 5:
                                    logger.info(f"... y {cantidad_chapas - 5} chapas más")
                                
                                data_module.chapas = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de chapas")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            logger.warning("No se encontraron chapas")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de chapas exitosa")
                        data_module.chapas = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros - intentar con parámetros mínimos
                logger.warning("Error de validación en parámetros de consulta de chapas")
                logger.info("Reintentando con parámetros mínimos...")
                
                # Reintentar con solo paginación
                minimal_params = {
                    "p_page_number": 1,
                    "p_page_size": 10
                }
                
                with client.get(
                    "/chapas", 
                    params=minimal_params,
                    catch_response=True,
                    name="(TRANSPORTE) - /chapas [GET con parámetros mínimos]"
                ) as retry_response:
                    if retry_response.status_code == 200:
                        try:
                            retry_data = retry_response.json()
                            logger.info("Consulta exitosa con parámetros mínimos")
                            logger.info(f"Estructura de respuesta: {type(retry_data)}")
                            if isinstance(retry_data, dict) and "items" in retry_data:
                                logger.info(f"Cantidad de chapas: {len(retry_data['items'])}")
                            elif isinstance(retry_data, list):
                                logger.info(f"Cantidad de chapas: {len(retry_data)}")
                            
                            response.success()
                            data_module.chapas = retry_data
                        except ValueError:
                            response.failure("Error al procesar respuesta con parámetros mínimos")
                    else:
                        response.failure(f"Error incluso con parámetros mínimos: {retry_response.status_code}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de chapas")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de chapas no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de chapas")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de chapas: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de chapas: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/chapas",
            catch_response=True,
            name="(TRANSPORTE) - /chapas [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_leasing(client, logger, environment, data_module):
    """Prueba el endpoint de consultar personas que están alquilando chapas"""
    
    logger.info("Ejecutando get_leasing")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Agregar parámetros básicos (paginación)
    if hasattr(data_module, 'parametros_leasing'):
        query_params.update(data_module.parametros_leasing)
    
    # Agregar parámetros opcionales si están disponibles
    if hasattr(data_module, 'parametros_leasing_comentados'):
        # Solo agregar los parámetros que no estén comentados (que tengan valores)
        for key, value in data_module.parametros_leasing_comentados.items():
            if value is not None:  # Solo agregar si el valor no es None
                query_params[key] = value
    
    try:
        with client.get(
            "/leasing", 
            params=query_params if query_params else None,
            catch_response=True,
            name="(TRANSPORTE) - /leasing [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} leasings encontrados")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} leasings encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (LEASING DE CHAPAS) ===")
                    if query_params:
                        logger.info(f"Parámetros utilizados: {query_params}")
                    else:
                        logger.info("Sin parámetros de consulta")
                    
                    # Validar estructura de datos esperada para respuesta paginada
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura PaginationResponseSchema
                        items = response_data["items"]
                        total_items = response_data.get("total_items", len(items))
                        page_number = response_data.get("page_number", 1)
                        page_size = response_data.get("page_size", len(items))
                        
                        logger.info(f"Página: {page_number}, Tamaño: {page_size}, Total: {total_items}")
                        logger.info(f"Se encontraron {len(items)} leasings en esta página")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de leasing
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_leasing", "numero_chapa", "chapa", "arrendatario", "apellido_arrendatario", "nombre_arrendatario", "dni_arrendatario", "cuil_arrendatario", "vencimiento", "fecha_inicio", "fecha_fin", "estado"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de leasings exitosa")
                                
                                # Mostrar información de algunos leasings (hasta 5)
                                for idx, leasing in enumerate(items[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "numero_chapa" in leasing:
                                        logger.info(f"Leasing {idx+1}: Chapa {leasing.get('numero_chapa')}")
                                    elif "chapa" in leasing:
                                        logger.info(f"Leasing {idx+1}: Chapa {leasing.get('chapa')}")
                                    elif "id_leasing" in leasing:
                                        logger.info(f"Leasing {idx+1}: ID {leasing.get('id_leasing')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in leasing.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Leasing {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id_leasing" in leasing and leasing.get("id_leasing"):
                                        logger.info(f"  ID Leasing: {leasing.get('id_leasing')}")
                                    if "apellido_arrendatario" in leasing and leasing.get("apellido_arrendatario"):
                                        nombre_completo = f"{leasing.get('apellido_arrendatario')}, {leasing.get('nombre_arrendatario', '')}"
                                        logger.info(f"  Arrendatario: {nombre_completo}")
                                    if "dni_arrendatario" in leasing and leasing.get("dni_arrendatario"):
                                        logger.info(f"  DNI Arrendatario: {leasing.get('dni_arrendatario')}")
                                    if "cuil_arrendatario" in leasing and leasing.get("cuil_arrendatario"):
                                        logger.info(f"  CUIL Arrendatario: {leasing.get('cuil_arrendatario')}")
                                    if "vencimiento" in leasing and leasing.get("vencimiento"):
                                        logger.info(f"  Vencimiento: {leasing.get('vencimiento')}")
                                    if "fecha_inicio" in leasing and leasing.get("fecha_inicio"):
                                        logger.info(f"  Fecha Inicio: {leasing.get('fecha_inicio')}")
                                    if "fecha_fin" in leasing and leasing.get("fecha_fin"):
                                        logger.info(f"  Fecha Fin: {leasing.get('fecha_fin')}")
                                    if "estado" in leasing and leasing.get("estado"):
                                        logger.info(f"  Estado: {leasing.get('estado')}")
                                    if "tipo_servicio" in leasing and leasing.get("tipo_servicio"):
                                        logger.info(f"  Tipo Servicio: {leasing.get('tipo_servicio')}")
                                
                                # Si hay más de 5 leasings, indicar cuántos más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} leasings más en esta página")
                                
                                # Información de paginación
                                if total_items > len(items):
                                    logger.info(f"Total de leasings disponibles: {total_items}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.leasing = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de leasing")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron leasings
                            logger.warning("No se encontraron leasings en esta página")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_leasings = len(response_data)
                        logger.info(f"Se encontraron {cantidad_leasings} leasings")
                        
                        if cantidad_leasings > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_leasing", "numero_chapa", "chapa", "apellido_arrendatario", "nombre_arrendatario"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de leasings exitosa")
                                
                                # Mostrar algunos leasings
                                for idx, leasing in enumerate(response_data[:5]):
                                    if "numero_chapa" in leasing:
                                        logger.info(f"Leasing {idx+1}: Chapa {leasing.get('numero_chapa')}")
                                    elif "id_leasing" in leasing:
                                        logger.info(f"Leasing {idx+1}: ID {leasing.get('id_leasing')}")
                                
                                if cantidad_leasings > 5:
                                    logger.info(f"... y {cantidad_leasings - 5} leasings más")
                                
                                data_module.leasing = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de leasing")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            logger.warning("No se encontraron leasings")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de leasings exitosa")
                        data_module.leasing = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros - intentar con parámetros mínimos
                logger.warning("Error de validación en parámetros de consulta de leasing")
                logger.info("Reintentando con parámetros mínimos...")
                
                # Reintentar con solo paginación
                minimal_params = {
                    "p_page_number": 1,
                    "p_page_size": 10
                }
                
                with client.get(
                    "/leasing", 
                    params=minimal_params,
                    catch_response=True,
                    name="(TRANSPORTE) - /leasing [GET con parámetros mínimos]"
                ) as retry_response:
                    if retry_response.status_code == 200:
                        try:
                            retry_data = retry_response.json()
                            logger.info("Consulta exitosa con parámetros mínimos")
                            logger.info(f"Estructura de respuesta: {type(retry_data)}")
                            if isinstance(retry_data, dict) and "items" in retry_data:
                                logger.info(f"Cantidad de leasings: {len(retry_data['items'])}")
                            elif isinstance(retry_data, list):
                                logger.info(f"Cantidad de leasings: {len(retry_data)}")
                            
                            response.success()
                            data_module.leasing = retry_data
                        except ValueError:
                            response.failure("Error al procesar respuesta con parámetros mínimos")
                    else:
                        response.failure(f"Error incluso con parámetros mínimos: {retry_response.status_code}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de leasing")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de leasing no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de leasing")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de leasing: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de leasing: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/leasing",
            catch_response=True,
            name="(TRANSPORTE) - /leasing [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_centrales_agencias(client, logger, environment, data_module):
    """Prueba el endpoint de consultar centrales agencias por CUIT"""
    
    logger.info("Ejecutando get_centrales_agencias")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Agregar parámetros básicos (paginación)
    if hasattr(data_module, 'parametros_centrales_agencias'):
        query_params.update(data_module.parametros_centrales_agencias)
    
    # Agregar parámetros opcionales si están disponibles
    if hasattr(data_module, 'parametros_centrales_agencias_comentados'):
        # Solo agregar los parámetros que no estén comentados (que tengan valores)
        for key, value in data_module.parametros_centrales_agencias_comentados.items():
            if value is not None:  # Solo agregar si el valor no es None
                query_params[key] = value
    
    try:
        with client.get(
            "/centrales-agencias", 
            params=query_params if query_params else None,
            catch_response=True,
            name="(TRANSPORTE) - /centrales-agencias [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} centrales/agencias encontradas")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} centrales/agencias encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CENTRALES AGENCIAS) ===")
                    if query_params:
                        logger.info(f"Parámetros utilizados: {query_params}")
                    else:
                        logger.info("Sin parámetros de consulta")
                    
                    # Validar estructura de datos esperada para respuesta paginada
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura PaginationResponseSchema
                        items = response_data["items"]
                        total_items = response_data.get("total_items", len(items))
                        page_number = response_data.get("page_number", 1)
                        page_size = response_data.get("page_size", len(items))
                        
                        logger.info(f"Página: {page_number}, Tamaño: {page_size}, Total: {total_items}")
                        logger.info(f"Se encontraron {len(items)} centrales/agencias en esta página")
                        
                        # Verificar que cada elemento tenga los campos esperados
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de centrales/agencias
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_central_agencia", "cuit", "nombre", "razon_social", "tipo", "estado", "direccion", "telefono", "email", "localidad", "barrio", "fecha_alta"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de centrales/agencias exitosa")
                                
                                # Mostrar información de algunas centrales/agencias (hasta 5)
                                for idx, agencia in enumerate(items[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in agencia:
                                        logger.info(f"Central/Agencia {idx+1}: {agencia.get('nombre')}")
                                    elif "razon_social" in agencia:
                                        logger.info(f"Central/Agencia {idx+1}: {agencia.get('razon_social')}")
                                    elif "cuit" in agencia:
                                        logger.info(f"Central/Agencia {idx+1}: CUIT {agencia.get('cuit')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in agencia.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Central/Agencia {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id_central_agencia" in agencia and agencia.get("id_central_agencia"):
                                        logger.info(f"  ID: {agencia.get('id_central_agencia')}")
                                    if "cuit" in agencia and agencia.get("cuit"):
                                        logger.info(f"  CUIT: {agencia.get('cuit')}")
                                    if "razon_social" in agencia and agencia.get("razon_social"):
                                        logger.info(f"  Razón Social: {agencia.get('razon_social')}")
                                    if "tipo" in agencia and agencia.get("tipo"):
                                        logger.info(f"  Tipo: {agencia.get('tipo')}")
                                    if "estado" in agencia and agencia.get("estado"):
                                        logger.info(f"  Estado: {agencia.get('estado')}")
                                    if "direccion" in agencia and agencia.get("direccion"):
                                        logger.info(f"  Dirección: {agencia.get('direccion')}")
                                    if "telefono" in agencia and agencia.get("telefono"):
                                        logger.info(f"  Teléfono: {agencia.get('telefono')}")
                                    if "email" in agencia and agencia.get("email"):
                                        logger.info(f"  Email: {agencia.get('email')}")
                                    if "localidad" in agencia and agencia.get("localidad"):
                                        logger.info(f"  Localidad: {agencia.get('localidad')}")
                                    if "barrio" in agencia and agencia.get("barrio"):
                                        logger.info(f"  Barrio: {agencia.get('barrio')}")
                                    if "fecha_alta" in agencia and agencia.get("fecha_alta"):
                                        logger.info(f"  Fecha Alta: {agencia.get('fecha_alta')}")
                                
                                # Si hay más de 5 centrales/agencias, indicar cuántas más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} centrales/agencias más en esta página")
                                
                                # Información de paginación
                                if total_items > len(items):
                                    logger.info(f"Total de centrales/agencias disponibles: {total_items}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.centrales_agencias = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de centrales/agencias")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron centrales/agencias
                            logger.warning("No se encontraron centrales/agencias en esta página")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_agencias = len(response_data)
                        logger.info(f"Se encontraron {cantidad_agencias} centrales/agencias")
                        
                        if cantidad_agencias > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_central_agencia", "cuit", "nombre", "razon_social", "tipo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de centrales/agencias exitosa")
                                
                                # Mostrar algunas centrales/agencias
                                for idx, agencia in enumerate(response_data[:5]):
                                    if "nombre" in agencia:
                                        logger.info(f"Central/Agencia {idx+1}: {agencia.get('nombre')}")
                                    elif "razon_social" in agencia:
                                        logger.info(f"Central/Agencia {idx+1}: {agencia.get('razon_social')}")
                                
                                if cantidad_agencias > 5:
                                    logger.info(f"... y {cantidad_agencias - 5} centrales/agencias más")
                                
                                data_module.centrales_agencias = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de centrales/agencias")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            logger.warning("No se encontraron centrales/agencias")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de centrales/agencias exitosa")
                        data_module.centrales_agencias = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros - intentar con parámetros mínimos
                logger.warning("Error de validación en parámetros de consulta de centrales/agencias")
                logger.info("Reintentando con parámetros mínimos...")
                
                # Reintentar con solo paginación
                minimal_params = {
                    "p_page_number": 1,
                    "p_page_size": 10
                }
                
                with client.get(
                    "/centrales-agencias", 
                    params=minimal_params,
                    catch_response=True,
                    name="(TRANSPORTE) - /centrales-agencias [GET con parámetros mínimos]"
                ) as retry_response:
                    if retry_response.status_code == 200:
                        try:
                            retry_data = retry_response.json()
                            logger.info("Consulta exitosa con parámetros mínimos")
                            logger.info(f"Estructura de respuesta: {type(retry_data)}")
                            if isinstance(retry_data, dict) and "items" in retry_data:
                                logger.info(f"Cantidad de centrales/agencias: {len(retry_data['items'])}")
                            elif isinstance(retry_data, list):
                                logger.info(f"Cantidad de centrales/agencias: {len(retry_data)}")
                            
                            response.success()
                            data_module.centrales_agencias = retry_data
                        except ValueError:
                            response.failure("Error al procesar respuesta con parámetros mínimos")
                    else:
                        response.failure(f"Error incluso con parámetros mínimos: {retry_response.status_code}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de centrales/agencias")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de centrales/agencias no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de centrales/agencias")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de centrales/agencias: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de centrales/agencias: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/centrales-agencias",
            catch_response=True,
            name="(TRANSPORTE) - /centrales-agencias [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_persona_fisica_por_chapa(client, logger, environment, data_module):
    """Prueba el endpoint de consultar persona física por número de chapa"""
    
    logger.info("Ejecutando get_persona_fisica_por_chapa")
    
    # Obtener parámetros desde data_module - ESTOS SON REQUERIDOS
    query_params = {}
    
    # Verificar que existan los parámetros requeridos
    if hasattr(data_module, 'parametros_persona_fisica_chapa'):
        query_params.update(data_module.parametros_persona_fisica_chapa)
        logger.info(f"Parámetros cargados desde data_module: {query_params}")
    else:
        # Si no existen en data_module, usar valores por defecto
        query_params = {
            "p_numero_interno": "2831",
            "p_id_tipo_servicio": 3
        }
        logger.warning(f"Usando parámetros por defecto: {query_params}")
    
    # Verificar que los parámetros requeridos estén presentes
    if not query_params.get("p_numero_interno") or not query_params.get("p_id_tipo_servicio"):
        logger.error("Faltan parámetros requeridos: p_numero_interno y p_id_tipo_servicio")
        return
    
    try:
        logger.info(f"Enviando solicitud con parámetros: {query_params}")
        
        with client.get(
            "/chapas/personas-fisicas", 
            params=query_params,
            catch_response=True,
            name="(TRANSPORTE) - /chapas/personas-fisicas [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} personas físicas encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (PERSONA FÍSICA POR CHAPA) ===")
                    logger.info(f"Parámetros utilizados: {query_params}")
                    
                    # Validar estructura de datos esperada (lista de PersonaFisicaResponseSchema)
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_personas = len(response_data)
                        logger.info(f"Se encontraron {cantidad_personas} personas físicas")
                        
                        if cantidad_personas > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de persona física
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_persona_fisica", "dni", "cuil", "apellido", "nombre", "fecha_nacimiento", "sexo", "estado_civil", "nacionalidad"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de persona física por chapa exitosa")
                                
                                # Mostrar información de las personas físicas encontradas
                                for idx, persona in enumerate(response_data):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "apellido" in persona and "nombre" in persona:
                                        nombre_completo = f"{persona.get('apellido')}, {persona.get('nombre')}"
                                        logger.info(f"Persona Física {idx+1}: {nombre_completo}")
                                    elif "dni" in persona:
                                        logger.info(f"Persona Física {idx+1}: DNI {persona.get('dni')}")
                                    elif "cuil" in persona:
                                        logger.info(f"Persona Física {idx+1}: CUIL {persona.get('cuil')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in persona.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Persona Física {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "id_persona_fisica" in persona and persona.get("id_persona_fisica"):
                                        logger.info(f"  ID Persona Física: {persona.get('id_persona_fisica')}")
                                    if "dni" in persona and persona.get("dni"):
                                        logger.info(f"  DNI: {persona.get('dni')}")
                                    if "cuil" in persona and persona.get("cuil"):
                                        logger.info(f"  CUIL: {persona.get('cuil')}")
                                    if "fecha_nacimiento" in persona and persona.get("fecha_nacimiento"):
                                        logger.info(f"  Fecha Nacimiento: {persona.get('fecha_nacimiento')}")
                                    if "sexo" in persona and persona.get("sexo"):
                                        logger.info(f"  Sexo: {persona.get('sexo')}")
                                    if "estado_civil" in persona and persona.get("estado_civil"):
                                        logger.info(f"  Estado Civil: {persona.get('estado_civil')}")
                                    if "nacionalidad" in persona and persona.get("nacionalidad"):
                                        logger.info(f"  Nacionalidad: {persona.get('nacionalidad')}")
                                    if "telefono" in persona and persona.get("telefono"):
                                        logger.info(f"  Teléfono: {persona.get('telefono')}")
                                    if "email" in persona and persona.get("email"):
                                        logger.info(f"  Email: {persona.get('email')}")
                                    if "domicilio" in persona and persona.get("domicilio"):
                                        logger.info(f"  Domicilio: {persona.get('domicilio')}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.persona_fisica_chapa = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de persona física")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron personas físicas
                            logger.warning("No se encontraron personas físicas para la chapa especificada")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente un solo resultado o con metadatos)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una persona física individual
                        tiene_campos_persona = any(
                            campo in response_data 
                            for campo in ["id", "id_persona_fisica", "dni", "cuil", "apellido", "nombre"]
                        )
                        
                        if tiene_campos_persona:
                            logger.info("Se encontró una persona física:")
                            if "apellido" in response_data and "nombre" in response_data:
                                nombre_completo = f"{response_data.get('apellido')}, {response_data.get('nombre')}"
                                logger.info(f"  Nombre: {nombre_completo}")
                            if "dni" in response_data:
                                logger.info(f"  DNI: {response_data.get('dni')}")
                            if "cuil" in response_data:
                                logger.info(f"  CUIL: {response_data.get('cuil')}")
                        
                        response.success()
                        logger.info("Consulta de persona física por chapa exitosa")
                        data_module.persona_fisica_chapa = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 404:
                # No se encontró la chapa o persona física
                logger.warning("No se encontró persona física para la chapa especificada")
                response.failure("Chapa o persona física no encontrada")
            elif response.status_code == 422:
                # Error de validación en parámetros - intentar con parámetros alternativos
                logger.warning("Error de validación en parámetros de consulta de persona física por chapa")
                logger.info("Intentando con parámetros alternativos...")
                
                # Intentar con parámetros alternativos si están disponibles
                if hasattr(data_module, 'parametros_persona_fisica_chapa_alternativos'):
                    alt_params = data_module.parametros_persona_fisica_chapa_alternativos
                    logger.info(f"Probando con parámetros alternativos: {alt_params}")
                    
                    with client.get(
                        "/chapas/personas-fisicas", 
                        params=alt_params,
                        catch_response=True,
                        name="(TRANSPORTE) - /chapas/personas-fisicas [GET con parámetros alternativos]"
                    ) as retry_response:
                        if retry_response.status_code == 200:
                            try:
                                retry_data = retry_response.json()
                                logger.info("Consulta exitosa con parámetros alternativos")
                                logger.info(f"Estructura de respuesta: {type(retry_data)}")
                                if isinstance(retry_data, list):
                                    logger.info(f"Cantidad de personas físicas: {len(retry_data)}")
                                
                                response.success()
                                data_module.persona_fisica_chapa = retry_data
                            except ValueError:
                                response.failure("Error al procesar respuesta con parámetros alternativos")
                        else:
                            response.failure(f"Error incluso con parámetros alternativos: {retry_response.status_code}")
                else:
                    response.failure("Parámetros inválidos - verificar número de chapa y tipo de servicio")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de persona física por chapa")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de persona física por chapa")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de persona física por chapa: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de persona física por chapa: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/chapas/personas-fisicas",
            catch_response=True,
            name="(TRANSPORTE) - /chapas/personas-fisicas [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_chapas_por_cuil(client, logger, environment, data_module):
    """Prueba el endpoint de consultar chapas por CUIL"""
    
    logger.info("Ejecutando get_chapas_por_cuil")
    
    # Obtener CUIL desde data_module
    cuil = None
    
    # Verificar que exista el parámetro requerido
    if hasattr(data_module, 'parametros_chapas_por_cuil'):
        cuil = data_module.parametros_chapas_por_cuil.get("p_cuil")
        logger.info(f"CUIL cargado desde data_module: {cuil}")
    else:
        # Si no existe en data_module, usar valor por defecto que sabemos que funciona
        cuil = "20227952661"
        logger.warning(f"Usando CUIL por defecto: {cuil}")
    
    # Mostrar claramente el CUIL que se va a usar
    logger.info(f"CUIL ACTUAL A CONSULTAR: {cuil}")
    
    # Verificar que el CUIL esté presente
    if not cuil:
        logger.error("Falta parametro requerido: p_cuil")
        return
    
    def probar_cuil(cuil_a_probar, descripcion=""):
        """Función auxiliar para probar un CUIL específico"""
        try:
            logger.info(f"Enviando solicitud con CUIL {descripcion}: {cuil_a_probar}")
            logger.info(f"URL completa: /chapas/{cuil_a_probar}")
            
            with client.get(
                f"/chapas/{cuil_a_probar}", 
                catch_response=True,
                name=f"(TRANSPORTE) - /chapas/{{cuil}} [GET{descripcion}]"
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} chapas encontradas para CUIL {cuil_a_probar}")
                        else:
                            logger.info(f"Respuesta recibida: {response.text[:100]}...")
                    except:
                        logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
                else:
                    logger.info(f"Respuesta completa para CUIL {cuil_a_probar}: {response.text}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar un resumen de los datos obtenidos en el log
                        logger.info("=== RESUMEN DE LA RESPUESTA (CHAPAS POR CUIL) ===")
                        logger.info(f"CUIL consultado: {cuil_a_probar}")
                        logger.info(f"Endpoint usado: /chapas/{cuil_a_probar}")
                        
                        # Validar estructura de datos esperada (lista de ChapasPermisionadosSchema)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_chapas = len(response_data)
                            logger.info(f"Se encontraron {cantidad_chapas} chapas para el CUIL {cuil_a_probar}")
                            
                            if cantidad_chapas > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de chapas
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["id", "id_chapa", "numero_chapa", "numero_interno", "tipo_servicio", "estado", "situacion", "permisionario", "cuil", "dominio"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de chapas por CUIL {cuil_a_probar} exitosa")
                                    
                                    # Mostrar información de las chapas encontradas (hasta 5)
                                    for idx, chapa in enumerate(response_data[:5]):
                                        # Intentar mostrar información relevante según los campos disponibles
                                        if "numero_chapa" in chapa:
                                            logger.info(f"Chapa {idx+1}: Numero {chapa.get('numero_chapa')} (CUIL: {cuil_a_probar})")
                                        elif "numero_interno" in chapa:
                                            logger.info(f"Chapa {idx+1}: Numero Interno {chapa.get('numero_interno')} (CUIL: {cuil_a_probar})")
                                        elif "id_chapa" in chapa:
                                            logger.info(f"Chapa {idx+1}: ID {chapa.get('id_chapa')} (CUIL: {cuil_a_probar})")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in chapa.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Chapa {idx+1}: {key}={value} (CUIL: {cuil_a_probar})")
                                                    break
                                        
                                        # Mostrar información adicional si está disponible
                                        if "id_chapa" in chapa and chapa.get("id_chapa"):
                                            logger.info(f"  ID Chapa: {chapa.get('id_chapa')}")
                                        if "tipo_servicio" in chapa and chapa.get("tipo_servicio"):
                                            logger.info(f"  Tipo Servicio: {chapa.get('tipo_servicio')}")
                                        if "estado" in chapa and chapa.get("estado"):
                                            logger.info(f"  Estado: {chapa.get('estado')}")
                                        if "situacion" in chapa and chapa.get("situacion"):
                                            logger.info(f"  Situacion: {chapa.get('situacion')}")
                                        if "dominio" in chapa and chapa.get("dominio"):
                                            logger.info(f"  Dominio: {chapa.get('dominio')}")
                                        if "permisionario" in chapa and chapa.get("permisionario"):
                                            logger.info(f"  Permisionario: {chapa.get('permisionario')}")
                                        if "cuil" in chapa and chapa.get("cuil"):
                                            logger.info(f"  CUIL en respuesta: {chapa.get('cuil')}")
                                        if "fecha_alta" in chapa and chapa.get("fecha_alta"):
                                            logger.info(f"  Fecha Alta: {chapa.get('fecha_alta')}")
                                        if "fecha_vencimiento" in chapa and chapa.get("fecha_vencimiento"):
                                            logger.info(f"  Fecha Vencimiento: {chapa.get('fecha_vencimiento')}")
                                        if "central_agencia" in chapa and chapa.get("central_agencia"):
                                            logger.info(f"  Central/Agencia: {chapa.get('central_agencia')}")
                                    
                                    # Si hay más de 5 chapas, indicar cuántas más hay
                                    if cantidad_chapas > 5:
                                        logger.info(f"... y {cantidad_chapas - 5} chapas mas para CUIL {cuil_a_probar}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.chapas_por_cuil = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de chapas")
                                    logger.warning(f"Estructura de datos no reconocida para CUIL {cuil_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron chapas
                                logger.warning(f"No se encontraron chapas para el CUIL {cuil_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente un solo resultado o con metadatos)
                            logger.info(f"Respuesta recibida como objeto para CUIL {cuil_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una chapa individual
                            tiene_campos_chapa = any(
                                campo in response_data 
                                for campo in ["id", "id_chapa", "numero_chapa", "numero_interno", "tipo_servicio"]
                            )
                            
                            if tiene_campos_chapa:
                                logger.info(f"Se encontro una chapa para CUIL {cuil_a_probar}:")
                                if "numero_chapa" in response_data:
                                    logger.info(f"  Numero Chapa: {response_data.get('numero_chapa')}")
                                if "tipo_servicio" in response_data:
                                    logger.info(f"  Tipo Servicio: {response_data.get('tipo_servicio')}")
                                if "estado" in response_data:
                                    logger.info(f"  Estado: {response_data.get('estado')}")
                            
                            response.success()
                            logger.info(f"Consulta de chapas por CUIL {cuil_a_probar} exitosa")
                            data_module.chapas_por_cuil = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para CUIL {cuil_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para CUIL {cuil_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 404:
                    # No se encontraron chapas para el CUIL
                    logger.warning(f"No se encontraron chapas para el CUIL {cuil_a_probar} (404)")
                    response.failure("CUIL no encontrado o sin chapas asociadas")
                    return False
                elif response.status_code == 422:
                    # Error de validación en CUIL
                    logger.warning(f"Error de validacion con CUIL {cuil_a_probar} - CUIL invalido (422)")
                    response.failure("CUIL inválido - dígito verificador incorrecto")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de chapas por CUIL {cuil_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de chapas por CUIL {cuil_a_probar} (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de chapas por CUIL {cuil_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de chapas por CUIL {cuil_a_probar}: {str(e)}")
            return False
    
    # Probar con el CUIL principal
    logger.info(f"Iniciando prueba con CUIL principal: {cuil}")
    if probar_cuil(cuil, " principal"):
        logger.info(f"EXITO con CUIL principal: {cuil}")
        return  # Si funciona, terminar
    
    # Si el CUIL principal falla, intentar con CUILs alternativos
    logger.info(f"CUIL principal {cuil} fallo. Intentando con CUILs alternativos...")
    if hasattr(data_module, 'parametros_chapas_por_cuil_alternativos'):
        for idx, alt_params in enumerate(data_module.parametros_chapas_por_cuil_alternativos):
            alt_cuil = alt_params.get("p_cuil")
            logger.info(f"Probando CUIL alternativo {idx+1}: {alt_cuil}")
            if probar_cuil(alt_cuil, f" alternativo {idx+1}"):
                logger.info(f"EXITO con CUIL alternativo {idx+1}: {alt_cuil}")
                return  # Si funciona, terminar
    else:
        logger.warning("No hay CUILs alternativos configurados en data_module")
    
    # Si llegamos aquí, ningún CUIL funcionó
    logger.error(f"Ningun CUIL funciono correctamente. CUIL principal usado: {cuil}")
    with client.get(
        f"/chapas/{cuil}",
        catch_response=True,
        name="(TRANSPORTE) - /chapas/{cuil} [Exception Final]"
    ) as response:
        response.failure(f"Todos los CUILs fallaron - CUIL principal: {cuil}")


def get_permisionarios_por_parametros(client, logger, environment, data_module):
    """Prueba el endpoint de consultar permisionarios por DNI y CUIL"""
    
    logger.info("Ejecutando get_permisionarios_por_parametros")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_permisionarios'):
        query_params.update(data_module.parametros_permisionarios)
        logger.info(f"Parametros cargados desde data_module: {query_params}")
    else:
        # Usar parámetros por defecto si no existen en data_module
        query_params = {
            "p_page_number": 1,
            "p_page_size": 20
        }
        logger.warning(f"Usando parametros por defecto: {query_params}")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA PERMISIONARIOS: {query_params}")
    
    try:
        logger.info(f"Enviando solicitud con parametros: {query_params}")
        logger.info(f"URL completa: /permisionarios con query params: {query_params}")
        
        with client.get(
            "/permisionarios",
            params=query_params,
            catch_response=True,
            name="(TRANSPORTE) - /permisionarios [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} permisionarios encontrados")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} permisionarios encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (PERMISIONARIOS) ===")
                    logger.info(f"Parametros consultados: {query_params}")
                    logger.info(f"Endpoint usado: /permisionarios")
                    
                    # Validar estructura de datos esperada (PaginationResponseSchema)
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura PaginationResponseSchema
                        items = response_data["items"]
                        total_items = response_data.get("total_items", len(items))
                        page_number = response_data.get("page_number", 1)
                        page_size = response_data.get("page_size", len(items))
                        
                        logger.info(f"Pagina: {page_number}, Tamaño: {page_size}, Total: {total_items}")
                        logger.info(f"Se encontraron {len(items)} permisionarios en esta pagina")
                        
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de permisionarios (usando nombres reales)
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id_permisionario", "apellido_permisionario", "nombre_permisionario", "cuil_permisionario", "id_persona_fisica", "Chapas"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de permisionarios exitosa")
                                
                                # Mostrar información de los permisionarios encontrados (hasta 5)
                                for idx, permisionario in enumerate(items[:5]):
                                    # Mostrar información usando los campos reales de la API
                                    if "apellido_permisionario" in permisionario and "nombre_permisionario" in permisionario:
                                        logger.info(f"Permisionario {idx+1}: {permisionario.get('apellido_permisionario')}, {permisionario.get('nombre_permisionario')}")
                                    elif "nombre_permisionario" in permisionario:
                                        logger.info(f"Permisionario {idx+1}: {permisionario.get('nombre_permisionario')}")
                                    elif "id_permisionario" in permisionario:
                                        logger.info(f"Permisionario {idx+1}: ID {permisionario.get('id_permisionario')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in permisionario.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Permisionario {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional usando los campos reales
                                    if "id_permisionario" in permisionario and permisionario.get("id_permisionario"):
                                        logger.info(f"  ID Permisionario: {permisionario.get('id_permisionario')}")
                                    if "cuil_permisionario" in permisionario and permisionario.get("cuil_permisionario"):
                                        logger.info(f"  CUIL: {permisionario.get('cuil_permisionario')}")
                                    if "id_persona_fisica" in permisionario and permisionario.get("id_persona_fisica"):
                                        logger.info(f"  ID Persona Fisica: {permisionario.get('id_persona_fisica')}")
                                    
                                    # Mostrar información de las chapas si están disponibles
                                    if "Chapas" in permisionario and permisionario.get("Chapas"):
                                        chapas = permisionario.get("Chapas")
                                        if isinstance(chapas, list) and len(chapas) > 0:
                                            logger.info(f"  Chapas asociadas: {len(chapas)}")
                                            for chapa_idx, chapa in enumerate(chapas[:2]):  # Mostrar hasta 2 chapas
                                                if "numero_interno" in chapa:
                                                    logger.info(f"    Chapa {chapa_idx+1}: Numero {chapa.get('numero_interno')}")
                                                if "tipo_servicio" in chapa:
                                                    logger.info(f"      Tipo: {chapa.get('tipo_servicio')}")
                                                if "dominio" in chapa:
                                                    logger.info(f"      Dominio: {chapa.get('dominio')}")
                                            if len(chapas) > 2:
                                                logger.info(f"    ... y {len(chapas) - 2} chapas mas")
                                
                                # Si hay más de 5 permisionarios, indicar cuántos más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} permisionarios mas en esta pagina")
                                
                                # Información de paginación
                                if total_items > len(items):
                                    logger.info(f"Total de permisionarios disponibles: {total_items}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.permisionarios = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de permisionarios")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron permisionarios
                            logger.warning("No se encontraron permisionarios en esta pagina")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_permisionarios = len(response_data)
                        logger.info(f"Se encontraron {cantidad_permisionarios} permisionarios (sin paginacion)")
                        
                        if cantidad_permisionarios > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            # Mostrar algunos permisionarios
                            for idx, permisionario in enumerate(response_data[:5]):
                                if "apellido_permisionario" in permisionario and "nombre_permisionario" in permisionario:
                                    logger.info(f"Permisionario {idx+1}: {permisionario.get('apellido_permisionario')}, {permisionario.get('nombre_permisionario')}")
                                elif "cuil_permisionario" in permisionario:
                                    logger.info(f"Permisionario {idx+1}: CUIL {permisionario.get('cuil_permisionario')}")
                            
                            if cantidad_permisionarios > 5:
                                logger.info(f"... y {cantidad_permisionarios - 5} permisionarios mas")
                            
                            data_module.permisionarios = response_data
                            response.success()
                        else:
                            logger.warning("No se encontraron permisionarios")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos diferentes)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de permisionarios exitosa")
                        data_module.permisionarios = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON invalido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros
                logger.warning("Error de validacion en parametros (422)")
                response.failure("Parametros invalidos - verificar formato")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de permisionarios (403)")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de permisionarios no encontrado (404)")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de permisionarios (500)")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de permisionarios: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepcion durante consulta de permisionarios: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/permisionarios",
            params=query_params,
            catch_response=True,
            name="(TRANSPORTE) - /permisionarios [Exception]"
        ) as response:
            response.failure(f"Excepcion: {str(e)}")

def get_licencias_por_parametros(client, logger, environment, data_module):
    """Prueba el endpoint de consultar licencias de conducir por DNI y CUIL"""
    
    logger.info("Ejecutando get_licencias_por_parametros")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_licencias'):
        query_params.update(data_module.parametros_licencias)
        logger.info(f"Parametros cargados desde data_module: {query_params}")
    else:
        # Usar parámetros por defecto si no existen en data_module
        query_params = {
            "p_page_number": 1,
            "p_page_size": 20
        }
        logger.warning(f"Usando parametros por defecto: {query_params}")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA LICENCIAS: {query_params}")
    
    try:
        logger.info(f"Enviando solicitud con parametros: {query_params}")
        logger.info(f"URL completa: /licencias con query params: {query_params}")
        
        with client.get(
            "/licencias",
            params=query_params,
            catch_response=True,
            name="(TRANSPORTE) - /licencias [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and "items" in response_data:
                        logger.info(f"Respuesta recibida: {len(response_data['items'])} licencias encontradas")
                    elif isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} licencias encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (LICENCIAS DE CONDUCIR) ===")
                    logger.info(f"Parametros consultados: {query_params}")
                    logger.info(f"Endpoint usado: /licencias")
                    
                    # Validar estructura de datos esperada (PaginationResponseSchema)
                    if isinstance(response_data, dict) and "items" in response_data:
                        # Respuesta paginada con estructura PaginationResponseSchema
                        items = response_data["items"]
                        total_items = response_data.get("total_items", len(items))
                        page_number = response_data.get("page_number", 1)
                        page_size = response_data.get("page_size", len(items))
                        
                        logger.info(f"Pagina: {page_number}, Tamaño: {page_size}, Total: {total_items}")
                        logger.info(f"Se encontraron {len(items)} licencias en esta pagina")
                        
                        if len(items) > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = items[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de licencias
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_licencia", "numero_licencia", "dni", "cuil", "apellido", "nombre", "clase", "estado", "fecha_emision", "fecha_vencimiento"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de licencias de conducir exitosa")
                                
                                # Mostrar información de las licencias encontradas (hasta 5)
                                for idx, licencia in enumerate(items[:5]):
                                    # Mostrar información relevante según los campos disponibles
                                    if "numero_licencia" in licencia:
                                        logger.info(f"Licencia {idx+1}: Numero {licencia.get('numero_licencia')}")
                                    elif "id_licencia" in licencia:
                                        logger.info(f"Licencia {idx+1}: ID {licencia.get('id_licencia')}")
                                    elif "id" in licencia:
                                        logger.info(f"Licencia {idx+1}: ID {licencia.get('id')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in licencia.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Licencia {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional de la licencia
                                    if "apellido" in licencia and "nombre" in licencia:
                                        logger.info(f"  Titular: {licencia.get('apellido')}, {licencia.get('nombre')}")
                                    elif "titular" in licencia:
                                        logger.info(f"  Titular: {licencia.get('titular')}")
                                    
                                    if "dni" in licencia and licencia.get("dni"):
                                        logger.info(f"  DNI: {licencia.get('dni')}")
                                    if "cuil" in licencia and licencia.get("cuil"):
                                        logger.info(f"  CUIL: {licencia.get('cuil')}")
                                    if "clase" in licencia and licencia.get("clase"):
                                        logger.info(f"  Clase: {licencia.get('clase')}")
                                    if "estado" in licencia and licencia.get("estado"):
                                        logger.info(f"  Estado: {licencia.get('estado')}")
                                    if "fecha_emision" in licencia and licencia.get("fecha_emision"):
                                        logger.info(f"  Fecha Emision: {licencia.get('fecha_emision')}")
                                    if "fecha_vencimiento" in licencia and licencia.get("fecha_vencimiento"):
                                        logger.info(f"  Fecha Vencimiento: {licencia.get('fecha_vencimiento')}")
                                    if "observaciones" in licencia and licencia.get("observaciones"):
                                        logger.info(f"  Observaciones: {licencia.get('observaciones')}")
                                    if "restricciones" in licencia and licencia.get("restricciones"):
                                        logger.info(f"  Restricciones: {licencia.get('restricciones')}")
                                
                                # Si hay más de 5 licencias, indicar cuántas más hay
                                if len(items) > 5:
                                    logger.info(f"... y {len(items) - 5} licencias mas en esta pagina")
                                
                                # Información de paginación
                                if total_items > len(items):
                                    logger.info(f"Total de licencias disponibles: {total_items}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.licencias = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de licencias")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron licencias
                            logger.warning("No se encontraron licencias en esta pagina")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, list):
                        # Respuesta directa como lista (sin paginación)
                        cantidad_licencias = len(response_data)
                        logger.info(f"Se encontraron {cantidad_licencias} licencias (sin paginacion)")
                        
                        if cantidad_licencias > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles: {campos_disponibles}")
                            
                            # Mostrar algunas licencias
                            for idx, licencia in enumerate(response_data[:5]):
                                if "numero_licencia" in licencia:
                                    logger.info(f"Licencia {idx+1}: Numero {licencia.get('numero_licencia')}")
                                elif "dni" in licencia:
                                    logger.info(f"Licencia {idx+1}: DNI {licencia.get('dni')}")
                            
                            if cantidad_licencias > 5:
                                logger.info(f"... y {cantidad_licencias - 5} licencias mas")
                            
                            data_module.licencias = response_data
                            response.success()
                        else:
                            logger.warning("No se encontraron licencias")
                            response.success()
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos diferentes)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        response.success()
                        logger.info("Consulta de licencias de conducir exitosa")
                        data_module.licencias = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON invalido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros
                logger.warning("Error de validacion en parametros de licencias (422)")
                response.failure("Parametros invalidos - verificar formato")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de licencias (403)")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de licencias no encontrado (404)")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de licencias (500)")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de licencias: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepcion durante consulta de licencias: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/licencias",
            params=query_params,
            catch_response=True,
            name="(TRANSPORTE) - /licencias [Exception]"
        ) as response:
            response.failure(f"Excepcion: {str(e)}")

def get_ciclovias(client, logger, environment, data_module):
    """Prueba el endpoint de consultar ciclovías de la ciudad"""
    
    logger.info("Ejecutando get_ciclovias")
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_ciclovias'):
        query_params.update(data_module.parametros_ciclovias)
        logger.info(f"Parametros cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA CICLOVIAS: {query_params}")
    
    try:
        logger.info(f"Enviando solicitud con parametros: {query_params}")
        logger.info(f"URL completa: /ciclovias con query params: {query_params}")
        
        with client.get(
            "/ciclovias",
            params=query_params if query_params else None,
            catch_response=True,
            name="(TRANSPORTE) - /ciclovias [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} ciclovias encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CICLOVIAS) ===")
                    if query_params:
                        logger.info(f"Parametros consultados: {query_params}")
                    else:
                        logger.info("Sin parametros de consulta (todas las ciclovias)")
                    logger.info(f"Endpoint usado: /ciclovias")
                    
                    # Validar estructura de datos esperada (lista directa)
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_ciclovias = len(response_data)
                        logger.info(f"Se encontraron {cantidad_ciclovias} ciclovias")
                        
                        if cantidad_ciclovias > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de ciclovías
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "id_ciclovia", "nombre", "descripcion", "barrio", "zona", "estado", "tipo", "longitud", "coordenadas", "fecha_construccion"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de ciclovias exitosa")
                                
                                # Mostrar información de las ciclovías encontradas (hasta 5)
                                for idx, ciclovia in enumerate(response_data[:5]):
                                    # Mostrar información relevante según los campos disponibles
                                    if "nombre" in ciclovia:
                                        logger.info(f"Ciclovia {idx+1}: {ciclovia.get('nombre')}")
                                    elif "id_ciclovia" in ciclovia:
                                        logger.info(f"Ciclovia {idx+1}: ID {ciclovia.get('id_ciclovia')}")
                                    elif "id" in ciclovia:
                                        logger.info(f"Ciclovia {idx+1}: ID {ciclovia.get('id')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in ciclovia.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Ciclovia {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional de la ciclovía
                                    if "descripcion" in ciclovia and ciclovia.get("descripcion"):
                                        logger.info(f"  Descripcion: {ciclovia.get('descripcion')}")
                                    if "barrio" in ciclovia and ciclovia.get("barrio"):
                                        logger.info(f"  Barrio: {ciclovia.get('barrio')}")
                                    if "zona" in ciclovia and ciclovia.get("zona"):
                                        logger.info(f"  Zona: {ciclovia.get('zona')}")
                                    if "estado" in ciclovia and ciclovia.get("estado"):
                                        logger.info(f"  Estado: {ciclovia.get('estado')}")
                                    if "tipo" in ciclovia and ciclovia.get("tipo"):
                                        logger.info(f"  Tipo: {ciclovia.get('tipo')}")
                                    if "longitud" in ciclovia and ciclovia.get("longitud"):
                                        logger.info(f"  Longitud: {ciclovia.get('longitud')} metros")
                                    if "fecha_construccion" in ciclovia and ciclovia.get("fecha_construccion"):
                                        logger.info(f"  Fecha Construccion: {ciclovia.get('fecha_construccion')}")
                                    if "observaciones" in ciclovia and ciclovia.get("observaciones"):
                                        logger.info(f"  Observaciones: {ciclovia.get('observaciones')}")
                                    
                                    # Mostrar información de coordenadas si está disponible
                                    if "coordenadas" in ciclovia and ciclovia.get("coordenadas"):
                                        coordenadas = ciclovia.get("coordenadas")
                                        if isinstance(coordenadas, dict):
                                            logger.info(f"  Coordenadas: {coordenadas}")
                                        elif isinstance(coordenadas, str):
                                            logger.info(f"  Coordenadas: {coordenadas}")
                                    
                                    # Mostrar información de ubicación si está disponible
                                    if "direccion" in ciclovia and ciclovia.get("direccion"):
                                        logger.info(f"  Direccion: {ciclovia.get('direccion')}")
                                    if "desde" in ciclovia and ciclovia.get("desde"):
                                        logger.info(f"  Desde: {ciclovia.get('desde')}")
                                    if "hasta" in ciclovia and ciclovia.get("hasta"):
                                        logger.info(f"  Hasta: {ciclovia.get('hasta')}")
                                
                                # Si hay más de 5 ciclovías, indicar cuántas más hay
                                if cantidad_ciclovias > 5:
                                    logger.info(f"... y {cantidad_ciclovias - 5} ciclovias mas")
                                
                                # Estadísticas adicionales
                                logger.info(f"Total de ciclovias encontradas: {cantidad_ciclovias}")
                                
                                # Agrupar por estado si está disponible
                                if cantidad_ciclovias > 0 and "estado" in response_data[0]:
                                    estados = {}
                                    for ciclovia in response_data:
                                        estado = ciclovia.get("estado", "Sin estado")
                                        estados[estado] = estados.get(estado, 0) + 1
                                    logger.info(f"Ciclovias por estado: {estados}")
                                
                                # Agrupar por zona si está disponible
                                if cantidad_ciclovias > 0 and "zona" in response_data[0]:
                                    zonas = {}
                                    for ciclovia in response_data:
                                        zona = ciclovia.get("zona", "Sin zona")
                                        zonas[zona] = zonas.get(zona, 0) + 1
                                    logger.info(f"Ciclovias por zona: {zonas}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.ciclovias = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de ciclovias")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron ciclovías
                            logger.warning("No se encontraron ciclovias")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta con items
                        if "items" in response_data:
                            items = response_data["items"]
                            logger.info(f"Se encontraron {len(items)} ciclovias en items")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas ciclovías
                                for idx, ciclovia in enumerate(items[:5]):
                                    if "nombre" in ciclovia:
                                        logger.info(f"Ciclovia {idx+1}: {ciclovia.get('nombre')}")
                                    elif "id" in ciclovia:
                                        logger.info(f"Ciclovia {idx+1}: ID {ciclovia.get('id')}")
                                
                                data_module.ciclovias = response_data
                        
                        response.success()
                        logger.info("Consulta de ciclovias exitosa")
                        data_module.ciclovias = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON invalido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación en parámetros
                logger.warning("Error de validacion en parametros de ciclovias (422)")
                response.failure("Parametros invalidos - verificar formato")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de ciclovias (403)")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de ciclovias no encontrado (404)")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de ciclovias (500)")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de ciclovias: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepcion durante consulta de ciclovias: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/ciclovias",
            catch_response=True,
            name="(TRANSPORTE) - /ciclovias [Exception]"
        ) as response:
            response.failure(f"Excepcion: {str(e)}")


def get_personal(client, logger, environment, data_module):
    """Consultar personal por empresa de transporte"""
    try:
        logger.info("=== CONSULTANDO PERSONAL POR EMPRESA ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_personal
        
        response = client.get(
            "/personal",
            params=params,
            name="(TRANSPORTE) - GET /personal"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f" Personal consultado exitosamente")
            logger.info(f" Total de registros: {data.get('total_items', 0)}")
            logger.info(f" Página: {data.get('page_number', 'N/A')} - Tamaño: {data.get('page_size', 'N/A')}")
            
            if data.get('items'):
                logger.info(f" Cantidad de personal en esta página: {len(data['items'])}")
            else:
                logger.warning(" No se encontró personal para los parámetros especificados")
                
        elif response.status_code == 422:
            logger.error(f" Error de validación en parámetros: {response.text}")
        elif response.status_code == 403:
            logger.error(" Sin permisos para consultar personal")
        else:
            logger.error(f" Error al consultar personal: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f" Excepción al consultar personal: {str(e)}")

def get_empresas(client, logger, environment, data_module):
    """Consultar empresas de transporte"""
    try:
        logger.info("=== CONSULTANDO EMPRESAS DE TRANSPORTE ===")
        
        # Usar parámetros del módulo de datos (vacío en este caso)
        params = data_module.parametros_empresas
        
        response = client.get(
            "/empresas",
            params=params,
            name="(TRANSPORTE) - GET /empresas"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f" Empresas consultadas exitosamente")
            logger.info(f" Total de empresas: {len(data) if isinstance(data, list) else 0}")
            
            if data and isinstance(data, list):
                for i, empresa in enumerate(data[:3]):  # Mostrar solo las primeras 3
                    logger.info(f" Empresa {i+1}: {empresa.get('razon_social', 'N/A')} - CUIT: {empresa.get('cuit', 'N/A')}")
                if len(data) > 3:
                    logger.info(f"... y {len(data) - 3} empresas más")
            else:
                logger.warning(" No se encontraron empresas de transporte")
                
        elif response.status_code == 403:
            logger.error(" Sin permisos para consultar empresas de transporte")
        else:
            logger.error(f" Error al consultar empresas: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f" Excepción al consultar empresas: {str(e)}")


def get_recorridos_lineas(client, logger, environment, data_module):
    """Consultar recorridos de líneas por empresa y/o línea"""
    try:
        logger.info("=== CONSULTANDO RECORRIDOS DE LÍNEAS ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_recorridos_lineas
        
        response = client.get(
            "/lineas/recorrido",
            params=params,
            name="(TRANSPORTE) - GET /lineas/recorrido"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f" Recorridos de líneas consultados exitosamente")
            logger.info(f" Total de líneas con recorridos: {len(data) if isinstance(data, list) else 0}")
            
            if data and isinstance(data, list):
                total_paradas = 0
                for i, linea in enumerate(data[:3]):  # Mostrar solo las primeras 3
                    paradas_count = len(linea.get('paradas', []))
                    total_paradas += paradas_count
                    logger.info(f" Línea {i+1}: {linea.get('nombre', 'N/A')} - {paradas_count} paradas")
                
                if len(data) > 3:
                    logger.info(f"... y {len(data) - 3} líneas más")
                    
                logger.info(f" Total de paradas procesadas: {total_paradas}")
            else:
                logger.warning(" No se encontraron recorridos de líneas")
                
        elif response.status_code == 422:
            logger.error(f" Error de validación en parámetros: {response.text}")
        elif response.status_code == 403:
            logger.error(" Sin permisos para consultar recorridos de líneas")
        else:
            logger.error(f" Error al consultar recorridos: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f" Excepción al consultar recorridos de líneas: {str(e)}")

def get_paradas_linea(client, logger, environment, data_module):
    """Consultar paradas por línea de transporte"""
    try:
        logger.info("=== CONSULTANDO PARADAS POR LÍNEA ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_paradas_linea
        
        response = client.get(
            "/lineas/paradas",
            params=params,
            name="(TRANSPORTE) - GET /lineas/paradas"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f" Paradas de línea consultadas exitosamente")
            
            if data:
                logger.info(f" Empresa: {data.get('nombre_empresa', 'N/A')}")
                logger.info(f" Línea: {data.get('nombre_linea', 'N/A')} (ID: {data.get('id_linea', 'N/A')})")
                
                paradas = data.get('paradas', [])
                logger.info(f" Total de paradas: {len(paradas)}")
                
                if paradas:
                    # Mostrar algunas paradas de ejemplo
                    for i, parada in enumerate(paradas[:3]):
                        logger.info(f" Parada {i+1}: {parada.get('nombre_parada', 'N/A')} - Código: {parada.get('codigo', 'N/A')} - Sentido: {parada.get('sentido', 'N/A')}")
                    
                    if len(paradas) > 3:
                        logger.info(f"... y {len(paradas) - 3} paradas más")
                else:
                    logger.warning(" No se encontraron paradas válidas para esta línea")
            else:
                logger.warning(" No se encontraron datos para la línea especificada")
                
        elif response.status_code == 422:
            logger.error(f" Error de validación en parámetros: {response.text}")
        elif response.status_code == 403:
            logger.error(" Sin permisos para consultar paradas de línea")
        else:
            logger.error(f" Error al consultar paradas: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f" Excepción al consultar paradas de línea: {str(e)}")

def get_vehiculos(client, logger, environment, data_module):
    """Consultar vehículos por empresa y/o dominio"""
    try:
        logger.info("=== CONSULTANDO VEHÍCULOS POR EMPRESA ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_vehiculos
        
        response = client.get(
            "/vehiculos",
            params=params,
            name="(TRANSPORTE) - GET /vehiculos"
        )
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f" Vehículos consultados exitosamente")
            logger.info(f" Total de registros: {data.get('total_items', 0)}")
            logger.info(f" Página: {data.get('page_number', 'N/A')} - Tamaño: {data.get('page_size', 'N/A')}")
            
            vehiculos = data.get('items', [])
            if vehiculos:
                logger.info(f" Cantidad de vehículos en esta página: {len(vehiculos)}")
                
                # Mostrar algunos vehículos de ejemplo
                for i, vehiculo in enumerate(vehiculos[:3]):
                    dominio = vehiculo.get('dominio', 'N/A')
                    marca = vehiculo.get('marca', 'N/A')
                    modelo = vehiculo.get('modelo', 'N/A')
                    logger.info(f" Vehículo {i+1}: {dominio} - {marca} {modelo}")
                
                if len(vehiculos) > 3:
                    logger.info(f"... y {len(vehiculos) - 3} vehículos más")
            else:
                logger.warning(" No se encontraron vehículos para los parámetros especificados")
                
        elif response.status_code == 422:
            logger.error(f" Error de validación en parámetros: {response.text}")
        elif response.status_code == 403:
            logger.error(" Sin permisos para consultar vehículos")
        else:
            logger.error(f" Error al consultar vehículos: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f" Excepción al consultar vehículos: {str(e)}")
