"""
Vistas para la aplicación de Estudiantes.

Este módulo contiene todas las vistas necesarias para la funcionalidad del estudiante,
incluyendo el dashboard, gestión de cursos, lecciones y progreso.
"""

from __future__ import annotations

# Standard library imports
from typing import Any, TypeVar

# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView

# Local application imports
from appProfesores.models import Curso, Leccion, Material

from .forms import ComentarioForm, NotaPersonalForm, PerfilEstudianteForm
from .models import Comentario, Inscripcion, MaterialDescargado, PerfilEstudiante, ProgresoLeccion

# Type variables for generic types
T = TypeVar("T")
ModelFormT = TypeVar("ModelFormT", bound=BaseModelForm)

# Type aliases
HttpResponseOrRedirect = HttpResponse | HttpResponseRedirect


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Vista del panel de control del estudiante.

    Muestra los cursos en los que está inscrito el estudiante y su progreso general.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla del dashboard con el contexto.

    """
    # Obtener cursos inscritos
    inscripciones: QuerySet[Inscripcion] = Inscripcion.objects.filter(
        estudiante=request.user,
    ).select_related("curso")

    # Obtener estadísticas de progreso
    progreso_lecciones: int = ProgresoLeccion.objects.filter(
        estudiante=request.user,
        completado=True,
    ).count()

    # Calcular porcentaje general de progreso
    total_lecciones: int = ProgresoLeccion.objects.filter(
        estudiante=request.user,
    ).count()

    porcentaje_progreso: float = 0.0
    if total_lecciones > 0:
        porcentaje_progreso = (progreso_lecciones / total_lecciones) * 100

    context: dict[str, Any] = {
        "inscripciones": inscripciones,
        "progreso_lecciones": progreso_lecciones,
        "porcentaje_progreso": round(porcentaje_progreso, 2),
    }
    return render(request, "appEstudiantes/dashboard.html", context)

@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    """
    Vista para ver y editar el perfil del estudiante.

    Permite al estudiante ver y actualizar su información de perfil.
    Si el perfil no existe, se crea uno nuevo automáticamente.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla de perfil con el formulario.

    """
    # Obtener o crear el perfil del estudiante
    perfil_estudiante, created = PerfilEstudiante.objects.get_or_create(
        usuario=request.user,
        defaults={
            "biografia": "",
            "idioma_nativo": "",
        },
    )

    if request.method == "POST":
        form = PerfilEstudianteForm(
            data=request.POST,
            files=request.FILES,
            instance=perfil_estudiante,
        )
        
        # Check if this is an AJAX request (for photo upload)
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        
        if form.is_valid():
            try:
                perfil_actualizado = form.save(commit=False)
                perfil_actualizado.usuario = request.user
                
                # Handle file upload
                if "foto" in request.FILES:
                    # Delete old photo if it's not the default one
                    if perfil_estudiante.foto and perfil_estudiante.foto.name != "default_profile.png":
                        perfil_estudiante.foto.delete(save=False)
                
                perfil_actualizado.save()
                
                messages.success(
                    request,
                    "Tu perfil ha sido actualizado correctamente.",
                    extra_tags="success",
                )
                
                if is_ajax:
                    return JsonResponse({
                        "success": True,
                        "message": "Foto de perfil actualizada correctamente.",
                        "foto_url": perfil_actualizado.foto.url if perfil_actualizado.foto else "",
                    })
                    
                return redirect("appEstudiantes:perfil")
                
            except Exception as e:
                error_msg = f"Error al actualizar el perfil: {e!s}"
                messages.error(request, error_msg, extra_tags="danger")
                if is_ajax:
                    return JsonResponse({"success": False, "message": error_msg}, status=400)
        else:
            error_msg = "Por favor, corrige los errores en el formulario."
            if is_ajax:
                return JsonResponse({
                    "success": False,
                    "message": error_msg,
                    "errors": form.errors,
                }, status=400)
            messages.error(request, error_msg, extra_tags="danger")
    else:
        form = PerfilEstudianteForm(instance=perfil_estudiante)

    context: dict[str, Any] = {
        "form": form,
        "perfil": perfil_estudiante,
    }
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": False,
            "message": "Método no permitido o error en la solicitud.",
        }, status=400)

    return render(
        request,
        "appEstudiantes/profile.html",
        context,
    )

class CursoListView(LoginRequiredMixin, ListView):
    """Vista para listar los cursos disponibles para los estudiantes."""

    model = Curso
    template_name: str = "appEstudiantes/cursos.html"
    context_object_name: str = "cursos"
    paginate_by: int = 9

    def get_queryset(self) -> QuerySet[Curso]:
        """
        Obtiene el queryset de cursos filtrados según los parámetros de búsqueda.

        Returns:
            QuerySet[Curso]: QuerySet de cursos filtrados.

        """
        queryset = super().get_queryset().filter(activo=True)

        # Filtrar por búsqueda
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(descripcion__icontains=query),
            )

        # Ordenar
        orden = self.request.GET.get("orden", "recientes")
        if orden == "antiguos":
            queryset = queryset.order_by("fecha_creacion")
        elif orden == "a-z":
            queryset = queryset.order_by("titulo")
        elif orden == "z-a":
            queryset = queryset.order_by("-titulo")
        else:  # recientes por defecto
            queryset = queryset.order_by("-fecha_creacion")

        return queryset.select_related("profesor", "nivel_plan")

    def get_context_data(self, **kwargs: object) -> dict[str, Any]:
        """
        Añade datos adicionales al contexto de la vista.

        Args:
            **kwargs: Argumentos variables del contexto.

        Returns:
            Dict[str, Any]: Contexto actualizado con información adicional.

        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["categoria_actual"] = self.request.GET.get("categoria", "")
        context["orden_actual"] = self.request.GET.get("orden", "fecha_creacion")

        # No hay categorías disponibles por el momento
        context["categorias"] = []

        return context

@login_required
def curso_detalle(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Muestra los detalles de un curso y permite la inscripción.

    Args:
        request: La solicitud HTTP.
        pk: ID del curso a mostrar.

    Returns:
        HttpResponse: Renderiza la plantilla de detalle del curso.

    """
    # Obtener el curso
    curso: Curso = get_object_or_404(Curso, pk=pk, activo=True)

    # Verificar si el usuario ya está inscrito
    esta_inscrito: bool = Inscripcion.objects.filter(
        estudiante=request.user,
        curso=curso,
    ).exists()

    # Obtener información adicional del curso
    lecciones: QuerySet[Leccion] = Leccion.objects.filter(
        curso=curso,
    ).order_by("numero_orden")

    # Manejar la inscripción al curso
    if request.method == "POST" and "inscribirse" in request.POST:
        # Verificar si el usuario ya está inscrito
        if not esta_inscrito:
            # Crear la inscripción
            Inscripcion.objects.create(
                estudiante=request.user,
                curso=curso,
                fecha_inscripcion=timezone.now(),
            )
            messages.success(
                request,
                f"¡Te has inscrito correctamente al curso {curso.titulo}!",
            )
            return redirect("appEstudiantes:curso_detalle", pk=pk)

        messages.warning(request, "Ya estás inscrito en este curso.")
        return redirect("appEstudiantes:curso_detalle", pk=pk)

    # Obtener comentarios del curso (filtrando por lecciones del curso)
    comentarios: QuerySet[Comentario] = Comentario.objects.filter(
        leccion__curso=curso,
    ).select_related("estudiante", "leccion")

    # Calcular progreso del curso si el usuario está inscrito
    total_lecciones = lecciones.count()
    lecciones_completadas = 0
    porcentaje_completado = 0
    
    if esta_inscrito and total_lecciones > 0:
        lecciones_completadas = ProgresoLeccion.objects.filter(
            estudiante=request.user,
            leccion__curso=curso,
            completado=True,
        ).count()
        porcentaje_completado = (lecciones_completadas / total_lecciones) * 100

    # Formulario para comentarios
    form_comentario = ComentarioForm()

    context: dict[str, Any] = {
        "curso": curso,
        "esta_inscrito": esta_inscrito,
        "lecciones": lecciones,
        "comentarios": comentarios,
        "form_comentario": form_comentario,
        "total_lecciones": total_lecciones,
        "lecciones_completadas": lecciones_completadas,
        "porcentaje_completado": round(porcentaje_completado, 2),
    }
    return render(request, "appEstudiantes/curso_detalle.html", context)

@login_required
def leccion_detalle(
    request: HttpRequest,
    curso_pk: int,
    leccion_pk: int,
) -> HttpResponse:
    """
    Muestra los detalles de una lección y permite interactuar con ella.

    Args:
        request: La solicitud HTTP.
        curso_pk: ID del curso al que pertenece la lección.
        leccion_pk: ID de la lección a mostrar.

    Returns:
        HttpResponse: Renderiza la plantilla de detalle de la lección.

    Raises:
        Http404: Si el curso o la lección no existen o no están activos.

    """
    # Obtener el curso y la lección
    curso: Curso = get_object_or_404(Curso, pk=curso_pk, activo=True)
    leccion: Leccion = get_object_or_404(
        Leccion,
        pk=leccion_pk,
        curso=curso,
        activa=True,
    )

    # Verificar si el usuario está inscrito en el curso
    esta_inscrito: bool = Inscripcion.objects.filter(
        estudiante=request.user,
        curso=curso,
    ).exists()

    if not esta_inscrito:
        messages.error(
            request,
            "Debes estar inscrito en este curso para acceder a las lecciones.",
        )
        return redirect("appEstudiantes:curso_detalle", pk=curso_pk)

    # Obtener todas las lecciones del curso para la navegación
    lecciones: QuerySet[Leccion] = Leccion.objects.filter(
        curso=curso,
        activa=True,
    ).order_by("orden")

    # Obtener materiales de la lección
    materiales: QuerySet[Material] = Material.objects.filter(
        leccion=leccion,
        activo=True,
    ).order_by("orden")

    # Obtener información de progreso de la lección actual
    progreso, _ = ProgresoLeccion.objects.get_or_create(
        estudiante=request.user,
        leccion=leccion,
        defaults={"completado": False},
    )
    
    # Obtener el progreso de todas las lecciones del curso para el usuario actual
    progreso_lecciones = {
        pl.leccion_id: pl
        for pl in ProgresoLeccion.objects.filter(
            estudiante=request.user,
            leccion__in=lecciones,
        )
    }

    # Manejar el envío del formulario de notas personales
    if request.method == "POST" and "guardar_notas" in request.POST:
        form = NotaPersonalForm(request.POST, instance=progreso)
        if form.is_valid():
            form.save()
            messages.success(request, "Tus notas se han guardado correctamente.")
            return redirect(
                "appEstudiantes:leccion_detalle",
                curso_pk=curso_pk,
                leccion_pk=leccion_pk,
            )
    else:
        form = NotaPersonalForm(instance=progreso)

    # Obtener lecciones previas y siguientes para navegación
    leccion_anterior: Leccion | None = (
        lecciones.filter(orden__lt=leccion.orden).order_by("-orden").first()
    )
    leccion_siguiente: Leccion | None = (
        lecciones.filter(orden__gt=leccion.orden).order_by("orden").first()
    )

    context: dict[str, Any] = {
        "curso": curso,
        "leccion": leccion,
        "lecciones": lecciones,
        "materiales": materiales,
        "progreso": progreso,
        "form": form,
        "leccion_anterior": leccion_anterior,
        "leccion_siguiente": leccion_siguiente,
        "progreso_lecciones": progreso_lecciones,
    }

    return render(request, "appEstudiantes/leccion_detalle.html", context)

@login_required
def marcar_leccion_completada(
    request: HttpRequest,
    leccion_pk: int,
) -> HttpResponseRedirect:
    """
    Marca una lección como completada por el estudiante.

    Args:
        request: La solicitud HTTP.
        leccion_pk: ID de la lección a marcar como completada.

    Returns:
        HttpResponseRedirect: Redirige a la página de la lección.

    Raises:
        Http404: Si la lección no existe o no está activa.
        PermissionDenied: Si el usuario no tiene permiso para acceder a la lección.

    """
    # Obtener la lección o devolver 404 si no existe o no está activa
    leccion: Leccion = get_object_or_404(
        Leccion.objects.select_related("curso"),
        pk=leccion_pk,
        activa=True,
    )

    # Verificar que el usuario esté inscrito en el curso de la lección
    if not Inscripcion.objects.filter(
        estudiante=request.user,
        curso=leccion.curso,
    ).exists():
        messages.error(
            request,
            "No estás inscrito en este curso.",
            extra_tags="alert-danger",
        )
        return redirect("appEstudiantes:curso_detalle", pk=leccion.curso.pk)

    try:
        # Obtener o crear el progreso de la lección
        progreso, created = ProgresoLeccion.objects.get_or_create(
            estudiante=request.user,
            leccion=leccion,
            defaults={
                "completado": True,
                "fecha_completado": timezone.now(),
            },
        )

        # Si ya existía, actualizar el estado
        if not created and not progreso.completado:
            progreso.completado = True
            progreso.fecha_completado = timezone.now()
            progreso.save()

            messages.success(
                request,
                f"¡Lección '{leccion.titulo}' marcada como completada!",
                extra_tags="alert-success",
            )
        elif not created:
            messages.info(
                request,
                f"La lección '{leccion.titulo}' ya estaba marcada como completada.",
                extra_tags="alert-info",
            )

    except Exception as e:
        messages.error(
            request,
            f"Error al marcar la lección como completada: {e!s}",
            extra_tags="alert-danger",
        )
        if settings.DEBUG:
            raise

    return redirect(
        "appEstudiantes:leccion_detalle",
        curso_pk=leccion.curso.pk,
        leccion_pk=leccion.pk,
    )


@login_required
def descargar_material(
    request: HttpRequest,
    material_pk: int,
) -> HttpResponseRedirect:
    """
    Permite la descarga de un material y registra la acción.

    Args:
        request: La solicitud HTTP.
        material_pk: ID del material a descargar.

    Returns:
        HttpResponseRedirect: Redirige a la URL del archivo para su descarga.

    Raises:
        Http404: Si el material no existe o no está activo.

    """
    material: Material = get_object_or_404(Material, pk=material_pk, activo=True)

    # Verificar que el usuario esté inscrito en el curso
    if not Inscripcion.objects.filter(
        estudiante=request.user,
        curso=material.leccion.curso,
    ).exists():
        messages.warning(
            request,
            "No tienes permiso para descargar este material.",
        )
        return redirect(
            "appEstudiantes:curso_detalle",
            pk=material.leccion.curso.pk,
        )

    # Registrar la descarga
    MaterialDescargado.objects.get_or_create(
        estudiante=request.user,
        material=material,
    )

    # Redirigir a la descarga del archivo
    return redirect(material.archivo.url)

@login_required
def mis_cursos(request: HttpRequest) -> HttpResponse:
    """
    Muestra la lista de cursos en los que está inscrito el estudiante.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla de mis cursos.

    """
    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user,
    ).select_related("curso")
    return render(
        request,
        "appEstudiantes/mis_cursos.html",
        {"inscripciones": inscripciones},
    )

@login_required
def progreso(request: HttpRequest) -> HttpResponse:
    """
    Muestra el progreso general del estudiante en todos sus cursos.

    Args:
        request: La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la plantilla de progreso.

    """
    # Obtener todos los cursos en los que está inscrito el usuario
    cursos_inscritos: QuerySet[Curso] = Curso.objects.filter(
        estudiantes_inscritos__estudiante=request.user,
    ).prefetch_related("lecciones")

    # Calcular el progreso por curso
    progreso_cursos: list[dict[str, Any]] = []
    for curso in cursos_inscritos:
        total_lecciones: int = curso.lecciones.count()
        if total_lecciones == 0:
            continue

        lecciones_completadas: int = ProgresoLeccion.objects.filter(
            estudiante=request.user,
            leccion__curso=curso,
            completado=True,
        ).count()

        porcentaje: float = (lecciones_completadas / total_lecciones) * 100
        progreso_cursos.append({
            "curso": curso,
            "lecciones_completadas": lecciones_completadas,
            "total_lecciones": total_lecciones,
            "porcentaje": round(porcentaje, 2),
        })

    return render(
        request,
        "appEstudiantes/progreso.html",
        {"progreso_cursos": progreso_cursos},
    )

@login_required
def guardar_notas(
    request: HttpRequest,
    leccion_pk: int,
) -> HttpResponseRedirect:
    """
    Guarda las notas personales de un estudiante para una lección.

    Args:
        request: La solicitud HTTP.
        leccion_pk: ID de la lección para la que se guardan las notas.

    Returns:
        HttpResponseRedirect: Redirige a la página de la lección.

    Raises:
        Http404: Si la lección no existe o no está activa.

    """
    leccion: Leccion = get_object_or_404(Leccion, pk=leccion_pk, activa=True)

    # Verificar que el usuario esté inscrito en el curso
    if not Inscripcion.objects.filter(
        estudiante=request.user,
        curso=leccion.curso,
    ).exists():
        messages.warning(
            request,
            "No tienes permiso para realizar esta acción.",
        )
        return redirect(
            "appEstudiantes:curso_detalle",
            pk=leccion.curso.pk,
        )

    # Obtener o crear el progreso de la lección
    progreso, created = ProgresoLeccion.objects.get_or_create(
        estudiante=request.user,
        leccion=leccion,
    )

    if request.method == "POST":
        notas: str = request.POST.get("notas", "")
        progreso.notas = notas
        progreso.save()
        messages.success(
            request,
            "Tus notas han sido guardadas correctamente.",
        )

    return redirect(
        "appEstudiantes:leccion_detalle",
        curso_pk=leccion.curso.pk,
        leccion_pk=leccion.pk,
    )
