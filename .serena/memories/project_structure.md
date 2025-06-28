# Estructura del Proyecto

## Estado Actual:
El proyecto está en fase inicial - solo contiene configuración de Docker y documentación. **NO** hay código Django implementado aún.

## Estructura Requerida (según PRD):
```
sis-acc-autom/
├── carriacces/                    # Proyecto principal Django
│   ├── __init__.py
│   ├── settings.py               # Configuración de Django
│   ├── urls.py                   # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── trabajadores/                 # Aplicación Trabajadores
│   ├── models.py                # Modelo Trabajador
│   ├── views.py                 # Vistas CRUD
│   ├── urls.py                  # URLs específicas
│   ├── forms.py                 # ModelForms
│   └── templates/trabajadores/   # Templates
├── empresa/                      # Aplicación Empresa
│   ├── models.py                # Modelo Empresa
│   ├── views.py                 # Vistas CRUD
│   ├── urls.py                  # URLs específicas
│   ├── forms.py                 # ModelForms
│   └── templates/empresa/        # Templates
├── productos/                    # Aplicación Productos
│   ├── models.py                # Modelo Producto
│   ├── views.py                 # Vistas CRUD
│   ├── urls.py                  # URLs específicas
│   ├── forms.py                 # ModelForms
│   └── templates/productos/      # Templates
├── proveedores/                  # Aplicación Proveedores
│   ├── models.py                # Modelo Proveedor
│   ├── views.py                 # Vistas CRUD
│   ├── urls.py                  # URLs específicas
│   ├── forms.py                 # ModelForms
│   └── templates/proveedores/    # Templates
├── templates/                    # Templates base
│   ├── base.html               # Template base con navegación
│   └── home.html               # Página principal estática
├── static/                       # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── media/                        # Archivos subidos (imágenes)
└── manage.py                     # Script de gestión Django
```

## Aplicaciones Django a Crear:
1. **trabajadores**: CRUD para empleados
2. **empresa**: CRUD para información de empresa (una sola instancia)
3. **productos**: CRUD para accesorios de automóviles
4. **proveedores**: CRUD para proveedores

## Modelos de Datos:
- **Trabajador**: nombre, apellido, correo, cedula, codigo_empleado, imagen
- **Empresa**: nombre, direccion, mision, vision, anio_fundacion, ruc, imagen
- **Producto**: nombre, descripcion, precio, iva (15 ó 0), imagen
- **Proveedor**: nombre, descripcion, telefono, pais, correo, direccion

## Estado de Implementación:
🔴 **PENDIENTE**: Todo el código Django está por implementar
- Proyecto Django principal
- Cuatro aplicaciones Django
- Modelos de datos
- Vistas CRUD
- Templates HTML
- Configuración de URLs
- Archivos estáticos