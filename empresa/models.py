from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class EmpresaManager(models.Manager):
    """Manager personalizado para manejar la lógica singleton de Empresa."""

    def get_empresa(self):
        """Obtiene la única instancia de empresa o None si no existe."""
        return self.first()

    def create_empresa(self, **kwargs):
        """Crea la empresa solo si no existe otra."""
        if self.exists():
            raise ValidationError("Ya existe una empresa registrada en el sistema.")
        return self.create(**kwargs)


class Empresa(models.Model):
    """Modelo singleton para la información de la empresa CarriAcces."""

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Empresa",
        help_text="Nombre oficial de la empresa",
    )

    direccion = models.TextField(
        verbose_name="Dirección", help_text="Dirección física completa de la empresa"
    )

    mision = models.TextField(verbose_name="Misión", help_text="Misión de la empresa")

    vision = models.TextField(verbose_name="Visión", help_text="Visión de la empresa")

    anio_fundacion = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1900, message="El año de fundación debe ser mayor a 1900"
            ),
            MinValueValidator(1900),
        ],
        verbose_name="Año de Fundación",
        help_text="Año en que fue fundada la empresa",
    )

    ruc = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{13}$", message="El RUC debe contener exactamente 13 dígitos"
            )
        ],
        verbose_name="RUC",
        help_text="Registro Único de Contribuyente (13 dígitos)",
    )

    imagen = models.ImageField(
        upload_to="empresa/",
        blank=True,
        null=True,
        verbose_name="Logo/Imagen",
        help_text="Logo o imagen representativa de la empresa (opcional)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmpresaManager()

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        constraints = [
            models.UniqueConstraint(fields=["ruc"], name="unique_empresa_ruc"),
        ]

    def __str__(self) -> str:
        return self.nombre

    def clean(self) -> None:
        """Validación personalizada del modelo."""
        super().clean()

        # Validar que solo exista una empresa
        if not self.pk and Empresa.objects.exists():
            raise ValidationError("Solo puede existir una empresa en el sistema.")

        # Normalizar datos
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        if self.direccion:
            self.direccion = self.direccion.strip()
        if self.mision:
            self.mision = self.mision.strip()
        if self.vision:
            self.vision = self.vision.strip()

        # Validar año de fundación
        from datetime import datetime

        current_year = datetime.now().year
        if self.anio_fundacion and self.anio_fundacion > current_year:
            raise ValidationError(
                f"El año de fundación no puede ser mayor al año actual ({current_year})"
            )

    def save(self, *args, **kwargs):
        """Override save para garantizar singleton."""
        if not self.pk and Empresa.objects.exists():
            raise ValidationError("Solo puede existir una empresa en el sistema.")
        self.full_clean()
        super().save(*args, **kwargs)
