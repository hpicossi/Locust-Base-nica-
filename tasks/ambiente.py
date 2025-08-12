import random
import copy
from typing import Dict, Any

def get_espacios_verdes(client, logger, environment, data_module):
    """Prueba el endpoint de obtener espacios verdes de Córdoba"""
    
    logger.info("Ejecutando get_espacios_verdes")
    
    try:
        with client.get(
            "/ambiente/espacios-verdes", 
            catch_response=True,
            name=" (AMBIENTE) - /ambiente/espacios-verdes [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (ESPACIOS VERDES) ===")
                    logger.info(f"Cantidad de espacios verdes obtenidos: {len(response_data) if isinstance(response_data, list) else 'No es lista'}")
                    
                    # Mostrar solo los primeros elementos para no saturar el log
                    if isinstance(response_data, list) and response_data:
                        logger.info(f"Primeros 3 espacios verdes: {response_data[:3]}")
                    else:
                        logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        if not response_data:
                            # Lista vacía es un resultado válido
                            logger.info("No se encontraron espacios verdes en la base de datos")
                            response.success()
                        else:
                            # Verificar que los elementos de la lista contengan los campos esperados
                            # Campos típicos que podrían estar en espacios verdes
                            campos_posibles = [
                                "id", "nombre", "tipo", "superficie", "ubicacion",
                                "barrio", "direccion", "coordenadas", "descripcion",
                                "estado", "fecha_creacion", "fecha_modificacion"
                            ]
                            
                            primer_elemento = response_data[0]
                            campos_presentes = [campo for campo in campos_posibles if campo in primer_elemento]
                            
                            if campos_presentes:
                                response.success()
                                logger.info(f"Obtención de espacios verdes exitosa")
                                logger.info(f"Cantidad de espacios verdes: {len(response_data)}")
                                logger.info(f"Campos presentes en el primer elemento: {campos_presentes}")
                                
                                # Guardar algunos datos para posibles pruebas futuras
                                data_module.espacios_verdes = response_data
                                data_module.primer_espacio_verde = primer_elemento
                                
                                # Mostrar información del primer espacio verde
                                logger.info("=== INFORMACIÓN DEL PRIMER ESPACIO VERDE ===")
                                for campo in campos_presentes[:10]:  # Mostrar hasta 10 campos
                                    valor = primer_elemento.get(campo)
                                    if valor is not None:
                                        logger.info(f"- {campo}: {valor}")
                                
                                # Estadísticas adicionales si hay múltiples espacios verdes
                                if len(response_data) > 1:
                                    logger.info(f"=== ESTADÍSTICAS DE ESPACIOS VERDES ===")
                                    
                                    # Contar por tipo si existe el campo
                                    if "tipo" in primer_elemento:
                                        tipos = {}
                                        for espacio in response_data:
                                            tipo = espacio.get("tipo", "Sin tipo")
                                            tipos[tipo] = tipos.get(tipo, 0) + 1
                                        logger.info(f"Distribución por tipo: {tipos}")
                                    
                                    # Contar por barrio si existe el campo
                                    if "barrio" in primer_elemento:
                                        barrios = {}
                                        for espacio in response_data:
                                            barrio = espacio.get("barrio", "Sin barrio")
                                            barrios[barrio] = barrios.get(barrio, 0) + 1
                                        # Mostrar solo los 5 barrios con más espacios verdes
                                        top_barrios = sorted(barrios.items(), key=lambda x: x[1], reverse=True)[:5]
                                        logger.info(f"Top 5 barrios con más espacios verdes: {top_barrios}")
                                    
                                    # Información sobre superficie si existe el campo
                                    if "superficie" in primer_elemento:
                                        superficies = [espacio.get("superficie") for espacio in response_data if espacio.get("superficie") is not None]
                                        if superficies:
                                            superficie_total = sum(superficies)
                                            superficie_promedio = superficie_total / len(superficies)
                                            logger.info(f"Superficie total: {superficie_total}")
                                            logger.info(f"Superficie promedio: {superficie_promedio:.2f}")
                                            logger.info(f"Espacios con superficie definida: {len(superficies)}/{len(response_data)}")
                            else:
                                # Si no hay campos reconocidos, aún puede ser válido
                                logger.warning("No se reconocieron campos estándar, pero la respuesta es válida")
                                logger.info(f"Campos del primer elemento: {list(primer_elemento.keys())}")
                                response.success()
                                
                                # Guardar datos básicos
                                data_module.espacios_verdes = response_data
                                data_module.primer_espacio_verde = primer_elemento
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en respuesta: {type(response_data)}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 404:
                # No se encontraron espacios verdes (comportamiento esperado)
                try:
                    error_data = response.json()
                    logger.info("No se encontraron espacios verdes")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info("No hay espacios verdes registrados - respuesta 404 esperada")
                            response.success()  # Marcamos como éxito porque es comportamiento esperado
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.success()  # Marcamos como éxito porque es comportamiento esperado
                        
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
                    
            elif response.status_code == 400:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    response.failure(f"Error de validación: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
                    
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al consultar espacios verdes")
                response.failure("Error de autenticación")
                
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al consultar espacios verdes")
                response.failure("Error de permisos")
                
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al consultar espacios verdes")
                response.failure("Error interno del servidor")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de espacios verdes: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de espacios verdes: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            "/ambiente/espacios-verdes",
            catch_response=True,
            name="(AMBIENTE) - /ambiente/espacios-verdes [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_campanas_pet(client, logger, environment, data_module):
    """Prueba el endpoint de obtener campanas PET de Córdoba"""
    
    logger.info("Ejecutando get_campanas_pet")
    
    try:
        with client.get(
            "/ambiente/campanas-pet", 
            catch_response=True,
            name="(AMBIENTE) - /ambiente/campanas-pet [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (CAMPANAS PET) ===")
                    logger.info(f"Cantidad de campanas PET obtenidas: {len(response_data) if isinstance(response_data, list) else 'No es lista'}")
                    
                    # Mostrar solo los primeros elementos para no saturar el log
                    if isinstance(response_data, list) and response_data:
                        logger.info(f"Primeras 3 campanas PET: {response_data[:3]}")
                    else:
                        logger.info(f"Respuesta completa: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        if not response_data:
                            # Lista vacía es un resultado válido
                            logger.info("No se encontraron campanas PET en la base de datos")
                            response.success()
                        else:
                            # Verificar que los elementos de la lista contengan los campos esperados
                            # Campos típicos que podrían estar en campanas PET
                            campos_posibles = [
                                "id", "nombre", "tipo", "ubicacion", "direccion",
                                "barrio", "coordenadas", "latitud", "longitud",
                                "descripcion", "estado", "capacidad", "horario_atencion",
                                "fecha_instalacion", "fecha_creacion", "fecha_modificacion"
                            ]
                            
                            primer_elemento = response_data[0]
                            campos_presentes = [campo for campo in campos_posibles if campo in primer_elemento]
                            
                            if campos_presentes:
                                response.success()
                                logger.info(f"Obtención de campanas PET exitosa")
                                logger.info(f"Cantidad de campanas PET: {len(response_data)}")
                                logger.info(f"Campos presentes en el primer elemento: {campos_presentes}")
                                
                                # Guardar algunos datos para posibles pruebas futuras
                                data_module.campanas_pet = response_data
                                data_module.primera_campana_pet = primer_elemento
                                
                                # Mostrar información de la primera campana PET
                                logger.info("=== INFORMACIÓN DE LA PRIMERA CAMPANA PET ===")
                                for campo in campos_presentes[:10]:  # Mostrar hasta 10 campos
                                    valor = primer_elemento.get(campo)
                                    if valor is not None:
                                        logger.info(f"- {campo}: {valor}")
                                
                                # Estadísticas adicionales si hay múltiples campanas PET
                                if len(response_data) > 1:
                                    logger.info(f"=== ESTADÍSTICAS DE CAMPANAS PET ===")
                                    
                                    # Contar por tipo si existe el campo
                                    if "tipo" in primer_elemento:
                                        tipos = {}
                                        for campana in response_data:
                                            tipo = campana.get("tipo", "Sin tipo")
                                            tipos[tipo] = tipos.get(tipo, 0) + 1
                                        logger.info(f"Distribución por tipo: {tipos}")
                                    
                                    # Contar por barrio si existe el campo
                                    if "barrio" in primer_elemento:
                                        barrios = {}
                                        for campana in response_data:
                                            barrio = campana.get("barrio", "Sin barrio")
                                            barrios[barrio] = barrios.get(barrio, 0) + 1
                                        # Mostrar solo los 5 barrios con más campanas PET
                                        top_barrios = sorted(barrios.items(), key=lambda x: x[1], reverse=True)[:5]
                                        logger.info(f"Top 5 barrios con más campanas PET: {top_barrios}")
                                    
                                    # Contar por estado si existe el campo
                                    if "estado" in primer_elemento:
                                        estados = {}
                                        for campana in response_data:
                                            estado = campana.get("estado", "Sin estado")
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Distribución por estado: {estados}")
                                    
                                    # Información sobre capacidad si existe el campo
                                    if "capacidad" in primer_elemento:
                                        capacidades = [campana.get("capacidad") for campana in response_data if campana.get("capacidad") is not None]
                                        if capacidades:
                                            capacidad_total = sum(capacidades)
                                            capacidad_promedio = capacidad_total / len(capacidades)
                                            logger.info(f"Capacidad total: {capacidad_total}")
                                            logger.info(f"Capacidad promedio: {capacidad_promedio:.2f}")
                                            logger.info(f"Campanas con capacidad definida: {len(capacidades)}/{len(response_data)}")
                                    
                                    # Información sobre coordenadas si existen
                                    campanas_con_coordenadas = 0
                                    for campana in response_data:
                                        if (campana.get("latitud") is not None and campana.get("longitud") is not None) or campana.get("coordenadas") is not None:
                                            campanas_con_coordenadas += 1
                                    
                                    if campanas_con_coordenadas > 0:
                                        logger.info(f"Campanas con coordenadas: {campanas_con_coordenadas}/{len(response_data)}")
                                        porcentaje_geo = (campanas_con_coordenadas / len(response_data)) * 100
                                        logger.info(f"Porcentaje geolocalizado: {porcentaje_geo:.1f}%")
                            else:
                                # Si no hay campos reconocidos, aún puede ser válido
                                logger.warning("No se reconocieron campos estándar, pero la respuesta es válida")
                                logger.info(f"Campos del primer elemento: {list(primer_elemento.keys())}")
                                response.success()
                                
                                # Guardar datos básicos
                                data_module.campanas_pet = response_data
                                data_module.primera_campana_pet = primer_elemento
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                        logger.warning(f"Formato inesperado en respuesta: {type(response_data)}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 404:
                # No se encontraron campanas PET (comportamiento esperado)
                try:
                    error_data = response.json()
                    logger.info("No se encontraron campanas PET")
                    
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info("No hay campanas PET registradas - respuesta 404 esperada")
                            response.success()  # Marcamos como éxito porque es comportamiento esperado
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.success()  # Marcamos como éxito porque es comportamiento esperado
                        
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
                    
            elif response.status_code == 400:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación 400: {error_data}")
                    response.failure(f"Error de validación: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
                    
            elif response.status_code == 401:
                # Error de autenticación
                logger.error("Error de autenticación al consultar campanas PET")
                response.failure("Error de autenticación")
                
            elif response.status_code == 403:
                # Error de permisos
                logger.error("Error de permisos al consultar campanas PET")
                response.failure("Error de permisos")
                
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor al consultar campanas PET")
                response.failure("Error interno del servidor")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de campanas PET: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepción durante consulta de campanas PET: {str(e)}")
        
        # Registrar el error como una respuesta fallida
        with client.get(
            "/ambiente/campanas-pet",
            catch_response=True,
            name="(AMBIENTE) - /ambiente/campanas-pet [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_recoleccion_residuos_diferenciada(client, logger, environment, data_module):
    """Prueba el endpoint de obtener recolección diferenciada de residuos de Córdoba"""
    
    logger.info("Ejecutando get_recoleccion_residuos_diferenciada")
    
    # Obtener parámetros de consulta
    if hasattr(data_module, 'parametros_recoleccion_residuos') and data_module.parametros_recoleccion_residuos:
        lista_parametros = data_module.parametros_recoleccion_residuos
    else:
        # Parámetros por defecto si no están definidos
        lista_parametros = [
            {},  # Sin parámetros
            {"p_barrio": "Centro"},
            {"p_tipo_residuo": "Reciclables"}
        ]
    
    logger.info(f"Ejecutando consultas con {len(lista_parametros)} conjuntos de parámetros")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "sin_resultados": 0,
        "errores": 0
    }
    
    # Realizar consulta para cada conjunto de parámetros
    for idx, params in enumerate(lista_parametros):
        logger.info(f"Consulta {idx + 1}: Parámetros = {params}")
        
        # Construir query string
        query_string = ""
        if params:
            query_params = []
            for key, value in params.items():
                query_params.append(f"{key}={value}")
            query_string = "?" + "&".join(query_params)
        
        url = f"/ambiente/recoleccion-residuos-diferenciada{query_string}"
        
        try:
            with client.get(
                url, 
                catch_response=True,
                name=f"(AMBIENTE) - /ambiente/recoleccion-residuos-diferenciada [GET {idx+1}]"
            ) as response:
                # Guardar la respuesta en el log (versión resumida para no saturar)
                logger.info(f"Respuesta para consulta {idx + 1}: Código {response.status_code}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar los datos completos obtenidos en el log
                        logger.info(f"=== DATOS COMPLETOS DE LA RESPUESTA (RECOLECCIÓN RESIDUOS {idx + 1}) ===")
                        logger.info(f"Cantidad de registros obtenidos: {len(response_data) if isinstance(response_data, list) else 'No es lista'}")
                        
                        # Mostrar solo los primeros elementos para no saturar el log
                        if isinstance(response_data, list) and response_data:
                            logger.info(f"Primeros 2 registros: {response_data[:2]}")
                        else:
                            logger.info(f"Respuesta completa: {response_data}")
                        
                        # Validar estructura de datos esperada
                        if isinstance(response_data, list):
                            if not response_data:
                                # Lista vacía es un resultado válido
                                logger.info(f"No se encontraron datos de recolección para los parámetros: {params}")
                                response.success()
                                resultados["sin_resultados"] += 1
                            else:
                                # Verificar que los elementos de la lista contengan los campos esperados
                                campos_posibles = [
                                    "id", "barrio", "zona", "tipo_residuo", "dia_semana",
                                    "horario_inicio", "horario_fin", "frecuencia", "descripcion",
                                    "empresa_recolectora", "telefono_contacto", "observaciones",
                                    "estado", "fecha_inicio_servicio", "fecha_fin_servicio",
                                    "coordenadas", "latitud", "longitud", "direccion_referencia"
                                ]
                                
                                primer_elemento = response_data[0]
                                campos_presentes = [campo for campo in campos_posibles if campo in primer_elemento]
                                
                                if campos_presentes:
                                    response.success()
                                    logger.info(f"Obtención de datos de recolección exitosa")
                                    logger.info(f"Cantidad de registros: {len(response_data)}")
                                    logger.info(f"Campos presentes: {campos_presentes}")
                                    
                                    # Guardar algunos datos para posibles pruebas futuras
                                    if not hasattr(data_module, 'recoleccion_residuos_data'):
                                        data_module.recoleccion_residuos_data = []
                                    data_module.recoleccion_residuos_data.extend(response_data)
                                    data_module.primer_registro_recoleccion = primer_elemento
                                    
                                    # Mostrar información del primer registro
                                    logger.info("=== INFORMACIÓN DEL PRIMER REGISTRO ===")
                                    for campo in campos_presentes[:8]:  # Mostrar hasta 8 campos
                                        valor = primer_elemento.get(campo)
                                        if valor is not None:
                                            logger.info(f"- {campo}: {valor}")
                                    
                                    # Estadísticas adicionales si hay múltiples registros
                                    if len(response_data) > 1:
                                        logger.info(f"=== ESTADÍSTICAS DE RECOLECCIÓN DE RESIDUOS ===")
                                        
                                        # Distribución por tipo de residuo
                                        if "tipo_residuo" in primer_elemento:
                                            tipos = {}
                                            for registro in response_data:
                                                tipo = registro.get("tipo_residuo", "Sin tipo")
                                                tipos[tipo] = tipos.get(tipo, 0) + 1
                                            logger.info(f"Distribución por tipo de residuo: {tipos}")
                                        
                                        # Distribución por día de la semana
                                        if "dia_semana" in primer_elemento:
                                            dias = {}
                                            for registro in response_data:
                                                dia = registro.get("dia_semana", "Sin día")
                                                dias[dia] = dias.get(dia, 0) + 1
                                            logger.info(f"Distribución por día de la semana: {dias}")
                                        
                                        # Distribución por barrio
                                        if "barrio" in primer_elemento:
                                            barrios = {}
                                            for registro in response_data:
                                                barrio = registro.get("barrio", "Sin barrio")
                                                barrios[barrio] = barrios.get(barrio, 0) + 1
                                            # Mostrar solo los 5 barrios con más servicios
                                            top_barrios = sorted(barrios.items(), key=lambda x: x[1], reverse=True)[:5]
                                            logger.info(f"Top 5 barrios con más servicios: {top_barrios}")
                                        
                                        # Distribución por zona
                                        if "zona" in primer_elemento:
                                            zonas = {}
                                            for registro in response_data:
                                                zona = registro.get("zona", "Sin zona")
                                                zonas[zona] = zonas.get(zona, 0) + 1
                                            logger.info(f"Distribución por zona: {zonas}")
                                        
                                        # Distribución por frecuencia
                                        if "frecuencia" in primer_elemento:
                                            frecuencias = {}
                                            for registro in response_data:
                                                frecuencia = registro.get("frecuencia", "Sin frecuencia")
                                                frecuencias[frecuencia] = frecuencias.get(frecuencia, 0) + 1
                                            logger.info(f"Distribución por frecuencia: {frecuencias}")
                                        
                                        # Información sobre empresas recolectoras
                                        if "empresa_recolectora" in primer_elemento:
                                            empresas = {}
                                            for registro in response_data:
                                                empresa = registro.get("empresa_recolectora", "Sin empresa")
                                                empresas[empresa] = empresas.get(empresa, 0) + 1
                                            logger.info(f"Empresas recolectoras: {empresas}")
                                        
                                        # Información sobre coordenadas si existen
                                        registros_con_coordenadas = 0
                                        for registro in response_data:
                                            if (registro.get("latitud") is not None and registro.get("longitud") is not None) or registro.get("coordenadas") is not None:
                                                registros_con_coordenadas += 1
                                        
                                        if registros_con_coordenadas > 0:
                                            logger.info(f"Registros con coordenadas: {registros_con_coordenadas}/{len(response_data)}")
                                            porcentaje_geo = (registros_con_coordenadas / len(response_data)) * 100
                                            logger.info(f"Porcentaje geolocalizado: {porcentaje_geo:.1f}%")
                                    
                                    resultados["exitosos"] += 1
                                else:
                                    # Si no hay campos reconocidos, aún puede ser válido
                                    logger.warning("No se reconocieron campos estándar, pero la respuesta es válida")
                                    logger.info(f"Campos del primer elemento: {list(primer_elemento.keys())}")
                                    response.success()
                                    
                                    # Guardar datos básicos
                                    if not hasattr(data_module, 'recoleccion_residuos_data'):
                                        data_module.recoleccion_residuos_data = []
                                    data_module.recoleccion_residuos_data.extend(response_data)
                                    data_module.primer_registro_recoleccion = primer_elemento
                                    resultados["exitosos"] += 1
                        else:
                            response.failure("Formato de respuesta inesperado (se esperaba una lista)")
                            logger.warning(f"Formato inesperado en respuesta: {type(response_data)}")
                            resultados["errores"] += 1
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 404:
                    # No se encontraron datos (comportamiento esperado)
                    try:
                        error_data = response.json()
                        logger.info(f"No se encontraron datos de recolección para parámetros: {params}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                                logger.info("No hay datos de recolección para los parámetros especificados - respuesta 404 esperada")
                                response.success()  # Marcamos como éxito porque es comportamiento esperado
                            else:
                                response.failure(f"Error 404: {detail}")
                        else:
                            response.success()  # Marcamos como éxito porque es comportamiento esperado
                        
                        resultados["sin_resultados"] += 1
                    except ValueError:
                        response.failure(f"Error 404 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 400:
                    # Error de validación de parámetros
                    try:
                        error_data = response.json()
                        logger.warning(f"Error de validación 400 para parámetros {params}: {error_data}")
                        
                        if "detail" in error_data:
                            detail = error_data["detail"]
                            if isinstance(detail, list):
                                for error_item in detail:
                                    error_msg = error_item.get("msg", "")
                                    error_loc = error_item.get("loc", [])
                                    logger.warning(f"Error de validación en {error_loc}: {error_msg}")
                                
                                response.failure(f"Error de validación de parámetros: {detail}")
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
                        logger.warning(f"Error de validación 422 para parámetros {params}: {error_data}")
                        response.failure(f"Error de validación de esquema: {error_data}")
                        resultados["errores"] += 1
                    except ValueError:
                        response.failure(f"Error 422 con formato inesperado: {response.text}")
                        resultados["errores"] += 1
                        
                elif response.status_code == 401:
                    # Error de autenticación
                    logger.error("Error de autenticación al consultar recolección de residuos")
                    response.failure("Error de autenticación")
                    resultados["errores"] += 1
                    
                elif response.status_code == 403:
                    # Error de permisos
                    logger.error("Error de permisos al consultar recolección de residuos")
                    response.failure("Error de permisos")
                    resultados["errores"] += 1
                    
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error("Error interno del servidor al consultar recolección de residuos")
                    response.failure("Error interno del servidor")
                    resultados["errores"] += 1
                    
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de recolección de residuos: {response.status_code} - {response.text}")
                    resultados["errores"] += 1
                    
        except Exception as e:
            logger.error(f"Excepción durante consulta de recolección de residuos {idx + 1}: {str(e)}")
            resultados["errores"] += 1
            
            # Registrar el error como una respuesta fallida
            with client.get(
                url,
                catch_response=True,
                name=f"(AMBIENTE) - /ambiente/recoleccion-residuos-diferenciada [Exception {idx+1}]"
            ) as response:
                response.failure(f"Excepción: {str(e)}")
