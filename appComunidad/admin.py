"""Configuración del panel de administración para la aplicación Comunidad."""

from typing import ClassVar

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import ContactoMensaje, Noticia, Plan, Testimonio


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Plan."""

    list_display: ClassVar[tuple[str, ...]] = ("nombre", "nivel", "precio", "duracion_meses")
    search_fields: ClassVar[list[str]] = ["nombre", "descripcion"]
    list_filter: ClassVar[list[str]] = ["nivel"]


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Noticia."""

    list_display: ClassVar[tuple[str, ...]] = ("titulo", "fecha_publicacion")
    search_fields: ClassVar[list[str]] = ["titulo", "contenido"]
    list_filter: ClassVar[list[str]] = ["fecha_publicacion"]
    date_hierarchy: ClassVar[str] = "fecha_publicacion"


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Testimonio."""

    list_display: ClassVar[tuple[str, ...]] = ("nombre", "rol", "fecha")
    search_fields: ClassVar[list[str]] = ["nombre", "rol", "contenido"]
    list_filter: ClassVar[list[str]] = ["fecha"]
    date_hierarchy: ClassVar[str] = "fecha"


@admin.register(ContactoMensaje)
class ContactoMensajeAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo ContactoMensaje."""

    list_display: ClassVar[tuple[str, ...]] = ("asunto", "email", "fecha", "leido")
    list_filter: ClassVar[list[str]] = ["leido", "fecha"]
    search_fields: ClassVar[list[str]] = ["nombre", "email", "asunto", "mensaje"]
    date_hierarchy: ClassVar[str] = "fecha"
    readonly_fields: ClassVar[list[str]] = ["fecha"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """
        Obtiene el queryset de mensajes.

        Args:
            request: La petición HTTP.

        Returns:
            QuerySet: El queryset de mensajes.

        """
        return super().get_queryset(request).select_related()
