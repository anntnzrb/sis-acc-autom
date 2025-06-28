from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm


class ProductoListView(ListView):
    """Vista para listar todos los productos."""
    model = Producto
    template_name = 'productos/list.html'
    context_object_name = 'productos'
    paginate_by = 15  # 3 columnas x 5 filas
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NUESTROS PRODUCTOS'
        context['total_productos'] = Producto.objects.count()
        return context


class ProductoCreateView(CreateView):
    """Vista para crear un nuevo producto."""
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('productos:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AGREGAR PRODUCTO'
        context['action'] = 'Crear'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'El producto "{self.object.nombre}" ha sido creado exitosamente.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


class ProductoUpdateView(UpdateView):
    """Vista para editar un producto existente."""
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/form.html'
    success_url = reverse_lazy('productos:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EDITAR PRODUCTO'
        context['action'] = 'Actualizar'
        context['producto'] = self.object
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'El producto "{self.object.nombre}" ha sido actualizado exitosamente.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


class ProductoDeleteView(DeleteView):
    """Vista para eliminar un producto."""
    model = Producto
    template_name = 'productos/confirm_delete.html'
    success_url = reverse_lazy('productos:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ELIMINAR PRODUCTO'
        context['producto'] = self.object
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.nombre
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            f'El producto "{nombre}" ha sido eliminado exitosamente.'
        )
        return response
