# Arquitectura de Infraestructura - CarriAcces

## 1. Entorno de Desarrollo vs Producción

### 1.1 Arquitectura de Desarrollo (Docker)
```
┌─────────────────────────────────────────────────────────────┐
│                     DOCKER DEVELOPMENT                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │   WEB CONTAINER │     │   DB CONTAINER  │               │
│  │                 │     │                 │               │
│  │ Django 5.2.2    │◄────┤ PostgreSQL 15   │               │
│  │ Python 3.13     │     │                 │               │
│  │ Port: 8000      │     │ Port: 5432      │               │
│  │                 │     │                 │               │
│  │ Volumes:        │     │ Volumes:        │               │
│  │ - ./:/app       │     │ - postgres_data │               │
│  │ - ./media:/app/ │     │                 │               │
│  │   media         │     │ Env:            │               │
│  │                 │     │ - POSTGRES_DB   │               │
│  │ Dependencies:   │     │ - POSTGRES_USER │               │
│  │ - db container  │     │ - POSTGRES_PASS │               │
│  └─────────────────┘     └─────────────────┘               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │   HOST FILESYSTEM   │
              │                     │
              │ ./media/           │◄──── Image uploads
              │ ./static/          │◄──── Static files
              │ ./logs/            │◄──── Application logs
              └─────────────────────┘
```

### 1.2 Arquitectura de Producción (Standalone)
```
┌─────────────────────────────────────────────────────────────┐
│                   PRODUCTION SERVER                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                DJANGO APPLICATION                       ││
│  │                                                         ││
│  │  Django 5.2.2 + Python 3.13                           ││
│  │  ├── carriacces/ (project)                             ││
│  │  ├── trabajadores/ (app)                               ││
│  │  ├── empresa/ (app)                                    ││
│  │  ├── productos/ (app)                                  ││
│  │  ├── proveedores/ (app)                                ││
│  │  ├── static/ (collected)                               ││
│  │  └── media/ (uploads)                                  ││
│  │                                                         ││
│  │  Port: 8000 (runserver)                                ││
│  │  No gunicorn/nginx required                            ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              POSTGRESQL DATABASE                        ││
│  │                                                         ││
│  │  PostgreSQL 15+                                        ││
│  │  Database: practicatpe2                                ││
│  │  User: practicausr25                                   ││
│  │  Host: localhost                                       ││
│  │  Port: 5432                                            ││
│  │                                                         ││
│  │  Tables:                                               ││
│  │  ├── trabajadores_trabajador                          ││
│  │  ├── empresa_empresa                                  ││
│  │  ├── productos_producto                               ││
│  │  ├── proveedores_proveedor                            ││
│  │  └── django_* (core tables)                           ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 2. Configuración de Base de Datos

### 2.1 Esquema de Base de Datos
```sql
-- Tabla trabajadores_trabajador
CREATE TABLE trabajadores_trabajador (
    id BIGINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(254) UNIQUE NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    codigo_empleado VARCHAR(20) UNIQUE NOT NULL,
    imagen VARCHAR(100)
);

-- Tabla empresa_empresa (singleton)
CREATE TABLE empresa_empresa (
    id BIGINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    nombre VARCHAR(200) NOT NULL,
    direccion TEXT NOT NULL,
    mision TEXT NOT NULL,
    vision TEXT NOT NULL,
    anio_fundacion INTEGER NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    imagen VARCHAR(100),
    CONSTRAINT empresa_anio_fundacion_check 
        CHECK (anio_fundacion >= 1900 AND anio_fundacion <= EXTRACT(YEAR FROM CURRENT_DATE))
);

-- Tabla productos_producto
CREATE TABLE productos_producto (
    id BIGINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    iva INTEGER NOT NULL,
    imagen VARCHAR(100),
    CONSTRAINT productos_precio_check CHECK (precio > 0),
    CONSTRAINT productos_iva_check CHECK (iva IN (0, 15))
);

-- Tabla proveedores_proveedor
CREATE TABLE proveedores_proveedor (
    id BIGINT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    direccion TEXT NOT NULL
);

-- Índices para optimización
CREATE INDEX idx_trabajador_apellido_nombre ON trabajadores_trabajador(apellido, nombre);
CREATE INDEX idx_producto_nombre ON productos_producto(nombre);
CREATE INDEX idx_proveedor_nombre ON proveedores_proveedor(nombre);
CREATE INDEX idx_proveedor_pais ON proveedores_proveedor(pais);
```

### 2.2 Configuración de Conexión
```python
# settings/database.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'practicatpe2',
        'USER': 'practicausr25',
        'PASSWORD': 'practic35',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60,  # Connection pooling
        'ATOMIC_REQUESTS': True,  # Transacciones automáticas
    }
}

# Para desarrollo con Docker
if os.environ.get('DOCKER_ENVIRONMENT'):
    DATABASES['default']['HOST'] = 'db'  # Servicio Docker
```

## 3. Gestión de Archivos Estáticos y Media

### 3.1 Configuración de Archivos Estáticos
```python
# settings/static.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para collectstatic

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de archivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuración de storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

### 3.2 Estructura de Archivos
```
static/                          # Archivos estáticos de desarrollo
├── css/
│   ├── bootstrap.min.css       # Bootstrap 5.3
│   ├── bootstrap-icons.css     # Iconos Bootstrap
│   └── carriacces.css          # Estilos personalizados
├── js/
│   ├── bootstrap.bundle.min.js # Bootstrap JS + Popper
│   └── carriacces.js           # JavaScript personalizado
├── images/
│   ├── logo-carriacces.png     # Logo principal
│   ├── carousel/
│   │   ├── empresa-01.jpg      # Imágenes descripción empresa
│   │   ├── empresa-02.jpg
│   │   ├── empresa-03.jpg
│   │   ├── empresa-04.jpg
│   │   ├── historia-01.jpg     # Imágenes historia empresa
│   │   ├── historia-02.jpg
│   │   ├── historia-03.jpg
│   │   └── historia-04.jpg
│   └── placeholders/
│       ├── trabajador-placeholder.svg
│       ├── producto-placeholder.svg
│       └── empresa-placeholder.svg

media/                           # Archivos subidos por usuarios
├── trabajadores/
│   ├── juan_perez_abc123.jpg   # Fotos empleados
│   └── maria_lopez_def456.jpg
├── empresa/
│   └── logo_empresa_xyz789.png # Logo empresa
└── productos/
    ├── aceite_motor_ghi012.jpg # Imágenes productos
    └── filtro_aire_jkl345.jpg

staticfiles/                     # Archivos estáticos recolectados (producción)
├── admin/                      # Admin de Django
├── css/                        # CSS recolectados
├── js/                         # JavaScript recolectados
└── images/                     # Imágenes recolectadas
```

## 4. Configuración de Logging y Monitoreo

### 4.1 Sistema de Logging
```python
# settings/logging.py
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'carriacces.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        }
    },
    'root': {
        'handlers': ['console', 'file'],
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
        },
        'carriacces': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Crear directorio de logs si no existe
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
```

### 4.2 Health Check Endpoint
```python
# carriacces/health.py
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import os

def health_check(request):
    """Endpoint para verificar salud del sistema"""
    status = {
        'status': 'healthy',
        'checks': {
            'database': 'unknown',
            'media_directory': 'unknown',
            'static_directory': 'unknown',
        },
        'version': getattr(settings, 'VERSION', '1.0.0'),
        'environment': getattr(settings, 'ENVIRONMENT', 'production'),
    }
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['checks']['database'] = 'healthy'
    except Exception as e:
        status['checks']['database'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check media directory
    try:
        media_root = settings.MEDIA_ROOT
        if os.path.exists(media_root) and os.access(media_root, os.W_OK):
            status['checks']['media_directory'] = 'healthy'
        else:
            status['checks']['media_directory'] = 'error: not accessible'
            status['status'] = 'unhealthy'
    except Exception as e:
        status['checks']['media_directory'] = f'error: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check static directory
    try:
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root and os.path.exists(static_root):
            status['checks']['static_directory'] = 'healthy'
        else:
            status['checks']['static_directory'] = 'warning: not collected'
    except Exception as e:
        status['checks']['static_directory'] = f'error: {str(e)}'
    
    return JsonResponse(status)
```

## 5. Configuración de Seguridad

### 5.1 Settings de Seguridad
```python
# settings/security.py

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-this-in-production-xyz123abc456def789'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',  # Para Docker
    # Agregar dominios de producción aquí
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (para producción)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# File upload security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Allowed file types for uploads
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
```

### 5.2 Validación de Archivos
```python
# utils/validators.py
from django.core.exceptions import ValidationError
from django.conf import settings
import os

def validate_image_file(image):
    """Validador para archivos de imagen"""
    if not image:
        return  # Archivo opcional
    
    # Validar tamaño
    if image.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(
            f'El archivo es demasiado grande. Tamaño máximo: {settings.FILE_UPLOAD_MAX_MEMORY_SIZE // (1024*1024)}MB'
        )
    
    # Validar extensión
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f'Tipo de archivo no permitido. Extensiones permitidas: {", ".join(settings.ALLOWED_IMAGE_EXTENSIONS)}'
        )
    
    # Validar tipo MIME
    if hasattr(image, 'content_type') and image.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f'Tipo de contenido no permitido. Tipos permitidos: {", ".join(settings.ALLOWED_IMAGE_TYPES)}'
        )
```

## 6. Configuración de Performance

### 6.1 Cache Configuration
```python
# settings/cache.py

# Para desarrollo (dummy cache)
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    # Para producción (local-memory cache)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'carriacces-cache',
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
                'CULL_FREQUENCY': 3,
            }
        }
    }

# Cache timeout settings
CACHE_TTL = 60 * 15  # 15 minutos

# Template caching
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
```

### 6.2 Database Optimization
```python
# settings/database_optimization.py

# Optimizaciones de base de datos
DATABASES['default'].update({
    'CONN_MAX_AGE': 60,  # Reutilizar conexiones por 60 segundos
    'OPTIONS': {
        'MAX_CONNS': 20,
        'AUTOCOMMIT': True,
    }
})

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Paginación por defecto
PAGINATE_BY = 12

# Configuración de querysets
FIXTURE_DIRS = [
    BASE_DIR / 'fixtures',
]
```

## 7. Deployment Configuration

### 7.1 Environment Variables
```bash
# .env.example (para producción)
DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://practicausr25:practic35@localhost:5432/practicatpe2
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
MEDIA_ROOT=/var/www/carriacces/media
STATIC_ROOT=/var/www/carriacces/static
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ADMINS=admin@yourdomain.com
```

### 7.2 Production Checklist
```python
# management/commands/production_checklist.py
from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verificar configuración para producción'
    
    def handle(self, *args, **options):
        checks = []
        
        # Security checks
        if settings.DEBUG:
            checks.append('❌ DEBUG está activado')
        else:
            checks.append('✅ DEBUG desactivado')
            
        if 'django-insecure' in settings.SECRET_KEY:
            checks.append('❌ SECRET_KEY insegura')
        else:
            checks.append('✅ SECRET_KEY configurada')
            
        # Database checks
        if settings.DATABASES['default']['HOST'] == 'localhost':
            checks.append('✅ Base de datos local configurada')
        
        # Media/Static checks
        if os.path.exists(settings.MEDIA_ROOT):
            checks.append('✅ Directorio MEDIA_ROOT existe')
        else:
            checks.append('❌ Directorio MEDIA_ROOT no existe')
            
        # Permissions checks
        if os.access(settings.MEDIA_ROOT, os.W_OK):
            checks.append('✅ MEDIA_ROOT es escribible')
        else:
            checks.append('❌ MEDIA_ROOT no es escribible')
            
        # Output results
        self.stdout.write('\n=== PRODUCTION CHECKLIST ===\n')
        for check in checks:
            self.stdout.write(check)
        
        errors = [c for c in checks if c.startswith('❌')]
        if errors:
            self.stdout.write(f'\n⚠️  {len(errors)} problemas encontrados')
        else:
            self.stdout.write('\n🎉 Todas las verificaciones pasaron')
```

## 8. Monitoring y Observabilidad

### 8.1 Application Metrics
```python
# utils/metrics.py
import time
import logging
from functools import wraps
from django.db import connection

logger = logging.getLogger('carriacces.metrics')

def track_performance(func_name=None):
    """Decorator para medir performance de funciones"""
    def decorator(func):
        name = func_name or f"{func.__module__}.{func.__name__}"
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            queries_before = len(connection.queries)
            
            try:
                result = func(*args, **kwargs)
                status = 'success'
                return result
            except Exception as e:
                status = 'error'
                logger.error(f"Error in {name}: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                queries_count = len(connection.queries) - queries_before
                
                logger.info(
                    f"Performance: {name} | "
                    f"Duration: {duration:.3f}s | "
                    f"Queries: {queries_count} | "
                    f"Status: {status}"
                )
        
        return wrapper
    return decorator

class PerformanceMiddleware:
    """Middleware para tracking de performance de requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        queries_before = len(connection.queries)
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        queries_count = len(connection.queries) - queries_before
        
        logger.info(
            f"Request: {request.method} {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.3f}s | "
            f"Queries: {queries_count}"
        )
        
        return response
```

Esta arquitectura de infraestructura garantiza:
- ✅ Separación clara entre desarrollo y producción
- ✅ Configuración segura y escalable
- ✅ Monitoreo y logging comprehensivo
- ✅ Performance optimizada
- ✅ Deployment automatizado y verificado
- ✅ Cumplimiento de restricciones técnicas
