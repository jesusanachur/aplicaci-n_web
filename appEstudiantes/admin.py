"""Configuración del administrador para la aplicación de Estudiantes."""
from typing import ClassVar

from django.contrib import admin

from .models import (
    Comentario,
    Inscripcion,
    MaterialDescargado,
    PerfilEstudiante,
    ProgresoLeccion,
)


@admin.register(PerfilEstudiante)
class PerfilEstudianteAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo PerfilEstudiante."""

    list_display: ClassVar[list[str]] = ["usuario", "plan", "fecha_inscripcion", "idioma_nativo"]
    search_fields: ClassVar[list[str]] = [
        "usuario__username",
        "usuario__email",
        "usuario__first_name",
        "usuario__last_name",
    ]
    list_filter: ClassVar[list[str]] = ["plan", "fecha_inscripcion"]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Inscripcion."""

    list_display: ClassVar[list[str]] = ["estudiante", "curso", "fecha_inscripcion", "completado"]
    search_fields: ClassVar[list[str]] = ["estudiante__username", "curso__titulo"]
    list_filter: ClassVar[list[str]] = ["completado", "fecha_inscripcion"]


@admin.register(ProgresoLeccion)
class ProgresoLeccionAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo ProgresoLeccion."""

    list_display: ClassVar[list[str]] = [
        "estudiante",
        "leccion",
        "completado",
        "fecha_inicio",
        "fecha_completado",
    ]
    search_fields: ClassVar[list[str]] = ["estudiante__username", "leccion__titulo"]
    list_filter: ClassVar[list[str]] = ["completado", "fecha_inicio", "fecha_completado"]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Comentario."""

    list_display: ClassVar[list[str]] = ["estudiante", "leccion", "fecha"]
    search_fields: ClassVar[list[str]] = ["estudiante__username", "leccion__titulo", "contenido"]
    list_filter: ClassVar[list[str]] = ["fecha"]


@admin.register(MaterialDescargado)
class MaterialDescargadoAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo MaterialDescargado."""

    list_display: ClassVar[list[str]] = ["estudiante", "material", "fecha_descarga"]
    search_fields: ClassVar[list[str]] = ["estudiante__username", "material__titulo"]
    list_filter: ClassVar[list[str]] = ["fecha_descarga"]
