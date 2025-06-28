# Stack Tecnológico

## Tecnologías Principales:
- **Python**: 3.13
- **Framework**: Django 5.2.2
- **Gestor de Paquetes**: UV (se debe usar `uv` como interfaz, no `python` directamente)
- **Base de Datos**: PostgreSQL
- **Frontend**: HTML, CSS/Bootstrap, JavaScript (opcional)
- **Adaptador de Base de Datos**: psycopg2-binary

## Dependencias del Proyecto:
```
django==5.2.2
psycopg2-binary>=2.9.0
pillow>=10.0.0
gunicorn>=21.0.0
coverage>=7.9.1
```

## Configuración de Base de Datos:
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

## Entorno de Desarrollo:
- **Desarrollo**: Docker y Docker Compose para PostgreSQL y Django
- **Contenedor PostgreSQL**: postgres:15
- **Puerto de aplicación**: 8000
- **Puerto de base de datos**: 5432