"""Formularios para la aplicación de Estudiantes."""
from typing import Any, ClassVar

from django import forms

from .models import Comentario, PerfilEstudiante, ProgresoLeccion


class PerfilEstudianteForm(forms.ModelForm):
    """Formulario para crear o actualizar el perfil de un estudiante."""

    class Meta:
        """Metadatos para el formulario de PerfilEstudiante."""

        model = PerfilEstudiante
        fields: ClassVar[list[str]] = ["foto", "biografia", "idioma_nativo"]
        widgets: ClassVar[dict[str, Any]] = {
            "biografia": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "idioma_nativo": forms.TextInput(attrs={"class": "form-control"}),
            "foto": forms.FileInput(attrs={"class": "d-none", "accept": "image/*"}),
        }


class ComentarioForm(forms.ModelForm):
    """Formulario para crear o actualizar un comentario."""

    class Meta:
        """Metadatos para el formulario de Comentario."""

        model = Comentario
        fields: ClassVar[list[str]] = ["contenido"]
        widgets: ClassVar[dict[str, Any]] = {
            "contenido": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe tu comentario aquí...",
            }),
        }


class NotaPersonalForm(forms.ModelForm):
    """Formulario para que los estudiantes agreguen notas personales."""

    class Meta:
        """Metadatos para el formulario de NotaPersonal."""

        model = ProgresoLeccion
        fields: ClassVar[list[str]] = ["notas"]
        widgets: ClassVar[dict[str, Any]] = {
            "notas": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe tus notas personales aquí...",
            }),
        }
