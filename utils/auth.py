import os

def authenticate(client, logger, credentials=None):
    """Maneja la autenticación del usuario con el API"""

    # Usar credenciales pasadas como parámetro o tomar de variables de entorno
    username = credentials.get("username") if credentials else os.getenv("USERNAME", "")
    password = credentials.get("password") if credentials else os.getenv("PASSWORD", "")
    
    if not username or not password:
        logger.error("Credenciales no configuradas en archivo .env")
        logger.error("Asegúrate de tener las variables USER_LOGIN y USER_PASSWORD configuradas")
        return None
    
    # Autenticación usando form-data
    login_data = {
        "username": username,
        "password": password
    }
    
    logger.info(f"Iniciando autenticación para usuario: {username}")
    
    try:
        with client.post("/login", data=login_data, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    token = response_data.get("access_token")
                    
                    # Verificar que el token sea válido
                    if not token:
                        response.failure("Token no encontrado en la respuesta")
                        logger.error("La respuesta de autenticación no contiene un token válido")
                        return None
                    
                    response.success()
                    logger.info("Autenticación exitosa")
                    return token
                    
                except ValueError as e:
                    response.failure(f"Error decodificando JSON: {str(e)}")
                    logger.error(f"La respuesta no es un JSON válido: {str(e)}")
                    return None
            
            else:
                response.failure(f"Error de autenticación: {response.status_code}")
                logger.error(f"Error en autenticación: {response.status_code}")
                return None
                
    except Exception as e:
        logger.error(f"Excepción durante la autenticación: {str(e)}")
        return None
