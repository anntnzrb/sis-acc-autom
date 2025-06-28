# Comandos Sugeridos

## Comandos de Desarrollo (usando UV):
```bash
# Instalar dependencias
uv add django==5.2.2
uv add psycopg2-binary
uv add Pillow

# Ejecutar comandos Django
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py runserver
uv run python manage.py createsuperuser
uv run python manage.py collectstatic

# Linting y formateo
uvx ruff check
uvx ruff format

# Testing con coverage
uv run coverage run --source='.' manage.py test
uv run coverage report
uv run coverage html
```

## Comandos de Docker (Desarrollo):
```bash
# Construir y ejecutar contenedores
docker-compose up --build -d

# Ejecutar migraciones en contenedor
docker-compose exec web python manage.py migrate

# Acceder al contenedor web
docker-compose exec web bash

# Ver logs
docker-compose logs web
docker-compose logs db

# Detener contenedores
docker-compose down

# Ver aplicación
http://localhost:8000
```

## Comandos del Sistema (macOS):
```bash
# Git
git status
git add .
git commit -m "mensaje"
git push

# Navegación de archivos
ls -la
cd directorio
find . -name "*.py"
grep -r "patrón" .

# Proceso de desarrollo
ps aux | grep python
kill -9 PID
```

## Comandos de Base de Datos:
```bash
# Conectar a PostgreSQL (dentro del contenedor)
docker-compose exec db psql -U practicausr25 -d practicatpe2

# Backup de base de datos
docker-compose exec db pg_dump -U practicausr25 practicatpe2 > backup.sql

# Restaurar base de datos
docker-compose exec -i db psql -U practicausr25 -d practicatpe2 < backup.sql
```