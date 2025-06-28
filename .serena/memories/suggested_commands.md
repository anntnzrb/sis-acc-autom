# Comandos Sugeridos para Desarrollo

## Comandos de Desarrollo (Docker)
- **Iniciar servicios**: `docker-compose up -d`
- **Ver logs**: `docker-compose logs -f web`
- **Acceder al contenedor web**: `docker-compose exec web bash`
- **Ejecutar comando Django**: `docker-compose exec web python manage.py <comando>`

## Comandos Django (dentro del contenedor)
- **Migraciones**: `python manage.py makemigrations && python manage.py migrate`
- **Servidor de desarrollo**: `python manage.py runserver 0.0.0.0:8000`
- **Crear superusuario**: `python manage.py createsuperuser`
- **Collectstatic**: `python manage.py collectstatic --noinput`
- **Shell interactivo**: `python manage.py shell`

## Testing
- **Ejecutar todos los tests**: `python manage.py test`
- **Test específico**: `python manage.py test <app>.<test_file>.<TestClass>.<test_method>`
- **Test con coverage**: `coverage run manage.py test && coverage report`

## Linting y Formateo (fuera de Docker)
- **Linter**: `uvx ruff check`
- **Formatter**: `uvx ruff format`
- **Ambos**: `uvx ruff check --fix && uvx ruff format`

## Base de Datos
- **Acceso a PostgreSQL**: `docker-compose exec db psql -U practicausr25 -d practicatpe2`
- **Backup**: `docker-compose exec db pg_dump -U practicausr25 practicatpe2 > backup.sql`
- **Restore**: `docker-compose exec -T db psql -U practicausr25 -d practicatpe2 < backup.sql`

## Gestión de Archivos
- **Logs del contenedor**: `docker-compose logs web`
- **Reiniciar servicios**: `docker-compose restart`
- **Limpiar contenedores**: `docker-compose down && docker-compose up -d`

## Sistema (macOS)
- **Listar archivos**: `ls -la`
- **Buscar archivos**: `find . -name "*.py" -type f`
- **Buscar en contenido**: `grep -r "pattern" .`
- **Editar archivos**: `nano <archivo>` o `vim <archivo>`