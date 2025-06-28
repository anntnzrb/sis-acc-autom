# Estrategia de Testing - CarriAcces

## 1. Enfoque TDD London School

### 1.1 Filosofía de Testing
- **Outside-In:** Comenzar con tests de integración y derivar hacia unit tests
- **Mocking:** Uso extensivo de mocks para aislar unidades bajo test
- **Behavior-Driven:** Focus en comportamiento del sistema, no implementación
- **Red-Green-Refactor:** Ciclo estricto de desarrollo dirigido por tests

### 1.2 Principios Fundamentales
```python
# Ejemplo del ciclo Red-Green-Refactor
def test_trabajador_creation_with_valid_data():
    """RED: Test falla porque no existe implementación"""
    data = {'nombre': 'Juan', 'apellido': 'Pérez'}
    form = TrabajadorForm(data)
    assert form.is_valid()  # FALLA - form no existe

def test_trabajador_creation_with_valid_data():
    """GREEN: Implementación mínima para pasar test"""
    class TrabajadorForm(forms.Form):
        nombre = forms.CharField()
        apellido = forms.CharField()
    # Test PASA

def test_trabajador_creation_with_valid_data():
    """REFACTOR: Mejorar sin romper funcionalidad"""
    class TrabajadorForm(forms.ModelForm):
        class Meta:
            model = Trabajador
            fields = ['nombre', 'apellido']
    # Test sigue PASANDO, código mejorado
```

## 2. Estructura de Testing

### 2.1 Organización de Tests
```
tests/
├── __init__.py
├── test_models/
│   ├── __init__.py
│   ├── test_trabajador.py
│   ├── test_empresa.py
│   ├── test_producto.py
│   └── test_proveedor.py
├── test_views/
│   ├── __init__.py
│   ├── test_trabajador_views.py
│   ├── test_empresa_views.py
│   ├── test_producto_views.py
│   └── test_proveedor_views.py
├── test_forms/
│   ├── __init__.py
│   ├── test_trabajador_forms.py
│   ├── test_empresa_forms.py
│   ├── test_producto_forms.py
│   └── test_proveedor_forms.py
├── test_integration/
│   ├── __init__.py
│   ├── test_crud_flows.py
│   ├── test_navigation.py
│   └── test_image_upload.py
└── test_utils/
    ├── __init__.py
    ├── factories.py        # Factory Boy para datos de prueba
    ├── mixins.py          # Test mixins reutilizables
    └── helpers.py         # Funciones auxiliares de testing
```

### 2.2 Configuración de Testing
```python
# settings/test.py
from .base import *

# Base de datos en memoria para velocidad
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Desactivar migraciones para velocidad
class DisableMigrations:
    def __contains__(self, item):
        return True
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Media files en directorio temporal
import tempfile
MEDIA_ROOT = tempfile.mkdtemp()

# Desactivar cache para testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Logging silencioso en tests
LOGGING_CONFIG = None
```

## 3. Tipos de Tests

### 3.1 Unit Tests (Modelos)

#### Test Trabajador Model
```python
class TrabajadorModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan@example.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_string_representation(self):
        """Test método __str__ del modelo"""
        trabajador = Trabajador(**self.valid_data)
        expected = 'Juan Pérez'
        self.assertEqual(str(trabajador), expected)
    
    def test_get_absolute_url(self):
        """Test URL absoluta del modelo"""
        trabajador = TrabajadorFactory()
        expected_url = f'/trabajadores/{trabajador.pk}/'
        self.assertEqual(trabajador.get_absolute_url(), expected_url)
    
    def test_unique_email_constraint(self):
        """Test restricción de unicidad en correo"""
        TrabajadorFactory(correo='test@example.com')
        with self.assertRaises(IntegrityError):
            TrabajadorFactory(correo='test@example.com')
    
    def test_unique_cedula_constraint(self):
        """Test restricción de unicidad en cédula"""
        TrabajadorFactory(cedula='1234567890')
        with self.assertRaises(IntegrityError):
            TrabajadorFactory(cedula='1234567890')
    
    def test_image_upload_path(self):
        """Test ruta de carga de imágenes"""
        trabajador = TrabajadorFactory()
        # Mock image file
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        trabajador.imagen = image
        trabajador.save()
        
        expected_path = f'trabajadores/test_image'
        self.assertIn(expected_path, trabajador.imagen.name)
```

#### Test Empresa Model (Singleton)
```python
class EmpresaModelTest(TestCase):
    def test_singleton_pattern(self):
        """Test que solo se puede crear una empresa"""
        EmpresaFactory()
        with self.assertRaises(ValidationError):
            EmpresaFactory()
    
    def test_get_instance_creates_if_not_exists(self):
        """Test que get_instance crea instancia si no existe"""
        self.assertEqual(Empresa.objects.count(), 0)
        empresa = Empresa.get_instance()
        self.assertEqual(Empresa.objects.count(), 1)
        self.assertIsInstance(empresa, Empresa)
    
    def test_get_instance_returns_existing(self):
        """Test que get_instance retorna instancia existente"""
        existing = EmpresaFactory()
        returned = Empresa.get_instance()
        self.assertEqual(existing.pk, returned.pk)
```

### 3.2 Unit Tests (Forms)

#### Test TrabajadorForm
```python
class TrabajadorFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan@example.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_form_with_valid_data(self):
        """Test formulario con datos válidos"""
        form = TrabajadorForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['nombre'], 'Juan')
    
    def test_form_missing_required_fields(self):
        """Test formulario con campos requeridos faltantes"""
        invalid_data = {'nombre': 'Juan'}  # Faltan otros campos
        form = TrabajadorForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellido', form.errors)
        self.assertIn('correo', form.errors)
    
    def test_email_validation(self):
        """Test validación de formato de correo"""
        invalid_data = self.valid_data.copy()
        invalid_data['correo'] = 'correo_invalido'
        form = TrabajadorForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('correo', form.errors)
    
    def test_duplicate_email_validation(self):
        """Test validación de correo duplicado"""
        TrabajadorFactory(correo='existing@example.com')
        invalid_data = self.valid_data.copy()
        invalid_data['correo'] = 'existing@example.com'
        form = TrabajadorForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este correo ya está registrado', str(form.errors))
    
    def test_image_file_validation(self):
        """Test validación de archivo de imagen"""
        # Test archivo válido
        valid_image = SimpleUploadedFile(
            "test.jpg",
            b"image_content",
            content_type="image/jpeg"
        )
        form = TrabajadorForm(
            data=self.valid_data,
            files={'imagen': valid_image}
        )
        self.assertTrue(form.is_valid())
        
        # Test archivo inválido
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"text_content",
            content_type="text/plain"
        )
        form = TrabajadorForm(
            data=self.valid_data,
            files={'imagen': invalid_file}
        )
        self.assertFalse(form.is_valid())
```

### 3.3 Integration Tests (Views)

#### Test CRUD Flow Completo
```python
class TrabajadorCRUDIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.trabajador_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan@example.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_create_read_update_delete_flow(self):
        """Test flujo CRUD completo"""
        # CREATE - Crear trabajador
        response = self.client.post(
            reverse('trabajadores:create'),
            data=self.trabajador_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect después de crear
        
        trabajador = Trabajador.objects.get(correo='juan@example.com')
        self.assertEqual(trabajador.nombre, 'Juan')
        
        # READ - Leer trabajador en lista
        response = self.client.get(reverse('trabajadores:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        
        # UPDATE - Actualizar trabajador
        updated_data = self.trabajador_data.copy()
        updated_data['nombre'] = 'Juan Carlos'
        response = self.client.post(
            reverse('trabajadores:update', kwargs={'pk': trabajador.pk}),
            data=updated_data
        )
        self.assertEqual(response.status_code, 302)
        
        trabajador.refresh_from_db()
        self.assertEqual(trabajador.nombre, 'Juan Carlos')
        
        # DELETE - Eliminar trabajador
        response = self.client.post(
            reverse('trabajadores:delete', kwargs={'pk': trabajador.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Trabajador.objects.filter(pk=trabajador.pk).exists())
    
    def test_list_view_empty_state(self):
        """Test estado vacío en lista"""
        response = self.client.get(reverse('trabajadores:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No hay trabajadores registrados')
        self.assertContains(response, 'AGREGAR TRABAJADOR')
    
    def test_list_view_with_pagination(self):
        """Test paginación en lista"""
        # Crear 15 trabajadores (más que paginate_by=12)
        TrabajadorFactory.create_batch(15)
        
        response = self.client.get(reverse('trabajadores:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 12)
        self.assertTrue(response.context['is_paginated'])
        
        # Test página 2
        response = self.client.get(reverse('trabajadores:list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
```

### 3.4 UI/Template Tests
```python
class TemplateRenderingTest(TestCase):
    def test_base_template_navigation(self):
        """Test renderizado de navegación en template base"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar elementos de navegación
        nav_items = ['HOME', 'NOSOTROS', 'PRODUCTOS', 'TRABAJADORES', 'PROVEEDORES']
        for item in nav_items:
            self.assertContains(response, item)
    
    def test_responsive_layout_classes(self):
        """Test clases CSS responsivas en templates"""
        response = self.client.get(reverse('trabajadores:list'))
        self.assertContains(response, 'container-fluid')
        self.assertContains(response, 'row')
        self.assertContains(response, 'col-md-6')  # 2 columnas en trabajadores
        
    def test_form_bootstrap_classes(self):
        """Test clases Bootstrap en formularios"""
        response = self.client.get(reverse('trabajadores:create'))
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'btn btn-primary')
        self.assertContains(response, 'was-validated')
```

## 4. Testing Utilities

### 4.1 Factory Boy para Datos de Prueba
```python
# tests/test_utils/factories.py
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from trabajadores.models import Trabajador
from empresa.models import Empresa
from productos.models import Producto
from proveedores.models import Proveedor

class TrabajadorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trabajador
    
    nombre = factory.Faker('first_name', locale='es_ES')
    apellido = factory.Faker('last_name', locale='es_ES')
    correo = factory.Sequence(lambda n: f'trabajador{n}@carriacces.com')
    cedula = factory.Sequence(lambda n: f'{1000000000 + n}')
    codigo_empleado = factory.Sequence(lambda n: f'EMP{n:03d}')
    imagen = factory.LazyAttribute(lambda obj: SimpleUploadedFile(
        f'{obj.nombre}.jpg',
        b"fake_image_content",
        content_type="image/jpeg"
    ))

class EmpresaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Empresa
        django_get_or_create = ('nombre',)  # Singleton pattern
    
    nombre = 'CarriAcces - Tienda de Accesorios'
    direccion = factory.Faker('address', locale='es_ES')
    mision = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    vision = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    anio_fundacion = factory.Faker('pyint', min_value=1990, max_value=2020)
    ruc = factory.Sequence(lambda n: f'2000{n:07d}001')

class ProductoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Producto
    
    nombre = factory.Faker('word', locale='es_ES')
    descripcion = factory.Faker('text', max_nb_chars=300, locale='es_ES')
    precio = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    iva = factory.Iterator([0, 15])

class ProveedorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Proveedor
    
    nombre = factory.Faker('company', locale='es_ES')
    descripcion = factory.Faker('text', max_nb_chars=200, locale='es_ES')
    telefono = factory.Faker('phone_number', locale='es_ES')
    pais = factory.Faker('country', locale='es_ES')
    correo = factory.Faker('company_email', locale='es_ES')
    direccion = factory.Faker('address', locale='es_ES')
```

### 4.2 Test Mixins Reutilizables
```python
# tests/test_utils/mixins.py
class CRUDTestMixin:
    """Mixin para tests CRUD estándar"""
    model = None
    factory = None
    form_class = None
    list_url = None
    create_url = None
    
    def test_list_view(self):
        """Test vista de lista estándar"""
        self.factory.create_batch(3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)
    
    def test_create_view_get(self):
        """Test GET en vista de creación"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], self.form_class)
    
    def test_create_view_post_valid(self):
        """Test POST válido en vista de creación"""
        initial_count = self.model.objects.count()
        response = self.client.post(self.create_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.model.objects.count(), initial_count + 1)

class ImageUploadTestMixin:
    """Mixin para tests de carga de imágenes"""
    def create_test_image(self, name="test.jpg"):
        """Crear imagen de prueba"""
        return SimpleUploadedFile(
            name,
            b"fake_image_content",
            content_type="image/jpeg"
        )
    
    def test_image_upload(self):
        """Test carga de imagen válida"""
        image = self.create_test_image()
        data = self.valid_data.copy()
        response = self.client.post(
            self.create_url,
            data=data,
            files={'imagen': image}
        )
        self.assertEqual(response.status_code, 302)
        obj = self.model.objects.last()
        self.assertTrue(obj.imagen)
```

## 5. Métricas de Cobertura

### 5.1 Objetivos de Cobertura
```python
# .coveragerc
[run]
source = .
omit = 
    */venv/*
    */migrations/*
    */settings/*
    */tests/*
    manage.py
    carriacces/wsgi.py
    carriacces/asgi.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError

# Targets por componente:
# - Models: 95%
# - Views: 90%  
# - Forms: 95%
# - Utils: 100%
# - Global: 85%
```

### 5.2 Comandos de Testing
```bash
# Test completo con cobertura
coverage run --source='.' manage.py test
coverage report --show-missing
coverage html

# Test específico por app
python manage.py test trabajadores
python manage.py test empresa.tests.test_models

# Test con verbose output
python manage.py test --verbosity=2

# Test con failfast (parar en primer fallo)
python manage.py test --failfast

# Test de performance
python manage.py test --debug-mode
```

## 6. Testing Best Practices

### 6.1 Principios de Buenos Tests
- **F.I.R.S.T:** Fast, Independent, Repeatable, Self-Validating, Timely
- **AAA Pattern:** Arrange, Act, Assert
- **Given-When-Then:** Estructura clara de escenarios
- **Single Responsibility:** Un test, una funcionalidad
- **Descriptive Names:** Nombres que explican el escenario

### 6.2 Qué Testear
✅ **Testear:**
- Lógica de negocio
- Validaciones de formularios
- Restricciones de modelos
- Flujos de navegación
- Manejo de errores
- Estados edge case

❌ **No testear:**
- Funcionalidad Django core
- Bibliotecas third-party
- Configuración simple
- Templates HTML estático
- CSS/JavaScript básico

### 6.3 Datos de Prueba
- Usar Factory Boy para consistencia
- Datos realistas en español
- Cubrir casos edge (valores límite)
- Datos inválidos para validaciones
- Archivos de diferentes tamaños/tipos

Esta estrategia garantiza:
- ✅ Cobertura 85%+ en todas las funcionalidades
- ✅ Tests rápidos y confiables
- ✅ Detección temprana de errores
- ✅ Refactoring seguro
- ✅ Documentación viva del sistema
