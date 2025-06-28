@docs/python-guidelines.md

## Idioma del Proyecto
- **Interfaz de usuario**: TODO el contenido visible debe estar en **español**
- **Código**: Puede estar en inglés o español según sea pertinente
- **Producto final**: Completamente en español para el usuario final
## Herramientas de Desarrollo
- **OBLIGATORIO**: Usar Docker como herramienta de desarrollo para evitar contaminar el entorno local
- **NO** instalar o emplear dependencias directamente en el sistema local
- Todos los comandos de desarrollo deben ejecutarse a través de Docker:

  ```bash
  docker-compose exec <container> <cmd>
  ```

  - **Linter**: `uvx ruff check`
  - **Formatter**: `uvx ruff format`

## Restricciones de Implementación
- **NO** implementar componentes adicionales como nginx, servidores web externos, o tecnologías no especificadas
- **NO** implementar sistema de usuarios, roles, permisos o autenticación
- **NO** hay administradores, usuarios finales o diferentes tipos de acceso
- **NO** se requiere login, registro o cualquier forma de autenticación
- **NO** implementar restricciones de acceso de ningún tipo
- La aplicación debe ser completamente abierta y pública
- Todas las operaciones CRUD son públicas y accesibles para cualquier visitante

## Entorno de Desarrollo vs Producción
- **Desarrollo**: Usar Docker y Docker Compose para PostgreSQL y Django en contenedores
- **Proyecto Final**: Configuración estándar de Django con PostgreSQL (sin dependencia de Docker)
- El proyecto entregable debe funcionar sin Docker

## Patrones de Desarrollo
- Implementar correctamente el patrón MVC de Django
- Usar Django ModelForms para cada modelo
- Implementar patrones de URL RESTful para operaciones CRUD
