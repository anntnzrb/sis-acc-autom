# Estructura del Proyecto

## Directorios Principales
```
sis-acc-autom/
├── carriacces/          # Configuración principal Django
│   ├── settings.py      # Configuración del proyecto
│   ├── urls.py         # URLs principales
│   ├── views.py        # Vista home y handlers de error
│   └── utils.py        # Utilidades (validación imágenes)
├── empresa/            # App gestión empresa
├── trabajadores/       # App gestión trabajadores
├── productos/          # App gestión productos
├── proveedores/        # App gestión proveedores
├── templates/          # Templates Django
├── static/             # Archivos estáticos
├── media/              # Archivos subidos
└── docs/               # Documentación del proyecto
```

## Estructura de cada App Django
```
<app>/
├── __init__.py
├── admin.py           # Configuración admin Django
├── apps.py            # Configuración de la app
├── forms.py           # ModelForms
├── models.py          # Modelos de datos
├── tests.py           # Tests básicos (vacío)
├── test_<app>.py      # Tests completos
├── urls.py            # URLs específicas de la app
├── views.py           # Class-Based Views
└── migrations/        # Migraciones de BD
```

## Templates
```
templates/
├── base.html              # Template base
├── home.html             # Página principal
├── components/           # Componentes reutilizables
│   ├── pagination.html
│   ├── page_header.html
│   ├── form_field.html
│   ├── empty_state.html
│   └── *_card.html      # Tarjetas para cada entidad
├── errors/              # Páginas de error
│   ├── 404.html
│   └── 500.html
└── <app>/               # Templates específicos por app
    ├── form.html        # Formulario crear/editar
    ├── list.html        # Lista de elementos
    └── confirm_delete.html # Confirmación eliminar
```

## Archivos Estáticos
```
static/
├── css/
│   └── carriacces.css   # Estilos principales
├── js/                  # JavaScript (si existe)
├── images/
│   ├── placeholders/    # Imágenes placeholder
│   └── carousel/        # Imágenes del carrusel
```

## Configuración Docker
- `Dockerfile` - Imagen Python 3.13
- `docker-compose.yml` - PostgreSQL + Django
- `.dockerignore` - Archivos a ignorar
- `requirements.txt` - Dependencias Python