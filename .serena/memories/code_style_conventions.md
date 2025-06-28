# Convenciones de Código y Estilo

## Estilo Python General
- **Python 3.13+** con características modernas
- **Type hints** en todas las funciones
- **Docstrings** en español para clases y métodos complejos
- **Snake_case** para variables y funciones
- **PascalCase** para clases
- **UPPERCASE** para constantes

## Convenciones Django
- **ModelForms** para todos los formularios
- **Class-Based Views** para todas las vistas
- **Validación en clean()** para lógica personalizada
- **Manager personalizado** cuando sea necesario
- **Timestamps** (created_at, updated_at) en todos los modelos
- **Verbose names** en español para todos los campos
- **Help texts** descriptivos en campos complejos

## Estructura de Modelos
```python
class MiModelo(models.Model):
    """Docstring en español."""
    
    # Campos principales
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Texto de ayuda"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Manager personalizado
    objects = MiModeloManager()
    
    class Meta:
        verbose_name = "Mi Modelo"
        verbose_name_plural = "Mis Modelos"
        ordering = ["nombre"]
    
    def __str__(self) -> str:
        return self.nombre
    
    def clean(self) -> None:
        """Validación personalizada."""
        super().clean()
        # Lógica de validación
```

## Nomenclatura
- **URLs**: en español con guiones (`/trabajadores/agregar/`)
- **Templates**: organizados por app (`templates/trabajadores/`)
- **CSS classes**: kebab-case (`card-header`)
- **Variables JavaScript**: camelCase
- **Archivos estáticos**: organizados por tipo

## Validaciones
- **Backend**: Django clean() methods
- **Frontend**: HTML5 + JavaScript
- **Mensajes**: siempre en español
- **Unicidad**: validar en modelo y formulario
- **Archivos**: validar tipo y tamaño

## Testing
- **Test por funcionalidad** (modelo, formulario, vista)
- **Nombres descriptivos**: `test_<accion>_<condicion>_<resultado>`
- **SetUp compartido** cuando sea posible
- **Asserts específicos** con mensajes claros
- **Cobertura completa** de casos edge