"""
Configuración de URLs para la aplicación appProfesores.

Este módulo define las rutas URL para las vistas de la aplicación appProfesores,
incluyendo el dashboard, perfil, gestión de cursos, lecciones, materiales y evaluaciones.
"""

from django.urls import path

from appProfesores import views

app_name = "appProfesores"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),
    path("cursos/", views.CursoListView.as_view(), name="cursos"),
    path("cursos/nuevo/", views.CursoCreateView.as_view(), name="crear_curso"),
    path("cursos/<int:pk>/", views.curso_detalle, name="curso_detalle"),
    path("cursos/<int:pk>/editar/", views.CursoUpdateView.as_view(), name="editar_curso"),
    path("cursos/<int:pk>/eliminar/", views.CursoDeleteView.as_view(), name="eliminar_curso"),
    path("cursos/<int:curso_pk>/leccion/nueva/", views.LeccionCreateView.as_view(), name="crear_leccion"),
    path("leccion/<int:pk>/editar/", views.LeccionUpdateView.as_view(), name="editar_leccion"),
    path("leccion/<int:leccion_pk>/material/nuevo/", views.agregar_material, name="agregar_material"),
    path("material/<int:material_pk>/eliminar/", views.eliminar_material, name="eliminar_material"),
    path("cursos/<int:curso_pk>/estudiantes/", views.estudiantes_curso, name="estudiantes_curso"),
    path("cursos/<int:pk>/toggle-active/", views.toggle_curso_activo, name="toggle_curso_activo"),
]
