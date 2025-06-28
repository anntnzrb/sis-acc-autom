# Arquitectura del Sistema - CarriAcces

## 1. Arquitectura General

### 1.1 Patrón MVC Django
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     MODELS      │    │     VIEWS       │    │   TEMPLATES     │
│   (Data Layer)  │    │  (Controller)   │    │   (View Layer)  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Trabajador    │◄──►│ • CreateView    │◄──►│ • base.html     │
│ • Empresa       │    │ • UpdateView    │    │ • list.html     │
│ • Producto      │    │ • DeleteView    │    │ • form.html     │
│ • Proveedor     │    │ • ListView      │    │ • detail.html   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Django URLs   │    │  Bootstrap CSS  │
│   Database      │    │   Routing       │    │   Components    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 Estructura de Aplicaciones
```
carriacces/                 # Proyecto principal Django
├── __init__.py
├── settings.py            # Configuración central
├── urls.py               # URLs principales + home
├── views.py              # Vista home estática
├── wsgi.py               # WSGI application
└── asgi.py               # ASGI application

trabajadores/              # App gestión empleados
├── models.py             # Modelo Trabajador
├── views.py              # CRUD views
├── urls.py               # URLs /trabajadores/
├── forms.py              # TrabajadorForm
├── admin.py              # Admin interface
├── apps.py               # App config
└── templates/trabajadores/
    ├── list.html         # Lista trabajadores
    ├── form.html         # Crear/editar
    └── confirm_delete.html

empresa/                   # App información empresa
├── models.py             # Modelo Empresa (singleton)
├── views.py              # CRUD + lógica única instancia
├── urls.py               # URLs /nosotros/
├── forms.py              # EmpresaForm
└── templates/empresa/
    ├── nosotros.html     # Vista principal
    ├── form.html         # Crear/editar
    └── empty.html        # Estado sin empresa

productos/                 # App catálogo productos  
├── models.py             # Modelo Producto
├── views.py              # CRUD views
├── urls.py               # URLs /productos/
├── forms.py              # ProductoForm
└── templates/productos/
    ├── list.html         # Grilla productos
    ├── form.html         # Crear/editar
    └── confirm_delete.html

proveedores/               # App gestión proveedores
├── models.py             # Modelo Proveedor
├── views.py              # CRUD views  
├── urls.py               # URLs /proveedores/
├── forms.py              # ProveedorForm
└── templates/proveedores/
    ├── list.html         # Grilla proveedores
    ├── form.html         # Crear/editar
    └── confirm_delete.html

templates/                 # Templates globales
├── base.html             # Template base + navegación
└── home.html             # Página principal estática

static/                    # Archivos estáticos
├── css/
│   ├── bootstrap.min.css # Bootstrap framework
│   └── custom.css        # Estilos personalizados
├── js/
│   ├── bootstrap.min.js  # Bootstrap JS
│   └── custom.js         # JavaScript mínimo
└── images/
    ├── logo.png          # Logo empresa
    ├── carousel/         # Imágenes carrusel
    └── placeholders/     # Placeholders productos

media/                     # Archivos subidos
├── trabajadores/         # Fotos empleados
├── empresa/              # Logo empresa
└── productos/            # Imágenes productos
```

## 2. Componentes del Sistema

### 2.1 Modelos de Datos

#### Trabajador Model
```python
class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    cedula = models.CharField(max_length=20, unique=True)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    imagen = models.ImageField(upload_to='trabajadores/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ['apellido', 'nombre']
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
        
    def get_absolute_url(self):
        return reverse('trabajadores:detail', kwargs={'pk': self.pk})
        
    def full_clean(self):
        # Validaciones personalizadas
        super().full_clean()
```

#### Empresa Model (Singleton)
```python
class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    mision = models.TextField()
    vision = models.TextField()
    anio_fundacion = models.IntegerField()
    ruc = models.CharField(max_length=20, unique=True)
    imagen = models.ImageField(upload_to='empresa/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
        
    def save(self, *args, **kwargs):
        # Singleton pattern - solo una instancia
        if not self.pk and Empresa.objects.exists():
            raise ValidationError("Solo puede existir una empresa")
        super().save(*args, **kwargs)
        
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
```

#### Producto Model  
```python
class Producto(models.Model):
    IVA_CHOICES = [(0, '0%'), (15, '15%')]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.IntegerField(choices=IVA_CHOICES)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
        
    def precio_con_iva(self):
        return self.precio * (1 + self.iva / 100)
        
    def __str__(self):
        return self.nombre
```

#### Proveedor Model
```python
class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)
    correo = models.EmailField()
    direccion = models.TextField()
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
```

### 2.2 Vistas y Controladores

#### Generic CRUD Pattern
```python
# Base CRUD pattern para todas las entidades
class BaseListView(ListView):
    paginate_by = 12
    template_name = '{app}/list.html'
    context_object_name = 'objects'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['create_url'] = self.create_url
        return context

class BaseCreateView(CreateView):
    template_name = '{app}/form.html'
    
    def get_success_url(self):
        messages.success(self.request, f'{self.model._meta.verbose_name} creado exitosamente')
        return reverse_lazy(f'{self.app_name}:list')

class BaseUpdateView(UpdateView):
    template_name = '{app}/form.html'
    
    def get_success_url(self):
        messages.success(self.request, f'{self.model._meta.verbose_name} actualizado exitosamente')
        return reverse_lazy(f'{self.app_name}:list')

class BaseDeleteView(DeleteView):
    template_name = '{app}/confirm_delete.html'
    
    def get_success_url(self):
        messages.success(self.request, f'{self.model._meta.verbose_name} eliminado exitosamente')
        return reverse_lazy(f'{self.app_name}:list')
```

#### Trabajadores Views
```python
class TrabajadorListView(BaseListView):
    model = Trabajador
    title = "NUESTRO PERSONAL"
    create_url = 'trabajadores:create'

class TrabajadorCreateView(BaseCreateView):
    model = Trabajador
    form_class = TrabajadorForm
    app_name = 'trabajadores'

class TrabajadorUpdateView(BaseUpdateView):
    model = Trabajador
    form_class = TrabajadorForm
    app_name = 'trabajadores'

class TrabajadorDeleteView(BaseDeleteView):
    model = Trabajador
    app_name = 'trabajadores'
```

#### Empresa Views (Singleton Logic)
```python
class EmpresaNosotrosView(View):
    def get(self, request):
        try:
            empresa = Empresa.objects.get()
            return render(request, 'empresa/nosotros.html', {'empresa': empresa})
        except Empresa.DoesNotExist:
            return render(request, 'empresa/empty.html')

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    
    def dispatch(self, request, *args, **kwargs):
        if Empresa.objects.exists():
            return redirect('empresa:update', pk=Empresa.objects.first().pk)
        return super().dispatch(request, *args, **kwargs)

class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    
    def get_object(self):
        return Empresa.objects.first()
```

### 2.3 Formularios y Validación

#### Forms Pattern
```python
class BaseTiendaForm(forms.ModelForm):
    class Meta:
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = True

class TrabajadorForm(BaseTiendaForm):
    class Meta(BaseTiendaForm.Meta):
        model = Trabajador
        fields = ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado', 'imagen']
        
    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Trabajador.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este correo ya está registrado')
        return correo
        
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isalnum():
            raise ValidationError('La cédula debe contener solo números y letras')
        return cedula
```

### 2.4 URLs y Enrutamiento

#### Main URLs
```python
# carriacces/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('nosotros/', include('empresa.urls')),
    path('trabajadores/', include('trabajadores.urls')),
    path('productos/', include('productos.urls')),
    path('proveedores/', include('proveedores.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### App URLs Pattern
```python
# trabajadores/urls.py
app_name = 'trabajadores'
urlpatterns = [
    path('', views.TrabajadorListView.as_view(), name='list'),
    path('crear/', views.TrabajadorCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.TrabajadorUpdateView.as_view(), name='update'),
    path('<int:pk>/eliminar/', views.TrabajadorDeleteView.as_view(), name='delete'),
]
```

## 3. Algoritmos y Lógica de Negocio

### 3.1 Algoritmo de Navegación
```python
def get_navigation_context():
    """
    Algoritmo para generar contexto de navegación
    """
    nav_items = [
        {'name': 'HOME', 'url': 'home', 'active': True},
        {'name': 'NOSOTROS', 'url': 'empresa:nosotros', 'active': True},
        {'name': 'CLIENTES', 'url': '#', 'active': False},  # No funcional
        {'name': 'PRODUCTOS', 'url': 'productos:list', 'active': True},
        {'name': 'TRABAJADORES', 'url': 'trabajadores:list', 'active': True},
        {'name': 'PROVEEDORES', 'url': 'proveedores:list', 'active': True},
        {'name': 'SUCURSALES', 'url': '#', 'active': False},  # No funcional
    ]
    return {'nav_items': nav_items}
```

### 3.2 Algoritmo de Estado Vacío
```python
def get_empty_state_context(entity_name, create_url):
    """
    Algoritmo para mostrar estados vacíos consistentes
    """
    messages = {
        'trabajadores': 'No hay trabajadores registrados',
        'productos': 'No hay productos en el catálogo',
        'proveedores': 'No hay proveedores registrados',
        'empresa': 'NO SE HA INGRESADO INFORMACION DE LA EMPRESA!!'
    }
    
    return {
        'empty_message': messages.get(entity_name),
        'create_url': create_url,
        'create_text': f'AGREGAR {entity_name.upper()[:-1]}'  # Singular
    }
```

### 3.3 Algoritmo de Validación de Imágenes
```python
def validate_image(image_file):
    """
    Algoritmo de validación de archivos de imagen
    """
    if not image_file:
        return True  # Opcional
        
    # Validar tamaño (5MB máximo)
    if image_file.size > 5 * 1024 * 1024:
        raise ValidationError('La imagen no puede superar 5MB')
    
    # Validar tipo MIME
    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    if image_file.content_type not in allowed_types:
        raise ValidationError('Solo se permiten imágenes JPG, PNG y WebP')
        
    # Validar extensión
    ext = image_file.name.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
        raise ValidationError('Extensión de archivo no válida')
        
    return True
```

### 3.4 Algoritmo de Precio con IVA
```python
def calculate_price_with_iva(precio_base, iva_percentage):
    """
    Algoritmo para calcular precio final con IVA
    """
    if iva_percentage not in [0, 15]:
        raise ValueError('IVA debe ser 0 o 15')
        
    precio_final = precio_base * (1 + iva_percentage / 100)
    return round(precio_final, 2)

def format_price_display(producto):
    """
    Algoritmo para formatear visualización de precios
    """
    precio_base = producto.precio
    iva = producto.iva
    precio_final = calculate_price_with_iva(precio_base, iva)
    
    return {
        'precio_principal': f'${precio_final:,.2f}',
        'precio_detalle': f'{iva}% IVA incluido' if iva > 0 else 'Sin IVA'
    }
```

## 4. Estrategia de Testing

### 4.1 Estructura de Tests
```
tests/
├── test_models.py         # Tests de modelos y validaciones
├── test_views.py          # Tests de vistas y formularios  
├── test_forms.py          # Tests de validación de formularios
├── test_urls.py           # Tests de enrutamiento
├── test_integration.py    # Tests de flujos completos
└── test_utils.py          # Tests de funciones auxiliares
```

### 4.2 Testing Strategy (TDD London School)
```python
# Test structure pattern
class TrabajadorModelTestCase(TestCase):
    def setUp(self):
        """Configurar datos de prueba"""
        self.trabajador_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez', 
            'correo': 'juan@example.com',
            'cedula': '1234567890',
            'codigo_empleado': 'EMP001'
        }
    
    def test_create_trabajador_valid_data(self):
        """Test creación con datos válidos"""
        trabajador = Trabajador.objects.create(**self.trabajador_data)
        self.assertEqual(trabajador.nombre, 'Juan')
        self.assertTrue(trabajador.correo)
        
    def test_unique_constraints(self):
        """Test restricciones de unicidad"""
        Trabajador.objects.create(**self.trabajador_data)
        with self.assertRaises(IntegrityError):
            Trabajador.objects.create(**self.trabajador_data)
            
    def test_string_representation(self):
        """Test método __str__"""
        trabajador = Trabajador(**self.trabajador_data)
        self.assertEqual(str(trabajador), 'Juan Pérez')
```

### 4.3 Coverage Target: 85%
```bash
# Comando para verificar cobertura
uv run coverage run --source='.' manage.py test
uv run coverage report --show-missing
uv run coverage html

# Target de cobertura por componente:
# - Models: 90%+
# - Views: 85%+  
# - Forms: 90%+
# - Utils: 95%+
# - Templates: N/A (tests de integración)
```

## 5. Flujos de Datos

### 5.1 Flujo CRUD Típico
```
Usuario → Template → Form → View → Model → Database
    ↑                                        ↓
    ← Template ← Context ← View ← Model ← Database
```

### 5.2 Flujo de Carga de Imágenes
```
Upload → Validation → Storage → Database → Display
   ↓        ↓          ↓         ↓         ↓
   Form → Clean() → MEDIA_ROOT → ImageField → <img>
```

### 5.3 Flujo de Navegación
```
Base Template → Navigation Context → Active Page → Breadcrumbs
      ↓              ↓                    ↓           ↓
    Header → Menu Items → Current URL → Page Title
```

Esta arquitectura garantiza:
- ✅ Separación clara de responsabilidades
- ✅ Reutilización de código común
- ✅ Facilidad de mantenimiento
- ✅ Escalabilidad horizontal
- ✅ Testing comprehensivo
- ✅ Cumplimiento de restricciones técnicas