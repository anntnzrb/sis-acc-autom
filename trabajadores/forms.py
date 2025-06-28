from django import forms
from django.core.exceptions import ValidationError
from .models import Trabajador
from carriacces.utils import validate_uploaded_image


class TrabajadorForm(forms.ModelForm):
    """Formulario para crear y editar trabajadores."""
    
    class Meta:
        model = Trabajador
        fields = ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del trabajador',
                'maxlength': 100
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido del trabajador',
                'maxlength': 100
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890',
                'maxlength': 10,
                'pattern': '[0-9]{10}'
            }),
            'codigo_empleado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del empleado',
                'maxlength': 20
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg,image/jpg,image/png,image/webp'
            })
        }
        help_texts = {
            'nombre': 'Nombre del trabajador (máximo 100 caracteres)',
            'apellido': 'Apellido del trabajador (máximo 100 caracteres)',
            'correo': 'Correo electrónico único del trabajador',
            'cedula': 'Número de cédula de identidad (10 dígitos)',
            'codigo_empleado': 'Código único de empleado',
            'imagen': 'Imagen del trabajador (opcional, formatos: JPG, PNG, WebP)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos requeridos
        for field_name in ['nombre', 'apellido', 'correo', 'cedula', 'codigo_empleado']:
            self.fields[field_name].required = True
        
        # Imagen es opcional
        self.fields['imagen'].required = False
    
    def clean_nombre(self):
        """Validación personalizada para el nombre."""
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            if len(nombre) < 2:
                raise ValidationError("El nombre debe tener al menos 2 caracteres.")
            if not nombre.replace(' ', '').isalpha():
                raise ValidationError("El nombre solo puede contener letras y espacios.")
        return nombre
    
    def clean_apellido(self):
        """Validación personalizada para el apellido."""
        apellido = self.cleaned_data.get('apellido')
        if apellido:
            apellido = apellido.strip().title()
            if len(apellido) < 2:
                raise ValidationError("El apellido debe tener al menos 2 caracteres.")
            if not apellido.replace(' ', '').isalpha():
                raise ValidationError("El apellido solo puede contener letras y espacios.")
        return apellido
    
    def clean_correo(self):
        """Validación personalizada para el correo."""
        correo = self.cleaned_data.get('correo')
        if correo:
            correo = correo.strip().lower()
            # Verificar unicidad
            if self.instance.pk:
                # Editando registro existente
                if Trabajador.objects.filter(correo=correo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("Ya existe un trabajador con este correo electrónico.")
            else:
                # Creando nuevo registro
                if Trabajador.objects.filter(correo=correo).exists():
                    raise ValidationError("Ya existe un trabajador con este correo electrónico.")
        return correo
    
    def clean_cedula(self):
        """Validación personalizada para la cédula."""
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            cedula = cedula.strip()
            if not cedula.isdigit() or len(cedula) != 10:
                raise ValidationError("La cédula debe contener exactamente 10 dígitos.")
            
            # Verificar unicidad
            if self.instance.pk:
                # Editando registro existente
                if Trabajador.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("Ya existe un trabajador con esta cédula.")
            else:
                # Creando nuevo registro
                if Trabajador.objects.filter(cedula=cedula).exists():
                    raise ValidationError("Ya existe un trabajador con esta cédula.")
        return cedula
    
    def clean_codigo_empleado(self):
        """Validación personalizada para el código de empleado."""
        codigo = self.cleaned_data.get('codigo_empleado')
        if codigo:
            codigo = codigo.strip().upper()
            if len(codigo) < 3:
                raise ValidationError("El código de empleado debe tener al menos 3 caracteres.")
            
            # Verificar unicidad
            if self.instance.pk:
                # Editando registro existente
                if Trabajador.objects.filter(codigo_empleado=codigo).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("Ya existe un trabajador con este código de empleado.")
            else:
                # Creando nuevo registro
                if Trabajador.objects.filter(codigo_empleado=codigo).exists():
                    raise ValidationError("Ya existe un trabajador con este código de empleado.")
        return codigo
    
    def clean_imagen(self):
        """Validación personalizada para la imagen."""
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Use the centralized validation utility
            imagen = validate_uploaded_image(imagen)
        return imagen