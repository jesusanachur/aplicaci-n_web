"""
Configuración de la aplicación Comunidad.

Este módulo contiene la configuración específica para la aplicación Comunidad,
que maneja noticias, testimonios y planes de suscripción.
"""

from django.apps import AppConfig


class AppcomunidadConfig(AppConfig):
    """
    Configuración de la aplicación Comunidad.

    Esta clase contiene la configuración específica para la aplicación Comunidad.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "appComunidad"
