from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Vista para la página principal estática."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "CarriAcces - Accesorios para Automóviles"
        context["page"] = "home"
        return context


def handler404(request, exception):
    """Manejador personalizado para error 404."""
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """Manejador personalizado para error 500."""
    return render(request, "errors/500.html", status=500)
