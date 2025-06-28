from django.urls import path
from .views import (
    ProveedorListView,
    ProveedorCreateView,
    ProveedorUpdateView,
    ProveedorDeleteView,
)

app_name = "proveedores"

urlpatterns = [
    path("", ProveedorListView.as_view(), name="list"),
    path("agregar/", ProveedorCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", ProveedorUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", ProveedorDeleteView.as_view(), name="delete"),
]
