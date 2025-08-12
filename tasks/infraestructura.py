import random
from typing import Dict, Any

def get_puntos_wifi(client, logger, environment, data_module):
    """Prueba el endpoint de obtener puntos de wifi de la ciudad de Córdoba"""
    
    logger.info("Ejecutando get_puntos_wifi")
    
    try:
        with client.get(
            "/infraestructura/puntos-wifi", 
            catch_response=True,
            name="(INFRACUCTURA) - /infraestructura/puntos-wifi [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} puntos wifi encontrados")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (PUNTOS WIFI) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_puntos = len(response_data)
                        logger.info(f"Se encontraron {cantidad_puntos} puntos wifi")
                        
                        if cantidad_puntos > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # El endpoint funciona correctamente, marcar como exitoso
                            response.success()
                            logger.info("Consulta de puntos wifi exitosa")
                            
                            # Mostrar información de algunos puntos wifi (hasta 5)
                            for idx, punto in enumerate(response_data[:5]):
                                # Mostrar información usando los campos reales de la respuesta
                                if "descripcion" in punto:
                                    logger.info(f"Punto Wifi {idx+1}: {punto.get('descripcion')}")
                                elif "categoria" in punto:
                                    logger.info(f"Punto Wifi {idx+1}: {punto.get('categoria')}")
                                else:
                                    # Mostrar el primer campo que contenga información útil
                                    for key, value in punto.items():
                                        if isinstance(value, str) and len(value) > 0:
                                            logger.info(f"Punto Wifi {idx+1}: {key}={value}")
                                            break
                                
                                # Mostrar información adicional si está disponible
                                if "domicilio_alt" in punto and punto.get("domicilio_alt"):
                                    logger.info(f"  Dirección: {punto.get('domicilio_alt')}")
                                if "barrio_alt" in punto and punto.get("barrio_alt"):
                                    logger.info(f"  Barrio: {punto.get('barrio_alt')}")
                                if "cpc" in punto and punto.get("cpc"):
                                    logger.info(f"  CPC: {punto.get('cpc')}")
                                if "categoria" in punto and punto.get("categoria"):
                                    logger.info(f"  Categoría: {punto.get('categoria')}")
                                if "telefono" in punto and punto.get("telefono"):
                                    logger.info(f"  Teléfono: {punto.get('telefono')}")
                                if "lat" in punto and punto.get("lat"):
                                    logger.info(f"  Coordenadas: {punto.get('lat')}, {punto.get('long', 'N/A')}")
                            
                            # Si hay más de 5 puntos, indicar cuántos más hay
                            if cantidad_puntos > 5:
                                logger.info(f"... y {cantidad_puntos - 5} puntos wifi más")
                            
                            # Guardar los datos para posibles pruebas futuras
                            data_module.puntos_wifi = response_data
                        else:
                            # Si no se encontraron puntos wifi
                            logger.warning("No se encontraron puntos wifi")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} puntos wifi en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunos puntos wifi
                                for idx, punto in enumerate(items[:5]):
                                    if "descripcion" in punto:
                                        logger.info(f"Punto Wifi {idx+1}: {punto.get('descripcion')}")
                                    elif "categoria" in punto:
                                        logger.info(f"Punto Wifi {idx+1}: {punto.get('categoria')}")
                                
                                data_module.puntos_wifi = response_data
                        
                        response.success()
                        logger.info("Consulta de puntos wifi exitosa")
                        data_module.puntos_wifi = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de puntos wifi")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de puntos wifi no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de puntos wifi")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de puntos wifi: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de puntos wifi: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/infraestructura/puntos-wifi",
            catch_response=True,
            name="(INFRACUCTURA) - /infraestructura/puntos-wifi [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_obra_publica(client, logger, environment, data_module):
    """Prueba el endpoint de consulta de obras públicas finalizadas y en ejecución"""
    
    logger.info("Ejecutando get_obra_publica")
    
    try:
        with client.get(
            "/infraestructura/obra-publica", 
            catch_response=True,
            name="(INFRACUCTURA) - /infraestructura/obra-publica [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} obras públicas encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (OBRA PÚBLICA) ===")
                    logger.info("Sin parámetros de consulta (endpoint no los requiere)")
                    
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_obras = len(response_data)
                        logger.info(f"Se encontraron {cantidad_obras} obras públicas")
                        
                        if cantidad_obras > 0:
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de obras públicas
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id", "nombre", "descripcion", "estado", "fecha_inicio", "fecha_fin", "ubicacion", "barrio", "zona", "tipo_obra", "presupuesto", "contratista"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de obras públicas exitosa")
                                
                                # Mostrar información de algunas obras (hasta 5)
                                for idx, obra in enumerate(response_data[:5]):
                                    # Intentar mostrar información relevante según los campos disponibles
                                    if "nombre" in obra:
                                        logger.info(f"Obra Pública {idx+1}: {obra.get('nombre')}")
                                    elif "descripcion" in obra:
                                        logger.info(f"Obra Pública {idx+1}: {obra.get('descripcion')}")
                                    elif "tipo_obra" in obra:
                                        logger.info(f"Obra Pública {idx+1}: {obra.get('tipo_obra')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in obra.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Obra Pública {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional si está disponible
                                    if "estado" in obra and obra.get("estado"):
                                        logger.info(f"  Estado: {obra.get('estado')}")
                                    if "ubicacion" in obra and obra.get("ubicacion"):
                                        logger.info(f"  Ubicación: {obra.get('ubicacion')}")
                                    if "barrio" in obra and obra.get("barrio"):
                                        logger.info(f"  Barrio: {obra.get('barrio')}")
                                    if "zona" in obra and obra.get("zona"):
                                        logger.info(f"  Zona: {obra.get('zona')}")
                                    if "fecha_inicio" in obra and obra.get("fecha_inicio"):
                                        logger.info(f"  Fecha Inicio: {obra.get('fecha_inicio')}")
                                    if "fecha_fin" in obra and obra.get("fecha_fin"):
                                        logger.info(f"  Fecha Fin: {obra.get('fecha_fin')}")
                                    if "presupuesto" in obra and obra.get("presupuesto"):
                                        logger.info(f"  Presupuesto: {obra.get('presupuesto')}")
                                    if "contratista" in obra and obra.get("contratista"):
                                        logger.info(f"  Contratista: {obra.get('contratista')}")
                                
                                # Si hay más de 5 obras, indicar cuántas más hay
                                if cantidad_obras > 5:
                                    logger.info(f"... y {cantidad_obras - 5} obras públicas más")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.obras_publicas = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de obras públicas")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron obras públicas
                            logger.warning("No se encontraron obras públicas")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta paginada
                        if "items" in response_data:
                            items = response_data["items"]
                            total = response_data.get("total", len(items))
                            logger.info(f"Se encontraron {len(items)} obras públicas en esta página de {total} totales")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas obras públicas
                                for idx, obra in enumerate(items[:5]):
                                    if "nombre" in obra:
                                        logger.info(f"Obra Pública {idx+1}: {obra.get('nombre')}")
                                    elif "descripcion" in obra:
                                        logger.info(f"Obra Pública {idx+1}: {obra.get('descripcion')}")
                                
                                data_module.obras_publicas = response_data
                        
                        response.success()
                        logger.info("Consulta de obras públicas exitosa")
                        data_module.obras_publicas = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de obras públicas")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de obras públicas no encontrado")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de obras públicas")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de obras públicas: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de obras públicas: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/infraestructura/obra-publica",
            catch_response=True,
            name="(INFRACUCTURA) - /infraestructura/obra-publica [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")
