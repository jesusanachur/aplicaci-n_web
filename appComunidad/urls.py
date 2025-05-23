"""
Configuración de URLs para la aplicación appComunidad.

Este módulo define las rutas URL para las vistas de la aplicación appComunidad,
incluyendo la página de inicio, acerca de, contacto y planes.
"""

from django.urls import path

from . import views

app_name = "appComunidad"

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca-de/", views.about, name="acerca_de"),
    path("contacto/", views.contacto, name="contacto"),
    path("planes/", views.planes, name="planes"),
    path("noticias/", views.noticias, name="noticias"),
    path("noticias/<int:pk>/", views.noticia_detalle, name="noticia_detalle"),
]
