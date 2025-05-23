"""
Formularios para la aplicación de Profesores.

Este módulo contiene todos los formularios necesarios para la gestión de perfiles de profesores,
cursos, lecciones, materiales y evaluaciones en la plataforma educativa.
"""
from typing import Any, ClassVar, TypeVar

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import BaseModelForm, ModelForm

from .models import Curso, Leccion, Material

# Type variable para formularios
ModelFormT = TypeVar("ModelFormT", bound=BaseModelForm)


class PerfilProfesorForm(UserChangeForm):
    """Formulario para la gestión del perfil del profesor."""

    password = None

    class Meta:
        """Metadatos para el formulario de perfil de profesor."""

        model: ClassVar[type[User]] = User
        fields: ClassVar[list[str]] = ["first_name", "last_name", "email"]
        labels: ClassVar[dict[str, str]] = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo Electrónico",
        }
        widgets: ClassVar[dict[str, Any]] = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class CursoForm(ModelForm):
    """Formulario para la creación y edición de cursos."""

    class Meta:
        """Metadatos para el formulario de curso."""

        model: ClassVar[type[Curso]] = Curso
        fields: ClassVar[list[str]] = ["titulo", "descripcion", "nivel_plan", "imagen", "activo"]
        widgets: ClassVar[dict[str, Any]] = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "nivel_plan": forms.Select(attrs={"class": "form-select"}),
            "imagen": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class LeccionForm(ModelForm):
    """Formulario para la creación y edición de lecciones."""

    class Meta:
        """Metadatos para el formulario de lección."""

        model: ClassVar[type[Leccion]] = Leccion
        fields: ClassVar[list[str]] = ["titulo", "descripcion", "contenido", "numero_orden", "duracion_minutos"]
        widgets: ClassVar[dict[str, Any]] = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "contenido": forms.Textarea(attrs={"rows": 10, "class": "form-control"}),
            "numero_orden": forms.NumberInput(attrs={"class": "form-control"}),
            "duracion_minutos": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """
        Inicializa el formulario de lección.

        Args:
            *args: Argumentos posicionales variables.
            **kwargs: Argumentos de palabra clave variables. Puede contener 'user' que será eliminado.

        """
        kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

class MaterialForm(ModelForm):
    """Formulario para la carga y edición de materiales."""

    class Meta:
        """Metadatos para el formulario de material."""

        model: ClassVar[type[Material]] = Material
        fields: ClassVar[list[str]] = ["titulo", "descripcion", "tipo", "archivo"]
        widgets: ClassVar[dict[str, Any]] = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
        }
