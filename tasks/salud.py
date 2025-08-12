import random
from typing import Dict, Any

def get_centros_salud(client, logger, environment, data_module):
    """Prueba el endpoint de obtener centros de salud de Córdoba"""
    
    logger.info("Ejecutando get_centros_salud")
    
    try:
        with client.get(
            "/salud/centros-salud", 
            catch_response=True,
            name="(SALUD) - /salud/centros-salud [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} centros de salud encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CENTROS DE SALUD) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_centros = len(response_data)
                        logger.info(f"Se encontraron {cantidad_centros} centros de salud")
                        
                        if cantidad_centros > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de centros de salud
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "direccion", "telefono", "email", "barrio", "zona", "tipo", "especialidades", "horario", "latitud", "longitud"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de centros de salud exitosa")
                                
                                # Mostrar información de algunos centros (hasta 5)
                                for idx, centro in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in centro:
                                        logger.info(f"Centro de Salud {idx+1}: {centro.get('nombre')}")
                                    elif "tipo" in centro:
                                        logger.info(f"Centro de Salud {idx+1}: {centro.get('tipo')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in centro.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Centro de Salud {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "direccion" in centro and centro.get("direccion"):
                                        logger.info(f"  Dirección: {centro.get('direccion')}")
                                    if "barrio" in centro and centro.get("barrio"):
                                        logger.info(f"  Barrio: {centro.get('barrio')}")
                                    if "zona" in centro and centro.get("zona"):
                                        logger.info(f"  Zona: {centro.get('zona')}")
                                    if "telefono" in centro and centro.get("telefono"):
                                        logger.info(f"  Teléfono: {centro.get('telefono')}")
                                    if "email" in centro and centro.get("email"):
                                        logger.info(f"  Email: {centro.get('email')}")
                                    if "tipo" in centro and centro.get("tipo"):
                                        logger.info(f"  Tipo: {centro.get('tipo')}")
                                    if "especialidades" in centro and centro.get("especialidades"):
                                        logger.info(f"  Especialidades: {centro.get('especialidades')}")
                                    if "horario" in centro and centro.get("horario"):
                                        logger.info(f"  Horario: {centro.get('horario')}")
                                    if "latitud" in centro and centro.get("latitud"):
                                        logger.info(f"  Coordenadas: {centro.get('latitud')}, {centro.get('longitud', 'N/A')}")
                                
                                # Si hay más de 5 centros, indicar cuántos más hay
                                if cantidad_centros > 5:
                                    logger.info(f"... y {cantidad_centros - 5} centros de salud más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.centros_salud = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de centros de salud")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron centros de salud
                            logger.warning("No se encontraron centros de salud")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} centros de salud en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos centros de salud
                                for idx, centro in enumerate(items[:5]):
                                    if "nombre" in centro:
                                        logger.info(f"Centro de Salud {idx+1}: {centro.get('nombre')}")
                                    elif "tipo" in centro:
                                        logger.info(f"Centro de Salud {idx+1}: {centro.get('tipo')}")
                                
                                data_module.centros_salud = response_data
                        
                        response.success()
                        logger.info("Consulta de centros de salud exitosa")
                        data_module.centros_salud = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de centros de salud")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de centros de salud no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de centros de salud")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de centros de salud: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de centros de salud: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/salud/centros-salud",
            catch_response=True,
            name="(SALUD) - /salud/centros-salud [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")
