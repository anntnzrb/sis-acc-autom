from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from carriacces.utils import validate_uploaded_image


class Trabajador(models.Model):
    """Modelo para trabajadores de la empresa CarriAcces."""

    nombre = models.CharField(
        max_length=100, verbose_name="Nombre", help_text="Nombre del trabajador"
    )

    apellido = models.CharField(
        max_length=100, verbose_name="Apellido", help_text="Apellido del trabajador"
    )

    correo = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Correo Electrónico",
        help_text="Correo electrónico único del trabajador",
    )

    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="La cédula debe contener exactamente 10 dígitos",
            )
        ],
        verbose_name="Cédula",
        help_text="Número de cédula de identidad (10 dígitos)",
    )

    codigo_empleado = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código de Empleado",
        help_text="Código único de empleado",
    )

    imagen = models.ImageField(
        upload_to="trabajadores/",
        blank=True,
        null=True,
        verbose_name="Imagen",
        help_text="Foto del trabajador (opcional)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        ordering = ["apellido", "nombre"]
        constraints = [
            models.UniqueConstraint(fields=["correo"], name="unique_trabajador_correo"),
            models.UniqueConstraint(fields=["cedula"], name="unique_trabajador_cedula"),
            models.UniqueConstraint(
                fields=["codigo_empleado"], name="unique_trabajador_codigo"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def get_nombre_completo(self) -> str:
        """Retorna el nombre completo del trabajador."""
        return f"{self.nombre} {self.apellido}"

    def clean(self) -> None:
        """Validación personalizada del modelo."""
        super().clean()
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        if self.apellido:
            self.apellido = self.apellido.strip().title()
        if self.correo:
            self.correo = self.correo.strip().lower()
        if self.codigo_empleado:
            self.codigo_empleado = self.codigo_empleado.strip().upper()
        if self.imagen:
            validate_uploaded_image(self.imagen)
