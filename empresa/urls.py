from django.urls import path
from .views import EmpresaDetailView, EmpresaCreateView, EmpresaUpdateView

app_name = "empresa"

urlpatterns = [
    path("", EmpresaDetailView.as_view(), name="detail"),
    path("agregar/", EmpresaCreateView.as_view(), name="create"),
    path("editar/", EmpresaUpdateView.as_view(), name="update"),
]
