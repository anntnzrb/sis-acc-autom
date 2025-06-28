# Proceso de Finalización de Tareas

## Herramientas de Desarrollo Obligatorias:
- **OBLIGATORIO**: Usar Docker como herramienta de desarrollo
- **NO** instalar dependencias directamente en el sistema local
- Todos los comandos deben ejecutarse a través de Docker:
  ```bash
  docker-compose exec <container> <cmd>
  ```

## Comandos de Validación al Completar Tareas:
```bash
# Linting (obligatorio)
docker-compose exec web uvx ruff check

# Formateo (obligatorio)
docker-compose exec web uvx ruff format

# Ejecutar migraciones si hay cambios en modelos
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Testing (si hay tests)
docker-compose exec web uv run coverage run --source='.' manage.py test
docker-compose exec web uv run coverage report

# Verificar que la aplicación funcione
docker-compose up -d
# Visitar http://localhost:8000
```

## Git Workflow:
```bash
# Crear branch antes de cualquier cambio
git checkout -b feature/descripcion-tarea

# Commits incrementales en branch
git add .
git commit -m "feat: descripción del cambio"

# Al finalizar, cambiar a main y hacer rebase merge
git checkout main
git rebase feature/descripcion-tarea
# NUNCA hacer merge commits
```

## Validaciones Finales:
1. **Funcionalidad CRUD**: Todas las operaciones deben ser funcionales
2. **Integración de base de datos**: Debe funcionar correctamente
3. **Navegación**: Todas las páginas deben renderizar apropiadamente
4. **Carga de imágenes**: Funcionalidad debe funcionar
5. **Diseño responsivo**: Implementación correcta
6. **Manejo de errores**: Validación apropiada
7. **Sin autenticación**: Sistema completamente público

## Restricciones de Implementación:
- **NO** implementar nginx, servidores web externos, o tecnologías no especificadas
- **NO** implementar sistema de usuarios, roles, permisos o autenticación
- **NO** hay administradores o diferentes tipos de acceso
- La aplicación debe ser completamente abierta y pública