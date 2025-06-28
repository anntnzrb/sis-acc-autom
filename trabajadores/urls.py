from django.urls import path
from .views import (
    TrabajadorListView,
    TrabajadorCreateView,
    TrabajadorUpdateView,
    TrabajadorDeleteView,
)

app_name = "trabajadores"

urlpatterns = [
    path("", TrabajadorListView.as_view(), name="list"),
    path("agregar/", TrabajadorCreateView.as_view(), name="create"),
    path("<int:pk>/editar/", TrabajadorUpdateView.as_view(), name="update"),
    path("<int:pk>/eliminar/", TrabajadorDeleteView.as_view(), name="delete"),
]
