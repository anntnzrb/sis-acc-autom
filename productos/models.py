from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Producto(models.Model):
    """Modelo para productos de CarriAcces."""
    
    IVA_CHOICES = [
        (0, '0% IVA'),
        (15, '15% IVA'),
    ]
    
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del Producto",
        help_text="Nombre descriptivo del producto"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del producto"
    )
    
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio",
        help_text="Precio del producto en USD (sin IVA)"
    )
    
    iva = models.IntegerField(
        choices=IVA_CHOICES,
        default=15,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(15)
        ],
        verbose_name="IVA",
        help_text="Porcentaje de IVA aplicable (0% o 15%)"
    )
    
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        verbose_name="Imagen",
        help_text="Imagen del producto (opcional)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['precio']),
        ]
    
    def __str__(self) -> str:
        return self.nombre
    
    def clean(self) -> None:
        """Validación personalizada del modelo."""
        super().clean()
        
        # Normalizar nombre
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        
        # Normalizar descripción
        if self.descripcion:
            self.descripcion = self.descripcion.strip()
        
        # Validar IVA
        if self.iva is not None and self.iva not in [0, 15]:
            raise ValidationError("El IVA debe ser 0% o 15%")
        
        # Validar precio
        if self.precio is not None and self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
    
    @property
    def precio_con_iva(self) -> Decimal:
        """Calcula el precio incluyendo el IVA."""
        if self.precio and self.iva is not None:
            iva_decimal = Decimal(str(self.iva)) / Decimal('100')
            return self.precio * (Decimal('1') + iva_decimal)
        return self.precio or Decimal('0')
    
    @property
    def valor_iva(self) -> Decimal:
        """Calcula el valor del IVA."""
        if self.precio and self.iva is not None:
            iva_decimal = Decimal(str(self.iva)) / Decimal('100')
            return self.precio * iva_decimal
        return Decimal('0')
    
    def get_precio_display(self) -> str:
        """Retorna el precio formateado para mostrar."""
        if self.precio:
            return f"${self.precio:.2f}"
        return "$0.00"
    
    def get_precio_con_iva_display(self) -> str:
        """Retorna el precio con IVA formateado para mostrar."""
        precio_total = self.precio_con_iva
        return f"${precio_total:.2f}"
    
    def get_iva_display_text(self) -> str:
        """Retorna el texto de IVA para mostrar."""
        return f"{self.iva}% IVA" if self.iva else "0% IVA"
