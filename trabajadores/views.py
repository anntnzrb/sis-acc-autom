from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Trabajador
from .forms import TrabajadorForm


class TrabajadorListView(ListView):
    """Vista para listar todos los trabajadores."""

    model = Trabajador
    template_name = "trabajadores/list.html"
    context_object_name = "trabajadores"
    paginate_by = 12  # 2 columnas x 6 filas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "NUESTRO PERSONAL"
        context["total_trabajadores"] = Trabajador.objects.count()
        return context


class TrabajadorCreateView(CreateView):
    """Vista para crear un nuevo trabajador."""

    model = Trabajador
    form_class = TrabajadorForm
    template_name = "trabajadores/form.html"
    success_url = reverse_lazy("trabajadores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "AGREGAR TRABAJADOR"
        context["action"] = "Crear"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"El trabajador {self.object.get_nombre_completo()} ha sido creado exitosamente.",
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)


class TrabajadorUpdateView(UpdateView):
    """Vista para editar un trabajador existente."""

    model = Trabajador
    form_class = TrabajadorForm
    template_name = "trabajadores/form.html"
    success_url = reverse_lazy("trabajadores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "EDITAR TRABAJADOR"
        context["action"] = "Actualizar"
        context["trabajador"] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"El trabajador {self.object.get_nombre_completo()} ha sido actualizado exitosamente.",
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)


class TrabajadorDeleteView(DeleteView):
    """Vista para eliminar un trabajador."""

    model = Trabajador
    template_name = "trabajadores/confirm_delete.html"
    success_url = reverse_lazy("trabajadores:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ELIMINAR TRABAJADOR"
        context["trabajador"] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre_completo = self.object.get_nombre_completo()
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request, f"El trabajador {nombre_completo} ha sido eliminado exitosamente."
        )
        return response
