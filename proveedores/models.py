from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Proveedor(models.Model):
    """Modelo para proveedores de CarriAcces."""
    
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del Proveedor",
        help_text="Nombre o razón social del proveedor"
    )
    
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de los productos/servicios que ofrece"
    )
    
    telefono = models.CharField(
        max_length=15,
        validators=[RegexValidator(
            regex=r'^\+?[\d\s\-\(\)]{7,15}$',
            message='Ingrese un número de teléfono válido'
        )],
        verbose_name="Teléfono",
        help_text="Número de teléfono de contacto"
    )
    
    pais = models.CharField(
        max_length=100,
        verbose_name="País",
        help_text="País donde se encuentra ubicado el proveedor"
    )
    
    correo = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Correo Electrónico",
        help_text="Correo electrónico de contacto"
    )
    
    direccion = models.TextField(
        verbose_name="Dirección",
        help_text="Dirección física completa del proveedor"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['pais']),
        ]
    
    def __str__(self) -> str:
        return self.nombre
    
    def clean(self) -> None:
        """Validación personalizada del modelo."""
        super().clean()
        
        # Normalizar datos
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        if self.descripcion:
            self.descripcion = self.descripcion.strip()
        if self.pais:
            self.pais = self.pais.strip().title()
        if self.correo:
            self.correo = self.correo.strip().lower()
        if self.direccion:
            self.direccion = self.direccion.strip()
        if self.telefono:
            # Limpiar espacios en teléfono
            self.telefono = self.telefono.strip()
    
    def get_contact_info(self) -> str:
        """Retorna información de contacto formateada."""
        contact_parts = []
        if self.correo:
            contact_parts.append(f"Email: {self.correo}")
        if self.telefono:
            contact_parts.append(f"Tel: {self.telefono}")
        return " | ".join(contact_parts)
    
    def get_location_info(self) -> str:
        """Retorna información de ubicación formateada."""
        location_parts = []
        if self.pais:
            location_parts.append(self.pais)
        if self.direccion:
            location_parts.append(self.direccion)
        return ", ".join(location_parts)
