"""
Configuración de la aplicación Profesores.

Este módulo contiene la configuración específica para la aplicación Profesores,
que maneja la gestión de cursos, lecciones, materiales y evaluaciones.
"""

from django.apps import AppConfig


class AppprofesoresConfig(AppConfig):
    """
    Configuración de la aplicación Profesores.

    Esta clase contiene la configuración específica para la aplicación Profesores.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "appProfesores"
