# SPARC Architecture Phase - Detailed System Design

## 1. Component Architecture

### A. Django Application Structure
```
carriacces/ (Main Project)
├── settings/
│   ├── __init__.py
│   ├── base.py (common settings)
│   ├── development.py (Docker + debug)
│   └── production.py (optimized)
├── urls.py (main routing)
├── wsgi.py (WSGI application)
├── asgi.py (ASGI application)
└── views.py (home page view)

Apps Structure:
├── trabajadores/ (Workers Management)
│   ├── models.py (Trabajador model)
│   ├── views.py (CBV CRUD views)
│   ├── forms.py (TrabajadorForm)
│   ├── urls.py (RESTful routes)
│   ├── tests/ (test modules)
│   └── templates/trabajadores/
├── empresa/ (Company Management - Singleton)
├── productos/ (Products Management)  
└── proveedores/ (Suppliers Management)
```

### B. Template Component Hierarchy
```
templates/
├── base.html (Master template)
│   ├── {% block head %} (meta, CSS)
│   ├── {% block navigation %} (responsive nav)
│   ├── {% block messages %} (Django messages)
│   ├── {% block content %} (page content)
│   └── {% block scripts %} (JS includes)
├── components/
│   ├── navigation.html (reusable nav)
│   ├── messages.html (alert components)
│   ├── pagination.html (page navigation)
│   └── empty_state.html (no data states)
├── errors/
│   ├── 404.html (not found)
│   └── 500.html (server error)
└── [entity]/
    ├── list.html (grid/cards view)
    ├── form.html (create/update)
    ├── detail.html (individual view)
    └── confirm_delete.html (confirmation)
```

### C. Static Files Architecture
```
static/
├── css/
│   ├── bootstrap.min.css (framework)
│   ├── carriacces.css (custom automotive theme)
│   ├── components.css (reusable components)
│   └── responsive.css (media queries)
├── js/
│   ├── bootstrap.bundle.min.js
│   ├── carriacces.js (custom interactions)
│   └── forms.js (validation enhancements)
├── images/
│   ├── logo/ (company branding)
│   ├── carousel/ (home page images)
│   ├── placeholders/ (default images)
│   └── icons/ (UI iconography)
└── fonts/ (web fonts if needed)

media/ (User Uploads)
├── trabajadores/ (employee photos)
├── empresa/ (company logo)
├── productos/ (product images)
└── uploads/ (temporary storage)
```

## 2. Data Architecture

### A. Database Schema Design
```sql
-- Trabajador Table
CREATE TABLE trabajadores_trabajador (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(254) UNIQUE NOT NULL,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    codigo_empleado VARCHAR(20) UNIQUE NOT NULL,
    imagen VARCHAR(100), -- ImageField path
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_trabajador_apellido_nombre ON trabajadores_trabajador(apellido, nombre);
CREATE INDEX idx_trabajador_correo ON trabajadores_trabajador(correo);
CREATE INDEX idx_trabajador_cedula ON trabajadores_trabajador(cedula);

-- Empresa Table (Singleton pattern)
CREATE TABLE empresa_empresa (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    direccion TEXT NOT NULL,
    mision TEXT NOT NULL,
    vision TEXT NOT NULL,
    anio_fundacion INTEGER NOT NULL CHECK (anio_fundacion >= 1900),
    ruc VARCHAR(13) UNIQUE NOT NULL,
    imagen VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Constraint to ensure only one company
ALTER TABLE empresa_empresa ADD CONSTRAINT single_empresa_check CHECK (id = 1);

-- Producto Table
CREATE TABLE productos_producto (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    iva INTEGER NOT NULL CHECK (iva IN (0, 15)),
    imagen VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_producto_nombre ON productos_producto(nombre);
CREATE INDEX idx_producto_precio ON productos_producto(precio);

-- Proveedor Table
CREATE TABLE proveedores_proveedor (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    direccion TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_proveedor_nombre ON proveedores_proveedor(nombre);
CREATE INDEX idx_proveedor_pais ON proveedores_proveedor(pais);
```

### B. Model Layer Design Patterns
```python
# Base Model with common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Always validate before save
        super().save(*args, **kwargs)

# Custom Manager Pattern
class EmpresaManager(models.Manager):
    def get_empresa(self):
        return self.first()
    
    def create_empresa(self, **kwargs):
        if self.exists():
            raise ValidationError("Solo puede existir una empresa.")
        return self.create(**kwargs)

# Validation Mixins
class ImageValidationMixin:
    def clean_imagen(self):
        if self.imagen:
            validate_image_file(self.imagen)
        return self.imagen

class UniqueFieldsMixin:
    def validate_unique_fields(self, exclude=None):
        # Custom uniqueness validation
        pass
```

### C. QuerySet Optimization Strategy
```python
# Optimized QuerySets for common operations
class TrabajadorQuerySet(models.QuerySet):
    def with_images(self):
        return self.exclude(imagen__isnull=True).exclude(imagen__exact='')
    
    def search(self, query):
        return self.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) |
            Q(correo__icontains=query)
        )
    
    def ordered_by_name(self):
        return self.order_by('apellido', 'nombre')

class ProductoQuerySet(models.QuerySet):
    def con_iva(self):
        return self.filter(iva__gt=0)
    
    def sin_iva(self):
        return self.filter(iva=0)
    
    def por_rango_precio(self, min_precio, max_precio):
        return self.filter(precio__gte=min_precio, precio__lte=max_precio)
```

## 3. Infrastructure Architecture

### A. Development Environment (Docker)
```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DOCKER_ENVIRONMENT=true
    volumes:
      - .:/app
      - media_files:/app/media
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: practicatpe2
      POSTGRES_USER: practicausr25
      POSTGRES_PASSWORD: practic35
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  media_files:
```

### B. Production Deployment Architecture
```python
# settings/production.py
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database optimizations
DATABASES['default'].update({
    'CONN_MAX_AGE': 600,
    'OPTIONS': {
        'MAX_CONNS': 20,
        'MIN_CONNS': 5,
    }
})

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Performance
USE_TZ = True
USE_I18N = True
USE_L10N = True
```

### C. Security Architecture
```python
# Security Configuration
SECURITY_SETTINGS = {
    'ALLOWED_IMAGE_EXTENSIONS': ['.jpg', '.jpeg', '.png', '.webp'],
    'ALLOWED_IMAGE_TYPES': ['image/jpeg', 'image/png', 'image/webp'],
    'MAX_FILE_SIZE': 5 * 1024 * 1024,  # 5MB
    'UPLOAD_PATH_SANITIZATION': True,
    'FILE_VALIDATION_REQUIRED': True,
}

# CSRF Protection
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True

# Session Security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hour

# Content Security Policy
CSP_DEFAULT_SRC = ["'self'"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"]
CSP_SCRIPT_SRC = ["'self'", "cdn.jsdelivr.net"]
CSP_IMG_SRC = ["'self'", "data:", "blob:"]
```

## 4. API Design (Internal)

### A. View Layer Architecture
```python
# Base View Classes
class BaseListView(ListView):
    paginate_by = 12
    context_object_name = 'objects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['total_count'] = self.get_queryset().count()
        return context
    
    def get_title(self):
        return f"Lista de {self.model._meta.verbose_name_plural}"

class BaseCreateUpdateView:
    def form_valid(self, form):
        response = super().form_valid(form)
        action = "creado" if not self.object.pk else "actualizado"
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name} {action} exitosamente.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrija los errores en el formulario.'
        )
        return super().form_invalid(form)
```

### B. URL Design Patterns
```python
# RESTful URL patterns
app_name = 'trabajadores'
urlpatterns = [
    path('', TrabajadorListView.as_view(), name='list'),           # GET /trabajadores/
    path('crear/', TrabajadorCreateView.as_view(), name='create'), # GET/POST /trabajadores/crear/
    path('<int:pk>/', TrabajadorDetailView.as_view(), name='detail'), # GET /trabajadores/1/
    path('<int:pk>/editar/', TrabajadorUpdateView.as_view(), name='update'), # GET/POST /trabajadores/1/editar/
    path('<int:pk>/eliminar/', TrabajadorDeleteView.as_view(), name='delete'), # GET/POST /trabajadores/1/eliminar/
]
```

### C. Form Architecture
```python
# Advanced Form Design
class BaseCRUDForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()
        self.add_required_asterisks()
    
    def add_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    def add_required_asterisks(self):
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label} *"

class ImageValidationForm(BaseCRUDForm):
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            return validate_uploaded_image(imagen)
        return imagen
```

## 5. Testing Architecture

### A. Test Structure Organization
```
tests/
├── unit/
│   ├── test_models.py (model validation)
│   ├── test_forms.py (form validation)
│   ├── test_managers.py (custom managers)
│   └── test_utils.py (utility functions)
├── integration/
│   ├── test_views.py (view + form + model)
│   ├── test_crud_flows.py (complete CRUD)
│   └── test_file_uploads.py (media handling)
├── functional/
│   ├── test_navigation.py (page navigation)
│   ├── test_user_flows.py (end-to-end)
│   └── test_responsive.py (UI responsiveness)
└── fixtures/
    ├── test_data.json (sample data)
    └── test_images/ (sample images)
```

### B. Test Configuration
```python
# settings/test.py
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = tempfile.mkdtemp()
STATIC_ROOT = tempfile.mkdtemp()

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
```

This detailed architecture provides a robust foundation for implementing the CarriAcces application with proper separation of concerns, security, and maintainability.