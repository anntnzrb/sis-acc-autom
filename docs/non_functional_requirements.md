# Requerimientos No Funcionales - CarriAcces

## 1. Rendimiento

### 1.1 Tiempo de Respuesta
- **Páginas estáticas:** < 500ms
- **Operaciones CRUD simples:** < 1 segundo
- **Carga de imágenes:** < 2 segundos
- **Consultas de base de datos:** < 300ms

### 1.2 Capacidad
- **Trabajadores:** Hasta 500 registros
- **Productos:** Hasta 2000 registros
- **Proveedores:** Hasta 100 registros
- **Imágenes:** Máximo 5MB por archivo
- **Usuarios concurrentes:** Hasta 50 usuarios

### 1.3 Optimización
- Uso de indexes en campos de búsqueda
- Compresión de imágenes automática
- Cache de consultas frecuentes
- Lazy loading de imágenes
- Paginación en listas grandes

## 2. Seguridad

### 2.1 Validación de Datos
- **Sanitización:** Todos los inputs HTML
- **Validación:** Campos requeridos y formatos
- **Prevención XSS:** Escape de contenido dinámico
- **Prevención CSRF:** Tokens en formularios
- **SQL Injection:** Uso de ORM Django

### 2.2 Archivos
- **Tipos permitidos:** JPG, PNG, WebP únicamente
- **Tamaño máximo:** 5MB por imagen
- **Ubicación segura:** Fuera del directorio web
- **Nombres sanitizados:** Prevención de path traversal
- **Validación de headers:** Verificación de tipo MIME

### 2.3 Configuración
- **DEBUG:** Deshabilitado en producción
- **SECRET_KEY:** Generada aleatoriamente
- **Database:** Credenciales seguras
- **Headers de seguridad:** HSTS, CSP, X-Frame-Options
- **Logs:** Sin exposición de datos sensibles

## 3. Usabilidad

### 3.1 Interfaz de Usuario
- **Responsive:** Compatible con móviles, tablets, desktop
- **Navegación:** Intuitiva y consistente
- **Feedback:** Mensajes claros de estado
- **Accesibilidad:** Contraste mínimo WCAG 2.1 AA
- **Carga:** Indicadores de progreso visual

### 3.2 Experiencia de Usuario
- **Flujo:** Máximo 3 clics para cualquier operación
- **Errores:** Mensajes de error comprensibles
- **Confirmaciones:** Antes de operaciones destructivas
- **Autoguardado:** En formularios largos
- **Estados vacíos:** Guías para primeros pasos

### 3.3 Diseño Visual
- **Tema:** Colores apropiados para tienda automotriz
- **Tipografía:** Sans-serif legible
- **Iconografía:** Consistente y reconocible
- **Espaciado:** Suficiente para legibilidad
- **Contraste:** Mínimo 4.5:1 para texto normal

## 4. Compatibilidad

### 4.1 Navegadores Web
- **Chrome:** Versiones últimas 2
- **Firefox:** Versiones últimas 2
- **Safari:** Versiones últimas 2
- **Edge:** Versiones últimas 2
- **Mobile Safari:** iOS 14+
- **Chrome Mobile:** Android 8+

### 4.2 Dispositivos
- **Desktop:** 1024px+ (diseño completo)
- **Tablet:** 768px-1023px (diseño adaptado)
- **Mobile:** 320px-767px (diseño móvil)
- **Touch:** Compatible con interfaces táctiles
- **Keyboard:** Navegación completa con teclado

### 4.3 Tecnologías
- **HTML5:** Semántico y válido
- **CSS3:** Grid y Flexbox para layouts
- **JavaScript:** ES6+ con transpilación
- **Images:** WebP con fallback a PNG/JPG
- **Fonts:** Web fonts con sistema fallback

## 5. Mantenibilidad

### 5.1 Código
- **Estándares:** PEP 8 para Python
- **Documentación:** Docstrings en funciones complejas
- **Modularidad:** Máximo 500 líneas por archivo
- **Funciones:** Máximo 50 líneas por función
- **Comentarios:** Solo donde sea necesario explicar lógica

### 5.2 Estructura
- **Separación:** Lógica de negocio separada de presentación
- **Reutilización:** Componentes reutilizables
- **Configuración:** Centralizada en settings
- **Dependencies:** Versionado y documentado
- **Tests:** Cobertura mínima 85%

### 5.3 Base de Datos
- **Migraciones:** Versionadas y reversibles
- **Indexes:** En campos de búsqueda frecuente
- **Constraints:** Integridad referencial
- **Backups:** Estrategia automatizada
- **Performance:** Consultas optimizadas

## 6. Escalabilidad

### 6.1 Arquitectura
- **Horizontal:** Preparado para múltiples instancias
- **Database:** Conexiones pooled
- **Media files:** Separados del código
- **Cache:** Redis para sesiones y cache
- **CDN:** Preparado para archivos estáticos

### 6.2 Recursos
- **Memory:** Eficiente uso de memoria
- **CPU:** Operaciones no bloqueantes
- **Disk:** Rotación de logs
- **Network:** Compresión gzip
- **Database:** Índices optimizados

### 6.3 Monitoring
- **Logs:** Estructurados y centralizados
- **Metrics:** Tiempo de respuesta y errores
- **Health checks:** Endpoints de monitoreo
- **Alerts:** Umbrales de rendimiento
- **Debug:** Información para troubleshooting

## 7. Disponibilidad

### 7.1 Uptime
- **Objetivo:** 99.5% de disponibilidad
- **Downtime planificado:** Fuera de horario laboral
- **Recovery:** Tiempo máximo 1 hora
- **Backup:** Restauración en menos de 30 minutos
- **Health checks:** Cada 5 minutos

### 7.2 Tolerancia a Fallos
- **Database:** Manejo de conexiones perdidas
- **Network:** Retry logic en operaciones críticas
- **Files:** Validación antes de procesamiento
- **Memory:** Manejo de out of memory
- **Disk:** Validación de espacio disponible

### 7.3 Recuperación
- **Backups:** Diarios automáticos
- **Data integrity:** Verificación periódica
- **Rollback:** Capacidad de volver a versión anterior
- **Documentation:** Procedimientos de recuperación
- **Testing:** Simulacros de recuperación

## 8. Restricciones Técnicas

### 8.1 Plataforma
- **Python:** 3.13 exclusivamente
- **Django:** 5.2.2 exactamente
- **PostgreSQL:** 15+ requerido
- **Docker:** Para desarrollo únicamente
- **Bootstrap:** Framework CSS requerido

### 8.2 Implementación
- **NO:** Sistema de autenticación/usuarios
- **NO:** Roles o permisos
- **NO:** API REST externa
- **NO:** Microservicios
- **NO:** Containers en producción
- **NO:** Servidores web externos (nginx)

### 8.3 Entorno
- **Desarrollo:** Docker obligatorio
- **Producción:** Django standalone
- **Database:** PostgreSQL local obligatorio
- **Media:** Sistema de archivos local
- **Cache:** Sin sistema de cache externo

## 9. Estándares de Calidad

### 9.1 Testing
- **Unit tests:** Cobertura 85%+
- **Integration tests:** Flujos CRUD completos
- **UI tests:** Formularios y navegación
- **Performance tests:** Tiempo de respuesta
- **Security tests:** Validaciones y sanitización

### 9.2 Code Quality
- **Linting:** Ruff sin errores
- **Formatting:** Ruff format aplicado
- **Type hints:** En todas las funciones
- **Documentation:** README y docstrings actualizados
- **Dependencies:** Sin vulnerabilidades conocidas

### 9.3 Deployment
- **Migrations:** Aplicadas sin errores
- **Static files:** Servidos correctamente
- **Media files:** Upload y display funcionando
- **Database:** Conexión y operaciones exitosas
- **Health check:** Endpoint respondiendo correctamente