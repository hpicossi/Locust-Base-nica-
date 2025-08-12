import os
import importlib
import logging
import glob
import types
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Variable global para controlar si ya se configuró el logger
_logger_configured = False

# Detectar el ambiente basado en la URL de la API
def detect_environment(host_url=None):
    # Usar el host proporcionado o, si no está disponible, usar BASE_URL del .env
    base_url = host_url or os.getenv("BASE_URL", "")
    
    if "dev" in base_url:
        return "dev"
    elif "stage" in base_url:
        return "stage"
    elif "clon" in base_url:
        return "clon"
    elif "cordoba.gob.ar" in base_url:
        return "prod"
    else:
        return "prod"  # Por defecto

def load_data_for_environment(env_name, logger):
    # Lista de posibles nombres de módulos para intentar cargar
    possible_modules = [
        f"data.{env_name}.{env_name}_persona_juridica_data",
        f"data.{env_name}.{env_name}_cerrojo_institucional",
        f"data.{env_name}.{env_name}_persona_fisica",
       f"data.{env_name}.{env_name}_domicilio",
       f"data.{env_name}.{env_name}_proveedor",
       f"data.{env_name}.{env_name}_ambiente",
       f"data.{env_name}.{env_name}_educacion",
       f"data.{env_name}.{env_name}_habilitacion",
       f"data.{env_name}.{env_name}_infraestructura",
       f"data.{env_name}.{env_name}_salud",
       f"data.{env_name}.{env_name}_turismo",
       f"data.{env_name}.{env_name}_transporte",
       f"data.{env_name}.{env_name}_parametricas",
       f"data.{env_name}.{env_name}_tributario"
    ]
    
    # Crear un módulo combinado para acumular todos los datos
    combined_module = types.ModuleType('combined_data_module')
    
    loaded_any_module = False
    
    for module_name in possible_modules:
        try:
            logger.info(f"Intentando cargar módulo: {module_name}")
            data_module = importlib.import_module(module_name)
            logger.info(f"Datos cargados correctamente desde: {module_name}")
            
            # Copiar todos los atributos del módulo cargado al módulo combinado
            for attr_name in dir(data_module):
                # Ignorar atributos especiales de Python que comienzan con __
                if not attr_name.startswith('__'):
                    setattr(combined_module, attr_name, getattr(data_module, attr_name))
            
            loaded_any_module = True
        except ImportError as e:
            logger.warning(f"No se pudo cargar: {module_name}, error: {str(e)}")
    
    # Si al menos se cargó un módulo, devolver el módulo combinado
    if loaded_any_module:
        return combined_module
    
    # Si ninguno de los módulos se cargó, intentamos con los datos de producción
    logger.warning("Intentando cargar datos de producción como alternativa")
    possible_prod_modules = [
        "data.prod.prod_persona_juridica_data",
        "data.prod.prod_base_unica_data",
        "data.prod.prod_cerrojo_institucional",
        "data.prod.prod_persona_fisica",
        "data.prod.prod_domicilio",
        "data.prod.prod_proveedor",
        "data.prod.prod_ambiente",
        "data.prod.prod_educacion",
        "data.prod.prod_habilitacion",
        "data.prod.prod_infraestructura",
        "data.prod.prod_salud",
        "data.prod.prod_turismo",
        "data.prod.prod_transporte",
        "data.prod.prod_parametrica",
        "data.prod.prod_tributario",
    ]
    
    for module_name in possible_prod_modules:
        try:
            logger.info(f"Intentando cargar módulo de producción: {module_name}")
            data_module = importlib.import_module(module_name)
            logger.info("Datos de producción cargados como alternativa")
            
            # Copiar todos los atributos del módulo cargado al módulo combinado
            for attr_name in dir(data_module):
                if not attr_name.startswith('__'):
                    setattr(combined_module, attr_name, getattr(data_module, attr_name))
            
            loaded_any_module = True
        except ImportError as e:
            logger.warning(f"No se pudo cargar: {module_name}, error: {str(e)}")
    
    # Si se cargó algún módulo de producción, devolver el módulo combinado
    if loaded_any_module:
        return combined_module
    
    # Si todos los intentos fallan, creamos un módulo vacío con datos mínimos
    logger.critical("No se pudieron cargar los datos. El test podría fallar.")
    
    # Estructura mínima para evitar errores
    setattr(combined_module, 'p_cuit', ["00000000000"])
    setattr(combined_module, 'p_nivel', [2])  # Valor predeterminado para p_nivel
    
    return combined_module

# Obtener credenciales basadas en el entorno
def get_credentials_for_environment(env_name):
    env_name = env_name.upper()  # Convertir a mayúsculas para coincidir con las variables de entorno
    
    # Obtener credenciales específicas del .env según el ambiente detectado
    username = os.getenv(f"{env_name}_USER_LOGIN", "")
    password = os.getenv(f"{env_name}_USER_PASSWORD", "")
    
    logger = logging.getLogger("base_unica_test")
    logger.info(f"Usando credenciales para ambiente {env_name}: usuario={username}")
    
    if not username or not password:
        logger.warning(f"Credenciales no encontradas para ambiente {env_name}. Usando valores por defecto.")
        return {
            "username": os.getenv("USER_LOGIN", ""),
            "password": os.getenv("USER_PASSWORD", "")
        }
    
    return {
        "username": username,
        "password": password
    }

# Función para limpiar logs existentes
def clear_existing_logs():
    """Limpia todos los archivos .log del directorio logs"""
    log_dir = "logs"
    
    if os.path.exists(log_dir):
        for archivo_log in glob.glob(f"{log_dir}/*.log"):
            try:
                os.remove(archivo_log)
                print(f"Archivo de log eliminado: {archivo_log}")
            except Exception as e:
                print(f"No se pudo eliminar el archivo {archivo_log}: {str(e)}")

# Función para cerrar y limpiar handlers del logger
def close_logger_handlers():
    """Cierra todos los handlers del logger actual para liberar el archivo"""
    logger = logging.getLogger("base_unica_test")
    
    # Cerrar y remover todos los handlers
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

# Función para reiniciar el log para una nueva prueba
def reset_log_for_new_test():
    """Reinicia completamente el sistema de logging para una nueva prueba"""
    global _logger_configured
    
    print("=== INICIANDO NUEVA PRUEBA - LIMPIANDO LOGS ===")
    
    # Cerrar handlers existentes para liberar el archivo
    close_logger_handlers()
    
    # Limpiar logs existentes
    clear_existing_logs()
    
    # Marcar que necesitamos reconfigurar el logger
    _logger_configured = False
    
    # Configurar el logger nuevamente
    return setup_logger()

# Configurar el sistema de logging
def setup_logger():
    """Configura el logger para las pruebas"""
    global _logger_configured
    
    # Configurar directorio de logs
    log_dir = "logs"
    log_file = f"{log_dir}/base_unica_test.log"
    
    # Crear directorio de logs si no existe
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Directorio de logs creado: {log_dir}")
    
    # Si es la primera vez que se configura, limpiar logs existentes
    if not _logger_configured:
        clear_existing_logs()
        _logger_configured = True
    
    # Configuración del logger
    logger = logging.getLogger("base_unica_test")
    logger.setLevel(logging.INFO)
    
    # Limpiar los handlers existentes si los hay
    if logger.handlers:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info("=== INICIO DE NUEVA SESIÓN DE PRUEBAS ===")
    return logger
