from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Empresa


class EmpresaForm(forms.ModelForm):
    """Formulario para crear y editar la información de la empresa."""

    class Meta:
        model = Empresa
        fields = [
            "nombre",
            "direccion",
            "mision",
            "vision",
            "anio_fundacion",
            "ruc",
            "imagen",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre oficial de la empresa",
                    "maxlength": 200,
                }
            ),
            "direccion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Dirección física completa de la empresa",
                    "rows": 3,
                }
            ),
            "mision": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Misión de la empresa",
                    "rows": 4,
                }
            ),
            "vision": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Visión de la empresa",
                    "rows": 4,
                }
            ),
            "anio_fundacion": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Año de fundación",
                    "min": 1900,
                    "max": datetime.now().year,
                }
            ),
            "ruc": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1234567890001",
                    "maxlength": 13,
                    "pattern": "[0-9]{13}",
                }
            ),
            "imagen": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/jpeg,image/jpg,image/png,image/webp",
                }
            ),
        }
        help_texts = {
            "nombre": "Nombre oficial de la empresa",
            "direccion": "Dirección física completa",
            "mision": "Declaración de la misión empresarial",
            "vision": "Declaración de la visión empresarial",
            "anio_fundacion": f"Año de fundación (entre 1900 y {datetime.now().year})",
            "ruc": "Registro Único de Contribuyente (13 dígitos)",
            "imagen": "Logo o imagen de la empresa (opcional, formatos: JPG, PNG, WebP)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar todos los campos como requeridos excepto imagen
        for field_name in [
            "nombre",
            "direccion",
            "mision",
            "vision",
            "anio_fundacion",
            "ruc",
        ]:
            self.fields[field_name].required = True

        # Imagen es opcional
        self.fields["imagen"].required = False

    def clean_nombre(self):
        """Validación personalizada para el nombre."""
        nombre = self.cleaned_data.get("nombre")
        if nombre:
            nombre = nombre.strip().title()
            if len(nombre) < 3:
                raise ValidationError(
                    "El nombre de la empresa debe tener al menos 3 caracteres."
                )
        return nombre

    def clean_direccion(self):
        """Validación personalizada para la dirección."""
        direccion = self.cleaned_data.get("direccion")
        if direccion:
            direccion = direccion.strip()
            if len(direccion) < 10:
                raise ValidationError(
                    "La dirección debe ser más específica (al menos 10 caracteres)."
                )
        return direccion

    def clean_mision(self):
        """Validación personalizada para la misión."""
        mision = self.cleaned_data.get("mision")
        if mision:
            mision = mision.strip()
            if len(mision) < 20:
                raise ValidationError(
                    "La misión debe ser más descriptiva (al menos 20 caracteres)."
                )
        return mision

    def clean_vision(self):
        """Validación personalizada para la visión."""
        vision = self.cleaned_data.get("vision")
        if vision:
            vision = vision.strip()
            if len(vision) < 20:
                raise ValidationError(
                    "La visión debe ser más descriptiva (al menos 20 caracteres)."
                )
        return vision

    def clean_anio_fundacion(self):
        """Validación personalizada para el año de fundación."""
        anio = self.cleaned_data.get("anio_fundacion")
        if anio:
            current_year = datetime.now().year
            if anio < 1900:
                raise ValidationError(
                    "El año de fundación no puede ser anterior a 1900."
                )
            if anio > current_year:
                raise ValidationError(
                    f"El año de fundación no puede ser mayor al año actual ({current_year})."
                )
        return anio

    def clean_ruc(self):
        """Validación personalizada para el RUC."""
        ruc = self.cleaned_data.get("ruc")
        if ruc:
            ruc = ruc.strip()
            if not ruc.isdigit() or len(ruc) != 13:
                raise ValidationError("El RUC debe contener exactamente 13 dígitos.")

            # Verificar unicidad (solo puede haber una empresa)
            if self.instance.pk:
                # Editando registro existente
                if (
                    Empresa.objects.filter(ruc=ruc)
                    .exclude(pk=self.instance.pk)
                    .exists()
                ):
                    raise ValidationError("Ya existe una empresa con este RUC.")
            else:
                # Creando nuevo registro - verificar que no exista otra empresa
                if Empresa.objects.exists():
                    raise ValidationError(
                        "Solo puede existir una empresa en el sistema."
                    )
                if Empresa.objects.filter(ruc=ruc).exists():
                    raise ValidationError("Ya existe una empresa con este RUC.")
        return ruc

    def clean_imagen(self):
        """Validación personalizada para la imagen."""
        imagen = self.cleaned_data.get("imagen")
        if imagen:
            # Verificar tipo de archivo
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if imagen.content_type not in allowed_types:
                raise ValidationError(
                    "Solo se permiten imágenes en formato JPG, PNG o WebP."
                )

            # Verificar tamaño
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("La imagen no puede ser mayor a 5MB.")

        return imagen

    def clean(self):
        """Validación global del formulario."""
        cleaned_data = super().clean()

        # Verificar que solo exista una empresa (singleton)
        if not self.instance.pk and Empresa.objects.exists():
            raise ValidationError("Solo puede existir una empresa en el sistema.")

        return cleaned_data
