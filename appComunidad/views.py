"""
Vistas para la aplicación Comunidad.

Este módulo contiene las vistas que manejan las páginas principales
del sitio, incluyendo el inicio, acerca de, contacto, planes y noticias.
"""

from django import forms
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import ContactoForm
from .models import Noticia, Plan, Testimonio


def index(request: HttpRequest) -> HttpResponse:
    """
    Vista principal de la página de inicio.

    Args:
        request: La petición HTTP.

    Returns:
        HttpResponse: Respuesta HTTP con la plantilla renderizada.

    """
    planes = Plan.objects.all()[:3]  # Mostrar solo 3 planes en la página principal
    testimonios = Testimonio.objects.all()[:4]  # Mostrar solo 4 testimonios
    noticias_recientes = Noticia.objects.all().order_by("-fecha_publicacion")[:3]  # Últimas 3 noticias

    return render(request, "appComunidad/index.html", {
        "planes": planes,
        "testimonios": testimonios,
        "noticias_recientes": noticias_recientes,
    })


def about(request: HttpRequest) -> HttpResponse:
    """
    Vista de la página 'Acerca de'.

    Args:
        request: La petición HTTP.

    Returns:
        HttpResponse: Respuesta HTTP con la plantilla renderizada.

    """
    return render(request, "appComunidad/about.html")


def contacto(request: HttpRequest) -> HttpResponse:
    """
    Maneja el formulario de contacto.

    Args:
        request: La petición HTTP.

    Returns:
        HttpResponse: Respuesta HTTP con el formulario o redirección.

    """
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "¡Gracias por contactarnos! Te responderemos a la brevedad.",
            )
            return redirect("appComunidad:contacto")
    else:
        form = ContactoForm()

    return render(request, "appComunidad/contact.html", {"form": form})


def planes(request: HttpRequest) -> HttpResponse:
    """
    Muestra todos los planes disponibles.

    Args:
        request: La petición HTTP.

    Returns:
        HttpResponse: Respuesta HTTP con la lista de planes.

    """
    planes_list = Plan.objects.all()
    return render(request, "appComunidad/plans.html", {"planes": planes_list})


def noticias(request: HttpRequest) -> HttpResponse:
    """
    Muestra una lista paginada de noticias.

    Args:
        request: La petición HTTP.

    Returns:
        HttpResponse: Respuesta HTTP con la lista paginada de noticias.

    """
    todas_noticias = Noticia.objects.all()
    paginator = Paginator(todas_noticias, 9)  # 9 noticias por página
    page = request.GET.get("page")

    try:
        noticias_paginadas = paginator.page(page)
    except PageNotAnInteger:
        noticias_paginadas = paginator.page(1)
    except EmptyPage:
        noticias_paginadas = paginator.page(paginator.num_pages)

    return render(request, "appComunidad/noticias.html", {
        "noticias": noticias_paginadas,
    })


def noticia_detalle(
    request: HttpRequest,
    pk: int,
) -> HttpResponse:
    """
    Muestra el detalle de una noticia.

    Args:
        request: La petición HTTP.
        pk: ID de la noticia.

    Returns:
        HttpResponse: Respuesta HTTP con el detalle de la noticia.

    """
    noticia = get_object_or_404(Noticia, pk=pk)
    # Obtener 3 noticias recientes excluyendo la actual
    noticias_relacionadas = Noticia.objects.exclude(
        pk=pk,
    ).order_by("-fecha_publicacion")[:3]

    return render(request, "appComunidad/noticia_detalle.html", {
        "noticia": noticia,
        "noticias_relacionadas": noticias_relacionadas,
    })


class CustomLoginView(LoginView):
    """
    Vista personalizada para el inicio de sesión.

    Redirige a los usuarios según su tipo después del inicio de sesión.
    """

    template_name = "login.html"

    def get_success_url(self) -> str:
        """
        Redirige al usuario según su tipo después del inicio de sesión.

        Returns:
            str: URL de redirección.

        """
        if hasattr(self.request.user, "perfil_estudiante"):
            return str(reverse_lazy("appEstudiantes:dashboard"))
        if hasattr(self.request.user, "perfil_profesor"):
            return str(reverse_lazy("appProfesores:dashboard"))
        return str(super().get_success_url())

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """
        Inicia sesión al usuario si el formulario es válido.

        Args:
            form: Formulario de autenticación.

        Returns:
            HttpResponse: Redirección a la URL de éxito.

        """
        # Autenticar al usuario
        auth_login(self.request, form.get_user())

        # Mensaje de bienvenida personalizado
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"¡Bienvenido de nuevo, {username}!")

        # Redirigir según el tipo de usuario
        if hasattr(self.request.user, "perfil_estudiante"):
            return HttpResponseRedirect(reverse_lazy("appEstudiantes:dashboard"))
        if hasattr(self.request.user, "perfil_profesor"):
            return HttpResponseRedirect(reverse_lazy("appProfesores:dashboard"))

        return super().form_valid(form)
