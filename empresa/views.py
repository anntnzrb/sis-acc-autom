from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404
from .models import Empresa
from .forms import EmpresaForm


class EmpresaDetailView(DetailView):
    """Vista para mostrar la información de la empresa (singleton)."""
    model = Empresa
    template_name = 'empresa/detail.html'
    context_object_name = 'empresa'
    
    def get_object(self, queryset=None):
        """Obtiene la única instancia de empresa o None."""
        return Empresa.objects.get_empresa()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NOSOTROS'
        context['has_empresa'] = self.object is not None
        return context


class EmpresaCreateView(CreateView):
    """Vista para crear la información de la empresa."""
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('empresa:detail')
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar que no exista ya una empresa."""
        if Empresa.objects.exists():
            messages.warning(request, 'Ya existe información de la empresa registrada.')
            return redirect('empresa:detail')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'AGREGAR INFORMACIÓN DE LA EMPRESA'
        context['action'] = 'Crear'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'La información de {self.object.nombre} ha sido creada exitosamente.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrija los errores en el formulario.'
        )
        return super().form_invalid(form)


class EmpresaUpdateView(UpdateView):
    """Vista para editar la información de la empresa."""
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('empresa:detail')
    
    def get_object(self, queryset=None):
        """Obtiene la única instancia de empresa."""
        empresa = Empresa.objects.get_empresa()
        if not empresa:
            raise Http404("No existe información de la empresa.")
        return empresa
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'EDITAR INFORMACIÓN DE LA EMPRESA'
        context['action'] = 'Actualizar'
        context['empresa'] = self.object
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'La información de {self.object.nombre} ha sido actualizada exitosamente.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrija los errores en el formulario.'
        )
        return super().form_invalid(form)
