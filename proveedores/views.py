from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Proveedor
from .forms import ProveedorForm


class ProveedorListView(ListView):
    """Vista para listar todos los proveedores."""

    model = Proveedor
    template_name = "proveedores/list.html"
    context_object_name = "proveedores"
    paginate_by = 15  # 3 columnas x 5 filas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "NUESTROS PROVEEDORES"
        context["total_proveedores"] = Proveedor.objects.count()
        return context


class ProveedorCreateView(CreateView):
    """Vista para crear un nuevo proveedor."""

    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/form.html"
    success_url = reverse_lazy("proveedores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "AGREGAR PROVEEDOR"
        context["action"] = "Crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'El proveedor "{self.object.nombre}" ha sido creado exitosamente.',
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)


class ProveedorUpdateView(UpdateView):
    """Vista para editar un proveedor existente."""

    model = Proveedor
    form_class = ProveedorForm
    template_name = "proveedores/form.html"
    success_url = reverse_lazy("proveedores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EDITAR PROVEEDOR"
        context["action"] = "Actualizar"
        context["proveedor"] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'El proveedor "{self.object.nombre}" ha sido actualizado exitosamente.',
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)


class ProveedorDeleteView(DeleteView):
    """Vista para eliminar un proveedor."""

    model = Proveedor
    template_name = "proveedores/confirm_delete.html"
    success_url = reverse_lazy("proveedores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ELIMINAR PROVEEDOR"
        context["proveedor"] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.nombre
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request, f'El proveedor "{nombre}" ha sido eliminado exitosamente.'
        )
        return response
