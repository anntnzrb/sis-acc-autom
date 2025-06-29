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
sudo -u postgres psql
```

```sql
CREATE DATABASE practicatpe2;
CREATE USER practicausr25 WITH PASSWORD 'practic35';
GRANT ALL PRIVILEGES ON DATABASE practicatpe2 TO practicausr25;
ALTER USER practicausr25 CREATEDB;
\q
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
