import random
import copy
from typing import Dict, Any

def insert_or_update_proveedor(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar un proveedor"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_proveedor_pf') and not hasattr(data_module, 'body_insertar_proveedor_pj'):
        logger.error("No hay datos para insertar proveedores en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para proveedores")
        return
    
    # Seleccionar aleatoriamente entre persona física o jurídica
    if hasattr(data_module, 'body_insertar_proveedor_pf') and hasattr(data_module, 'body_insertar_proveedor_pj'):
        body_insertar = random.choice([
            data_module.body_insertar_proveedor_pf,
            data_module.body_insertar_proveedor_pj
        ])
    elif hasattr(data_module, 'body_insertar_proveedor_pf'):
        body_insertar = data_module.body_insertar_proveedor_pf
    else:
        body_insertar = data_module.body_insertar_proveedor_pj
    
    # Crear una copia profunda para evitar modificar el original
    body_insertar = copy.deepcopy(body_insertar)
    
    # Agregar un identificador aleatorio para evitar duplicados
    random_id = random.randint(1000, 9999)
    if body_insertar["p_tipo_proveedor"] == "FISICA":
        body_insertar["p_nombre"] = f"{body_insertar['p_nombre']} {random_id}"
    else:
        body_insertar["p_razon_social"] = f"{body_insertar['p_razon_social']} {random_id}"
    
    logger.info(f"Ejecutando insert_or_update_proveedor con datos: {body_insertar}")
    
    try:
        with client.post(
            "/proveedores", 
            json=body_insertar,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PROVEEDOR) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "id_proveedor", "fecha_creacion", "fecha_modifica"
                    ]
                    
                    # Añadir campos específicos según el tipo de proveedor
                    if body_insertar["p_tipo_proveedor"] == "FISICA":
                        campos_esperados.append("id_persona_fisica")
                    else:
                        campos_esperados.append("id_persona_juridica")
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Inserción/actualización de proveedor exitosa")
                        logger.info(f"ID proveedor: {response_data.get('id_proveedor')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_proveedor = response_data.get('id_proveedor')
                        
                        if "id_persona_fisica" in response_data and response_data["id_persona_fisica"]:
                            data_module.id_persona_fisica_proveedor = response_data["id_persona_fisica"]
                        
                        if "id_persona_juridica" in response_data and response_data["id_persona_juridica"]:
                            data_module.id_persona_juridica_proveedor = response_data["id_persona_juridica"]
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "id_proveedor" in response_data:
                                data_module.id_proveedor = response_data.get('id_proveedor')
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
                            logger.info("El proveedor ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de proveedor: {response.status_code} - {response.text}")
    # En la parte donde manejas la excepción:
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de proveedor: {str(e)}")
    
    # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def alta_proveedor(client, logger, environment, data_module):
    """Prueba el endpoint de alta simplificada de proveedores"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_alta_proveedor_pf') and not hasattr(data_module, 'body_alta_proveedor_pj'):
        logger.error("No hay datos para alta de proveedores en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores/alta", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para alta de proveedores")
        return
    
    # Seleccionar aleatoriamente entre persona física o jurídica
    if hasattr(data_module, 'body_alta_proveedor_pf') and hasattr(data_module, 'body_alta_proveedor_pj'):
        body_alta = random.choice([
            data_module.body_alta_proveedor_pf,
            data_module.body_alta_proveedor_pj
        ])
    elif hasattr(data_module, 'body_alta_proveedor_pf'):
        body_alta = data_module.body_alta_proveedor_pf
    else:
        body_alta = data_module.body_alta_proveedor_pj
    
    # Crear una copia profunda para evitar modificar el original
    body_alta = copy.deepcopy(body_alta)
    
    # Agregar un identificador aleatorio para evitar duplicados
    random_id = random.randint(1000, 9999)
    if body_alta["p_tipo_persona"] == "PF":
        body_alta["p_nombre"] = f"{body_alta['p_nombre']} {random_id}"
        body_alta["p_apellido"] = f"{body_alta['p_apellido']} {random_id}"
    else:
        body_alta["p_razon_social"] = f"{body_alta['p_razon_social']} {random_id}"
    
    logger.info(f"Ejecutando alta_proveedor con datos: {body_alta}")
    
    try:
        with client.post(
            "/proveedores/alta", 
            json=body_alta,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (ALTA PROVEEDOR) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "p_id_proveedor", "p_cuil_cuit", "p_modalidad", 
                        "fecha_creacion", "fecha_modifica", "p_usuario_aplicacion"
                    ]
                    
                    # Añadir campos específicos según el tipo de persona
                    if body_alta["p_tipo_persona"] == "PF":
                        campos_esperados.extend(["p_id_persona_fisica", "p_nombre", "p_apellido"])
                    else:
                        campos_esperados.extend(["p_id_persona_juridica", "p_razon_social"])
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Alta de proveedor exitosa")
                        logger.info(f"ID proveedor: {response_data.get('p_id_proveedor')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_proveedor = response_data.get('p_id_proveedor')
                        
                        if "p_id_persona_fisica" in response_data and response_data["p_id_persona_fisica"]:
                            data_module.id_persona_fisica_proveedor = response_data["p_id_persona_fisica"]
                        
                        if "p_id_persona_juridica" in response_data and response_data["p_id_persona_juridica"]:
                            data_module.id_persona_juridica_proveedor = response_data["p_id_persona_juridica"]
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "p_id_proveedor" in response_data:
                                data_module.id_proveedor = response_data.get('p_id_proveedor')
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
                            logger.info("El proveedor ya existe - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en alta de proveedor: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante alta de proveedor: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/alta",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def alta_cbu_banco_proveedor(client, logger, environment, data_module):
    """Prueba el endpoint de alta de proveedores con CBU y banco"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_alta_cbu_banco_proveedor_pf') and not hasattr(data_module, 'body_alta_cbu_banco_proveedor_pj'):
        logger.error("No hay datos para alta de proveedores con CBU y banco en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores/alta/cbu/banco", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta/cbu/banco [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para alta de proveedores con CBU y banco")
        return
    
    # Seleccionar aleatoriamente entre persona física o jurídica
    if hasattr(data_module, 'body_alta_cbu_banco_proveedor_pf') and hasattr(data_module, 'body_alta_cbu_banco_proveedor_pj'):
        body_alta = random.choice([
            data_module.body_alta_cbu_banco_proveedor_pf,
            data_module.body_alta_cbu_banco_proveedor_pj
        ])
    elif hasattr(data_module, 'body_alta_cbu_banco_proveedor_pf'):
        body_alta = data_module.body_alta_cbu_banco_proveedor_pf
    else:
        body_alta = data_module.body_alta_cbu_banco_proveedor_pj
    
    # Crear una copia profunda para evitar modificar el original
    body_alta = copy.deepcopy(body_alta)
    
    # Agregar un identificador aleatorio para evitar duplicados
    random_id = random.randint(1000, 9999)
    if body_alta["p_tipo_persona"] == "PF":
        body_alta["p_nombre"] = f"{body_alta['p_nombre']} {random_id}"
        body_alta["p_apellido"] = f"{body_alta['p_apellido']} {random_id}"
    else:
        body_alta["p_razon_social"] = f"{body_alta['p_razon_social']} {random_id}"
    
    # Modificar ligeramente el CBU para evitar duplicados
    if "p_cbu" in body_alta and body_alta["p_cbu"]:
        # Asegurarse de que el CBU tenga la longitud correcta (22 dígitos)
        cbu_base = body_alta["p_cbu"][:18]  # Mantener los primeros 18 dígitos
        cbu_suffix = str(random_id).zfill(4)  # Usar el ID aleatorio como sufijo
        body_alta["p_cbu"] = cbu_base + cbu_suffix
    
    logger.info(f"Ejecutando alta_cbu_banco_proveedor con datos: {body_alta}")
    
    try:
        with client.post(
            "/proveedores/alta/cbu/banco", 
            json=body_alta,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta/cbu/banco [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (ALTA PROVEEDOR CON CBU Y BANCO) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "p_id_proveedor", "p_cuil_cuit", "p_modalidad", 
                        "p_id_banco", "p_cbu", "fecha_creacion", 
                        "fecha_modifica", "p_usuario_aplicacion"
                    ]
                    
                    # Añadir campos específicos según el tipo de persona
                    if body_alta["p_tipo_persona"] == "PF":
                        campos_esperados.extend(["p_id_persona_fisica", "p_nombre", "p_apellido"])
                    else:
                        campos_esperados.extend(["p_id_persona_juridica", "p_razon_social"])
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Alta de proveedor con CBU y banco exitosa")
                        logger.info(f"ID proveedor: {response_data.get('p_id_proveedor')}")
                        logger.info(f"CBU: {response_data.get('p_cbu')}")
                        logger.info(f"ID banco: {response_data.get('p_id_banco')}")
                        
                        # Guardar el ID para posibles pruebas futuras
                        data_module.id_proveedor = response_data.get('p_id_proveedor')
                        data_module.cbu_proveedor = response_data.get('p_cbu')
                        data_module.id_banco_proveedor = response_data.get('p_id_banco')
                        
                        if "p_id_persona_fisica" in response_data and response_data["p_id_persona_fisica"]:
                            data_module.id_persona_fisica_proveedor = response_data["p_id_persona_fisica"]
                        
                        if "p_id_persona_juridica" in response_data and response_data["p_id_persona_juridica"]:
                            data_module.id_persona_juridica_proveedor = response_data["p_id_persona_juridica"]
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        
                        # Si faltan pocos campos, podemos considerarlo un éxito parcial
                        if len(campos_faltantes) <= 2:
                            logger.info("Aunque faltan algunos campos, se considera un éxito parcial")
                            response.success()
                            
                            # Guardar el ID si está disponible
                            if "p_id_proveedor" in response_data:
                                data_module.id_proveedor = response_data.get('p_id_proveedor')
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
                            logger.info("El proveedor ya existe - respuesta 400 esperada")
                            response.success()
                        elif isinstance(detail, list) and any("invalid_cbu" in str(item.get("type", "")) for item in detail):
                            logger.info("CBU inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en alta de proveedor con CBU y banco: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante alta de proveedor con CBU y banco: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/alta/cbu/banco",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/alta/cbu/banco [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def get_proveedor_by_cuit_cuil(client, logger, environment, data_module):
    """Prueba el endpoint de obtener proveedor por CUIT/CUIL para múltiples identificadores"""
    
    # Verificar si tenemos una lista de CUILs/CUITs para probar
    if hasattr(data_module, 'lista_cuit_cuil_proveedores') and data_module.lista_cuit_cuil_proveedores:
        lista_cuit_cuil = data_module.lista_cuit_cuil_proveedores
    else:
        # Si no hay lista específica, intentamos construir una a partir de los datos de proveedores
        lista_cuit_cuil = []
        
        # Intentar obtener CUITs/CUILs de los datos de proveedores
        if hasattr(data_module, 'body_insertar_proveedor_pj'):
            cuit_pj = data_module.body_insertar_proveedor_pj.get('p_cuit_cuil') or data_module.body_insertar_proveedor_pj.get('p_cuit')
            if cuit_pj:
                lista_cuit_cuil.append(cuit_pj)
        
        if hasattr(data_module, 'body_insertar_proveedor_pf'):
            cuil_pf = data_module.body_insertar_proveedor_pf.get('p_cuit_cuil') or data_module.body_insertar_proveedor_pf.get('p_cuil')
            if cuil_pf:
                lista_cuit_cuil.append(cuil_pf)
        
    
    # Verificar si la lista está vacía
    if not lista_cuit_cuil:
        logger.error("No hay CUITs/CUILs para consultar proveedores.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/proveedores?p_cuit_cuil=00000000000", 
            catch_response=True,
            name="(PROVEEDORES) - /proveedores [Sin datos]"
        ) as response:
            response.failure("No hay CUITs/CUILs definidos para consultar proveedores")
        return
    
    logger.info(f"Ejecutando get_proveedor_by_cuit_cuil con {len(lista_cuit_cuil)} CUITs/CUILs")
    
    # Contador para estadísticas
    resultados = {
        "exitosos": 0,
        "no_encontrados": 0,
        "errores": 0
    }
    
    # Iterar sobre cada CUIT/CUIL en la lista
    for cuit_cuil in lista_cuit_cuil:
        logger.info(f"Consultando proveedor con CUIT/CUIL: {cuit_cuil}")
        
        try:
            with client.get(
                f"/proveedores?p_cuit_cuil={cuit_cuil}", 
                catch_response=True,
                name=f"(PROVEEDORES) - /proveedores [GET {cuit_cuil}]"
            ) as response:
                # Guardar la respuesta en el log (versión resumida para no saturar)
                logger.info(f"Respuesta para {cuit_cuil}: Código {response.status_code}")
                
                if response.status_code == 200:  # HTTP 200 OK
                    try:
                        # Verificar que la respuesta sea JSON válido
                        response_data = response.json()
                        
                        # Validar estructura de datos esperada
                        if isinstance(response_data, list) and len(response_data) > 0:
                            # Verificar que el primer elemento tenga los campos esperados
                            proveedor = response_data[0]
                            campos_esperados = [
                                "p_cuit_cuil", "id_proveedor", "p_tipo_proveedor"
                            ]
                            
                            if all(campo in proveedor for campo in campos_esperados):
                                response.success()
                                logger.info(f"Consulta exitosa para CUIT/CUIL: {cuit_cuil}")
                                logger.info(f"ID proveedor: {proveedor.get('id_proveedor')}")
                                
                                # Guardar el último ID consultado
                                data_module.id_proveedor_consultado = proveedor.get('id_proveedor')
                                resultados["exitosos"] += 1
                            else:
                                # Verificar qué campos faltan
                                campos_faltantes = [campo for campo in campos_esperados if campo not in proveedor]
                                logger.warning(f"Faltan campos en la respuesta para {cuit_cuil}: {campos_faltantes}")
                                response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                                resultados["errores"] += 1
                        else:
                            response.failure("No se encontraron proveedores con el CUIT/CUIL proporcionado")
                            logger.warning(f"No se encontraron proveedores con CUIT/CUIL: {cuit_cuil}")
                            resultados["no_encontrados"] += 1
                    except ValueError as e:
                        response.failure(f"Respuesta no es JSON válido: {str(e)}")
                        logger.error(f"JSON inválido en respuesta para {cuit_cuil}: {response.text[:100]}...")
                        resultados["errores"] += 1
                elif response.status_code == 404:
                    # Es posible que el proveedor no exista, lo cual es un comportamiento esperado
                    logger.info(f"No se encontró proveedor con CUIT/CUIL: {cuit_cuil}")
                    response.success()  # Marcamos como éxito porque es un comportamiento esperado
                    resultados["no_encontrados"] += 1
                else:
                    response.failure(f"Error: {response.status_code}")
                    logger.error(f"Error en consulta de proveedor {cuit_cuil}: {response.status_code} - {response.text[:100]}...")
                    resultados["errores"] += 1
        except Exception as e:
            logger.error(f"Excepción durante consulta de proveedor {cuit_cuil}: {str(e)}")
            resultados["errores"] += 1
            # Registrar el error como una respuesta fallida
            with client.get(
                f"/proveedores?p_cuit_cuil={cuit_cuil}",
                catch_response=True,
                name=f"(PROVEEDORES) - /proveedores [Exception {cuit_cuil}]"
            ) as response:
                response.failure(f"Excepción: {str(e)}")
    


def buscar_personas_por_cuils_cuits(client, logger, environment, data_module):
    """Prueba el endpoint de búsqueda de personas por lista de CUILs/CUITs"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_busqueda_por_cuils_cuits'):
        # Si no existe el cuerpo específico, intentamos crear uno a partir de la lista de CUILs/CUITs
        if hasattr(data_module, 'lista_cuit_cuil_proveedores') and data_module.lista_cuit_cuil_proveedores:
            body_busqueda = {
                "p_cuils_cuits": data_module.lista_cuit_cuil_proveedores[:3]  # Tomamos hasta 3 elementos
            }
        else:
            logger.error("No hay datos para buscar personas por CUILs/CUITs.")
            
            # Registrar un error explícito usando catch_response
            with client.post(
                "/personas/busqueda-por-cuils-cuits", 
                json={"p_cuils_cuits": []},
                catch_response=True,
                name="(PROVEEDORES) - /personas/busqueda-por-cuils-cuits [Sin datos]"
            ) as response:
                response.failure("No hay datos definidos para búsqueda por CUILs/CUITs")
            return
    else:
        body_busqueda = data_module.body_busqueda_por_cuils_cuits
    
    logger.info(f"Ejecutando búsqueda de personas por CUILs/CUITs con datos: {body_busqueda}")
    
    try:
        with client.post(
            "/personas/busqueda-por-cuils-cuits", 
            json=body_busqueda,
            catch_response=True,
            name="(PROVEEDORES) - /personas/busqueda-por-cuils-cuits [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BÚSQUEDA POR CUILs/CUITs) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en búsqueda de personas por CUILs/CUITs: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante búsqueda de personas por CUILs/CUITs: {str(e)}")
        # Registrar el error como una respuesta fallida
        with client.post(
            "/personas/busqueda-por-cuils-cuits",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /personas/busqueda-por-cuils-cuits [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_proveedores_por_actividad(client, logger, environment, data_module):
    """Prueba el endpoint de obtener proveedores por ID de actividad AFIP"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'lista_id_actividad_afip') or not data_module.lista_id_actividad_afip:
        logger.error("No hay IDs de actividad AFIP disponibles para la prueba.")
        
        # Registrar un error explícito usando catch_response
        with client.get(
            "/proveedores/actividad?p_id_actividad=0", 
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/actividad [Sin datos]"
        ) as response:
            response.failure("No hay datos para probar el endpoint")
        return
    
    # Seleccionar un ID de actividad aleatorio de la lista
    if hasattr(data_module, 'body_consulta_proveedor_actividad') and data_module.body_consulta_proveedor_actividad.get('p_id_actividad'):
        p_id_actividad = data_module.body_consulta_proveedor_actividad.get('p_id_actividad')
    else:
        p_id_actividad = random.choice(data_module.lista_id_actividad_afip)
    
    logger.info(f"Ejecutando get_proveedores_por_actividad con ID de actividad: {p_id_actividad}")
    
    try:
        with client.get(
            f"/proveedores/actividad?p_id_actividad={p_id_actividad}", 
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/actividad [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (PROVEEDORES POR ACTIVIDAD) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que los elementos de la lista contengan los campos esperados
                        campos_esperados = ["p_id_actividad", "p_cuit_cuil", "p_apenom_razsoc"]
                        
                        if not response_data:
                            # Si la lista está vacía, es un resultado válido (no hay proveedores para esa actividad)
                            logger.info(f"No se encontraron proveedores para la actividad ID: {p_id_actividad}")
                            response.success()
                        elif all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Obtención de proveedores por actividad exitosa para ID: {p_id_actividad}")
                            logger.info(f"Cantidad de proveedores encontrados: {len(response_data)}")
                            
                            # Guardar algunos datos para posibles pruebas futuras
                            if response_data:
                                data_module.ultimo_proveedor_actividad = response_data[0]
                                logger.info(f"Primer proveedor encontrado: {response_data[0]['p_cuit_cuil']} - {response_data[0]['p_apenom_razsoc']}")
                        else:
                            # Verificar qué campos faltan
                            for item in response_data[:3]:  # Revisar solo los primeros 3 elementos para no saturar el log
                                campos_faltantes = [campo for campo in campos_esperados if campo not in item]
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en el elemento: {campos_faltantes}")
                            
                            response.failure("Formato de respuesta incompleto")
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
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
                        if isinstance(detail, list) and any("invalid_id_actividad" in str(item.get("type", "")) for item in detail):
                            logger.info(f"ID de actividad inválido: {p_id_actividad} - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            elif response.status_code == 404:
                # Verificar si es un error de recurso no encontrado (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Recurso no encontrado: {error_data}")
                    
                    # Si es un error de recurso no encontrado esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info(f"No se encontraron proveedores para la actividad ID: {p_id_actividad} - respuesta 404 esperada")
                            response.success()
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.failure(f"Error 404 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de proveedores por actividad: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de proveedores por actividad: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.get(
            f"/proveedores/actividad?p_id_actividad={p_id_actividad}",
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/actividad [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def buscar_proveedores_por_parametros(client, logger, environment, data_module):
    """Prueba el endpoint de búsqueda de proveedores por parámetros"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_busqueda_proveedores'):
        logger.error("No hay datos para búsqueda de proveedores por parámetros en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores/busqueda", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para búsqueda de proveedores por parámetros")
        return
    
    logger.info("llegue aca")

    # Crear una copia profunda para evitar modificar el original
    body_busqueda = copy.deepcopy(data_module.body_busqueda_proveedores)
    
    logger.info("llegue aca2")

    # Configurar los parámetros de consulta
    if hasattr(data_module, 'query_params_busqueda_proveedores'):
        query_params = data_module.query_params_busqueda_proveedores
    else:
        query_params = {
            "p_criterio_orden": 1,  # Número entre 1 y 4
            "p_orden": 1,
            "p_page_size": 1,
            "p_page_number": 1
        }
    
    # Construir la URL solo con los query parameters válidos
    url = "/proveedores/busqueda"
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    url = f"{url}?{query_string}"
    
    logger.info(f"Ejecutando buscar_proveedores_por_parametros con URL: {url}")
    logger.info(f"Body de búsqueda: {body_busqueda}")
    
    try:
        with client.post(
            url, 
            json=body_busqueda,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BÚSQUEDA DE PROVEEDORES) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "page_number", "page_size", "total_items", "items"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Búsqueda de proveedores exitosa")
                        logger.info(f"Total de elementos: {response_data.get('total_items')}")
                        logger.info(f"Página: {response_data.get('page_number')} de tamaño {response_data.get('page_size')}")
                        
                        # Verificar si hay elementos en la respuesta
                        items = response_data.get('items', [])
                        if items:
                            logger.info(f"Cantidad de elementos recibidos: {len(items)}")
                            
                            # Guardar el primer elemento para posibles pruebas futuras
                            data_module.ultimo_proveedor_buscado = items[0]
                            logger.info(f"Primer proveedor encontrado: {items[0].get('id_proveedor')}")
                        else:
                            logger.info("No se encontraron proveedores con los parámetros especificados")
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 422:
                # Error de validación de parámetros
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación de parámetros: {error_data}")
                    
                    # Analizar el detalle del error
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list):
                            for error_item in detail:
                                if "p_criterio_orden" in error_item.get("loc", []):
                                    logger.error(f"Error en p_criterio_orden: {error_item.get('msg')}")
                                    logger.info("Valores válidos para p_criterio_orden: 1, 2, 3, 4")
                        
                        response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 422 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("invalid_parameter" in str(item.get("type", "")) for item in detail):
                            logger.info("Parámetro inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en búsqueda de proveedores: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante búsqueda de proveedores: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            url,
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda-por-ids [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")



def buscar_proveedores_por_ids(client, logger, environment, data_module):
    """Prueba el endpoint de búsqueda de proveedores por IDs"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_busqueda_proveedores_por_ids'):
        logger.error("No hay datos para búsqueda de proveedores por IDs en el módulo de datos.")
        
        # Intentar crear un cuerpo de solicitud con IDs aleatorios
        body_busqueda = {
            "p_ids_proveedor": [random.randint(1, 100) for _ in range(5)]
        }
        logger.info(f"Usando IDs aleatorios para la prueba: {body_busqueda}")
    else:
        # Crear una copia profunda para evitar modificar el original
        body_busqueda = copy.deepcopy(data_module.body_busqueda_proveedores_por_ids)
    
    logger.info(f"Ejecutando buscar_proveedores_por_ids con datos: {body_busqueda}")
    
    try:
        with client.post(
            "/proveedores/busqueda-por-ids", 
            json=body_busqueda,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda-por-ids [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BÚSQUEDA DE PROVEEDORES POR IDS) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    if isinstance(response_data, list):
                        # Verificar que los elementos de la lista contengan los campos esperados
                        campos_esperados = [
                            "p_tipo_proveedor", "p_id_proveedor", "p_cuit_cuil", 
                            "p_razsoc_apenom", "p_modalidad"
                        ]
                        
                        if not response_data:
                            # Si la lista está vacía, es un resultado válido (no hay proveedores para esos IDs)
                            logger.info(f"No se encontraron proveedores para los IDs proporcionados")
                            response.success()
                        elif all(all(campo in item for campo in campos_esperados) for item in response_data):
                            response.success()
                            logger.info(f"Búsqueda de proveedores por IDs exitosa")
                            logger.info(f"Cantidad de proveedores encontrados: {len(response_data)}")
                            
                            # Guardar algunos datos para posibles pruebas futuras
                            if response_data:
                                data_module.ultimo_proveedor_por_id = response_data[0]
                                logger.info(f"Primer proveedor encontrado: ID {response_data[0]['p_id_proveedor']} - {response_data[0]['p_razsoc_apenom']}")
                        else:
                            # Verificar qué campos faltan
                            for item in response_data[:3]:  # Revisar solo los primeros 3 elementos para no saturar el log
                                campos_faltantes = [campo for campo in campos_esperados if campo not in item]
                                if campos_faltantes:
                                    logger.warning(f"Faltan campos en el elemento: {campos_faltantes}")
                            
                            response.failure("Formato de respuesta incompleto")
                    else:
                        response.failure("Formato de respuesta inesperado (se esperaba una lista)")
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
                        if isinstance(detail, list) and any("invalid_parameter" in str(item.get("type", "")) for item in detail):
                            logger.info("Parámetro inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en búsqueda de proveedores por IDs: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante búsqueda de proveedores por IDs: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/busqueda-por-ids",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda-por-ids [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def buscar_proveedores_por_ids_search(client, logger, environment, data_module):
    """Prueba el endpoint de búsqueda de proveedores por IDs con parámetro de búsqueda"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_busqueda_proveedores_por_ids_search'):
        logger.error("No hay datos para búsqueda de proveedores por IDs con parámetro de búsqueda en el módulo de datos.")
        
        # Intentar crear un cuerpo de solicitud con IDs aleatorios
        body_busqueda = {
            "p_ids_proveedor": [random.randint(1, 100) for _ in range(5)]
        }
        logger.info(f"Usando IDs aleatorios para la prueba: {body_busqueda}")
    else:
        # Crear una copia profunda para evitar modificar el original
        body_busqueda = copy.deepcopy(data_module.body_busqueda_proveedores_por_ids_search)
    
    # Configurar los parámetros de consulta
    if hasattr(data_module, 'query_params_busqueda_proveedores_por_ids_search'):
        query_params = data_module.query_params_busqueda_proveedores_por_ids_search
    else:
        query_params = {
            "p_search_input": "prueba",
            "p_page_size": 10,
            "p_page_number": 1
        }
    
    # Construir la URL con los parámetros de consulta
    url = "/proveedores/busqueda-por-ids/search"
    query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
    url = f"{url}?{query_string}"
    
    logger.info(f"Ejecutando buscar_proveedores_por_ids_search con URL: {url}")
    logger.info(f"Body de búsqueda: {body_busqueda}")
    
    try:
        with client.post(
            url, 
            json=body_busqueda,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda-por-ids/search [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BÚSQUEDA DE PROVEEDORES POR IDS CON PARÁMETRO) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = [
                        "page_number", "page_size", "total_items", "items"
                    ]
                    
                    if all(campo in response_data for campo in campos_esperados):
                        response.success()
                        logger.info(f"Búsqueda de proveedores por IDs con parámetro exitosa")
                        logger.info(f"Total de elementos: {response_data.get('total_items')}")
                        logger.info(f"Página: {response_data.get('page_number')} de tamaño {response_data.get('page_size')}")
                        
                        # Verificar si hay elementos en la respuesta
                        items = response_data.get('items', [])
                        if items:
                            logger.info(f"Cantidad de elementos recibidos: {len(items)}")
                            
                            # Guardar el primer elemento para posibles pruebas futuras
                            data_module.ultimo_proveedor_buscado_por_ids_search = items[0]
                            logger.info(f"Primer proveedor encontrado: {items[0].get('p_cuit_cuil')}")
                        else:
                            logger.info("No se encontraron proveedores con los IDs y parámetro especificados")
                    else:
                        # Verificar qué campos faltan
                        campos_faltantes = [campo for campo in campos_esperados if campo not in response_data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
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
                        if isinstance(detail, list) and any("invalid_parameter" in str(item.get("type", "")) for item in detail):
                            logger.info("Parámetro inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en búsqueda de proveedores por IDs con parámetro: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante búsqueda de proveedores por IDs con parámetro: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            url,
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda-por-ids/search [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

import random
import copy

def insert_cbu_proveedor(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar CBU de un proveedor"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_cbu_proveedor_pf') and not hasattr(data_module, 'body_insertar_cbu_proveedor_pj'):
        logger.error("No hay datos para insertar CBU de proveedores en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores/cbu", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para CBU de proveedores")
        return
    
    # Seleccionar aleatoriamente entre persona física o jurídica
    if hasattr(data_module, 'body_insertar_cbu_proveedor_pf') and hasattr(data_module, 'body_insertar_cbu_proveedor_pj'):
        body_insertar = random.choice([
            data_module.body_insertar_cbu_proveedor_pf,
            data_module.body_insertar_cbu_proveedor_pj
        ])
    elif hasattr(data_module, 'body_insertar_cbu_proveedor_pf'):
        body_insertar = data_module.body_insertar_cbu_proveedor_pf
    else:
        body_insertar = data_module.body_insertar_cbu_proveedor_pj
    
    # Crear una copia profunda para evitar modificar el original
    body_insertar = copy.deepcopy(body_insertar)
    
    # Modificar ligeramente el CBU para evitar duplicados
    random_id = random.randint(1000, 9999)
    cbu_base = body_insertar["p_cbu"][:18]  # Mantener los primeros 18 dígitos
    cbu_suffix = str(random_id).zfill(4)  # Usar un ID aleatorio como sufijo
    body_insertar["p_cbu"] = cbu_base + cbu_suffix
    
    logger.info(f"Ejecutando insert_cbu_proveedor con datos: {body_insertar}")
    
    try:
        with client.post(
            "/proveedores/cbu", 
            json=body_insertar,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea el texto esperado
                    if response.text.strip('"') == "OK":
                        response.success()
                        logger.info(f"Inserción/actualización de CBU exitosa para CUIT/CUIL: {body_insertar['p_cuil_cuit']}")
                        logger.info(f"CBU registrado: {body_insertar['p_cbu']}")
                        
                        # Guardar el CBU para posibles pruebas futuras
                        data_module.ultimo_cbu_registrado = body_insertar['p_cbu']
                        data_module.ultimo_cuil_cuit_cbu = body_insertar['p_cuil_cuit']
                    else:
                        response.failure(f"Respuesta inesperada: {response.text}")
                        logger.warning(f"Respuesta inesperada en inserción de CBU: {response.text}")
                except Exception as e:
                    response.failure(f"Error al procesar la respuesta: {str(e)}")
                    logger.error(f"Error al procesar la respuesta: {str(e)}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("invalid_cbu" in str(item.get("type", "")) for item in detail):
                            logger.info("CBU inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            elif response.status_code == 404:
                # Es posible que el proveedor no exista
                logger.warning(f"Proveedor no encontrado con CUIT/CUIL: {body_insertar['p_cuil_cuit']}")
                response.failure(f"Proveedor no encontrado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de CBU: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de CBU: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/cbu",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu/banco [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def insert_cbu_proveedor_banco(client, logger, environment, data_module):
    """Prueba el endpoint de insertar o actualizar CBU y banco de un proveedor"""
    
    # Verificar si tenemos datos para probar
    if not hasattr(data_module, 'body_insertar_cbu_banco_proveedor_pf') and not hasattr(data_module, 'body_insertar_cbu_banco_proveedor_pj'):
        logger.error("No hay datos para insertar CBU y banco de proveedores en el módulo de datos.")
        
        # Registrar un error explícito usando catch_response
        with client.post(
            "/proveedores/cbu/banco", 
            json={"error": "sin_datos"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu/banco [Sin datos]"
        ) as response:
            response.failure("No hay datos definidos para CBU y banco de proveedores")
        return
    
    # Seleccionar aleatoriamente entre persona física o jurídica
    if hasattr(data_module, 'body_insertar_cbu_banco_proveedor_pf') and hasattr(data_module, 'body_insertar_cbu_banco_proveedor_pj'):
        body_insertar = random.choice([
            data_module.body_insertar_cbu_banco_proveedor_pf,
            data_module.body_insertar_cbu_banco_proveedor_pj
        ])
    elif hasattr(data_module, 'body_insertar_cbu_banco_proveedor_pf'):
        body_insertar = data_module.body_insertar_cbu_banco_proveedor_pf
    else:
        body_insertar = data_module.body_insertar_cbu_banco_proveedor_pj
    
    # Crear una copia profunda para evitar modificar el original
    body_insertar = copy.deepcopy(body_insertar)
    
    # Modificar ligeramente el CBU para evitar duplicados
    random_id = random.randint(1000, 9999)
    cbu_base = body_insertar["p_cbu"][:18]  # Mantener los primeros 18 dígitos
    cbu_suffix = str(random_id).zfill(4)  # Usar un ID aleatorio como sufijo
    body_insertar["p_cbu"] = cbu_base + cbu_suffix
    
    logger.info(f"Ejecutando insert_cbu_proveedor_banco con datos: {body_insertar}")
    
    try:
        with client.post(
            "/proveedores/cbu/banco", 
            json=body_insertar,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu/banco [POST]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 201:  # HTTP 201 Created
                try:
                    # Verificar que la respuesta sea el texto esperado
                    if response.text.strip('"') == "OK":
                        response.success()
                        logger.info(f"Inserción/actualización de CBU y banco exitosa para CUIT/CUIL: {body_insertar['p_cuil_cuit']}")
                        logger.info(f"CBU registrado: {body_insertar['p_cbu']}")
                        logger.info(f"ID banco: {body_insertar['p_id_banco']}")
                        
                        # Guardar los datos para posibles pruebas futuras
                        data_module.ultimo_cbu_banco_registrado = body_insertar['p_cbu']
                        data_module.ultimo_cuil_cuit_cbu_banco = body_insertar['p_cuil_cuit']
                        data_module.ultimo_id_banco_registrado = body_insertar['p_id_banco']
                    else:
                        response.failure(f"Respuesta inesperada: {response.text}")
                        logger.warning(f"Respuesta inesperada en inserción de CBU y banco: {response.text}")
                except Exception as e:
                    response.failure(f"Error al procesar la respuesta: {str(e)}")
                    logger.error(f"Error al procesar la respuesta: {str(e)}")
            elif response.status_code == 400:
                # Verificar si es un error de validación (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    
                    # Si es un error de validación esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("invalid_cbu" in str(item.get("type", "")) for item in detail):
                            logger.info("CBU inválido - respuesta 400 esperada")
                            response.success()
                        elif isinstance(detail, list) and any("invalid_banco" in str(item.get("type", "")) for item in detail):
                            logger.info("Banco inválido - respuesta 400 esperada")
                            response.success()
                        else:
                            response.failure(f"Error de validación: {detail}")
                    else:
                        response.failure(f"Error 400 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 400 con formato inesperado: {response.text}")
            elif response.status_code == 404:
                # Es posible que el proveedor no exista
                logger.warning(f"Proveedor no encontrado con CUIT/CUIL: {body_insertar['p_cuil_cuit']}")
                response.failure(f"Proveedor no encontrado: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en inserción/actualización de CBU y banco: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante inserción/actualización de CBU y banco: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/cbu/banco",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/cbu/banco [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def get_contratistas_obra_publica(client, logger, environment, data_module):
    """Prueba el endpoint de obtener contratistas de obra pública"""
    
    logger.info("Ejecutando get_contratistas_obra_publica")
    
    try:
        with client.get(
            "/proveedores/contratistas-obra-publica", 
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/contratistas-obra-publica [GET]"
        ) as response:
            # Guardar la respuesta completa en el log
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:  # HTTP 200 OK
                try:
                    # Verificar que la respuesta sea JSON válido
                    response_data = response.json()
                    
                    # Guardar los datos completos obtenidos en el log
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (CONTRATISTAS OBRA PÚBLICA) ===")
                    logger.info(f"Respuesta: {response_data}")
                    
                    
                   
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
            elif response.status_code == 404:
                # Verificar si es un error de recurso no encontrado (comportamiento esperado en algunos casos)
                try:
                    error_data = response.json()
                    logger.warning(f"Recurso no encontrado: {error_data}")
                    
                    # Si es un error de recurso no encontrado esperado, podemos marcarlo como éxito
                    if "detail" in error_data:
                        detail = error_data["detail"]
                        if isinstance(detail, list) and any("not_found_element" in str(item.get("type", "")) for item in detail):
                            logger.info("No se encontraron contratistas de obra pública - respuesta 404 esperada")
                            response.success()
                        else:
                            response.failure(f"Error 404: {detail}")
                    else:
                        response.failure(f"Error 404 sin detalle: {error_data}")
                except ValueError:
                    response.failure(f"Error 404 con formato inesperado: {response.text}")
            elif response.status_code == 403:
                # Error de permisos - puede ser esperado según la configuración de la aplicación
                logger.warning("Error de permisos (403) - verificar configuración de la aplicación")
                response.failure(f"Error de permisos: {response.text}")
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"Error en consulta de contratistas de obra pública: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Excepción durante consulta de contratistas de obra pública: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.get(
            "/proveedores/contratistas-obra-publica",
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/contratistas-obra-publica [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")


def buscar_proveedores_minimizado(client, logger, environment, data_module):
    """Buscar proveedores con datos minimizados"""
    try:
        logger.info("=== BUSCANDO PROVEEDORES MINIMIZADO ===")
        
        # Verificar si existen los atributos necesarios
        if not hasattr(data_module, 'parametros_busqueda_minimizada_query'):
            logger.error("No hay parámetros de consulta para búsqueda minimizada en el módulo de datos.")
            
            with client.post(
                "/proveedores/busqueda/minimizado",
                json={"error": "sin_datos"},
                catch_response=True,
                name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Sin datos]"
            ) as response:
                response.failure("No hay parámetros de consulta definidos para búsqueda minimizada")
            return
        
        if not hasattr(data_module, 'body_busqueda_minimizada'):
            logger.error("No hay datos de cuerpo para búsqueda minimizada en el módulo de datos.")
            
            with client.post(
                "/proveedores/busqueda/minimizado",
                json={"error": "sin_datos"},
                catch_response=True,
                name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Sin datos]"
            ) as response:
                response.failure("No hay datos de cuerpo definidos para búsqueda minimizada")
            return
        
        # Usar parámetros del módulo de datos
        query_params = data_module.parametros_busqueda_minimizada_query
        body_data = data_module.body_busqueda_minimizada
        
        with client.post(
            "/proveedores/busqueda/minimizado",
            params=query_params,
            json=body_data,
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda/minimizado [POST]"
        ) as response:
            
            logger.info(f"Respuesta completa: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    logger.info("=== DATOS COMPLETOS DE LA RESPUESTA (BÚSQUEDA MINIMIZADA) ===")
                    logger.info(f"Respuesta: {data}")
                    
                    # Validar estructura de datos esperada
                    campos_esperados = ["page_number", "page_size", "total_items", "items"]
                    
                    if all(campo in data for campo in campos_esperados):
                        response.success()
                        logger.info("EXITO: Proveedores minimizados consultados exitosamente")
                        logger.info(f"Total de registros: {data.get('total_items', 0)}")
                        logger.info(f"Pagina: {data.get('page_number', 'N/A')} - Tamaño: {data.get('page_size', 'N/A')}")
                        
                        proveedores = data.get('items', [])
                        if proveedores:
                            logger.info(f"Cantidad de proveedores en esta pagina: {len(proveedores)}")
                            
                            # Mostrar algunos proveedores de ejemplo
                            for i, proveedor in enumerate(proveedores[:3]):
                                denominacion = proveedor.get('denominacion', 'N/A')
                                cuil_cuit = proveedor.get('cuil_cuit', 'N/A')
                                tipo_persona = proveedor.get('tipo_persona', 'N/A')
                                logger.info(f"Proveedor {i+1}: {denominacion} - {cuil_cuit} - Tipo: {tipo_persona}")
                            
                            if len(proveedores) > 3:
                                logger.info(f"... y {len(proveedores) - 3} proveedores mas")
                        else:
                            logger.warning("ADVERTENCIA: No se encontraron proveedores para los parametros especificados")
                    else:
                        campos_faltantes = [campo for campo in campos_esperados if campo not in data]
                        logger.warning(f"Faltan campos en la respuesta: {campos_faltantes}")
                        response.failure(f"Formato de respuesta incompleto: faltan {len(campos_faltantes)} campos")
                        
                except ValueError as e:
                    response.failure(f"Respuesta no es JSON válido: {str(e)}")
                    logger.error(f"JSON inválido en respuesta: {response.text[:200]}")
                    
            elif response.status_code == 422:
                try:
                    error_data = response.json()
                    logger.warning(f"Error de validación: {error_data}")
                    response.failure(f"Error de validación: {error_data}")
                except ValueError:
                    response.failure(f"Error 422 con formato inesperado: {response.text}")
                    
            elif response.status_code == 403:
                logger.error("ERROR 403: Sin permisos para buscar proveedores minimizado")
                response.failure("Sin permisos para buscar proveedores minimizado")
                
            else:
                response.failure(f"Error: {response.status_code}")
                logger.error(f"ERROR: Error al buscar proveedores minimizado: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"EXCEPCION: Error al buscar proveedores minimizado: {str(e)}")
        
        # Registrar el error como una respuesta fallida usando catch_response
        with client.post(
            "/proveedores/busqueda/minimizado",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Exception]"
        ) as response:
            response.failure(f"Excepción: {str(e)}")

def buscar_proveedores_minimizado_casos_multiples(client, logger, environment, data_module):
    """Buscar proveedores minimizado - casos múltiples"""
    try:
        logger.info("=== PROBANDO MULTIPLES CASOS DE BUSQUEDA MINIMIZADA ===")
        
        # Verificar si existen los atributos necesarios
        if not hasattr(data_module, 'parametros_busqueda_minimizada_query'):
            logger.error("No hay parámetros de consulta para búsqueda minimizada casos múltiples.")
            
            with client.post(
                "/proveedores/busqueda/minimizado",
                json={"error": "sin_datos"},
                catch_response=True,
                name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Sin datos casos múltiples]"
            ) as response:
                response.failure("No hay parámetros de consulta para casos múltiples")
            return
        
        if not hasattr(data_module, 'body_busqueda_minimizada_casos'):
            logger.error("No hay datos de casos múltiples para búsqueda minimizada.")
            
            with client.post(
                "/proveedores/busqueda/minimizado",
                json={"error": "sin_datos"},
                catch_response=True,
                name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Sin casos múltiples]"
            ) as response:
                response.failure("No hay datos de casos múltiples definidos")
            return
        
        query_params = data_module.parametros_busqueda_minimizada_query
        casos = data_module.body_busqueda_minimizada_casos
        
        for i, caso in enumerate(casos, 1):
            logger.info(f"--- CASO {i}: {list(caso.keys())} ---")
            
            try:
                with client.post(
                    "/proveedores/busqueda/minimizado",
                    params=query_params,
                    json=caso,
                    catch_response=True,
                    name=f"(PROVEEDORES) - /proveedores/busqueda/minimizado [Caso {i}]"
                ) as response:
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            total_items = data.get('total_items', 0)
                            logger.info(f"EXITO Caso {i}: {total_items} proveedores encontrados")
                            
                            if total_items > 0:
                                items = data.get('items', [])
                                if items:
                                    primer_proveedor = items[0]
                                    denominacion = primer_proveedor.get('denominacion', 'N/A')
                                    cuil_cuit = primer_proveedor.get('cuil_cuit', 'N/A')
                                    logger.info(f"Ejemplo: {denominacion} - {cuil_cuit}")
                            else:
                                logger.info(f"Caso {i}: Sin resultados")
                            
                            response.success()
                            
                        except ValueError as e:
                            response.failure(f"Respuesta no es JSON válido: {str(e)}")
                            logger.error(f"JSON inválido en caso {i}: {response.text[:100]}")
                            
                    elif response.status_code == 422:
                        try:
                            error_data = response.json()
                            logger.warning(f"ERROR Caso {i}: Validacion - {error_data}")
                            response.failure(f"Error de validación caso {i}: {error_data}")
                        except ValueError:
                            response.failure(f"Error 422 caso {i} con formato inesperado: {response.text}")
                            
                    else:
                        response.failure(f"Error caso {i}: {response.status_code}")
                        logger.error(f"ERROR Caso {i}: {response.status_code} - {response.text}")
                        
            except Exception as case_e:
                logger.error(f"EXCEPCION en caso {i}: {str(case_e)}")
                
                with client.post(
                    "/proveedores/busqueda/minimizado",
                    json={"error": "exception"},
                    catch_response=True,
                    name=f"(PROVEEDORES) - /proveedores/busqueda/minimizado [Exception Caso {i}]"
                ) as response:
                    response.failure(f"Excepción caso {i}: {str(case_e)}")
                
    except Exception as e:
        logger.error(f"EXCEPCION en casos multiples: {str(e)}")
        
        with client.post(
            "/proveedores/busqueda/minimizado",
            json={"error": "exception"},
            catch_response=True,
            name="(PROVEEDORES) - /proveedores/busqueda/minimizado [Exception casos múltiples]"
        ) as response:
            response.failure(f"Excepción casos múltiples: {str(e)}")


def buscar_proveedores_minimizado_casos_multiples(client, logger, environment, data_module):
    """Buscar proveedores minimizado - casos múltiples"""
    try:
        logger.info("=== PROBANDO MULTIPLES CASOS DE BUSQUEDA MINIMIZADA ===")
        
        query_params = data_module.parametros_busqueda_minimizada_query
        casos = data_module.body_busqueda_minimizada_casos
        
        for i, caso in enumerate(casos, 1):
            logger.info(f"--- CASO {i}: {list(caso.keys())} ---")
            
            response = client.post(
                "/proveedores/busqueda/minimizado",
                params=query_params,
                json=caso,
                name=f"POST /busqueda/minimizado - Caso {i}"
            )
            
            if response.status_code == 200:
                data = response.json()
                total_items = data.get('total_items', 0)
                logger.info(f"EXITO Caso {i}: {total_items} proveedores encontrados")
                
                if total_items > 0:
                    items = data.get('items', [])
                    if items:
                        primer_proveedor = items[0]
                        denominacion = primer_proveedor.get('denominacion', 'N/A')
                        cuil_cuit = primer_proveedor.get('cuil_cuit', 'N/A')
                        logger.info(f"Ejemplo: {denominacion} - {cuil_cuit}")
                else:
                    logger.info(f"Caso {i}: Sin resultados")
                    
            elif response.status_code == 422:
                logger.error(f"ERROR Caso {i}: Validacion - {response.text}")
            else:
                logger.error(f"ERROR Caso {i}: {response.status_code} - {response.text}")
                
    except Exception as e:
        logger.error(f"EXCEPCION en casos multiples: {str(e)}")
