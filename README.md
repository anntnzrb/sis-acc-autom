# Tienda de Accesorios para Automóviles

Aplicación web Django con CRUD completo.

## Ejecutar con Docker

```bash
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```

## Ejecutar Localmente

### 2. Configurar PostgreSQL

```bash
createdb practicatpe2
createuser practicausr25

psql -d practicatpe2 -c "ALTER USER practicausr25 PASSWORD 'practic35';"
psql -d practicatpe2 -c "GRANT ALL PRIVILEGES ON DATABASE practicatpe2 TO practicausr25;"
psql -d practicatpe2 -c "GRANT ALL ON SCHEMA public TO practicausr25;"
psql -d practicatpe2 -c "ALTER USER practicausr25 CREATEDB;"
```

### 3. Configurar Python

```bash
python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate    # Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

## Ver Aplicación

**URL**: http://localhost:8000

## Limpiar/Desinstalar

### Remover base de datos y usuario

```bash
dropdb practicatpe2
dropuser practicausr25
```
