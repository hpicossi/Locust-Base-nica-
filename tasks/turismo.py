import random
from typing import Dict, Any

def get_guias_turisticos(client, logger, environment, data_module):
    """Prueba el endpoint de consulta del registro oficial de guías turísticos habilitados en la Ciudad de Córdoba"""
    
    logger.info("Ejecutando get_guias_turisticos")
    
    try:
        with client.get(
            "/turismo/guias-turisticos", 
            catch_response=True,
            name=" (TURISMO) - /turismo/guias-turisticos [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} guías turísticos encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (GUÍAS TURÍSTICOS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_guias = len(response_data)
                        logger.info(f"Se encontraron {cantidad_guias} guías turísticos")
                        
                        if cantidad_guias > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de guías turísticos
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "apellido", "dni", "numero_registro", "telefono", "email", "especialidades", "idiomas", "estado", "fecha_habilitacion", "fecha_vencimiento"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de guías turísticos exitosa")
                                
                                # Mostrar información de algunos guías (hasta 5)
                                for idx, guia in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in guia and "apellido" in guia:
                                        logger.info(f"Guía Turístico {idx+1}: {guia.get('nombre')} {guia.get('apellido')}")
                                    elif "nombre" in guia:
                                        logger.info(f"Guía Turístico {idx+1}: {guia.get('nombre')}")
                                    elif "numero_registro" in guia:
                                        logger.info(f"Guía Turístico {idx+1}: Registro N° {guia.get('numero_registro')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in guia.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Guía Turístico {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "dni" in guia and guia.get("dni"):
                                        logger.info(f"  DNI: {guia.get('dni')}")
                                    if "numero_registro" in guia and guia.get("numero_registro"):
                                        logger.info(f"  Número de Registro: {guia.get('numero_registro')}")
                                    if "telefono" in guia and guia.get("telefono"):
                                        logger.info(f"  Teléfono: {guia.get('telefono')}")
                                    if "email" in guia and guia.get("email"):
                                        logger.info(f"  Email: {guia.get('email')}")
                                    if "especialidades" in guia and guia.get("especialidades"):
                                        logger.info(f"  Especialidades: {guia.get('especialidades')}")
                                    if "idiomas" in guia and guia.get("idiomas"):
                                        logger.info(f"  Idiomas: {guia.get('idiomas')}")
                                    if "estado" in guia and guia.get("estado"):
                                        logger.info(f"  Estado: {guia.get('estado')}")
                                    if "fecha_habilitacion" in guia and guia.get("fecha_habilitacion"):
                                        logger.info(f"  Fecha Habilitación: {guia.get('fecha_habilitacion')}")
                                    if "fecha_vencimiento" in guia and guia.get("fecha_vencimiento"):
                                        logger.info(f"  Fecha Vencimiento: {guia.get('fecha_vencimiento')}")
                                
                                # Si hay más de 5 guías, indicar cuántos más hay
                                if cantidad_guias > 5:
                                    logger.info(f"... y {cantidad_guias - 5} guías turísticos más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.guias_turisticos = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de guías turísticos")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron guías turísticos
                            logger.warning("No se encontraron guías turísticos")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} guías turísticos en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos guías turísticos
                                for idx, guia in enumerate(items[:5]):
                                    if "nombre" in guia and "apellido" in guia:
                                        logger.info(f"Guía Turístico {idx+1}: {guia.get('nombre')} {guia.get('apellido')}")
                                    elif "nombre" in guia:
                                        logger.info(f"Guía Turístico {idx+1}: {guia.get('nombre')}")
                                
                                data_module.guias_turisticos = response_data
                        
                        response.success()
                        logger.info("Consulta de guías turísticos exitosa")
                        data_module.guias_turisticos = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de guías turísticos")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de guías turísticos no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de guías turísticos")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de guías turísticos: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de guías turísticos: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/turismo/guias-turisticos",
            catch_response=True,
            name="(TURISMO) - /turismo/guias-turisticos [GET]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_anfitriones_turisticos(client, logger, environment, data_module):
    """Prueba el endpoint de obtener anfitriones turísticos de Córdoba"""
    
    logger.info("Ejecutando get_anfitriones_turisticos")
    
    try:
        with client.get(
            "/turismo/anfitriones-turisticos", 
            catch_response=True,
            name="(TURISMO) - /turismo/anfitriones-turisticos [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} anfitriones turísticos encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (ANFITRIONES TURÍSTICOS) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_anfitriones = len(response_data)
                        logger.info(f"Se encontraron {cantidad_anfitriones} anfitriones turísticos")
                        
                        if cantidad_anfitriones > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de anfitriones turísticos
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "apellido", "dni", "numero_registro", "telefono", "email", "direccion", "tipo_alojamiento", "capacidad", "servicios", "estado", "fecha_habilitacion"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de anfitriones turísticos exitosa")
                                
                                # Mostrar información de algunos anfitriones (hasta 5)
                                for idx, anfitrion in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in anfitrion and "apellido" in anfitrion:
                                        logger.info(f"Anfitrión Turístico {idx+1}: {anfitrion.get('nombre')} {anfitrion.get('apellido')}")
                                    elif "nombre" in anfitrion:
                                        logger.info(f"Anfitrión Turístico {idx+1}: {anfitrion.get('nombre')}")
                                    elif "numero_registro" in anfitrion:
                                        logger.info(f"Anfitrión Turístico {idx+1}: Registro N° {anfitrion.get('numero_registro')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in anfitrion.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Anfitrión Turístico {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "dni" in anfitrion and anfitrion.get("dni"):
                                        logger.info(f"  DNI: {anfitrion.get('dni')}")
                                    if "numero_registro" in anfitrion and anfitrion.get("numero_registro"):
                                        logger.info(f"  Número de Registro: {anfitrion.get('numero_registro')}")
                                    if "telefono" in anfitrion and anfitrion.get("telefono"):
                                        logger.info(f"  Teléfono: {anfitrion.get('telefono')}")
                                    if "email" in anfitrion and anfitrion.get("email"):
                                        logger.info(f"  Email: {anfitrion.get('email')}")
                                    if "direccion" in anfitrion and anfitrion.get("direccion"):
                                        logger.info(f"  Dirección: {anfitrion.get('direccion')}")
                                    if "tipo_alojamiento" in anfitrion and anfitrion.get("tipo_alojamiento"):
                                        logger.info(f"  Tipo de Alojamiento: {anfitrion.get('tipo_alojamiento')}")
                                    if "capacidad" in anfitrion and anfitrion.get("capacidad"):
                                        logger.info(f"  Capacidad: {anfitrion.get('capacidad')}")
                                    if "servicios" in anfitrion and anfitrion.get("servicios"):
                                        logger.info(f"  Servicios: {anfitrion.get('servicios')}")
                                    if "estado" in anfitrion and anfitrion.get("estado"):
                                        logger.info(f"  Estado: {anfitrion.get('estado')}")
                                    if "fecha_habilitacion" in anfitrion and anfitrion.get("fecha_habilitacion"):
                                        logger.info(f"  Fecha Habilitación: {anfitrion.get('fecha_habilitacion')}")
                                
                                # Si hay más de 5 anfitriones, indicar cuántos más hay
                                if cantidad_anfitriones > 5:
                                    logger.info(f"... y {cantidad_anfitriones - 5} anfitriones turísticos más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.anfitriones_turisticos = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de anfitriones turísticos")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron anfitriones turísticos
                            logger.warning("No se encontraron anfitriones turísticos")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} anfitriones turísticos en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos anfitriones turísticos
                                for idx, anfitrion in enumerate(items[:5]):
                                    if "nombre" in anfitrion and "apellido" in anfitrion:
                                        logger.info(f"Anfitrión Turístico {idx+1}: {anfitrion.get('nombre')} {anfitrion.get('apellido')}")
                                    elif "nombre" in anfitrion:
                                        logger.info(f"Anfitrión Turístico {idx+1}: {anfitrion.get('nombre')}")
                                
                                data_module.anfitriones_turisticos = response_data
                        
                        response.success()
                        logger.info("Consulta de anfitriones turísticos exitosa")
                        data_module.anfitriones_turisticos = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de anfitriones turísticos")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de anfitriones turísticos no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de anfitriones turísticos")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de anfitriones turísticos: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de anfitriones turísticos: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/turismo/anfitriones-turisticos",
            catch_response=True,
            name="(TURISMO) - /turismo/anfitriones-turisticos [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")
