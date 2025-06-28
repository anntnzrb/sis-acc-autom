from django.urls import path
from .views import (
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView
)

app_name = 'productos'

urlpatterns = [
    path('', ProductoListView.as_view(), name='list'),
    path('agregar/', ProductoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', ProductoUpdateView.as_view(), name='update'),
    path('<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='delete'),
]