"""Formularios para la aplicación Comunidad."""
from typing import ClassVar

from django import forms

from .models import ContactoMensaje


class ContactoForm(forms.ModelForm):
    """Formulario para el envío de mensajes de contacto."""

    class Meta:
        """Metadatos para el formulario de contacto."""

        model: ClassVar = ContactoMensaje
        fields: ClassVar[list[str]] = ["nombre", "email", "asunto", "mensaje"]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "mensaje": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
