# CarriAcces - Sistema de Gestión de Autopartes

## Propósito del Proyecto
Sistema web de gestión para una empresa de autopartes llamada CarriAcces. Permite administrar información de la empresa, trabajadores, productos y proveedores.

## Tecnologías Principales
- **Django 5.2+** con Python 3.13
- **PostgreSQL 15** como base de datos
- **Docker & Docker Compose** para desarrollo
- **Bootstrap/CSS personalizado** para frontend
- **Django ModelForms** para formularios
- **Django Class-Based Views** para vistas

## Arquitectura del Sistema
- **Patrón MVC** de Django implementado correctamente
- **4 aplicaciones principales**: empresa, trabajadores, productos, proveedores
- **Aplicación principal**: carriacces (configuración y URLs principales)
- **Templates reutilizables** con sistema de componentes
- **Archivos estáticos** organizados (CSS, JS, imágenes)

## Entidades Principales
1. **Empresa** (singleton) - información de la empresa CarriAcces
2. **Trabajador** - personal de la empresa
3. **Producto** - productos de autopartes
4. **Proveedor** - proveedores de la empresa

## Características Especiales
- Sistema completamente en **español**
- Sin sistema de autenticación (acceso público)
- Operaciones CRUD completas para cada entidad
- Validaciones exhaustivas en modelos y formularios
- Subida de imágenes con validación
- Sistema de paginación para listas
- Estados vacíos informativos
- Diseño responsivo con tarjetas