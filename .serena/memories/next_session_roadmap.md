# Next Session Development Roadmap

## 🎯 **Immediate Priority Tasks**

### **1. Model Implementation (HIGH)**
```python
# trabajadores/models.py
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
```

### **2. Database Migrations (HIGH)**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### **3. ModelForms Creation (MEDIUM)**
```python
# trabajadores/forms.py
class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = '__all__'
        widgets = {
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }
```

### **4. CRUD Views Implementation (MEDIUM)**
```python
# trabajadores/views.py
class TrabajadorListView(ListView):
    model = Trabajador
    template_name = 'trabajadores/list.html'
    context_object_name = 'trabajadores'
    paginate_by = 12
```

## 📋 **Development Sequence**

### **Phase 1: Data Layer (Session 1)**
1. ✅ **Models**: Implement all 4 models with proper field types
2. ✅ **Validations**: Add custom validation methods
3. ✅ **Meta classes**: Configure verbose names, ordering
4. ✅ **Migrations**: Generate and apply to database
5. ✅ **Admin**: Register models for easy testing

### **Phase 2: Form Layer (Session 1-2)**
1. **ModelForms**: Create forms for each entity
2. **Validation**: Custom clean methods and field validation
3. **Widgets**: Proper input types and Bootstrap classes
4. **Error messages**: Spanish localized error messages

### **Phase 3: View Layer (Session 2)**
1. **List Views**: Display entities with pagination
2. **Create Views**: Form handling and validation
3. **Update Views**: Pre-populated forms
4. **Delete Views**: Confirmation and soft delete
5. **Empty states**: Handle when no data exists

### **Phase 4: URL Configuration (Session 2)**
1. **Main URLs**: Configure project-level routing
2. **App URLs**: RESTful patterns for each app
3. **Static/Media**: Serve uploaded files
4. **Named URLs**: For reverse lookups

### **Phase 5: Template Layer (Session 3)**
1. **Base template**: Bootstrap layout with navigation
2. **List templates**: Card layouts per specifications
3. **Form templates**: Bootstrap form styling
4. **Home page**: Static content with carousels

### **Phase 6: Testing (Session 3-4)**
1. **Model tests**: Validation and business logic
2. **Form tests**: Validation and error handling
3. **View tests**: CRUD operations and edge cases
4. **Integration tests**: Full user workflows
5. **Coverage**: Achieve 85% target

## 🔧 **Commands Ready to Use**

```bash
# Development Environment
docker-compose up -d
docker-compose logs web
docker-compose exec web bash

# Django Management
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Quality Checks
docker-compose exec web uvx ruff check
docker-compose exec web uvx ruff format
docker-compose exec web uv run python manage.py test

# Coverage Testing
docker-compose exec web uv run coverage run --source='.' manage.py test
docker-compose exec web uv run coverage report
docker-compose exec web uv run coverage html
```

## 📁 **File Templates Ready**

### **Model Template**
```python
from django.db import models
from django.core.validators import ValidationError
from django.urls import reverse

class [Entity](models.Model):
    # Fields according to PRD specifications
    
    class Meta:
        verbose_name = "[Entity]"
        verbose_name_plural = "[Entities]"
        ordering = ['field']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('[app]:[entity]-detail', kwargs={'pk': self.pk})
    
    def clean(self):
        # Custom validation
        super().clean()
```

### **Form Template**
```python
from django import forms
from django.core.exceptions import ValidationError
from .models import [Entity]

class [Entity]Form(forms.ModelForm):
    class Meta:
        model = [Entity]
        fields = '__all__'
        widgets = {
            'field': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean_field(self):
        # Custom field validation
        return cleaned_data
```

### **View Template**
```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import [Entity]
from .forms import [Entity]Form

class [Entity]ListView(ListView):
    model = [Entity]
    template_name = '[app]/list.html'
    context_object_name = '[entities]'
    paginate_by = 12

class [Entity]CreateView(CreateView):
    model = [Entity]
    form_class = [Entity]Form
    template_name = '[app]/form.html'
    success_url = reverse_lazy('[app]:list')
    
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} creado exitosamente')
        return super().form_valid(form)
```

## 🎯 **Success Criteria**

### **Minimum Viable Product (MVP)**
- ✅ All 4 models implemented and migrated
- ✅ Basic CRUD operations working
- ✅ Forms with validation
- ✅ Bootstrap styling applied
- ✅ Spanish localization active

### **Full Implementation**
- ✅ 85% test coverage achieved
- ✅ All PRD specifications met
- ✅ Static home page implemented
- ✅ Image upload working
- ✅ Responsive design confirmed
- ✅ Production deployment ready

## 🚀 **Estimated Timeline**
- **Session 1**: Models + Migrations + Forms (3-4 hours)
- **Session 2**: Views + URLs + Basic Templates (3-4 hours)  
- **Session 3**: Complete Templates + Testing (4-5 hours)
- **Session 4**: Final Integration + Quality Gates (2-3 hours)

**Total**: 12-16 hours to complete full implementation

This roadmap ensures systematic development following the SPARC methodology with clear checkpoints and quality gates.