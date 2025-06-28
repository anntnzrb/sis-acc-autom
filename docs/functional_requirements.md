# Requerimientos Funcionales - CarriAcces

## 1. Entidades del Sistema

### 1.1 Trabajador
**Campos requeridos:**
- nombre (CharField, máx 100 caracteres)
- apellido (CharField, máx 100 caracteres)
- correo (EmailField, único)
- cedula (CharField, máx 20 caracteres, único)
- codigo_empleado (CharField, máx 20 caracteres, único)
- imagen (ImageField, opcional, upload_to='trabajadores/')

**Validaciones:**
- Correo debe ser válido y único en el sistema
- Cédula debe ser alfanumérica y única
- Código de empleado debe ser único
- Imagen debe ser formato válido (JPG, PNG, WebP)

### 1.2 Empresa
**Campos requeridos:**
- nombre (CharField, máx 200 caracteres)
- direccion (TextField)
- mision (TextField)
- vision (TextField)
- anio_fundacion (IntegerField, rango 1900-año actual)
- ruc (CharField, máx 20 caracteres, único)
- imagen (ImageField, opcional, upload_to='empresa/')

**Validaciones:**
- RUC debe ser único y seguir formato válido
- Año de fundación no puede ser futuro
- Solo una instancia de empresa permitida en el sistema

### 1.3 Producto
**Campos requeridos:**
- nombre (CharField, máx 200 caracteres)
- descripcion (TextField)
- precio (DecimalField, max_digits=10, decimal_places=2)
- iva (IntegerField, choices=[0, 15])
- imagen (ImageField, opcional, upload_to='productos/')

**Validaciones:**
- Precio debe ser positivo
- IVA solo puede ser 0 o 15
- Descripción mínimo 10 caracteres

### 1.4 Proveedor
**Campos requeridos:**
- nombre (CharField, máx 200 caracteres)
- descripcion (TextField)
- telefono (CharField, máx 20 caracteres)
- pais (CharField, máx 100 caracteres)
- correo (EmailField)
- direccion (TextField)

**Validaciones:**
- Correo debe ser formato válido
- Teléfono debe ser alfanumérico
- Descripción mínimo 20 caracteres

## 2. Operaciones CRUD

### 2.1 Crear (Create)
- Formularios de creación para cada entidad
- Validación completa antes de guardar
- Mensajes de confirmación al usuario
- Redirección a lista después de crear

### 2.2 Leer (Read)
- Página de listado para cada entidad
- Visualización en tarjetas responsivas
- Estados vacíos con mensaje informativo
- Paginación si hay más de 12 elementos

### 2.3 Actualizar (Update)
- Formularios de edición pre-poblados
- Validación completa antes de actualizar
- Confirmación de cambios guardados
- Mantenimiento de archivos no modificados

### 2.4 Eliminar (Delete)
- Confirmación antes de eliminar
- Mensaje de confirmación post-eliminación
- Eliminación en cascada donde aplique
- Limpieza de archivos huérfanos

## 3. Páginas del Sistema

### 3.1 Página Principal (/)
**Contenido estático:**
- Título del sitio web + Logo de la tienda
- Sección 1: "DESCRIPCION DE LA EMPRESA"
  - Carrusel de 4 imágenes (izquierda)
  - Texto descriptivo (derecha)
- Sección 2: "HISTORIA DE LA EMPRESA"
  - Texto narrativo (izquierda)
  - Carrusel de 4 imágenes (derecha)
- Menú de navegación completo

### 3.2 Página Nosotros (/nosotros/)
**Lógica condicional:**
- **Sin información de empresa:**
  - Tarjeta centrada con icono de advertencia
  - Mensaje: "NO SE HA INGRESADO INFORMACION DE LA EMPRESA!!"
  - Botón "AGREGAR INFORMACION" → formulario de creación
- **Con información de empresa:**
  - Layout de 2 columnas
  - Columna izquierda: nombre, RUC, dirección, imagen, año fundación
  - Columna derecha: botón "EDITAR INFORMACION", misión, visión

### 3.3 Página Trabajadores (/trabajadores/)
**Características:**
- Título: "NUESTRO PERSONAL"
- Tarjetas horizontales en 2 columnas
- Layout: imagen izquierda + información derecha
- Botón "AGREGAR TRABAJADOR" (esquina superior derecha)
- Información: imagen, nombre completo, correo, cédula, código empleado
- Botones editar/eliminar por tarjeta
- Estado vacío con opción de agregar primer trabajador

### 3.4 Página Productos (/productos/)
**Características:**
- Título: "NUESTROS PRODUCTOS"
- Grilla de 3 columnas con tarjetas verticales
- Layout: imagen arriba + información abajo
- Botón "AGREGAR PRODUCTO" (esquina superior derecha)
- Información: imagen del producto, nombre, precio + "% IVA"
- Placeholder de gradiente si no hay imagen
- Botones editar/eliminar por tarjeta
- Estado vacío con opción de agregar primer producto

### 3.5 Página Proveedores (/proveedores/)
**Características:**
- Título: "NUESTROS PROVEEDORES"
- Grilla de 3 columnas con tarjetas verticales
- Estructura: header con nombre + body con información
- Botón "AGREGAR PROVEEDOR" (centrado en parte superior)
- Información: nombre (header), correo, teléfono, país (body)
- Botones editar/eliminar por tarjeta
- Estado vacío con opción de agregar primer proveedor

## 4. Navegación

### 4.1 Menú Principal
**Estructura:** `HOME | NOSOTROS | CLIENTES | PRODUCTOS | TRABAJADORES | PROVEEDORES | SUCURSALES`

**Enlaces funcionales:**
- HOME → Página principal (/)
- NOSOTROS → Página empresa (/nosotros/)
- PRODUCTOS → Lista de productos (/productos/)
- TRABAJADORES → Lista de trabajadores (/trabajadores/)
- PROVEEDORES → Lista de proveedores (/proveedores/)

**Enlaces no funcionales (solo visuales):**
- CLIENTES (aparece en menú pero sin funcionalidad)
- SUCURSALES (aparece en menú pero sin funcionalidad)

## 5. Formularios

### 5.1 Características Generales
- Django ModelForms para cada entidad
- Validación HTML5 + Django backend
- Mensajes de error claros en español
- Campos requeridos marcados visualmente
- Upload de archivos con preview

### 5.2 Validaciones Específicas
- Unicidad de campos donde aplique
- Formatos de correo válidos
- Rangos numéricos apropiados
- Longitudes mínimas y máximas
- Tipos de archivo permitidos para imágenes

## 6. Estados del Sistema

### 6.1 Estados Vacíos
- Mensaje informativo centrado
- Icono representativo
- Botón de acción primaria para agregar primer elemento
- Diseño consistente entre entidades

### 6.2 Estados de Error
- Mensajes de error claros y específicos
- Conservación de datos ingresados
- Indicación visual de campos con errores
- Sugerencias de corrección

### 6.3 Estados de Confirmación
- Mensajes de éxito después de operaciones
- Confirmaciones antes de eliminaciones
- Feedback visual inmediato
- Redirecciones apropiadas

## 7. Internacionalización

### 7.1 Idioma
- **Interfaz de usuario:** Completamente en español
- **Mensajes del sistema:** En español
- **Etiquetas y botones:** En español
- **Validaciones:** Mensajes en español

### 7.2 Formato de Datos
- Fechas en formato DD/MM/YYYY
- Números decimales con coma como separador
- Moneda en formato $X.XXX,XX
- Teléfonos en formato internacional opcional