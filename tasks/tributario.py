def get_deuda_inmueble(client, logger, environment, data_module):
    """Consultar cuenta corriente municipal de un inmueble"""
    try:
        logger.info("=== CONSULTANDO CUENTA CORRIENTE DE INMUEBLE ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_deuda_inmueble
        
        response = client.get(
            "/tributario/inmuebles/ctacte",
            params=params,
            name="(TRIBUTARIO) - /tributario/inmuebles/ctacte"
        )   
        
        if response.status_code == 200:
            data = response.json()
            logger.info("EXITO: Cuenta corriente de inmueble consultada exitosamente")
            logger.info(f"ID Inmueble: {data.get('id_inmueble', 'N/A')}")
            logger.info(f"Superficie total: {data.get('superficie', 'N/A')} m2")
            logger.info(f"Total deuda: ${data.get('total_deuda', 'N/A')}")
            
            # Información del propietario
            if data.get('nombre') and data.get('apellido'):
                logger.info(f"Propietario PF: {data.get('apellido')} {data.get('nombre')} - CUIL: {data.get('cuil', 'N/A')}")
            elif data.get('razon_social'):
                logger.info(f"Propietario PJ: {data.get('razon_social')} - CUIT: {data.get('cuit', 'N/A')}")
            elif data.get('nombre_alt'):
                logger.info(f"Propietario Alt: {data.get('nombre_alt')} - CUIT: {data.get('cuit_alt', 'N/A')}")
            
            # Información de cuotas
            ctactes = data.get('ctactes_dict', [])
            if ctactes:
                logger.info(f"Total de cuotas en cuenta corriente: {len(ctactes)}")
                
                # Mostrar algunas cuotas de ejemplo
                for i, cuota in enumerate(ctactes[:3]):
                    estado = cuota.get('estado', 'N/A')
                    año = cuota.get('año', 'N/A')
                    num_cuota = cuota.get('cuota', 'N/A')
                    saldo = cuota.get('saldo', 'N/A')
                    logger.info(f"Cuota {i+1}: {año}/{num_cuota} - Saldo: ${saldo} - Estado: {estado}")
                
                if len(ctactes) > 3:
                    logger.info(f"... y {len(ctactes) - 3} cuotas mas")
            else:
                logger.info("No hay cuotas pendientes en la cuenta corriente")
                
        elif response.status_code == 400:
            logger.error(f"ERROR 400: Denominacion catastral invalida - {response.text}")
        elif response.status_code == 404:
            logger.error(f"ERROR 404: No se encontraron datos para la denominacion catastral - {response.text}")
        elif response.status_code == 403:
            logger.error("ERROR 403: Sin permisos para consultar cuenta corriente de inmuebles")
        else:
            logger.error(f"ERROR: Error al consultar cuenta corriente: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"EXCEPCION: Error al consultar cuenta corriente de inmueble: {str(e)}")

def get_deuda_rodado(client, logger, environment, data_module):
    """Consultar cuenta corriente municipal de un rodado"""
    try:
        logger.info("=== CONSULTANDO CUENTA CORRIENTE DE RODADO ===")
        
        # Usar parámetros del módulo de datos
        params = data_module.parametros_deuda_rodado
        
        # Log para debug - ver qué parámetros se están enviando
        logger.info(f"Parámetros enviados: {params}")
        
        response = client.get(
            "/tributario/rodados/ctacte",
            params=params,
            name="(TRIBUTARIO) - /tributario/rodados/ctacte",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        
        # Log para debug - ver la URL completa que se está llamando
        logger.info(f"URL completa: {response.url}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("EXITO: Cuenta corriente de rodado consultada exitosamente")
            logger.info(f"ID Rodado: {data.get('id_rodado', 'N/A')}")
            logger.info(f"Dominio: {params.get('p_dominio', 'N/A')}")
            logger.info(f"Marca: {data.get('marca', 'N/A')} - Modelo: {data.get('modelo', 'N/A')} ({data.get('modelo_anio', 'N/A')})")
            logger.info(f"Categoría: {data.get('categoria', 'N/A')} - Tipo: {data.get('tipo', 'N/A')}")
            logger.info(f"Total deuda: ${data.get('total_deuda', 'N/A')}")
            
            # Información del propietario
            if data.get('nombre') and data.get('apellido'):
                logger.info(f"Propietario PF: {data.get('apellido')} {data.get('nombre')} - CUIL: {data.get('cuil', 'N/A')}")
            elif data.get('razon_social'):
                logger.info(f"Propietario PJ: {data.get('razon_social')} - CUIT: {data.get('cuit', 'N/A')}")
            elif data.get('nombre_alt'):
                logger.info(f"Propietario Alt: {data.get('nombre_alt')} - CUIT: {data.get('cuit_alt', 'N/A')}")
            
            # Información de cuotas
            ctactes = data.get('ctactes_dict', [])
            if ctactes:
                logger.info(f"Total de cuotas en cuenta corriente: {len(ctactes)}")
                
                # Mostrar algunas cuotas de ejemplo
                for i, cuota in enumerate(ctactes[:3]):
                    estado = cuota.get('estado', 'N/A')
                    año = cuota.get('año', 'N/A')
                    num_cuota = cuota.get('cuota', 'N/A')
                    saldo = cuota.get('saldo', 'N/A')
                    logger.info(f"Cuota {i+1}: {año}/{num_cuota} - Saldo: ${saldo} - Estado: {estado}")
                
                if len(ctactes) > 3:
                    logger.info(f"... y {len(ctactes) - 3} cuotas más")
            else:
                logger.info("No hay cuotas pendientes en la cuenta corriente")
                
        elif response.status_code == 400:
            logger.error(f"ERROR 400: Dominio inválido - {response.text}")
        elif response.status_code == 404:
            logger.error(f"ERROR 404: No se encontraron datos para el dominio - {response.text}")
        elif response.status_code == 403:
            logger.error("ERROR 403: Sin permisos para consultar cuenta corriente de rodados")
        elif response.status_code == 500:
            logger.error(f"ERROR 500: Error interno del servidor - {response.text}")
            logger.error(f"Headers de la petición: {response.request.headers}")
            logger.error(f"URL de la petición: {response.request.url}")
        else:
            logger.error(f"ERROR: Error al consultar cuenta corriente: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"EXCEPCION: Error al consultar cuenta corriente de rodado: {str(e)}")
