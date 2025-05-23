"""
Vistas principales de la aplicación comunidad_educativa.

Este módulo contiene las vistas para el registro de usuarios, incluyendo
estudiantes y profesores, así como la lógica de autenticación relacionada.
"""

# Standard library imports
import logging
from typing import Any, ClassVar

# Third-party imports
# (Ninguna en este momento)
# Django imports
from django import forms
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Local application imports
from appEstudiantes.models import PerfilEstudiante
from appProfesores.models import PerfilProfesor

# Configure logger
logger = logging.getLogger(__name__)

# Constants
DEFAULT_ESPECIALIDAD = "General"

# Type aliases
HttpResponseOrRedirect = HttpResponse | HttpResponseRedirect


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creaciÃ³n de usuarios.

    Extiende UserCreationForm para incluir campos adicionales como
    email, nombre y apellido.
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Apellido")

    class Meta:
        """Metadatos para el formulario de creaciÃ³n de usuarios."""

        model = User
        fields: ClassVar[list[str]] = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets: ClassVar[dict[str, Any]] = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Inicializa el formulario con clases de Bootstrap."""
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Muestra la pÃ¡gina de selecciÃ³n de tipo de registro.

    Si el usuario ya estÃ¡ autenticado, lo redirige al dashboard correspondiente.

    Args:
        request: La solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza la plantilla de selecciÃ³n de registro.

    """
    if request.user.is_authenticated:
        if hasattr(request.user, "perfil_profesor"):
            return redirect("appProfesores:dashboard")
        return redirect("appEstudiantes:dashboard")

    return render(
        request=request,
        template_name="register_choice.html",
        context={"title": "SelecciÃ³n de Registro"},
    )


def register_student_view(request: HttpRequest) -> HttpResponseOrRedirect:
    """
    Maneja el registro de nuevos estudiantes.

    Args:
        request: La solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza el formulario de registro de estudiante.
        HttpResponseRedirect: Redirige al login despuÃ©s de un registro exitoso.

    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    PerfilEstudiante.objects.create(usuario=user)
                    messages.success(
                        request,
                        "Â¡Cuenta de estudiante creada exitosamente! "
                        "Ya puedes iniciar sesiÃ³n.",
                    )
                    return redirect("login")
            except (IntegrityError, ValidationError):
                messages.error(
                    request,
                    "Error al crear la cuenta de estudiante. Por favor verifica los datos e intÃ©ntalo de nuevo.",
                )
                logger.exception("Error al crear cuenta de estudiante")
        else:
            messages.error(
                request,
                "Por favor corrija los errores en el formulario.",
            )
    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "register_student.html",
        {
            "form": form,
            "title": "Registro de Estudiante",
        },
    )


def register_teacher_view(request: HttpRequest) -> HttpResponseOrRedirect:
    """
    Maneja el registro de nuevos profesores.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza el formulario de registro de profesor.
        HttpResponseRedirect: Redirige al dashboard del profesor despuÃ©s de un registro exitoso.

    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    PerfilProfesor.objects.create(
                        usuario=user,
                        biografia="",
                        especialidad="General",
                    )
                    # Autenticar al usuario automÃ¡ticamente despuÃ©s del registro
                    auth_login(request, user)
                    messages.success(
                        request,
                        "Â¡Cuenta de profesor creada exitosamente! "
                        "Bienvenido a tu panel de control.",
                    )
                    return redirect("appProfesores:dashboard")
            except (IntegrityError, ValidationError):
                messages.error(
                    request,
                    "Error al crear la cuenta de profesor. Por favor verifica los datos e intÃ©ntalo de nuevo.",
                )
                logger.exception("Error al crear cuenta de profesor")
        else:
            messages.error(
                request,
                "Por favor corrija los errores en el formulario.",
            )
    else:
        form = CustomUserCreationForm()

    return render(
        request,
        "register_teacher.html",
        {
            "form": form,
            "title": "Registro de Profesor",
        },
    )


class CustomLoginView(LoginView):
    """Vista personalizada para el inicio de sesiÃ³n."""

    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        """Redirige al dashboard correspondiente despuÃ©s del inicio de sesiÃ³n."""
        if hasattr(self.request.user, "perfil_profesor"):
            return reverse_lazy("appProfesores:dashboard")
        return reverse_lazy("appEstudiantes:dashboard")

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        """Maneja los errores de inicio de sesiÃ³n."""
        messages.error(
            self.request,
            "Usuario o contraseÃ±a incorrectos. Por favor, intente de nuevo.",
        )
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Vista personalizada para el cierre de sesiÃ³n."""

    next_page = reverse_lazy("login")

    def dispatch(self, request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        """Muestra un mensaje al cerrar sesiÃ³n."""
        if request.user.is_authenticated:
            messages.info(request, "Has cerrado sesiÃ³n exitosamente.")
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Vista para el perfil del usuario."""

    template_name = "profile.html"

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """Obtiene los datos del perfil del usuario."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, "perfil_profesor"):
            context["profile"] = user.perfil_profesor
            context["user_type"] = "profesor"
        elif hasattr(user, "perfil_estudiante"):
            context["profile"] = user.perfil_estudiante
            context["user_type"] = "estudiante"

        context["title"] = f"Perfil de {user.get_full_name()}"
        return context


def handler404(request: HttpRequest, _exception: Exception) -> HttpResponse:
    """Maneja errores 404."""
    return render(
        request,
        "404.html",
        status=404,
        context={"title": "PÃ¡gina no encontrada"},
    )


def handler500(request: HttpRequest) -> HttpResponse:
    """Maneja errores 500."""
    return render(
        request=request,
        template_name="500.html",
        status=500,
        context={"title": "Error del servidor"},
    )


def home_view(request: HttpRequest) -> HttpResponse:
    """Vista principal del sitio."""
    if request.user.is_authenticated:
        if hasattr(request.user, "perfil_profesor"):
            return redirect("appProfesores:dashboard")
        return redirect("appEstudiantes:dashboard")
    return render(request, "home.html", {"title": "Inicio"})
