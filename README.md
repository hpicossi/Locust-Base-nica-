# Base Única - Scripts de Testing

## Descripción

Este proyecto contiene scripts automatizados para realizar pruebas de carga y funcionales sobre la API "Base Única" utilizando Locust. El sistema permite ejecutar pruebas contra diferentes ambientes (desarrollo, staging, clon, producción) con protecciones especiales para ambientes productivos.

## Características Principales

- **Detección automática de ambiente**: Identifica automáticamente el ambiente según la URL configurada
- **Protección de producción**: En ambientes productivos solo ejecuta endpoints GET (lectura)
- **Pruebas completas**: En ambientes de desarrollo ejecuta todos los endpoints (GET, POST, PUT)
- **Sistema de logging**: Genera logs detallados de todas las operaciones
- **Autenticación automática**: Sistema de autenticación Bearer token automatizado
- **Configuración multi-ambiente**: Soporte para múltiples configuraciones según el ambiente

## Estructura del Proyecto

```
.
├── data/                           # Datos de prueba por ambiente
│   ├── dev/                       # Datos para desarrollo
│   ├── stage/                     # Datos para staging
│   ├── clon/                      # Datos para clon
│   └── prod/                      # Datos para producción
├── tasks/                         # Módulos de tareas por dominio
│   ├── ambiente.py               # Endpoints relacionados con ambiente
│   ├── cerrojo_institucional.py  # Endpoints institucionales
│   ├── domicilio.py              # Gestión de domicilios
│   ├── educacion.py              # Servicios educativos
│   ├── habilitacion.py           # Habilitaciones comerciales
│   ├── infraestructura.py        # Infraestructura urbana
│   ├── parametricas.py           # Datos parametrizados
│   ├── persona_fisica.py         # Gestión de personas físicas
│   ├── persona_juridica.py       # Gestión de personas jurídicas
│   ├── proveedor.py              # Gestión de proveedores
│   ├── salud.py                  # Servicios de salud
│   ├── transporte.py             # Sistema de transporte
│   ├── tributario.py             # Sistema tributario
│   └── turismo.py                # Servicios turísticos
├── utils/                         # Utilidades del sistema
│   ├── auth.py                   # Sistema de autenticación
│   └── config.py                 # Configuración y logging
├── logs/                          # Directorio de logs (generado automáticamente)
├── .env                          # Variables de entorno
├── .gitignore                    # Archivos ignorados por git
└── locustfile.py                 # Script principal de Locust
```

## Módulos Principales

### Base Única User (locustfile.py)
- **Detección de ambiente**: Automática según URL
- **Autenticación**: Bearer token automatizada
- **Modo de ejecución**:
  - **Producción**: Solo endpoints GET (seguro)
  - **Desarrollo/Testing**: Todos los endpoints (GET, POST, PUT)

### Sistema de Configuración (utils/config.py)
- Detección automática de ambiente
- Carga de datos específicos por ambiente
- Sistema de logging centralizado
- Gestión de credenciales por ambiente

### Sistema de Autenticación (utils/auth.py)
- Autenticación Bearer token
- Gestión automática de credenciales
- Manejo de errores de autenticación

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Configuración del Entorno

1. **Clonar o descargar el proyecto**
   ```bash
   cd "script de base unica(Ultima version 24-07-2025)"
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install locust python-dotenv requests
   ```

5. **Configurar variables de entorno**
   - Copiar el archivo `.env.example` a `.env` (si existe)
   - O crear un nuevo archivo `.env` con las siguientes variables:
   ```env
   # URL base del ambiente (se detecta automáticamente)
   BASE_URL=https://tu-api-url.com

   # Credenciales por ambiente
   DEV_USER_LOGIN=tu_usuario_dev
   DEV_USER_PASSWORD=tu_password_dev

   STAGE_USER_LOGIN=tu_usuario_stage
   STAGE_USER_PASSWORD=tu_password_stage

   CLON_USER_LOGIN=tu_usuario_clon
   CLON_USER_PASSWORD=tu_password_clon

   PROD_USER_LOGIN=tu_usuario_prod
   PROD_USER_PASSWORD=tu_password_prod

   # Credenciales por defecto (fallback)
   USER_LOGIN=usuario_default
   USER_PASSWORD=password_default
   ```

## Uso del Sistema

### Ejecución Básica

#### Desde Línea de Comandos

```bash
# Ejecutar con interfaz web (recomendado)
locust -f locustfile.py --host=https://tu-api-url.com

# Ejecutar sin interfaz web (headless)
locust -f locustfile.py --host=https://tu-api-url.com --headless -u 1 -r 1 -t 60s
```

#### Desde Interfaz Web

1. Ejecutar el comando con interfaz web
2. Abrir navegador en `http://localhost:8089`
3. Configurar:
   - **Number of users**: 1 (recomendado para pruebas funcionales)
   - **Spawn rate**: 1
   - **Host**: URL de tu API
4. Hacer clic en "Start swarming"

### Parámetros de Configuración

- **-u, --users**: Número de usuarios simulados (recomendado: 1)
- **-r, --spawn-rate**: Velocidad de generación de usuarios (recomendado: 1)
- **-t, --run-time**: Tiempo de ejecución (ej: 60s, 5m, 1h)
- **--host**: URL base de la API
- **--headless**: Ejecutar sin interfaz web

### Ejemplos de Uso

```bash
# Prueba funcional básica (1 usuario, 1 minuto)
locust -f locustfile.py --host=https://api-dev.ejemplo.com --headless -u 1 -r 1 -t 1m

# Prueba con interfaz web
locust -f locustfile.py --host=https://api-stage.ejemplo.com

# Prueba específica para ambiente de producción
locust -f locustfile.py --host=https://api.cordoba.gob.ar --headless -u 1 -r 1 -t 30s
```

## Configuración por Ambiente

### Detección Automática

El sistema detecta automáticamente el ambiente basándose en la URL:

- **dev**: URLs que contienen "dev"
- **stage**: URLs que contienen "stage"  
- **clon**: URLs que contienen "clon"
- **prod**: URLs que contienen "cordoba.gob.ar" o por defecto

### Datos de Prueba

Cada ambiente tiene su propio directorio en `data/` con archivos específicos:
- `{ambiente}_persona_juridica_data.py`
- `{ambiente}_persona_fisica.py`
- `{ambiente}_domicilio.py`
- etc.

### Protecciones de Seguridad

#### Ambiente de Producción
- ✅ Solo ejecuta endpoints GET (lectura)
- ❌ NO ejecuta endpoints POST/PUT (escritura)
- 🛡️ Protección automática sin configuración adicional

#### Ambientes de Desarrollo/Testing
- ✅ Ejecuta todos los endpoints
- ✅ Incluye operaciones de escritura (POST/PUT)
- 🔧 Ideal para pruebas completas

## Sistema de Logging

### Configuración Automática

- **Directorio**: `logs/`
- **Archivo**: `base_unica_test.log`
- **Rotación**: Se limpia en cada nueva ejecución
- **Niveles**: INFO, WARNING, ERROR, CRITICAL

### Información Registrada

- Detección de ambiente
- Proceso de autenticación
- Resultados de cada endpoint
- Errores y excepciones
- Tiempos de respuesta
- Estados de ejecución

## Troubleshooting

### Problemas Comunes

#### Error de Autenticación
```
ERROR - Authentication failed
```
**Solución**: Verificar credenciales en `.env` para el ambiente correspondiente

#### Error de Conexión
```
ConnectionError: Failed to establish a new connection
```
**Solución**: Verificar que la URL sea correcta y esté accesible

#### Módulo de Datos No Encontrado
```
WARNING - No se pudo cargar: data.dev.dev_persona_juridica_data
```
**Solución**: Verificar que existan los archivos de datos para el ambiente

#### Error de Permisos en Logs
```
PermissionError: [Errno 13] Permission denied: 'logs/base_unica_test.log'
```
**Solución**: Cerrar cualquier aplicación que tenga abierto el archivo de log

### Verificación del Sistema

```bash
# Verificar instalación de Locust
locust --version

# Verificar estructura de archivos
dir tasks\
dir data\
dir utils\

# Probar configuración básica
python -c "from utils.config import detect_environment; print(detect_environment('https://api-dev.ejemplo.com'))"
```

## Mejores Prácticas

### Para Desarrollo
- Usar ambientes de desarrollo/staging para pruebas extensivas
- Verificar logs después de cada ejecución
- Mantener datos de prueba actualizados

### Para Producción
- **NUNCA** ejecutar pruebas masivas en producción
- Usar solo pruebas funcionales (1 usuario)
- Ejecutar en horarios de bajo tráfico
- Verificar que solo se ejecuten endpoints GET

### Mantenimiento
- Revisar y actualizar datos de prueba regularmente
- Mantener credenciales seguras y actualizadas
- Limpiar logs antiguos periódicamente
- Verificar compatibilidad con nuevos endpoints

## Seguridad

- ✅ Archivo `.env` incluido en `.gitignore`
- ✅ Credenciales nunca hardcodeadas
- ✅ Protección automática para producción
- ✅ Logs no contienen información sensible

## Contribución

Para agregar nuevos endpoints o módulos:

1. Crear archivo en `tasks/` siguiendo la estructura existente
2. Agregar datos de prueba en `data/{ambiente}/`
3. Importar y usar en `locustfile.py`
4. Actualizar documentación

## Versionado

- **Versión actual**: 24-07-2025
- **Última actualización**: Julio 2025
- **Python compatible**: 3.8+
- **Locust compatible**: 2.0+
