# Estilo de Código y Convenciones

## Reglas de Arquitectura:
- **Modularidad**: Archivos máximo 500 líneas, funciones máximo 50 líneas
- **Responsabilidad única**: Cada módulo y función debe tener un propósito claro
- **Funcional sobre imperativo**: Usar `itertools` y `functools`
- **Menos líneas = menos mantenimiento**: Priorizar soluciones concisas y legibles

## Características Modernas de Python (3.13+):
- Data classes con `@dataclass(slots=True)` para rendimiento
- Generics integrados (`list[str]` no `List[str]`)
- `functools.cache` en lugar de `lru_cache(maxsize=None)`
- Type hints en **TODAS** las funciones
- `Self` type para retornos de métodos (Python 3.11+)
- `Override` decorator para sobrescritura de métodos (Python 3.12+)

## Reglas de Concisión:
- Operador walrus para patrones assign-and-use
- Comprensiones sobre bucles explícitos
- Match-case para coincidencia de patrones (3+ casos)
- Argument unpacking con `*args`/`**kwargs`

## Herramientas de Desarrollo:
- **Ruff**: Herramienta única para linting y formateo
- **UV**: Administrador de paquetes rápido
- **pyproject.toml**: Configuración completa del proyecto

## Django-Específico:
- Usar `@dataclass(slots=True)` para estructuras de datos no-ORM
- Administradores de modelos para lógica de consulta reutilizable
- Lógica de negocio en **funciones de servicio** (no métodos de modelo)
- Restricciones de modelo con `Meta.constraints`
- Siempre llamar `full_clean()` antes de guardar para validación
- ModelForms para cada modelo con validación apropiada

## Idioma del Proyecto:
- **Interfaz de usuario**: TODO el contenido visible debe estar en **español**
- **Código**: Puede estar en inglés o español según sea pertinente
- **Producto final**: Completamente en español para el usuario final