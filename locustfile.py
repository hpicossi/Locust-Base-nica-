import os
from locust import HttpUser, task, between, events

# Importar módulos refactorizados
from tasks.ambiente import get_espacios_verdes, get_campanas_pet, get_recoleccion_residuos_diferenciada
from tasks.domicilio import get_barrios_por_localidad, get_calles_por_localidad, get_departamentos_por_provincia, get_domicilio_cpc_by_id, get_localidades_por_departamento, get_paises, get_provincias_por_pais, insert_domicilio, insert_domicilio_ampliado, insert_domicilio_geo, get_domicilio_geo, get_domicilio_by_id, insert_incidente
from tasks.educacion import get_escuelas_municipales, get_jardines_municipales, get_parques_educativos
from tasks.habilitacion import get_comercios, get_geriatricos_privados, get_jardines_maternales_privados
from tasks.infraestructura import get_obra_publica, get_puntos_wifi
from tasks.parametricas import get_actividades, get_banco_by_id, get_bancos, get_cfiscal, get_dispositivos_pagos, get_fjuridica, get_medios_pagos, get_profesion_by_id, get_profesiones, put_medios_pagos
from tasks.persona_fisica import get_comunicaciones_personas, get_personas_fisicas, insert_comunicaciones_personas, insert_domicilio_persona_fisica, insert_or_update_persona_fisica, insert_or_update_persona_fisica_by_dni, insert_or_update_persona_fisica_simplificada
from tasks.persona_juridica import get_persona_juridica, get_sedes_pj, insert_domicilio_sede, insert_domicilio_sede_pj, insert_persona_juridica
from tasks.proveedor import alta_cbu_banco_proveedor, alta_proveedor, buscar_personas_por_cuils_cuits, buscar_proveedores_minimizado, buscar_proveedores_minimizado_casos_multiples, buscar_proveedores_por_ids, buscar_proveedores_por_parametros, get_proveedor_by_cuit_cuil, get_proveedores_por_actividad, insert_or_update_proveedor
from tasks.salud import get_centros_salud
from tasks.transporte import get_centrales_agencias, get_chapas, get_chapas_por_cuil, get_ciclovias, get_condiciones, get_empresas, get_estacionamiento_bicicletas, get_estados_licencias, get_leasing, get_licencias_por_parametros, get_paradas_linea, get_permisionarios_por_parametros, get_persona_fisica_por_chapa, get_personal, get_recorridos_lineas, get_situaciones_chapas, get_tipos_servicios, get_vehiculos, get_zona_semm
from tasks.tributario import get_deuda_inmueble, get_deuda_rodado
from tasks.turismo import get_anfitriones_turisticos, get_guias_turisticos
from utils.config import detect_environment, load_data_for_environment, reset_log_for_new_test, setup_logger, get_credentials_for_environment
from utils.auth import authenticate
from tasks.cerrojo_institucional import get_all_cpc, get_barrios_cpc, get_centros_operativos, get_centros_vecinales, get_dependencia_mas_alta, get_dependencias_directas, get_dependencias_por_parametros, get_dependencias_ruta, get_fechas_no_habiles, get_limites_administrativos, get_organigrama_completo, get_organigrama_por_dependencia, get_organigrama_por_nivel, get_organigrama_por_niveles, get_organizaciones_sociales, get_tipos_organizaciones_sociales, get_unidades_judiciales, post_dependencias_por_ids, update_dependencias_visibility

# Inicializar el logger
logger = setup_logger()

# Variables globales para host y ambiente
current_host = None
environment_name = None
data_module = None

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global current_host, environment_name, data_module, logger
    
    # Reiniciar el log para una nueva prueba
    logger = reset_log_for_new_test()
    logger.info("🔄 NUEVA PRUEBA INICIADA - LOG REINICIADO 🔄")
    
    # Capturar el host definido en la línea de comandos o en la interfaz web
    current_host = environment.host
    logger.info(f"Host capturado: {current_host}")
    
    # Detectar el ambiente basado en el host
    environment_name = detect_environment(current_host)
    logger.info(f"Ambiente detectado para el host {current_host}: {environment_name}")
    
    # Cargar datos correspondientes al ambiente
    data_module = load_data_for_environment(environment_name, logger)

class BaseUnicaUser(HttpUser):
    wait_time = between(1, 3)
   
    # Variables para autenticación
    token = None
    task_executed = False
   
    def on_start(self):
        try:
            # Usar el host capturado de la sesión
            self.host = current_host or os.getenv("BASE_URL")
            logger.info(f"Usando host: {self.host}")
            
            # Cargar lista de CUITs de muestra
            self.sample_cuits = data_module.p_cuit
            
            # Obtener credenciales específicas para el ambiente detectado
            credentials = get_credentials_for_environment(environment_name)
            logger.info(f"Usando credenciales para ambiente: {environment_name}")
            
            # Autenticar usuario con las credenciales específicas
            self.token = authenticate(self.client, logger, credentials)
            
            if not self.token and self.environment.parsed_options.headless:
                # En modo headless, terminamos la ejecución
                logger.error("Terminando ejecución en modo headless debido a falta de credenciales")
                self.environment.runner.quit()
                return
            
            # Configurar el token en los encabezados para todas las solicitudes
            if self.token:
                self.client.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                
        except Exception as e:
            # Capturar cualquier error en la configuración general
            logger.critical(f"ERROR CRÍTICO en on_start: {str(e)}")

    def on_stop(self):
        logger.info("Test finalizado. Se ejecutó una sola vez.")

    def is_production_environment(self):
        """Determina si estamos en ambiente de producción"""
        # Opción 1: Basado en el nombre del ambiente detectado
        if environment_name and environment_name.lower() in ['produccion', 'prod', 'production']:
            return True
        
        # Opción 2: Basado en el host
        if current_host and any(prod_indicator in current_host.lower() for prod_indicator in ['prod', 'production']):
            return True
        
        # Opción 3: Variable de entorno específica
        if os.getenv("LOCUST_PRODUCTION_MODE", "false").lower() == "true":
            return True
        
        # Opción 4: Basado en patrones de URL de producción
        production_patterns = [
            'api.cordoba.gob.ar',
            'produccion.',
            'prod.',
            # Agregar más patrones según sea necesario
        ]
        
        if current_host and any(pattern in current_host.lower() for pattern in production_patterns):
            return True
        
        return False

    def execute_get_endpoints_only(self):
        """Ejecuta solo endpoints GET (modo producción)"""
        logger.info("=== MODO PRODUCCIÓN: EJECUTANDO SOLO ENDPOINTS GET ===")
        
        # -------CERROJO(INSTITUCIONAL)----------- (Solo GET)

        get_centros_operativos(self.client, logger, self.environment, data_module)
        get_dependencias_por_parametros(self.client, logger, self.environment, data_module)
        post_dependencias_por_ids(self.client, logger, self.environment, data_module)  # POST
        get_fechas_no_habiles(self.client, logger, self.environment, data_module)
        get_limites_administrativos(self.client, logger, self.environment, data_module)
        get_organigrama_completo(self.client, logger, self.environment, data_module)
        get_dependencias_directas(self.client, logger, self.environment, data_module)
        get_dependencias_ruta(self.client, logger, self.environment, data_module)
        get_organigrama_por_nivel(self.client, logger, self.environment, data_module) 
        get_organigrama_por_niveles(self.client, logger, self.environment, data_module)   
        get_dependencia_mas_alta(self.client, logger, self.environment, data_module)
        get_organigrama_por_dependencia(self.client, logger, self.environment, data_module)
        get_centros_vecinales(self.client, logger, self.environment, data_module)
        get_all_cpc(self.client, logger, self.environment, data_module)   
        get_barrios_cpc(self.client, logger, self.environment, data_module)
        get_organizaciones_sociales(self.client, logger, self.environment, data_module)
        get_tipos_organizaciones_sociales(self.client, logger, self.environment, data_module)
        get_unidades_judiciales(self.client, logger, self.environment, data_module)

        # --------PERSONA FISICA------------ (Solo GET)
        get_personas_fisicas(self.client, logger, self.environment, data_module)
        get_comunicaciones_personas(self.client, logger, self.environment, data_module)

        # --------PERSONA JURIDICA----------- (Solo GET)
        get_persona_juridica(self.client, logger, self.environment, self.sample_cuits)
        get_sedes_pj(self.client, logger, self.environment, data_module)

        # --------PROVEEDOR------------ (Solo GET)
        get_proveedor_by_cuit_cuil(self.client, logger, self.environment, data_module)
        buscar_personas_por_cuils_cuits(self.client, logger, self.environment, data_module)
        get_proveedores_por_actividad(self.client, logger, self.environment, data_module)
        buscar_proveedores_por_parametros(self.client, logger, self.environment, data_module)
        buscar_proveedores_por_ids(self.client, logger, self.environment, data_module)
        buscar_proveedores_minimizado(self.client, logger, self.environment, data_module)
        # # # Prueba varias casos donde en los datos se tiene descomentar los multiples casos dependiendo del ambiente
        # buscar_proveedores_minimizado_casos_multiples(self.client, logger, self.environment, data_module)

        # --------DOMICILIO------------ (Solo GET)
        get_barrios_por_localidad(self.client, logger, self.environment, data_module)
        get_calles_por_localidad(self.client, logger, self.environment, data_module)
        get_paises(self.client, logger, self.environment, data_module)
        get_provincias_por_pais(self.client, logger, self.environment, data_module)
        get_departamentos_por_provincia(self.client, logger, self.environment, data_module)
        get_localidades_por_departamento(self.client, logger, self.environment, data_module)
        get_domicilio_geo(self.client, logger, self.environment, data_module)
        get_domicilio_by_id(self.client, logger, self.environment, data_module)
        get_domicilio_cpc_by_id(self.client, logger, self.environment, data_module)

        # --------AMBIENTE------------ (Solo GET)
        get_espacios_verdes(self.client, logger, self.environment, data_module)
        get_campanas_pet(self.client, logger, self.environment, data_module)
        get_recoleccion_residuos_diferenciada(self.client, logger, self.environment, data_module)

        # --------EDUCACION------------ (Solo GET)

        get_parques_educativos(self.client, logger, self.environment, data_module)
        get_escuelas_municipales(self.client, logger, self.environment, data_module)
        get_jardines_municipales(self.client, logger, self.environment, data_module)

        # --------HABILITACION------------ (Solo GET por ahora)

        get_comercios(self.client, logger, self.environment, data_module)
        get_geriatricos_privados(self.client, logger, self.environment, data_module)
        get_jardines_maternales_privados(self.client, logger, self.environment, data_module)

        # --------INFRAESTRUCTURA------------ (Solo GET por ahora)

        get_puntos_wifi(self.client, logger, self.environment, data_module)
        get_obra_publica(self.client, logger, self.environment, data_module)

        # --------SALUD------------ (Solo GET por ahora)

        get_centros_salud(self.client, logger, self.environment, data_module)

        # --------TURISMO------------ (Solo GET por ahora)

        get_guias_turisticos(self.client, logger, self.environment, data_module)
        get_anfitriones_turisticos(self.client, logger, self.environment, data_module)

        # --------TRANSPORTE------------ (Solo GET)
        get_condiciones(self.client, logger, self.environment, data_module)
        get_estacionamiento_bicicletas(self.client, logger, self.environment, data_module)
        get_estados_licencias(self.client, logger, self.environment, data_module)
        get_situaciones_chapas(self.client, logger, self.environment, data_module)
        get_tipos_servicios(self.client, logger, self.environment, data_module)
        get_zona_semm(self.client, logger, self.environment, data_module)
        get_chapas(self.client, logger, self.environment, data_module)
        get_leasing(self.client, logger, self.environment, data_module)
        get_centrales_agencias(self.client, logger, self.environment, data_module)
        get_persona_fisica_por_chapa(self.client, logger, self.environment, data_module)
        get_chapas_por_cuil(self.client, logger, self.environment, data_module)
        get_permisionarios_por_parametros(self.client, logger, self.environment, data_module)
        get_licencias_por_parametros(self.client, logger, self.environment, data_module)
        get_ciclovias(self.client, logger, self.environment, data_module)
        get_personal(self.client, logger, self.environment, data_module)
        get_empresas(self.client, logger, self.environment, data_module)
        get_recorridos_lineas(self.client, logger, self.environment, data_module)
        get_paradas_linea(self.client, logger, self.environment, data_module)
        get_vehiculos(self.client, logger, self.environment, data_module)


        # --------PARAMETRICAS------------ (Solo GET)

        get_medios_pagos(self.client, logger, self.environment, data_module)
        get_cfiscal(self.client, logger, self.environment, data_module)
        get_fjuridica(self.client, logger, self.environment, data_module)
        get_bancos(self.client, logger, self.environment, data_module)
        get_banco_by_id(self.client, logger, self.environment, data_module)
        get_profesiones(self.client, logger, self.environment, data_module)
        get_profesion_by_id(self.client, logger, self.environment, data_module)
        get_dispositivos_pagos(self.client, logger, self.environment, data_module)
        get_actividades(self.client, logger, self.environment, data_module)

        # # --------TRIBUTARIO------------ (Solo GET)
        get_deuda_inmueble(self.client, logger, self.environment, data_module)
        get_deuda_rodado(self.client, logger, self.environment, data_module)

    def execute_all_endpoints(self):
        """Ejecuta todos los endpoints (modo desarrollo/testing)"""
        logger.info("=== MODO DESARROLLO: EJECUTANDO TODOS LOS ENDPOINTS ===")
        
        # -------PERSONA JURIDICA----------- 
        get_persona_juridica(self.client, logger, self.environment, self.sample_cuits)
        get_sedes_pj(self.client, logger, self.environment, data_module)
        insert_persona_juridica(self.client, logger, self.environment, data_module.body_insertar_persona_juridica)
        insert_domicilio_sede_pj(self.client, logger, self.environment, data_module.body_insertar_sede)
        insert_domicilio_sede(self.client, logger, self.environment, data_module.body_insertar_domicilio_sede)

        # -------CERROJO(INSTITUCIONAL)----------- 
                
        get_centros_operativos(self.client, logger, self.environment, data_module)
        get_dependencias_por_parametros(self.client, logger, self.environment, data_module)
        post_dependencias_por_ids(self.client, logger, self.environment, data_module)  # POST
        update_dependencias_visibility(self.client, logger, self.environment, data_module)  # POST
        get_fechas_no_habiles(self.client, logger, self.environment, data_module)
        get_limites_administrativos(self.client, logger, self.environment, data_module)
        get_organigrama_completo(self.client, logger, self.environment, data_module)
        get_dependencias_directas(self.client, logger, self.environment, data_module)
        get_dependencias_ruta(self.client, logger, self.environment, data_module)
        get_organigrama_por_nivel(self.client, logger, self.environment, data_module) 
        get_organigrama_por_niveles(self.client, logger, self.environment, data_module)   
        get_dependencia_mas_alta(self.client, logger, self.environment, data_module)
        get_organigrama_por_dependencia(self.client, logger, self.environment, data_module)
        get_centros_vecinales(self.client, logger, self.environment, data_module)
        get_all_cpc(self.client, logger, self.environment, data_module)   
        get_barrios_cpc(self.client, logger, self.environment, data_module)
        get_organizaciones_sociales(self.client, logger, self.environment, data_module)
        get_tipos_organizaciones_sociales(self.client, logger, self.environment, data_module)
        get_unidades_judiciales(self.client, logger, self.environment, data_module)



        # --------PERSONA FISICA------------ 
        insert_or_update_persona_fisica(self.client, logger, self.environment, data_module)  # POST

        # Este endpoint queda excluido por la causa de que no se puede insertar una persona física con el mismo DNI
        # insert_or_update_persona_fisica_by_dni(self.client, logger, self.environment, data_module)  # POST

        insert_or_update_persona_fisica_simplificada(self.client, logger, self.environment, data_module)  # POST
        get_personas_fisicas(self.client, logger, self.environment, data_module)
        insert_domicilio_persona_fisica(self.client, logger, self.environment, data_module)  # POST
        get_comunicaciones_personas(self.client, logger, self.environment, data_module)
        insert_comunicaciones_personas(self.client, logger, self.environment, data_module)  # POST

        # --------PROVEEDOR------------ 
        get_proveedor_by_cuit_cuil(self.client, logger, self.environment, data_module)
        insert_or_update_proveedor(self.client, logger, self.environment, data_module)  # POST
        buscar_personas_por_cuils_cuits(self.client, logger, self.environment, data_module)
        alta_proveedor(self.client, logger, self.environment, data_module)  # POST
        alta_cbu_banco_proveedor(self.client, logger, self.environment, data_module)  # POST
        get_proveedores_por_actividad(self.client, logger, self.environment, data_module)
        buscar_proveedores_por_parametros(self.client, logger, self.environment, data_module)
        buscar_proveedores_por_ids(self.client, logger, self.environment, data_module)
        buscar_proveedores_minimizado(self.client, logger, self.environment, data_module)
        # # # Prueba varias casos donde en los datos se tiene descomentar los multiples casos dependiendo del ambiente
        # buscar_proveedores_minimizado_casos_multiples(self.client, logger, self.environment, data_module)

        # --------DOMICILIO------------ 
        get_barrios_por_localidad(self.client, logger, self.environment, data_module)
        get_calles_por_localidad(self.client, logger, self.environment, data_module)
        get_paises(self.client, logger, self.environment, data_module)
        get_provincias_por_pais(self.client, logger, self.environment, data_module)
        get_departamentos_por_provincia(self.client, logger, self.environment, data_module)
        get_localidades_por_departamento(self.client, logger, self.environment, data_module)
        insert_domicilio(self.client, logger, self.environment, data_module)  # POST
        insert_domicilio_ampliado(self.client, logger, self.environment, data_module)  # POST
        insert_domicilio_geo(self.client, logger, self.environment, data_module)  # POST
        get_domicilio_geo(self.client, logger, self.environment, data_module)
        get_domicilio_by_id(self.client, logger, self.environment, data_module)
        insert_incidente(self.client, logger, self.environment, data_module)  # POST
        get_domicilio_cpc_by_id(self.client, logger, self.environment, data_module)

        # --------AMBIENTE------------
        get_espacios_verdes(self.client, logger, self.environment, data_module)
        get_campanas_pet(self.client, logger, self.environment, data_module)
        get_recoleccion_residuos_diferenciada(self.client, logger, self.environment, data_module)

        # --------EDUCACION------------ 

        get_parques_educativos(self.client, logger, self.environment, data_module)
        get_escuelas_municipales(self.client, logger, self.environment, data_module)
        get_jardines_municipales(self.client, logger, self.environment, data_module)

        # --------HABILITACION------------ 

        get_comercios(self.client, logger, self.environment, data_module)
        get_geriatricos_privados(self.client, logger, self.environment, data_module)
        get_jardines_maternales_privados(self.client, logger, self.environment, data_module)

        # --------INFRAESTRUCTURA------------ 

        get_puntos_wifi(self.client, logger, self.environment, data_module)
        get_obra_publica(self.client, logger, self.environment, data_module)

        # --------SALUD------------ 

        get_centros_salud(self.client, logger, self.environment, data_module)

        # --------TURISMO------------ 

        get_guias_turisticos(self.client, logger, self.environment, data_module)
        get_anfitriones_turisticos(self.client, logger, self.environment, data_module)

        # --------TRANSPORTE------------ 

        get_condiciones(self.client, logger, self.environment, data_module)   
        get_estacionamiento_bicicletas(self.client, logger, self.environment, data_module)  
        get_estados_licencias(self.client, logger, self.environment, data_module)
        get_situaciones_chapas(self.client, logger, self.environment, data_module)
        get_tipos_servicios(self.client, logger, self.environment, data_module)
        get_zona_semm(self.client, logger, self.environment, data_module)
        get_chapas(self.client, logger, self.environment, data_module)
        get_leasing(self.client, logger, self.environment, data_module)
        get_centrales_agencias(self.client, logger, self.environment, data_module)
        get_persona_fisica_por_chapa(self.client, logger, self.environment, data_module)
        get_chapas_por_cuil(self.client, logger, self.environment, data_module)
        get_permisionarios_por_parametros(self.client, logger, self.environment, data_module)
        get_licencias_por_parametros(self.client, logger, self.environment, data_module)
        get_ciclovias(self.client, logger, self.environment, data_module)
        get_personal(self.client, logger, self.environment, data_module)
        get_empresas(self.client, logger, self.environment, data_module)
        get_recorridos_lineas(self.client, logger, self.environment, data_module)
        get_paradas_linea(self.client, logger, self.environment, data_module)
        get_vehiculos(self.client, logger, self.environment, data_module)

        # --------PARAMETRICAS------------ 

        get_medios_pagos(self.client, logger, self.environment, data_module)
        get_cfiscal(self.client, logger, self.environment, data_module)
        get_fjuridica(self.client, logger, self.environment, data_module)
        get_bancos(self.client, logger, self.environment, data_module)
        get_banco_by_id(self.client, logger, self.environment, data_module)
        get_profesiones(self.client, logger, self.environment, data_module)
        get_profesion_by_id(self.client, logger, self.environment, data_module)
        put_medios_pagos(self.client, logger, self.environment, data_module)
        get_dispositivos_pagos(self.client, logger, self.environment, data_module)
        get_actividades(self.client, logger, self.environment, data_module)

        # # --------TRIBUTARIO------------ 

        get_deuda_inmueble(self.client, logger, self.environment, data_module)
        get_deuda_rodado(self.client, logger, self.environment, data_module)

    @task
    def run_once(self):
        """Esta tarea ejecuta toda la secuencia de pruebas una sola vez"""
        if not self.task_executed:
            # Ejecutar las pruebas en secuencia
            logger.info("Iniciando ejecución única de pruebas")
            
            # Determinar qué endpoints ejecutar basado en el ambiente
            if self.is_production_environment():
                logger.warning("🚨 AMBIENTE DE PRODUCCIÓN DETECTADO - EJECUTANDO SOLO ENDPOINTS GET 🚨")
                self.execute_get_endpoints_only()
            else:
                logger.info("🔧 AMBIENTE DE DESARROLLO/TESTING - EJECUTANDO TODOS LOS ENDPOINTS 🔧")
                self.execute_all_endpoints()

            # Marcar como ejecutado y detener
            self.task_executed = True
            logger.info("Test completado con éxito. Deteniendo ejecución.")

            # Detener la ejecución después de completar la tarea
            self.environment.runner.quit()

