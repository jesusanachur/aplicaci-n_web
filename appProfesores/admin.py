"""
Admin configuration for the appProfesores app.

This module contains the admin interface configurations for all models
in the appProfesores application.
"""

from typing import ClassVar

from django.contrib import admin
from django.db.models import Model

from .models import (
    Curso,
    Evaluacion,
    Leccion,
    Material,
    Opcion,
    PerfilProfesor,
    Pregunta,
)


@admin.register(PerfilProfesor)
class PerfilProfesorAdmin(admin.ModelAdmin):
    """Admin interface for the PerfilProfesor model."""

    list_display: ClassVar[list[str]] = ["usuario", "especialidad", "anos_experiencia", "titulo_academico"]
    search_fields: ClassVar[list[str]] = ["usuario__username", "usuario__email", "especialidad"]

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin interface for the Curso model."""

    list_display: ClassVar[list[str]] = ["titulo", "profesor", "nivel_plan", "fecha_creacion", "activo"]
    list_filter: ClassVar[list[str]] = ["nivel_plan", "activo", "fecha_creacion"]
    search_fields: ClassVar[list[str]] = ["titulo", "descripcion", "profesor__username"]
    date_hierarchy: ClassVar[str] = "fecha_creacion"

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    """Admin interface for the Leccion model."""

    list_display: ClassVar[list[str]] = ["titulo", "curso", "numero_orden", "duracion_minutos"]
    list_filter: ClassVar[list[str]] = ["curso", "fecha_creacion"]
    search_fields: ClassVar[list[str]] = ["titulo", "descripcion", "contenido"]
    ordering: ClassVar[list[str]] = ["curso", "numero_orden"]

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """Admin interface for the Material model."""

    list_display: ClassVar[list[str]] = ["titulo", "leccion", "tipo", "fecha_subida"]
    list_filter: ClassVar[list[str]] = ["tipo", "fecha_subida"]
    search_fields: ClassVar[list[str]] = ["titulo", "descripcion"]

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    """Admin interface for the Evaluacion model."""

    list_display: ClassVar[list[str]] = ["titulo", "leccion", "puntaje_maximo", "fecha_creacion"]
    list_filter: ClassVar[list[str]] = ["fecha_creacion"]
    search_fields: ClassVar[list[str]] = ["titulo", "descripcion"]

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    """Admin interface for the Pregunta model."""

    # Constants
    MAX_ENUNCIADO_LENGTH: ClassVar[int] = 50
    list_display: ClassVar[list[str]] = ["get_short_enunciado", "evaluacion", "tipo", "puntaje"]
    list_filter: ClassVar[list[str]] = ["tipo", "evaluacion"]
    search_fields: ClassVar[list[str]] = ["enunciado"]

    def get_short_enunciado(self, obj: Model) -> str:
        """
        Return a shortened version of the question text for display.

        Args:
            obj: The Pregunta instance.

        Returns:
            str: The shortened question text with "..." if it exceeds MAX_ENUNCIADO_LENGTH.

        """
        if len(obj.enunciado) > self.MAX_ENUNCIADO_LENGTH:
            return f"{obj.enunciado[:self.MAX_ENUNCIADO_LENGTH]}..."
        return obj.enunciado
    get_short_enunciado.short_description = "Enunciado"

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    """Admin interface for the Opcion model."""

    list_display: ClassVar[list[str]] = ["texto", "pregunta", "es_correcta"]
    list_filter: ClassVar[list[str]] = ["es_correcta"]
    search_fields: ClassVar[list[str]] = ["texto"]
