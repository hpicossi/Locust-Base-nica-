def get_medios_pagos(client, logger, environment, data_module):
    """Prueba el endpoint de consultar medios de pago"""
    
    logger.info("Ejecutando get_medios_pagos")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/medios_pagos",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /medios_pagos "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} medios de pago encontrados")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (MEDIOS DE PAGO) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta (todos los medios de pago)")
                        logger.info(f"Endpoint usado: /medios_pagos")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_medios = len(response_data)
                            logger.info(f"Se encontraron {cantidad_medios} medios de pago")
                            
                            if cantidad_medios > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de medios de pago
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["id", "id_medio_pago", "nombre", "descripcion", "codigo", "estado", "tipo", "activo"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de medios de pago exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de los medios de pago encontrados (hasta 10)
                                    for idx, medio in enumerate(response_data[:10]):
                                        # Mostrar información relevante según los campos disponibles
                                        if "nombre" in medio:
                                            logger.info(f"Medio de Pago {idx+1}: {medio.get('nombre')}")
                                        elif "id_medio_pago" in medio:
                                            logger.info(f"Medio de Pago {idx+1}: ID {medio.get('id_medio_pago')}")
                                        elif "id" in medio:
                                            logger.info(f"Medio de Pago {idx+1}: ID {medio.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in medio.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Medio de Pago {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional del medio de pago
                                        if "descripcion" in medio and medio.get("descripcion"):
                                            logger.info(f"  Descripcion: {medio.get('descripcion')}")
                                        if "codigo" in medio and medio.get("codigo"):
                                            logger.info(f"  Codigo: {medio.get('codigo')}")
                                        if "estado" in medio and medio.get("estado"):
                                            logger.info(f"  Estado: {medio.get('estado')}")
                                        if "activo" in medio and medio.get("activo") is not None:
                                            logger.info(f"  Activo: {medio.get('activo')}")
                                        if "tipo" in medio and medio.get("tipo"):
                                            logger.info(f"  Tipo: {medio.get('tipo')}")
                                        if "observaciones" in medio and medio.get("observaciones"):
                                            logger.info(f"  Observaciones: {medio.get('observaciones')}")
                                        if "fecha_creacion" in medio and medio.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {medio.get('fecha_creacion')}")
                                        if "fecha_modificacion" in medio and medio.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {medio.get('fecha_modificacion')}")
                                    
                                    # Si hay más de 10 medios de pago, indicar cuántos más hay
                                    if cantidad_medios > 10:
                                        logger.info(f"... y {cantidad_medios - 10} medios de pago mas")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de medios de pago encontrados: {cantidad_medios}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_medios > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for medio in response_data:
                                            if "estado" in medio:
                                                estado = medio.get("estado", "Sin estado")
                                            elif "activo" in medio:
                                                estado = "Activo" if medio.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Medios de pago por estado: {estados}")
                                    
                                    # Agrupar por tipo si está disponible
                                    if cantidad_medios > 0 and "tipo" in response_data[0]:
                                        tipos = {}
                                        for medio in response_data:
                                            tipo = medio.get("tipo", "Sin tipo")
                                            tipos[tipo] = tipos.get(tipo, 0) + 1
                                        logger.info(f"Medios de pago por tipo: {tipos}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.medios_pagos = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de medios de pago")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron medios de pago
                                logger.warning(f"No se encontraron medios de pago con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} medios de pago en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunos medios de pago
                                    for idx, medio in enumerate(items[:5]):
                                        if "nombre" in medio:
                                            logger.info(f"Medio de Pago {idx+1}: {medio.get('nombre')}")
                                        elif "id" in medio:
                                            logger.info(f"Medio de Pago {idx+1}: ID {medio.get('id')}")
                                    
                                    data_module.medios_pagos = response_data
                            
                            response.success()
                            logger.info(f"Consulta de medios de pago exitosa con parametros: {params_a_probar}")
                            data_module.medios_pagos = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de medios de pago con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de medios de pago no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de medios de pago (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de medios de pago con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de medios de pago con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_medios_pagos'):
        query_params.update(data_module.parametros_medios_pagos)
        logger.info(f"Parametros principales cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA MEDIOS DE PAGO: {query_params}")
    
    # Probar primero con los parámetros principales
    exito_principal = probar_parametros(query_params, " PRINCIPALES")
    
    # Si no hubo éxito con los parámetros principales, intentar sin filtros
    if not exito_principal and query_params:
        logger.info("=== REINTENTANDO SIN PARAMETROS ===")
        probar_parametros({}, " SIN FILTROS")
    
    # Registrar el resultado final
    if exito_principal:
        logger.info("Consulta de medios de pago completada exitosamente")
    else:
        logger.warning("Consulta de medios de pago completada con advertencias")


def get_cfiscal(client, logger, environment, data_module):
    """Prueba el endpoint de consultar condiciones fiscales"""
    
    logger.info("Ejecutando get_cfiscal")
    
    # Obtener parámetros desde data_module (aunque este endpoint no usa parámetros)
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_cfiscal'):
        query_params.update(data_module.parametros_cfiscal)
        logger.info(f"Parametros cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto
        query_params = {}
        logger.info("Usando parametros vacios (endpoint no requiere parametros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA CONDICIONES FISCALES: {query_params}")
    
    try:
        logger.info(f"Enviando solicitud con parametros: {query_params}")
        logger.info(f"URL completa: /cfiscal")
        
        with client.get(
            "/cfiscal",
            params=query_params if query_params else None,
            catch_response=True,
            name="(PARAMETRICAS) - /cfiscal [GET]"
        ) as response:
            # Guardar la respuesta completa en el log (limitada para evitar saturación)
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, list):
                        logger.info(f"Respuesta recibida: {len(response_data)} condiciones fiscales encontradas")
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
                    logger.info("=== RESUMEN DE LA RESPUESTA (CONDICIONES FISCALES) ===")
                    logger.info("Sin parametros de consulta (endpoint no los requiere)")
                    logger.info(f"Endpoint usado: /cfiscal")
                    
                    # Validar estructura de datos esperada (lista directa de diccionarios)
                    if isinstance(response_data, list):
                        # Respuesta directa como lista (formato esperado según el schema)
                        cantidad_condiciones = len(response_data)
                        logger.info(f"Se encontraron {cantidad_condiciones} condiciones fiscales")
                        
                        if cantidad_condiciones > 0:
                            # Verificar el primer elemento para determinar la estructura real
                            primer_elemento = response_data[0]
                            campos_disponibles = list(primer_elemento.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de condiciones fiscales
                            tiene_campos_basicos = any(
                                campo in primer_elemento 
                                for campo in ["id_condicion_fiscal", "nombre", "id", "descripcion", "codigo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info("Consulta de condiciones fiscales exitosa")
                                
                                # Mostrar información de todas las condiciones fiscales encontradas
                                for idx, condicion in enumerate(response_data):
                                    # Mostrar información relevante según los campos disponibles
                                    if "nombre" in condicion:
                                        logger.info(f"Condicion Fiscal {idx+1}: {condicion.get('nombre')}")
                                    elif "descripcion" in condicion:
                                        logger.info(f"Condicion Fiscal {idx+1}: {condicion.get('descripcion')}")
                                    else:
                                        # Mostrar el primer campo que contenga información útil
                                        for key, value in condicion.items():
                                            if isinstance(value, str) and len(value) > 0:
                                                logger.info(f"Condicion Fiscal {idx+1}: {key}={value}")
                                                break
                                    
                                    # Mostrar información adicional de la condición fiscal
                                    if "id_condicion_fiscal" in condicion:
                                        logger.info(f"  ID Condicion Fiscal: {condicion.get('id_condicion_fiscal')}")
                                    if "id" in condicion and "id_condicion_fiscal" not in condicion:
                                        logger.info(f"  ID: {condicion.get('id')}")
                                    if "codigo" in condicion and condicion.get("codigo"):
                                        logger.info(f"  Codigo: {condicion.get('codigo')}")
                                    if "descripcion" in condicion and condicion.get("descripcion") and "nombre" in condicion:
                                        logger.info(f"  Descripcion: {condicion.get('descripcion')}")
                                    if "estado" in condicion and condicion.get("estado"):
                                        logger.info(f"  Estado: {condicion.get('estado')}")
                                    if "activo" in condicion and condicion.get("activo") is not None:
                                        logger.info(f"  Activo: {condicion.get('activo')}")
                                    if "fecha_creacion" in condicion and condicion.get("fecha_creacion"):
                                        logger.info(f"  Fecha Creacion: {condicion.get('fecha_creacion')}")
                                    if "fecha_modificacion" in condicion and condicion.get("fecha_modificacion"):
                                        logger.info(f"  Fecha Modificacion: {condicion.get('fecha_modificacion')}")
                                
                                # Estadísticas adicionales
                                logger.info(f"Total de condiciones fiscales encontradas: {cantidad_condiciones}")
                                
                                # Mostrar lista de nombres de condiciones fiscales para referencia
                                nombres_condiciones = []
                                for condicion in response_data:
                                    if "nombre" in condicion:
                                        nombres_condiciones.append(condicion.get("nombre"))
                                
                                if nombres_condiciones:
                                    logger.info(f"Condiciones fiscales disponibles: {', '.join(nombres_condiciones)}")
                                
                                # Agrupar por estado si está disponible
                                if cantidad_condiciones > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                    estados = {}
                                    for condicion in response_data:
                                        if "estado" in condicion:
                                            estado = condicion.get("estado", "Sin estado")
                                        elif "activo" in condicion:
                                            estado = "Activo" if condicion.get("activo") else "Inactivo"
                                        else:
                                            estado = "Sin estado"
                                        estados[estado] = estados.get(estado, 0) + 1
                                    logger.info(f"Condiciones fiscales por estado: {estados}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                data_module.condiciones_fiscales = response_data
                            else:
                                response.failure("Los elementos no tienen campos reconocibles de condiciones fiscales")
                                logger.warning(f"Estructura de datos no reconocida: {primer_elemento}")
                        else:
                            # Si no se encontraron condiciones fiscales
                            logger.warning("No se encontraron condiciones fiscales")
                            response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                    
                    elif isinstance(response_data, dict):
                        # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                        logger.info("Respuesta recibida como objeto")
                        logger.info(f"Claves disponibles: {list(response_data.keys())}")
                        
                        # Verificar si es una respuesta con items
                        if "items" in response_data:
                            items = response_data["items"]
                            logger.info(f"Se encontraron {len(items)} condiciones fiscales en items")
                            
                            if len(items) > 0:
                                primer_elemento = items[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles: {campos_disponibles}")
                                
                                # Mostrar algunas condiciones fiscales
                                for idx, condicion in enumerate(items):
                                    if "nombre" in condicion:
                                        logger.info(f"Condicion Fiscal {idx+1}: {condicion.get('nombre')}")
                                    elif "id_condicion_fiscal" in condicion:
                                        logger.info(f"Condicion Fiscal {idx+1}: ID {condicion.get('id_condicion_fiscal')}")
                                
                                data_module.condiciones_fiscales = response_data
                        
                        response.success()
                        logger.info("Consulta de condiciones fiscales exitosa")
                        data_module.condiciones_fiscales = response_data
                    else:
                        response.failure("Formato de respuesta inesperado")
                        logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON invalido en respuesta: {response.text[:200]}")
            elif response.status_code == 403:
                # Posible falta de permisos
                logger.warning("Acceso denegado al endpoint de condiciones fiscales (403)")
                response.failure("Acceso denegado - verificar permisos")
            elif response.status_code == 404:
                # Endpoint no encontrado
                logger.warning("Endpoint de condiciones fiscales no encontrado (404)")
                response.failure("Endpoint no encontrado")
            elif response.status_code == 500:
                # Error interno del servidor
                logger.error("Error interno del servidor en endpoint de condiciones fiscales (500)")
                response.failure("Error interno del servidor")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de condiciones fiscales: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"Excepcion durante consulta de condiciones fiscales: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.get(
            "/cfiscal",
            catch_response=True,
            name="(PARAMETRICAS) - /cfiscal [Exception]"
        ) as response:
            response.failure(f"Excepcion: {str(e)}")

def get_fjuridica(client, logger, environment, data_module):
    """Prueba el endpoint de consultar formas jurídicas"""
    
    logger.info("Ejecutando get_fjuridica")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/fjuridica",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /fjuridica "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} formas jurídicas encontradas")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (FORMAS JURÍDICAS) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta (todas las formas jurídicas)")
                        logger.info(f"Endpoint usado: /fjuridica")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_formas = len(response_data)
                            logger.info(f"Se encontraron {cantidad_formas} formas jurídicas")
                            
                            if cantidad_formas > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de formas jurídicas
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["id_forma_juridica", "nombre", "id", "descripcion", "codigo"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de formas jurídicas exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de las formas jurídicas encontradas
                                    for idx, forma in enumerate(response_data):
                                        # Mostrar información relevante según los campos disponibles
                                        if "nombre" in forma:
                                            logger.info(f"Forma Jurídica {idx+1}: {forma.get('nombre')}")
                                        elif "id_forma_juridica" in forma:
                                            logger.info(f"Forma Jurídica {idx+1}: ID {forma.get('id_forma_juridica')}")
                                        elif "id" in forma:
                                            logger.info(f"Forma Jurídica {idx+1}: ID {forma.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in forma.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Forma Jurídica {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional de la forma jurídica
                                        if "id_forma_juridica" in forma:
                                            logger.info(f"  ID Forma Jurídica: {forma.get('id_forma_juridica')}")
                                        if "descripcion" in forma and forma.get("descripcion"):
                                            logger.info(f"  Descripcion: {forma.get('descripcion')}")
                                        if "codigo" in forma and forma.get("codigo"):
                                            logger.info(f"  Codigo: {forma.get('codigo')}")
                                        if "estado" in forma and forma.get("estado"):
                                            logger.info(f"  Estado: {forma.get('estado')}")
                                        if "activo" in forma and forma.get("activo") is not None:
                                            logger.info(f"  Activo: {forma.get('activo')}")
                                        if "observaciones" in forma and forma.get("observaciones"):
                                            logger.info(f"  Observaciones: {forma.get('observaciones')}")
                                        if "fecha_creacion" in forma and forma.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {forma.get('fecha_creacion')}")
                                        if "fecha_modificacion" in forma and forma.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {forma.get('fecha_modificacion')}")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de formas jurídicas encontradas: {cantidad_formas}")
                                    
                                    # Mostrar lista de nombres de formas jurídicas para referencia
                                    nombres_formas = []
                                    for forma in response_data:
                                        if "nombre" in forma:
                                            nombres_formas.append(forma.get("nombre"))
                                    
                                    if nombres_formas:
                                        logger.info(f"Formas jurídicas disponibles: {', '.join(nombres_formas)}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_formas > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for forma in response_data:
                                            if "estado" in forma:
                                                estado = forma.get("estado", "Sin estado")
                                            elif "activo" in forma:
                                                estado = "Activo" if forma.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Formas jurídicas por estado: {estados}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.formas_juridicas = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de formas jurídicas")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron formas jurídicas
                                logger.warning(f"No se encontraron formas jurídicas con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} formas jurídicas en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunas formas jurídicas
                                    for idx, forma in enumerate(items[:10]):
                                        if "nombre" in forma:
                                            logger.info(f"Forma Jurídica {idx+1}: {forma.get('nombre')}")
                                        elif "id_forma_juridica" in forma:
                                            logger.info(f"Forma Jurídica {idx+1}: ID {forma.get('id_forma_juridica')}")
                                    
                                    data_module.formas_juridicas = response_data
                            
                            response.success()
                            logger.info(f"Consulta de formas jurídicas exitosa con parametros: {params_a_probar}")
                            data_module.formas_juridicas = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de formas jurídicas con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de formas jurídicas no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de formas jurídicas (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de formas jurídicas con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de formas jurídicas con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_fjuridica'):
        query_params.update(data_module.parametros_fjuridica)
        logger.info(f"Parametros principales cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA FORMAS JURÍDICAS: {query_params}")
    
    # Probar con los parámetros principales
    exito_principal = probar_parametros(query_params, " PRINCIPALES")
    
    # Si no hubo éxito con los parámetros principales, intentar sin filtros
    if not exito_principal and query_params:
        logger.info("=== REINTENTANDO SIN PARAMETROS ===")
        probar_parametros({}, " SIN FILTROS")
    
    # Registrar el resultado final
    if exito_principal:
        logger.info("Consulta de formas jurídicas completada exitosamente")
    else:
        logger.warning("Consulta de formas jurídicas completada con advertencias")

def get_bancos(client, logger, environment, data_module):
    """Prueba el endpoint de consultar bancos"""
    
    logger.info("Ejecutando get_bancos")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/bancos",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /bancos "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} bancos encontrados")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (BANCOS) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta (todos los bancos)")
                        logger.info(f"Endpoint usado: /bancos")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_bancos = len(response_data)
                            logger.info(f"Se encontraron {cantidad_bancos} bancos")
                            
                            if cantidad_bancos > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de bancos
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["p_id_banco", "p_nombre", "id_banco", "nombre", "id", "codigo"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de bancos exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de los bancos encontrados (hasta 20)
                                    for idx, banco in enumerate(response_data[:20]):
                                        # Mostrar información relevante según los campos disponibles
                                        if "p_nombre" in banco:
                                            logger.info(f"Banco {idx+1}: {banco.get('p_nombre')}")
                                        elif "nombre" in banco:
                                            logger.info(f"Banco {idx+1}: {banco.get('nombre')}")
                                        elif "p_id_banco" in banco:
                                            logger.info(f"Banco {idx+1}: ID {banco.get('p_id_banco')}")
                                        elif "id_banco" in banco:
                                            logger.info(f"Banco {idx+1}: ID {banco.get('id_banco')}")
                                        elif "id" in banco:
                                            logger.info(f"Banco {idx+1}: ID {banco.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in banco.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Banco {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional del banco
                                        if "p_id_banco" in banco:
                                            logger.info(f"  ID Banco: {banco.get('p_id_banco')}")
                                        elif "id_banco" in banco and "p_id_banco" not in banco:
                                            logger.info(f"  ID Banco: {banco.get('id_banco')}")
                                        if "codigo" in banco and banco.get("codigo"):
                                            logger.info(f"  Codigo: {banco.get('codigo')}")
                                        if "codigo_bcra" in banco and banco.get("codigo_bcra"):
                                            logger.info(f"  Codigo BCRA: {banco.get('codigo_bcra')}")
                                        if "descripcion" in banco and banco.get("descripcion"):
                                            logger.info(f"  Descripcion: {banco.get('descripcion')}")
                                        if "estado" in banco and banco.get("estado"):
                                            logger.info(f"  Estado: {banco.get('estado')}")
                                        if "activo" in banco and banco.get("activo") is not None:
                                            logger.info(f"  Activo: {banco.get('activo')}")
                                        if "fecha_creacion" in banco and banco.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {banco.get('fecha_creacion')}")
                                        if "fecha_modificacion" in banco and banco.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {banco.get('fecha_modificacion')}")
                                    
                                    # Si hay más de 20 bancos, indicar cuántos más hay
                                    if cantidad_bancos > 20:
                                        logger.info(f"... y {cantidad_bancos - 20} bancos mas")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de bancos encontrados: {cantidad_bancos}")
                                    
                                    # Mostrar lista de nombres de bancos para referencia (primeros 10)
                                    nombres_bancos = []
                                    for banco in response_data[:10]:
                                        if "p_nombre" in banco:
                                            nombres_bancos.append(banco.get("p_nombre"))
                                        elif "nombre" in banco:
                                            nombres_bancos.append(banco.get("nombre"))
                                    
                                    if nombres_bancos:
                                        logger.info(f"Primeros bancos disponibles: {', '.join(nombres_bancos)}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_bancos > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for banco in response_data:
                                            if "estado" in banco:
                                                estado = banco.get("estado", "Sin estado")
                                            elif "activo" in banco:
                                                estado = "Activo" if banco.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Bancos por estado: {estados}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.bancos = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de bancos")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron bancos
                                logger.warning(f"No se encontraron bancos con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} bancos en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunos bancos
                                    for idx, banco in enumerate(items[:10]):
                                        if "p_nombre" in banco:
                                            logger.info(f"Banco {idx+1}: {banco.get('p_nombre')}")
                                        elif "nombre" in banco:
                                            logger.info(f"Banco {idx+1}: {banco.get('nombre')}")
                                        elif "p_id_banco" in banco:
                                            logger.info(f"Banco {idx+1}: ID {banco.get('p_id_banco')}")
                                    
                                    data_module.bancos = response_data
                            
                            response.success()
                            logger.info(f"Consulta de bancos exitosa con parametros: {params_a_probar}")
                            data_module.bancos = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de bancos con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de bancos no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de bancos (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de bancos con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de bancos con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_bancos'):
        query_params.update(data_module.parametros_bancos)
        logger.info(f"Parametros principales cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA BANCOS: {query_params}")
    
    # Probar con los parámetros principales
    exito_principal = probar_parametros(query_params, " PRINCIPALES")
    
    # Si no hubo éxito con los parámetros principales, intentar sin filtros
    if not exito_principal and query_params:
        logger.info("=== REINTENTANDO SIN PARAMETROS ===")
        probar_parametros({}, " SIN FILTROS")
    
    # Registrar el resultado final
    if exito_principal:
        logger.info("Consulta de bancos completada exitosamente")
    else:
        logger.warning("Consulta de bancos completada con advertencias")


def get_banco_by_id(client, logger, environment, data_module):
    """Prueba el endpoint de consultar banco por ID"""
    
    logger.info("Ejecutando get_banco_by_id")
    
    # Función auxiliar para probar con diferentes IDs de banco
    def probar_id_banco(id_banco, descripcion=""):
        logger.info(f"=== PROBANDO ID BANCO{descripcion}: {id_banco} ===")
        
        try:
            with client.get(
                f"/bancos/{id_banco}",
                catch_response=True,
                name=f"(PARAMETRICAS) - /bancos/{{id}} "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        logger.info(f"Respuesta recibida para ID {id_banco}: {response.text[:200]}...")
                    except:
                        logger.info(f"Respuesta recibida (no JSON) para ID {id_banco}: {response.text[:100]}...")
                else:
                    logger.info(f"Respuesta completa para ID {id_banco}: {response.text}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar un resumen de los datos obtenidos en el log
                        logger.info("=== RESUMEN DE LA RESPUESTA (BANCO POR ID) ===")
                        logger.info(f"ID Banco consultado: {id_banco}")
                        logger.info(f"Endpoint usado: /bancos/{id_banco}")
                        
                        # Validar estructura de datos esperada (objeto único)
                        if isinstance(response_data, dict):
                            # Respuesta como objeto único (formato esperado según el schema)
                            campos_disponibles = list(response_data.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de banco
                            tiene_campos_basicos = any(
                                campo in response_data 
                                for campo in ["p_id_banco", "p_nombre", "id_banco", "nombre", "id", "codigo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info(f"Consulta de banco por ID exitosa: {id_banco}")
                                
                                # Mostrar información del banco encontrado
                                if "p_nombre" in response_data:
                                    logger.info(f"Banco encontrado: {response_data.get('p_nombre')}")
                                elif "nombre" in response_data:
                                    logger.info(f"Banco encontrado: {response_data.get('nombre')}")
                                
                                # Mostrar información adicional del banco
                                if "p_id_banco" in response_data:
                                    logger.info(f"  ID Banco: {response_data.get('p_id_banco')}")
                                elif "id_banco" in response_data:
                                    logger.info(f"  ID Banco: {response_data.get('id_banco')}")
                                elif "id" in response_data:
                                    logger.info(f"  ID: {response_data.get('id')}")
                                
                                if "codigo" in response_data and response_data.get("codigo"):
                                    logger.info(f"  Codigo: {response_data.get('codigo')}")
                                if "codigo_bcra" in response_data and response_data.get("codigo_bcra"):
                                    logger.info(f"  Codigo BCRA: {response_data.get('codigo_bcra')}")
                                if "descripcion" in response_data and response_data.get("descripcion"):
                                    logger.info(f"  Descripcion: {response_data.get('descripcion')}")
                                if "estado" in response_data and response_data.get("estado"):
                                    logger.info(f"  Estado: {response_data.get('estado')}")
                                if "activo" in response_data and response_data.get("activo") is not None:
                                    logger.info(f"  Activo: {response_data.get('activo')}")
                                if "fecha_creacion" in response_data and response_data.get("fecha_creacion"):
                                    logger.info(f"  Fecha Creacion: {response_data.get('fecha_creacion')}")
                                if "fecha_modificacion" in response_data and response_data.get("fecha_modificacion"):
                                    logger.info(f"  Fecha Modificacion: {response_data.get('fecha_modificacion')}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                if not hasattr(data_module, 'banco_por_id'):
                                    data_module.banco_por_id = {}
                                data_module.banco_por_id[id_banco] = response_data
                                return True  # Éxito
                            else:
                                response.failure("El objeto no tiene campos reconocibles de banco")
                                logger.warning(f"Estructura de datos no reconocida para ID {id_banco}: {response_data}")
                                return False
                        
                        elif isinstance(response_data, list):
                            # Si retorna una lista (caso inesperado pero posible)
                            logger.info(f"Respuesta recibida como lista para ID {id_banco}")
                            if len(response_data) > 0:
                                primer_elemento = response_data[0]
                                logger.info(f"Primer elemento: {primer_elemento}")
                                
                                # Guardar los datos
                                if not hasattr(data_module, 'banco_por_id'):
                                    data_module.banco_por_id = {}
                                data_module.banco_por_id[id_banco] = response_data
                            
                            response.success()
                            logger.info(f"Consulta de banco por ID exitosa: {id_banco}")
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para ID {id_banco}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para ID {id_banco}: {response.text[:200]}")
                        return False
                elif response.status_code == 404:
                    # Banco no encontrado
                    logger.warning(f"Banco con ID {id_banco} no encontrado (404)")
                    response.failure(f"Banco con ID {id_banco} no existe")
                    return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con ID {id_banco} (422)")
                    response.failure("ID de banco invalido - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de banco por ID {id_banco} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de banco por ID {id_banco} (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de banco por ID {id_banco}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de banco por ID {id_banco}: {str(e)}")
            return False
    
    # Obtener IDs de banco desde data_module
    ids_banco_a_probar = []
    
    # Verificar que existan los IDs de banco
    if hasattr(data_module, 'ids_banco'):
        ids_banco_a_probar = data_module.ids_banco
        logger.info(f"IDs de banco cargados desde data_module: {ids_banco_a_probar}")
    else:
        logger.warning("No se encontraron IDs de banco en data_module")
        return
    
    # Mostrar claramente los IDs que se van a probar
    logger.info(f"IDS DE BANCO A PROBAR: {ids_banco_a_probar}")
    
    # Probar cada ID de banco
    resultados_exitosos = 0
    total_ids = len(ids_banco_a_probar)
    
    for idx, id_banco in enumerate(ids_banco_a_probar):
        logger.info(f"=== PROBANDO ID {idx + 1} DE {total_ids}: {id_banco} ===")
        
        if probar_id_banco(id_banco, f" [{idx + 1}/{total_ids}]"):
            resultados_exitosos += 1
        
        # Pequeña pausa entre requests para no sobrecargar el servidor
        import time
        time.sleep(0.1)
    
    # Registrar el resultado final
    logger.info(f"=== RESUMEN FINAL ===")
    logger.info(f"Total de IDs probados: {total_ids}")
    logger.info(f"Consultas exitosas: {resultados_exitosos}")
    logger.info(f"Consultas fallidas: {total_ids - resultados_exitosos}")
    
    if resultados_exitosos > 0:
        logger.info("Consulta de bancos por ID completada con éxito")
    else:
        logger.warning("Ninguna consulta de banco por ID fue exitosa")


def get_profesiones(client, logger, environment, data_module):
    """Prueba el endpoint de consultar profesiones"""
    
    logger.info("Ejecutando get_profesiones")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/profesiones",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /profesiones "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} profesiones encontradas")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (PROFESIONES) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta (todas las profesiones)")
                        logger.info(f"Endpoint usado: /profesiones")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_profesiones = len(response_data)
                            logger.info(f"Se encontraron {cantidad_profesiones} profesiones")
                            
                            if cantidad_profesiones > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de profesiones
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["p_id_profesion", "p_nombre", "id_profesion", "nombre", "id", "codigo"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de profesiones exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de las profesiones encontradas (hasta 20)
                                    for idx, profesion in enumerate(response_data[:20]):
                                        # Mostrar información relevante según los campos disponibles
                                        if "p_nombre" in profesion:
                                            logger.info(f"Profesion {idx+1}: {profesion.get('p_nombre')}")
                                        elif "nombre" in profesion:
                                            logger.info(f"Profesion {idx+1}: {profesion.get('nombre')}")
                                        elif "p_id_profesion" in profesion:
                                            logger.info(f"Profesion {idx+1}: ID {profesion.get('p_id_profesion')}")
                                        elif "id_profesion" in profesion:
                                            logger.info(f"Profesion {idx+1}: ID {profesion.get('id_profesion')}")
                                        elif "id" in profesion:
                                            logger.info(f"Profesion {idx+1}: ID {profesion.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in profesion.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Profesion {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional de la profesión
                                        if "p_id_profesion" in profesion:
                                            logger.info(f"  ID Profesion: {profesion.get('p_id_profesion')}")
                                        elif "id_profesion" in profesion and "p_id_profesion" not in profesion:
                                            logger.info(f"  ID Profesion: {profesion.get('id_profesion')}")
                                        if "codigo" in profesion and profesion.get("codigo"):
                                            logger.info(f"  Codigo: {profesion.get('codigo')}")
                                        if "descripcion" in profesion and profesion.get("descripcion"):
                                            logger.info(f"  Descripcion: {profesion.get('descripcion')}")
                                        if "estado" in profesion and profesion.get("estado"):
                                            logger.info(f"  Estado: {profesion.get('estado')}")
                                        if "activo" in profesion and profesion.get("activo") is not None:
                                            logger.info(f"  Activo: {profesion.get('activo')}")
                                        if "fecha_creacion" in profesion and profesion.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {profesion.get('fecha_creacion')}")
                                        if "fecha_modificacion" in profesion and profesion.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {profesion.get('fecha_modificacion')}")
                                    
                                    # Si hay más de 20 profesiones, indicar cuántos más hay
                                    if cantidad_profesiones > 20:
                                        logger.info(f"... y {cantidad_profesiones - 20} profesiones mas")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de profesiones encontradas: {cantidad_profesiones}")
                                    
                                    # Mostrar lista de nombres de profesiones para referencia (primeros 10)
                                    nombres_profesiones = []
                                    for profesion in response_data[:10]:
                                        if "p_nombre" in profesion:
                                            nombres_profesiones.append(profesion.get("p_nombre"))
                                        elif "nombre" in profesion:
                                            nombres_profesiones.append(profesion.get("nombre"))
                                    
                                    if nombres_profesiones:
                                        logger.info(f"Primeras profesiones disponibles: {', '.join(nombres_profesiones)}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_profesiones > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for profesion in response_data:
                                            if "estado" in profesion:
                                                estado = profesion.get("estado", "Sin estado")
                                            elif "activo" in profesion:
                                                estado = "Activo" if profesion.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Profesiones por estado: {estados}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.profesiones = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de profesiones")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron profesiones
                                logger.warning(f"No se encontraron profesiones con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} profesiones en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunas profesiones
                                    for idx, profesion in enumerate(items[:10]):
                                        if "p_nombre" in profesion:
                                            logger.info(f"Profesion {idx+1}: {profesion.get('p_nombre')}")
                                        elif "nombre" in profesion:
                                            logger.info(f"Profesion {idx+1}: {profesion.get('nombre')}")
                                        elif "p_id_profesion" in profesion:
                                            logger.info(f"Profesion {idx+1}: ID {profesion.get('p_id_profesion')}")
                                    
                                    data_module.profesiones = response_data
                            
                            response.success()
                            logger.info(f"Consulta de profesiones exitosa con parametros: {params_a_probar}")
                            data_module.profesiones = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de profesiones con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de profesiones no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de profesiones (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de profesiones con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de profesiones con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_profesiones'):
        query_params.update(data_module.parametros_profesiones)
        logger.info(f"Parametros principales cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA PROFESIONES: {query_params}")
    
    # Probar con los parámetros principales
    exito_principal = probar_parametros(query_params, " PRINCIPALES")
    
    # Si no hubo éxito con los parámetros principales, intentar sin filtros
    if not exito_principal and query_params:
        logger.info("=== REINTENTANDO SIN PARAMETROS ===")
        probar_parametros({}, " SIN FILTROS")
    
    # Registrar el resultado final
    if exito_principal:
        logger.info("✅ Consulta de profesiones completada exitosamente")
    else:
        logger.warning("⚠️ Consulta de profesiones completada con advertencias")

def get_profesion_by_id(client, logger, environment, data_module):
    """Prueba el endpoint de consultar profesión por ID"""
    
    logger.info("Ejecutando get_profesion_by_id")
    
    # Función auxiliar para probar con diferentes IDs de profesión
    def probar_id_profesion(id_profesion, descripcion=""):
        logger.info(f"=== PROBANDO ID PROFESION{descripcion}: {id_profesion} ===")
        
        try:
            with client.get(
                f"/profesiones/{id_profesion}",
                catch_response=True,
                name=f"(PARAMETRICAS) - /profesiones/{{id}} "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        logger.info(f"Respuesta recibida para ID {id_profesion}: {response.text[:200]}...")
                    except:
                        logger.info(f"Respuesta recibida (no JSON) para ID {id_profesion}: {response.text[:100]}...")
                else:
                    logger.info(f"Respuesta completa para ID {id_profesion}: {response.text}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar un resumen de los datos obtenidos en el log
                        logger.info("=== RESUMEN DE LA RESPUESTA (PROFESION POR ID) ===")
                        logger.info(f"ID Profesion consultado: {id_profesion}")
                        logger.info(f"Endpoint usado: /profesiones/{id_profesion}")
                        
                        # Validar estructura de datos esperada (objeto único)
                        if isinstance(response_data, dict):
                            # Respuesta como objeto único (formato esperado según el schema)
                            campos_disponibles = list(response_data.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de profesión
                            tiene_campos_basicos = any(
                                campo in response_data 
                                for campo in ["p_id_profesion", "p_nombre", "id_profesion", "nombre", "id", "codigo"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                logger.info(f"Consulta de profesion por ID exitosa: {id_profesion}")
                                
                                # Mostrar información de la profesión encontrada
                                if "p_nombre" in response_data:
                                    logger.info(f"Profesion encontrada: {response_data.get('p_nombre')}")
                                elif "nombre" in response_data:
                                    logger.info(f"Profesion encontrada: {response_data.get('nombre')}")
                                
                                # Mostrar información adicional de la profesión
                                if "p_id_profesion" in response_data:
                                    logger.info(f"  ID Profesion: {response_data.get('p_id_profesion')}")
                                elif "id_profesion" in response_data:
                                    logger.info(f"  ID Profesion: {response_data.get('id_profesion')}")
                                elif "id" in response_data:
                                    logger.info(f"  ID: {response_data.get('id')}")
                                
                                if "codigo" in response_data and response_data.get("codigo"):
                                    logger.info(f"  Codigo: {response_data.get('codigo')}")
                                if "descripcion" in response_data and response_data.get("descripcion"):
                                    logger.info(f"  Descripcion: {response_data.get('descripcion')}")
                                if "estado" in response_data and response_data.get("estado"):
                                    logger.info(f"  Estado: {response_data.get('estado')}")
                                if "activo" in response_data and response_data.get("activo") is not None:
                                    logger.info(f"  Activo: {response_data.get('activo')}")
                                if "fecha_creacion" in response_data and response_data.get("fecha_creacion"):
                                    logger.info(f"  Fecha Creacion: {response_data.get('fecha_creacion')}")
                                if "fecha_modificacion" in response_data and response_data.get("fecha_modificacion"):
                                    logger.info(f"  Fecha Modificacion: {response_data.get('fecha_modificacion')}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                if not hasattr(data_module, 'profesion_por_id'):
                                    data_module.profesion_por_id = {}
                                data_module.profesion_por_id[id_profesion] = response_data
                                return True  # Éxito
                            else:
                                response.failure("El objeto no tiene campos reconocibles de profesión")
                                logger.warning(f"Estructura de datos no reconocida para ID {id_profesion}: {response_data}")
                                return False
                        
                        elif isinstance(response_data, list):
                            # Si retorna una lista (caso inesperado pero posible)
                            logger.info(f"Respuesta recibida como lista para ID {id_profesion}")
                            if len(response_data) > 0:
                                primer_elemento = response_data[0]
                                logger.info(f"Primer elemento: {primer_elemento}")
                                
                                # Guardar los datos
                                if not hasattr(data_module, 'profesion_por_id'):
                                    data_module.profesion_por_id = {}
                                data_module.profesion_por_id[id_profesion] = response_data
                            
                            response.success()
                            logger.info(f"Consulta de profesion por ID exitosa: {id_profesion}")
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para ID {id_profesion}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para ID {id_profesion}: {response.text[:200]}")
                        return False
                elif response.status_code == 404:
                    # Profesión no encontrada
                    logger.warning(f"Profesion con ID {id_profesion} no encontrada (404)")
                    response.failure(f"Profesion con ID {id_profesion} no existe")
                    return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con ID {id_profesion} (422)")
                    response.failure("ID de profesion invalido - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de profesion por ID {id_profesion} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de profesion por ID {id_profesion} (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de profesion por ID {id_profesion}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de profesion por ID {id_profesion}: {str(e)}")
            return False
    
    # Obtener IDs de profesión desde data_module
    ids_profesion_a_probar = []
    
    # Verificar que existan los IDs de profesión
    if hasattr(data_module, 'ids_profesion'):
        ids_profesion_a_probar = data_module.ids_profesion
        logger.info(f"IDs de profesion cargados desde data_module: {ids_profesion_a_probar}")
    else:
        logger.warning("No se encontraron IDs de profesion en data_module")
        return
    
    # Mostrar claramente los IDs que se van a probar
    logger.info(f"IDS DE PROFESION A PROBAR: {ids_profesion_a_probar}")
    
    # Probar cada ID de profesión
    resultados_exitosos = 0
    total_ids = len(ids_profesion_a_probar)
    
    for idx, id_profesion in enumerate(ids_profesion_a_probar):
        logger.info(f"=== PROBANDO ID {idx + 1} DE {total_ids}: {id_profesion} ===")
        
        if probar_id_profesion(id_profesion, f" [{idx + 1}/{total_ids}]"):
            resultados_exitosos += 1
        
        # Pequeña pausa entre requests para no sobrecargar el servidor
        import time
        time.sleep(0.1)
    
    # Registrar el resultado final
    logger.info(f"=== RESUMEN FINAL ===")
    logger.info(f"Total de IDs probados: {total_ids}")
    logger.info(f"Consultas exitosas: {resultados_exitosos}")
    logger.info(f"Consultas fallidas: {total_ids - resultados_exitosos}")
    
    if resultados_exitosos > 0:
        logger.info("Consulta de profesiones por ID completada con éxito")
    else:
        logger.warning("Ninguna consulta de profesion por ID fue exitosa")

def put_medios_pagos(client, logger, environment, data_module):
    """Prueba el endpoint de crear o actualizar medios de pago"""
    
    logger.info("Ejecutando put_medios_pagos")
    
    # Función auxiliar para probar diferentes cuerpos de solicitud
    def probar_body(body_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO BODY{descripcion}: {body_a_probar} ===")
        
        try:
            with client.put(
                "/medios_pagos",
                json=body_a_probar,
                catch_response=True,
                name=f"(PARAMETRICAS) - /medios_pagos [PUT{descripcion}]"
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code in [200, 201]:
                    try:
                        response_data = response.json()
                        logger.info(f"Respuesta recibida: {response.text[:200]}...")
                    except:
                        logger.info(f"Respuesta recibida (no JSON): {response.text[:100]}...")
                else:
                    logger.info(f"Respuesta completa: {response.text}")
                
                if response.status_code in [200, 201]:  # HTTP 200 OK o 201 CREATED
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Guardar un resumen de los datos obtenidos en el log
                        logger.info("=== RESUMEN DE LA RESPUESTA (PUT MEDIOS DE PAGO) ===")
                        logger.info(f"Body enviado: {body_a_probar}")
                        logger.info(f"Endpoint usado: /medios_pagos [PUT]")
                        logger.info(f"Status code: {response.status_code}")
                        
                        # Validar estructura de datos esperada
                        if isinstance(response_data, dict):
                            # Respuesta como objeto único (formato esperado según el schema)
                            campos_disponibles = list(response_data.keys())
                            logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                            
                            # Verificar si al menos tiene algunos campos básicos de respuesta
                            tiene_campos_basicos = any(
                                campo in response_data 
                                for campo in ["id_medio_pago", "p_nombre", "nombre", "id", "id_sistema_permisionados"]
                            )
                            
                            if tiene_campos_basicos:
                                response.success()
                                
                                if response.status_code == 201:
                                    logger.info(f"Medio de pago creado exitosamente")
                                else:
                                    logger.info(f"Medio de pago actualizado exitosamente")
                                
                                # Mostrar información del medio de pago creado/actualizado
                                if "p_nombre" in response_data:
                                    logger.info(f"Nombre: {response_data.get('p_nombre')}")
                                elif "nombre" in response_data:
                                    logger.info(f"Nombre: {response_data.get('nombre')}")
                                
                                # Mostrar información adicional
                                if "id_medio_pago" in response_data:
                                    logger.info(f"  ID Medio Pago: {response_data.get('id_medio_pago')}")
                                elif "id" in response_data:
                                    logger.info(f"  ID: {response_data.get('id')}")
                                
                                if "id_sistema_permisionados" in response_data:
                                    logger.info(f"  ID Sistema Permisionados: {response_data.get('id_sistema_permisionados')}")
                                if "calidad_dato" in response_data:
                                    logger.info(f"  Calidad Dato: {response_data.get('calidad_dato')}")
                                if "estado" in response_data:
                                    logger.info(f"  Estado: {response_data.get('estado')}")
                                if "fecha_creacion" in response_data:
                                    logger.info(f"  Fecha Creacion: {response_data.get('fecha_creacion')}")
                                if "fecha_modificacion" in response_data:
                                    logger.info(f"  Fecha Modificacion: {response_data.get('fecha_modificacion')}")
                                
                                # Guardar los datos para posibles pruebas futuras
                                if not hasattr(data_module, 'medios_pagos_creados'):
                                    data_module.medios_pagos_creados = []
                                data_module.medios_pagos_creados.append(response_data)
                                return True  # Éxito
                            else:
                                response.failure("El objeto no tiene campos reconocibles de medio de pago")
                                logger.warning(f"Estructura de datos no reconocida: {response_data}")
                                return False
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en el body
                    logger.warning(f"Error de validacion en body (422)")
                    response.failure("Body invalido - verificar formato y campos requeridos")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de medios de pago (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de medios de pago no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de medios de pago (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en creacion/actualizacion de medio de pago: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante creacion/actualizacion de medio de pago: {str(e)}")
            return False
    
    # Obtener bodies desde data_module
    bodies_a_probar = []
    
    # Verificar que existan los bodies
    if hasattr(data_module, 'body_medios_pagos'):
        bodies_a_probar = data_module.body_medios_pagos
        logger.info(f"Bodies cargados desde data_module: {len(bodies_a_probar)} elementos")
    else:
        logger.warning("No se encontraron bodies para medios de pago en data_module")
        return
    
    # Mostrar claramente los bodies que se van a probar
    logger.info(f"BODIES A PROBAR: {len(bodies_a_probar)} elementos")
    
    # Probar cada body
    resultados_exitosos = 0
    total_bodies = len(bodies_a_probar)
    
    for idx, body in enumerate(bodies_a_probar):
        logger.info(f"=== PROBANDO BODY {idx + 1} DE {total_bodies} ===")
        
        if probar_body(body, f" [{idx + 1}/{total_bodies}]"):
            resultados_exitosos += 1
        
        # Pequeña pausa entre requests para no sobrecargar el servidor
        import time
        time.sleep(0.2)
    
    # Registrar el resultado final
    logger.info(f"=== RESUMEN FINAL ===")
    logger.info(f"Total de bodies probados: {total_bodies}")
    logger.info(f"Operaciones exitosas: {resultados_exitosos}")
    logger.info(f"Operaciones fallidas: {total_bodies - resultados_exitosos}")
    
    if resultados_exitosos > 0:
        logger.info("Creacion/actualizacion de medios de pago completada con éxito")
    else:
        logger.warning("Ninguna operacion de medio de pago fue exitosa")

def get_dispositivos_pagos(client, logger, environment, data_module):
    """Prueba el endpoint de consultar dispositivos de pago"""
    
    logger.info("Ejecutando get_dispositivos_pagos")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/dispositivos_pagos",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /dispositivos_pagos "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} dispositivos de pago encontrados")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (DISPOSITIVOS DE PAGO) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta (todos los dispositivos de pago)")
                        logger.info(f"Endpoint usado: /dispositivos_pagos")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_dispositivos = len(response_data)
                            logger.info(f"Se encontraron {cantidad_dispositivos} dispositivos de pago")
                            
                            if cantidad_dispositivos > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de dispositivos de pago
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["id_dispositivo_pago", "nombre", "id", "descripcion", "codigo", "estado", "tipo", "activo"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de dispositivos de pago exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de los dispositivos de pago encontrados (hasta 10)
                                    for idx, dispositivo in enumerate(response_data[:10]):
                                        # Mostrar información relevante según los campos disponibles
                                        if "nombre" in dispositivo:
                                            logger.info(f"Dispositivo de Pago {idx+1}: {dispositivo.get('nombre')}")
                                        elif "id_dispositivo_pago" in dispositivo:
                                            logger.info(f"Dispositivo de Pago {idx+1}: ID {dispositivo.get('id_dispositivo_pago')}")
                                        elif "id" in dispositivo:
                                            logger.info(f"Dispositivo de Pago {idx+1}: ID {dispositivo.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in dispositivo.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Dispositivo de Pago {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional del dispositivo de pago
                                        if "id_dispositivo_pago" in dispositivo:
                                            logger.info(f"  ID Dispositivo Pago: {dispositivo.get('id_dispositivo_pago')}")
                                        if "descripcion" in dispositivo and dispositivo.get("descripcion"):
                                            logger.info(f"  Descripcion: {dispositivo.get('descripcion')}")
                                        if "codigo" in dispositivo and dispositivo.get("codigo"):
                                            logger.info(f"  Codigo: {dispositivo.get('codigo')}")
                                        if "estado" in dispositivo and dispositivo.get("estado"):
                                            logger.info(f"  Estado: {dispositivo.get('estado')}")
                                        if "activo" in dispositivo and dispositivo.get("activo") is not None:
                                            logger.info(f"  Activo: {dispositivo.get('activo')}")
                                        if "tipo" in dispositivo and dispositivo.get("tipo"):
                                            logger.info(f"  Tipo: {dispositivo.get('tipo')}")
                                        if "observaciones" in dispositivo and dispositivo.get("observaciones"):
                                            logger.info(f"  Observaciones: {dispositivo.get('observaciones')}")
                                        if "fecha_creacion" in dispositivo and dispositivo.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {dispositivo.get('fecha_creacion')}")
                                        if "fecha_modificacion" in dispositivo and dispositivo.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {dispositivo.get('fecha_modificacion')}")
                                    
                                    # Si hay más de 10 dispositivos, indicar cuántos más hay
                                    if cantidad_dispositivos > 10:
                                        logger.info(f"... y {cantidad_dispositivos - 10} dispositivos de pago mas")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de dispositivos de pago encontrados: {cantidad_dispositivos}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_dispositivos > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for dispositivo in response_data:
                                            if "estado" in dispositivo:
                                                estado = dispositivo.get("estado", "Sin estado")
                                            elif "activo" in dispositivo:
                                                estado = "Activo" if dispositivo.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Dispositivos de pago por estado: {estados}")
                                    
                                    # Agrupar por tipo si está disponible
                                    if cantidad_dispositivos > 0 and "tipo" in response_data[0]:
                                        tipos = {}
                                        for dispositivo in response_data:
                                            tipo = dispositivo.get("tipo", "Sin tipo")
                                            tipos[tipo] = tipos.get(tipo, 0) + 1
                                        logger.info(f"Dispositivos de pago por tipo: {tipos}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.dispositivos_pagos = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de dispositivos de pago")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron dispositivos de pago
                                logger.warning(f"No se encontraron dispositivos de pago con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} dispositivos de pago en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunos dispositivos de pago
                                    for idx, dispositivo in enumerate(items[:5]):
                                        if "nombre" in dispositivo:
                                            logger.info(f"Dispositivo de Pago {idx+1}: {dispositivo.get('nombre')}")
                                        elif "id" in dispositivo:
                                            logger.info(f"Dispositivo de Pago {idx+1}: ID {dispositivo.get('id')}")
                                    
                                    data_module.dispositivos_pagos = response_data
                            
                            response.success()
                            logger.info(f"Consulta de dispositivos de pago exitosa con parametros: {params_a_probar}")
                            data_module.dispositivos_pagos = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de dispositivos de pago con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 404:
                    # Endpoint no encontrado
                    logger.warning(f"Endpoint de dispositivos de pago no encontrado (404)")
                    response.failure("Endpoint no encontrado")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de dispositivos de pago (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de dispositivos de pago con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de dispositivos de pago con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    query_params = {}
    
    # Verificar que existan los parámetros básicos
    if hasattr(data_module, 'parametros_dispositivos_pagos'):
        query_params.update(data_module.parametros_dispositivos_pagos)
        logger.info(f"Parametros principales cargados desde data_module: {query_params}")
    else:
        # Usar parámetros vacíos por defecto (sin filtros)
        query_params = {}
        logger.info("Usando parametros vacios (sin filtros)")
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS ACTUALES PARA DISPOSITIVOS DE PAGO: {query_params}")
    
    # Probar con los parámetros principales
    exito_principal = probar_parametros(query_params, " PRINCIPALES")
    
    # Si no hubo éxito con los parámetros principales, intentar sin filtros
    if not exito_principal and query_params:
        logger.info("=== REINTENTANDO SIN PARAMETROS ===")
        probar_parametros({}, " SIN FILTROS")
    
    # Registrar el resultado final
    if exito_principal:
        logger.info("Consulta de dispositivos de pago completada exitosamente")
    else:
        logger.warning("Consulta de dispositivos de pago completada con advertencias")

def get_actividades(client, logger, environment, data_module):
    """Prueba el endpoint de consultar actividades"""
    
    logger.info("Ejecutando get_actividades")
    
    # Función auxiliar para probar diferentes combinaciones de parámetros
    def probar_parametros(params_a_probar, descripcion=""):
        logger.info(f"=== PROBANDO PARAMETROS{descripcion}: {params_a_probar} ===")
        
        try:
            with client.get(
                "/actividades",
                params=params_a_probar if params_a_probar else None,
                catch_response=True,
                name=f"(PARAMETRICAS) - /actividades "
            ) as response:
                # Guardar la respuesta completa en el log (limitada para evitar saturación)
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if isinstance(response_data, list):
                            logger.info(f"Respuesta recibida: {len(response_data)} actividades encontradas")
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
                        logger.info("=== RESUMEN DE LA RESPUESTA (ACTIVIDADES) ===")
                        if params_a_probar:
                            logger.info(f"Parametros consultados: {params_a_probar}")
                        else:
                            logger.info("Sin parametros de consulta")
                        logger.info(f"Endpoint usado: /actividades")
                        
                        # Validar estructura de datos esperada (lista directa)
                        if isinstance(response_data, list):
                            # Respuesta directa como lista (formato esperado según el schema)
                            cantidad_actividades = len(response_data)
                            logger.info(f"Se encontraron {cantidad_actividades} actividades")
                            
                            if cantidad_actividades > 0:
                                # Verificar el primer elemento para determinar la estructura real
                                primer_elemento = response_data[0]
                                campos_disponibles = list(primer_elemento.keys())
                                logger.info(f"Campos disponibles en la respuesta: {campos_disponibles}")
                                
                                # Verificar si al menos tiene algunos campos básicos de actividades
                                # CORREGIDO: Agregamos los campos con prefijo 'p_'
                                tiene_campos_basicos = any(
                                    campo in primer_elemento 
                                    for campo in ["id_actividad", "nombre", "id", "descripcion", "codigo", "estado", "activo",
                                                "p_id_actividad", "p_nombre", "p_codigo_afip", "p_descripcion"]
                                )
                                
                                if tiene_campos_basicos:
                                    response.success()
                                    logger.info(f"Consulta de actividades exitosa con parametros: {params_a_probar}")
                                    
                                    # Mostrar información de las actividades encontradas (hasta 15)
                                    for idx, actividad in enumerate(response_data[:15]):
                                        # Mostrar información relevante según los campos disponibles
                                        # CORREGIDO: Agregamos soporte para campos con prefijo 'p_'
                                        if "p_nombre" in actividad:
                                            logger.info(f"Actividad {idx+1}: {actividad.get('p_nombre')}")
                                        elif "nombre" in actividad:
                                            logger.info(f"Actividad {idx+1}: {actividad.get('nombre')}")
                                        elif "p_id_actividad" in actividad:
                                            logger.info(f"Actividad {idx+1}: ID {actividad.get('p_id_actividad')}")
                                        elif "id_actividad" in actividad:
                                            logger.info(f"Actividad {idx+1}: ID {actividad.get('id_actividad')}")
                                        elif "id" in actividad:
                                            logger.info(f"Actividad {idx+1}: ID {actividad.get('id')}")
                                        else:
                                            # Mostrar el primer campo que contenga información útil
                                            for key, value in actividad.items():
                                                if isinstance(value, str) and len(value) > 0:
                                                    logger.info(f"Actividad {idx+1}: {key}={value}")
                                                    break
                                        
                                        # Mostrar información adicional de la actividad
                                        # CORREGIDO: Agregamos soporte para campos con prefijo 'p_'
                                        if "p_id_actividad" in actividad:
                                            logger.info(f"  ID Actividad: {actividad.get('p_id_actividad')}")
                                        elif "id_actividad" in actividad:
                                            logger.info(f"  ID Actividad: {actividad.get('id_actividad')}")
                                        
                                        if "p_codigo_afip" in actividad and actividad.get("p_codigo_afip"):
                                            logger.info(f"  Codigo AFIP: {actividad.get('p_codigo_afip')}")
                                        elif "codigo" in actividad and actividad.get("codigo"):
                                            logger.info(f"  Codigo: {actividad.get('codigo')}")
                                        
                                        if "p_descripcion" in actividad and actividad.get("p_descripcion"):
                                            logger.info(f"  Descripcion: {actividad.get('p_descripcion')}")
                                        elif "descripcion" in actividad and actividad.get("descripcion"):
                                            logger.info(f"  Descripcion: {actividad.get('descripcion')}")
                                        
                                        if "estado" in actividad and actividad.get("estado"):
                                            logger.info(f"  Estado: {actividad.get('estado')}")
                                        if "activo" in actividad and actividad.get("activo") is not None:
                                            logger.info(f"  Activo: {actividad.get('activo')}")
                                        if "categoria" in actividad and actividad.get("categoria"):
                                            logger.info(f"  Categoria: {actividad.get('categoria')}")
                                        if "tipo" in actividad and actividad.get("tipo"):
                                            logger.info(f"  Tipo: {actividad.get('tipo')}")
                                        if "fecha_creacion" in actividad and actividad.get("fecha_creacion"):
                                            logger.info(f"  Fecha Creacion: {actividad.get('fecha_creacion')}")
                                        if "fecha_modificacion" in actividad and actividad.get("fecha_modificacion"):
                                            logger.info(f"  Fecha Modificacion: {actividad.get('fecha_modificacion')}")
                                    
                                    # Si hay más de 15 actividades, indicar cuántos más hay
                                    if cantidad_actividades > 15:
                                        logger.info(f"... y {cantidad_actividades - 15} actividades mas")
                                    
                                    # Estadísticas adicionales
                                    logger.info(f"Total de actividades encontradas: {cantidad_actividades}")
                                    
                                    # Agrupar por estado si está disponible
                                    if cantidad_actividades > 0 and ("estado" in response_data[0] or "activo" in response_data[0]):
                                        estados = {}
                                        for actividad in response_data:
                                            if "estado" in actividad:
                                                estado = actividad.get("estado", "Sin estado")
                                            elif "activo" in actividad:
                                                estado = "Activo" if actividad.get("activo") else "Inactivo"
                                            else:
                                                estado = "Sin estado"
                                            estados[estado] = estados.get(estado, 0) + 1
                                        logger.info(f"Actividades por estado: {estados}")
                                    
                                    # Agrupar por categoría si está disponible
                                    if cantidad_actividades > 0 and "categoria" in response_data[0]:
                                        categorias = {}
                                        for actividad in response_data:
                                            categoria = actividad.get("categoria", "Sin categoria")
                                            categorias[categoria] = categorias.get(categoria, 0) + 1
                                        logger.info(f"Actividades por categoria: {categorias}")
                                    
                                    # Guardar los datos para posibles pruebas futuras
                                    data_module.actividades = response_data
                                    return True  # Éxito
                                else:
                                    response.failure("Los elementos no tienen campos reconocibles de actividades")
                                    logger.warning(f"Estructura de datos no reconocida para parametros {params_a_probar}: {primer_elemento}")
                                    return False
                            else:
                                # Si no se encontraron actividades
                                logger.warning(f"No se encontraron actividades con parametros: {params_a_probar}")
                                response.success()  # Consideramos éxito porque el endpoint funcionó correctamente
                                return True
                        
                        elif isinstance(response_data, dict):
                            # Respuesta como objeto (posiblemente con metadatos o estructura diferente)
                            logger.info(f"Respuesta recibida como objeto para parametros {params_a_probar}")
                            logger.info(f"Claves disponibles: {list(response_data.keys())}")
                            
                            # Verificar si es una respuesta con items
                            if "items" in response_data:
                                items = response_data["items"]
                                logger.info(f"Se encontraron {len(items)} actividades en items")
                                
                                if len(items) > 0:
                                    primer_elemento = items[0]
                                    campos_disponibles = list(primer_elemento.keys())
                                    logger.info(f"Campos disponibles: {campos_disponibles}")
                                    
                                    # Mostrar algunas actividades
                                    for idx, actividad in enumerate(items[:10]):
                                        if "p_nombre" in actividad:
                                            logger.info(f"Actividad {idx+1}: {actividad.get('p_nombre')}")
                                        elif "nombre" in actividad:
                                            logger.info(f"Actividad {idx+1}: {actividad.get('nombre')}")
                                        elif "p_id_actividad" in actividad:
                                            logger.info(f"Actividad {idx+1}: ID {actividad.get('p_id_actividad')}")
                                        elif "id" in actividad:
                                            logger.info(f"Actividad {idx+1}: ID {actividad.get('id')}")
                                    
                                    data_module.actividades = response_data
                            
                            response.success()
                            logger.info(f"Consulta de actividades exitosa con parametros: {params_a_probar}")
                            data_module.actividades = response_data
                            return True
                        else:
                            response.failure("Formato de respuesta inesperado")
                            logger.warning(f"Formato inesperado en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                            return False
                            
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON invalido en respuesta para parametros {params_a_probar}: {response.text[:200]}")
                        return False
                elif response.status_code == 404:
                    # No se encontraron actividades con los parámetros dados
                    logger.warning(f"No se encontraron actividades con parametros {params_a_probar} (404)")
                    response.failure("No se encontraron actividades con los parametros especificados")
                    return False
                elif response.status_code == 422:
                    # Error de validación en parámetros
                    logger.warning(f"Error de validacion con parametros {params_a_probar} (422)")
                    response.failure("Parametros invalidos - verificar formato")
                    return False
                elif response.status_code == 403:
                    # Posible falta de permisos
                    logger.warning(f"Acceso denegado al endpoint de actividades con parametros {params_a_probar} (403)")
                    response.failure("Acceso denegado - verificar permisos")
                    return False
                elif response.status_code == 500:
                    # Error interno del servidor
                    logger.error(f"Error interno del servidor en endpoint de actividades (500)")
                    response.failure("Error interno del servidor")
                    return False
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de actividades con parametros {params_a_probar}: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Excepcion durante consulta de actividades con parametros {params_a_probar}: {str(e)}")
            return False
    
    # Obtener parámetros desde data_module
    parametros_a_probar = []
    
    # Verificar que existan los parámetros
    if hasattr(data_module, 'parametros_actividades'):
        parametros_a_probar = data_module.parametros_actividades
        logger.info(f"Parametros cargados desde data_module: {len(parametros_a_probar)} conjuntos")
    else:
        logger.warning("No se encontraron parametros para actividades en data_module")
        return
    
    # Mostrar claramente los parámetros que se van a usar
    logger.info(f"PARAMETROS A PROBAR: {len(parametros_a_probar)} conjuntos")
    
    # Probar cada conjunto de parámetros
    resultados_exitosos = 0
    total_parametros = len(parametros_a_probar)
    
    for idx, params in enumerate(parametros_a_probar):
        logger.info(f"=== PROBANDO PARAMETROS {idx + 1} DE {total_parametros} ===")
        
        if probar_parametros(params, f" [{idx + 1}/{total_parametros}]"):
            resultados_exitosos += 1
        
        # Pequeña pausa entre requests para no sobrecargar el servidor
        import time
        time.sleep(0.1)
    
    # Registrar el resultado final
    logger.info(f"=== RESUMEN FINAL ===")
    logger.info(f"Total de conjuntos de parametros probados: {total_parametros}")
    logger.info(f"Consultas exitosas: {resultados_exitosos}")
    logger.info(f"Consultas fallidas: {total_parametros - resultados_exitosos}")
    
    if resultados_exitosos > 0:
        logger.info("Consulta de actividades completada con éxito")
    else:
        logger.warning("Ninguna consulta de actividades fue exitosa")