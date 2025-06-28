# Restricciones Técnicas - CarriAcces

## 1. Stack Tecnológico Obligatorio

### 1.1 Backend Requerido
- **Python:** 3.13 (versión exacta)
- **Django:** 5.2.2 (versión exacta)
- **PostgreSQL:** 15+ (mínimo requerido)
- **psycopg2-binary:** Para conexión PostgreSQL
- **Pillow:** Para manejo de ImageField
- **UV:** Gestor de paquetes obligatorio (no pip directamente)

### 1.2 Frontend Requerido
- **HTML5:** Semántico y accesible
- **CSS/Bootstrap:** Framework CSS obligatorio
- **JavaScript:** Opcional y mínimo
- **No frameworks JS:** React, Vue, Angular prohibidos
- **No CSS preprocessors:** Sass, Less no requeridos

### 1.3 Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'practicatpe2',
        'USER': 'practicausr25',
        'PASSWORD': 'practic35',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 2. Restricciones de Implementación

### 2.1 Prohibiciones Explícitas
- **NO nginx:** Servidores web externos prohibidos
- **NO Docker en producción:** Solo para desarrollo
- **NO microservicios:** Aplicación monolítica requerida
- **NO autenticación:** Sistema completamente público
- **NO usuarios/roles:** Sin sistema de permisos
- **NO login/registro:** Acceso abierto total
- **NO APIs externas:** Solo interfaz web
- **NO CDN:** Archivos servidos localmente

### 2.2 Sistema de Usuarios
- **Acceso público:** Sin restricciones de ningún tipo
- **Sin autenticación:** No login, logout, registro
- **Sin roles:** No administradores, usuarios, etc.
- **Sin permisos:** Todas las operaciones CRUD públicas
- **Sin sesiones:** No manejo de estado de usuario

### 2.3 Seguridad Simplificada
- **No autenticación:** Pero sí validación de datos
- **No autorización:** Pero sí sanitización de inputs
- **No control de acceso:** Pero sí protección CSRF
- **No audit trail:** Sin logs de usuario
- **No rate limiting:** Sin limitaciones de uso

## 3. Arquitectura Obligatoria

### 3.1 Patrón MVC Django
```
carriacces/           # Proyecto principal
├── settings.py       # Configuración central
├── urls.py          # URLs principales
├── wsgi.py          # WSGI application
└── asgi.py          # ASGI application

trabajadores/         # App trabajadores
├── models.py        # Modelo Trabajador
├── views.py         # Vistas CRUD
├── urls.py          # URLs específicas
├── forms.py         # ModelForms
└── templates/       # Templates HTML

empresa/             # App empresa
productos/           # App productos
proveedores/         # App proveedores
```

### 3.2 Aplicaciones Django Requeridas
1. **trabajadores:** CRUD empleados
2. **empresa:** CRUD información empresa (única instancia)
3. **productos:** CRUD accesorios automotrices
4. **proveedores:** CRUD proveedores

### 3.3 Templates y Estáticos
```
templates/
├── base.html        # Template base
├── home.html        # Página principal estática
├── trabajadores/    # Templates trabajadores
├── empresa/         # Templates empresa
├── productos/       # Templates productos
└── proveedores/     # Templates proveedores

static/
├── css/            # Estilos CSS
├── js/             # JavaScript mínimo
└── images/         # Imágenes estáticas

media/              # Archivos subidos
├── trabajadores/   # Fotos empleados
├── empresa/        # Logo empresa
└── productos/      # Imágenes productos
```

## 4. Modelos de Datos Estrictos

### 4.1 Campos Exactos por Modelo
```python
# Trabajador - Campos exactos del PRD
- nombre (CharField)
- apellido (CharField)  
- correo (EmailField)
- cedula (CharField)
- codigo_empleado (CharField)
- imagen (ImageField)

# Empresa - Campos exactos del PRD
- nombre (CharField)
- direccion (TextField)
- mision (TextField)
- vision (TextField)
- anio_fundacion (IntegerField)
- ruc (CharField)
- imagen (ImageField)

# Producto - Campos exactos del PRD
- nombre (CharField)
- descripcion (TextField)
- precio (DecimalField)
- iva (IntegerField, choices=[0, 15])
- imagen (ImageField)

# Proveedor - Campos exactos del PRD
- nombre (CharField)
- descripcion (TextField)
- telefono (CharField)
- pais (CharField)
- correo (EmailField)
- direccion (TextField)
```

### 4.2 Sin Campos Adicionales
- **No timestamps:** created_at, updated_at
- **No soft delete:** is_active, deleted_at
- **No audit fields:** created_by, modified_by
- **No versioning:** version, revision
- **No SEO fields:** slug, meta_description

## 5. Entorno de Desarrollo

### 5.1 Docker Obligatorio
```bash
# Desarrollo - Docker requerido
docker-compose up --build -d
docker-compose exec web python manage.py migrate

# Comandos a través de Docker
docker-compose exec web python manage.py test
```

## 6. Configuración Específica

### 6.1 Settings.py Requerido
```python
# Idioma español obligatorio
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'America/Guayaquil'  # O zona horaria apropiada

# Media files configuración
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Apps requeridas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trabajadores',
    'empresa', 
    'productos',
    'proveedores',
]
```

### 6.2 URLs Estructura Obligatoria
```python
# URLs principales
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('nosotros/', include('empresa.urls')),
    path('trabajadores/', include('trabajadores.urls')),
    path('productos/', include('productos.urls')),
    path('proveedores/', include('proveedores.urls')),
]
```

## 7. Interfaz de Usuario

### 7.1 Navegación Exacta
```html
<!-- Menú requerido exacto -->
HOME | NOSOTROS | CLIENTES | PRODUCTOS | TRABAJADORES | PROVEEDORES | SUCURSALES

<!-- Enlaces funcionales -->
HOME → /
NOSOTROS → /nosotros/
PRODUCTOS → /productos/
TRABAJADORES → /trabajadores/
PROVEEDORES → /proveedores/

<!-- Enlaces no funcionales (solo visuales) -->
CLIENTES → #
SUCURSALES → #
```

### 7.2 Layout Específicos
- **Trabajadores:** Tarjetas horizontales, 2 columnas
- **Productos:** Tarjetas verticales, 3 columnas  
- **Proveedores:** Tarjetas verticales, 3 columnas
- **Empresa:** 2 columnas condicionales
- **Home:** Carruseles + texto estático

### 7.3 Idioma Obligatorio
- **Interfaz:** Todo en español
- **Mensajes:** En español
- **Validaciones:** En español
- **Botones/Labels:** En español
- **Estados vacíos:** En español

## 8. Testing y Calidad

### 8.1 Herramientas Obligatorias
```bash
# Testing - Cobertura mínima 85%
coverage run --source='.' manage.py test
coverage report
```

### 8.2 Validaciones Requeridas
- **Migraciones:** Sin conflictos
- **Tests:** Passing al 100%
- **Linting:** Zero errores
- **Formato:** Aplicado consistentemente
- **Funcionalidad:** CRUD completo funcional

## 9. Limitaciones de Producción

### 9.1 Entorno Final
- **Sin Docker:** Despliegue Django estándar
- **PostgreSQL local:** Base de datos en servidor
- **Archivos locales:** Sin almacenamiento en nube
- **Django standalone:** Sin nginx, gunicorn, etc.
- **Configuración simple:** Settings básicos

### 9.2 Sin Características Avanzadas
- **No caching:** Redis, Memcached
- **No queues:** Celery, RQ
- **No search:** Elasticsearch, Solr  
- **No monitoring:** Sentry, New Relic
- **No analytics:** Google Analytics, etc.

## 10. Criterios de Aceptación

### 10.1 Funcionalidad Mínima
- ✅ CRUD completo para 4 entidades
- ✅ Navegación funcional
- ✅ Formularios validados
- ✅ Carga de imágenes
- ✅ Estados vacíos implementados
- ✅ Página principal estática

### 10.2 Calidad Técnica
- ✅ Ruff linting sin errores
- ✅ Cobertura de tests 85%+
- ✅ Migraciones aplicadas correctamente
- ✅ Responsive design Bootstrap
- ✅ Validaciones funcionando
- ✅ Manejo de errores apropiado

### 10.3 Requisitos Específicos
- ✅ Solo 4 aplicaciones Django
- ✅ Campos exactos según PRD
- ✅ Navegación según diseño
- ✅ Interfaz completamente en español
- ✅ Sistema público sin autenticación
- ✅ Docker solo para desarrollo
