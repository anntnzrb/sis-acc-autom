from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Producto


class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos."""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'iva', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'maxlength': 200
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción detallada del producto',
                'rows': 4
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'iva': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/webp'
            })
        }
        help_texts = {
            'nombre': 'Nombre descriptivo del producto',
            'descripcion': 'Descripción detallada del producto',
            'precio': 'Precio del producto en USD (sin IVA)',
            'iva': 'Porcentaje de IVA aplicable',
            'imagen': 'Imagen del producto (opcional, formatos: JPG, PNG, WebP)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos requeridos
        for field_name in ['nombre', 'descripcion', 'precio', 'iva']:
            self.fields[field_name].required = True
        
        # Imagen es opcional
        self.fields['imagen'].required = False
        
        # Configurar choices para IVA
        self.fields['iva'].choices = Producto.IVA_CHOICES
    
    def clean_nombre(self):
        """Validación personalizada para el nombre."""
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            if len(nombre) < 3:
                raise ValidationError("El nombre del producto debe tener al menos 3 caracteres.")
            if len(nombre) > 200:
                raise ValidationError("El nombre del producto no puede exceder 200 caracteres.")
        return nombre
    
    def clean_descripcion(self):
        """Validación personalizada para la descripción."""
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) < 10:
                raise ValidationError("La descripción debe ser más detallada (al menos 10 caracteres).")
        return descripcion
    
    def clean_precio(self):
        """Validación personalizada para el precio."""
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a 0.")
            if precio > Decimal('999999.99'):
                raise ValidationError("El precio no puede exceder $999,999.99.")
            
            # Validar que tenga máximo 2 decimales
            if precio.as_tuple().exponent < -2:
                raise ValidationError("El precio no puede tener más de 2 decimales.")
        return precio
    
    def clean_iva(self):
        """Validación personalizada para el IVA."""
        iva = self.cleaned_data.get('iva')
        if iva is not None:
            if iva not in [0, 15]:
                raise ValidationError("El IVA debe ser 0% o 15%.")
        return iva
    
    def clean_imagen(self):
        """Validación personalizada para la imagen."""
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Verificar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if imagen.content_type not in allowed_types:
                raise ValidationError("Solo se permiten imágenes en formato JPG, PNG o WebP.")
            
            # Verificar tamaño
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("La imagen no puede ser mayor a 5MB.")
        
        return imagen
    
    def clean(self):
        """Validación global del formulario."""
        cleaned_data = super().clean()
        
        # Validaciones adicionales si es necesario
        nombre = cleaned_data.get('nombre')
        precio = cleaned_data.get('precio')
        
        if nombre and precio:
            # Verificar duplicados de nombre (opcional, según reglas de negocio)
            if self.instance.pk:
                # Editando registro existente
                existing = Producto.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk)
                if existing.exists():
                    raise ValidationError({
                        'nombre': 'Ya existe un producto con este nombre.'
                    })
            else:
                # Creando nuevo registro
                if Producto.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError({
                        'nombre': 'Ya existe un producto con este nombre.'
                    })
        
        return cleaned_data