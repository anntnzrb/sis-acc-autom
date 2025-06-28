# Lista de Verificación al Completar Tareas

## Antes de Finalizar Cualquier Tarea

### 1. Linting y Formateo
- [ ] Ejecutar `uvx ruff check` (debe pasar sin errores)
- [ ] Ejecutar `uvx ruff format` (formatear código)
- [ ] Verificar que no hay warnings de tipo o estilo

### 2. Testing
- [ ] Ejecutar `python manage.py test` (todos los tests deben pasar)
- [ ] Escribir tests para nueva funcionalidad
- [ ] Verificar cobertura de tests relevantes
- [ ] Tests específicos para validaciones personalizadas

### 3. Funcionalidad
- [ ] Verificar que las migraciones funcionan correctamente
- [ ] Probar la funcionalidad en el navegador
- [ ] Verificar formularios y validaciones
- [ ] Comprobar estados vacíos y de error
- [ ] Verificar que las imágenes se suben correctamente

### 4. Estilo y UX
- [ ] Verificar que todo el texto está en español
- [ ] Comprobar responsividad en diferentes pantallas
- [ ] Verificar navegación entre páginas
- [ ] Comprobar mensajes de éxito/error

### 5. Base de Datos
- [ ] Verificar que las migraciones se aplican sin errores
- [ ] Comprobar constraints y validaciones de BD
- [ ] Verificar integridad referencial

### 6. Archivos Estáticos
- [ ] Ejecutar `python manage.py collectstatic` si se agregaron archivos
- [ ] Verificar que CSS/JS se cargan correctamente
- [ ] Comprobar imágenes de placeholder

### 7. Documentación
- [ ] Actualizar docstrings si es necesario
- [ ] Comentarios en código complejo
- [ ] README actualizado si hay cambios importantes

## Comandos de Verificación Rápida
```bash
# Dentro del contenedor Docker
python manage.py check
python manage.py makemigrations --dry-run
python manage.py test
python manage.py collectstatic --dry-run

# Fuera del contenedor
uvx ruff check
uvx ruff format --check
```

## Casos Especiales
- **Nuevos modelos**: verificar migraciones y admin
- **Cambios en formularios**: probar validaciones exhaustivamente
- **Nuevas vistas**: verificar permisos y context data
- **Cambios en URLs**: verificar redirecciones
- **Archivos de media**: verificar permisos y limpieza