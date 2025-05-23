"""
Configuración de URLs para la aplicación appEstudiantes.

Este módulo define las rutas URL para las vistas de la aplicación appEstudiantes,
incluyendo el dashboard, perfil, cursos, lecciones y materiales.
"""

from django.urls import path

from . import views

app_name = "appEstudiantes"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),
    path("cursos/", views.CursoListView.as_view(), name="cursos"),
    path("cursos/<int:pk>/", views.curso_detalle, name="curso_detalle"),
    path("cursos/<int:curso_pk>/leccion/<int:leccion_pk>/", views.leccion_detalle, name="leccion_detalle"),
    path("leccion/<int:leccion_pk>/completar/", views.marcar_leccion_completada, name="completar_leccion"),
    path("material/<int:material_pk>/descargar/", views.descargar_material, name="descargar_material"),
    path("mis-cursos/", views.mis_cursos, name="mis_cursos"),
    path("leccion/<int:leccion_pk>/guardar-notas/", views.guardar_notas, name="guardar_notas"),
    path("progreso/", views.progreso, name="progreso"),
]
