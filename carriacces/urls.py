"""
URL configuration for carriacces project.
CarriAcces - Sistema de gestión para tienda de accesorios automotrices.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView

urlpatterns = [
    # Página principal
    path("", HomeView.as_view(), name="home"),
    # Administración
    path("admin/", admin.site.urls),
    # Apps principales
    path("nosotros/", include("empresa.urls")),
    path("trabajadores/", include("trabajadores.urls")),
    path("productos/", include("productos.urls")),
    path("proveedores/", include("proveedores.urls")),
]

# Configuración para servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Manejadores de errores personalizados
handler404 = "carriacces.views.handler404"
handler500 = "carriacces.views.handler500"
