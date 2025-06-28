from django import forms
from django.core.exceptions import ValidationError
from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    """Formulario para crear y editar proveedores."""
    
    class Meta:
        model = Proveedor
        fields = ['nombre', 'descripcion', 'telefono', 'pais', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o razón social del proveedor',
                'maxlength': 200
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de productos/servicios que ofrece',
                'rows': 4
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+593 99 123 4567',
                'maxlength': 15
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'País donde se encuentra ubicado',
                'maxlength': 100
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@proveedor.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección física completa del proveedor',
                'rows': 3
            })
        }
        help_texts = {
            'nombre': 'Nombre o razón social del proveedor',
            'descripcion': 'Descripción de productos/servicios que ofrece',
            'telefono': 'Número de teléfono de contacto',
            'pais': 'País donde se encuentra ubicado el proveedor',
            'correo': 'Correo electrónico de contacto',
            'direccion': 'Dirección física completa del proveedor'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar todos los campos como requeridos
        for field_name in self.fields:
            self.fields[field_name].required = True
    
    def clean_nombre(self):
        """Validación personalizada para el nombre."""
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = nombre.strip().title()
            if len(nombre) < 3:
                raise ValidationError("El nombre del proveedor debe tener al menos 3 caracteres.")
            if len(nombre) > 200:
                raise ValidationError("El nombre del proveedor no puede exceder 200 caracteres.")
        return nombre
    
    def clean_descripcion(self):
        """Validación personalizada para la descripción."""
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = descripcion.strip()
            if len(descripcion) < 10:
                raise ValidationError("La descripción debe ser más detallada (al menos 10 caracteres).")
        return descripcion
    
    def clean_telefono(self):
        """Validación personalizada para el teléfono."""
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono = telefono.strip()
            # Permitir formatos: +593999123456, 099-123-4567, (099) 123 4567, etc.
            import re
            if not re.match(r'^\+?[\d\s\-\(\)]{7,15}$', telefono):
                raise ValidationError("Ingrese un número de teléfono válido.")
            
            # Extraer solo dígitos para validar longitud
            digits_only = re.sub(r'[^\d]', '', telefono)
            if len(digits_only) < 7 or len(digits_only) > 15:
                raise ValidationError("El número de teléfono debe tener entre 7 y 15 dígitos.")
        return telefono
    
    def clean_pais(self):
        """Validación personalizada para el país."""
        pais = self.cleaned_data.get('pais')
        if pais:
            pais = pais.strip().title()
            if len(pais) < 2:
                raise ValidationError("El nombre del país debe tener al menos 2 caracteres.")
            if not pais.replace(' ', '').replace('-', '').isalpha():
                raise ValidationError("El país solo puede contener letras, espacios y guiones.")
        return pais
    
    def clean_correo(self):
        """Validación personalizada para el correo."""
        correo = self.cleaned_data.get('correo')
        if correo:
            correo = correo.strip().lower()
            # Validación adicional de formato si es necesario
            import re
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo):
                raise ValidationError("Ingrese un correo electrónico válido.")
        return correo
    
    def clean_direccion(self):
        """Validación personalizada para la dirección."""
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            direccion = direccion.strip()
            if len(direccion) < 10:
                raise ValidationError("La dirección debe ser más específica (al menos 10 caracteres).")
        return direccion
    
    def clean(self):
        """Validación global del formulario."""
        cleaned_data = super().clean()
        
        # Validar duplicados de nombre (opcional, según reglas de negocio)
        nombre = cleaned_data.get('nombre')
        if nombre:
            if self.instance.pk:
                # Editando registro existente
                existing = Proveedor.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk)
                if existing.exists():
                    raise ValidationError({
                        'nombre': 'Ya existe un proveedor con este nombre.'
                    })
            else:
                # Creando nuevo registro
                if Proveedor.objects.filter(nombre__iexact=nombre).exists():
                    raise ValidationError({
                        'nombre': 'Ya existe un proveedor con este nombre.'
                    })
        
        return cleaned_data