"""Configuración de la aplicación appEstudiantes."""
from django.apps import AppConfig


class AppEstudiantesConfig(AppConfig):
    """
    Configuración de la aplicación de Estudiantes.

    Esta clase define la configuración específica de la aplicación de Estudiantes,
    incluyendo el campo de clave primaria predeterminado y el nombre de la aplicación.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "appEstudiantes"
