"""Views para la aplicación de profesores."""

from typing import Any

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from appEstudiantes.models import Inscripcion, ProgresoLeccion

from .forms import CursoForm, LeccionForm, MaterialForm, PerfilProfesorForm
from .models import Curso, Leccion, Material, PerfilProfesor


class EsProfesorMixin(UserPassesTestMixin):
    """Verifica si el usuario es un profesor."""

    def test_func(self) -> bool:
        """
        Verifica si el usuario es un profesor.

        Returns:
            bool: True si el usuario es un profesor, False de lo contrario.

        """
        return hasattr(self.request.user, "perfil_profesor")


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Muestra el dashboard del profesor."""
    # Verificar si el usuario es un profesor
    if not hasattr(request.user, "perfil_profesor"):
        messages.warning(request, "Solo los profesores pueden acceder a esta sección.")
        return redirect("appComunidad:index")

    # Obtener los cursos del profesor
    cursos = Curso.objects.filter(profesor=request.user)
    total_cursos = cursos.count()

    # Obtener estadísticas generales
    total_estudiantes = Inscripcion.objects.filter(curso__profesor=request.user).values("estudiante").distinct().count()
    total_lecciones = Leccion.objects.filter(curso__profesor=request.user).count()
    total_materiales = Material.objects.filter(leccion__curso__profesor=request.user).count()

    # Obtener cursos recientes
    cursos_recientes = cursos.order_by("-fecha_creacion")[:5]

    # Obtener estudiantes recientes
    estudiantes_recientes = Inscripcion.objects.filter(
        curso__profesor=request.user,
    ).order_by("-fecha_inscripcion")[:5]

    context = {
        "total_cursos": total_cursos,
        "total_estudiantes": total_estudiantes,
        "total_lecciones": total_lecciones,
        "total_materiales": total_materiales,
        "cursos_recientes": cursos_recientes,
        "estudiantes_recientes": estudiantes_recientes,
    }
    return render(request, "appProfesores/dashboard.html", context)


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    """Muestra y actualiza el perfil del profesor."""
    # Verificar si el usuario es un profesor
    try:
        perfil = request.user.perfil_profesor
    except PerfilProfesor.DoesNotExist:
        perfil = PerfilProfesor(usuario=request.user)
        perfil.save()

    if request.method == "POST":
        form = PerfilProfesorForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado correctamente.")
            return redirect("appProfesores:perfil")
    else:
        form = PerfilProfesorForm(instance=perfil)

    return render(request, "appProfesores/perfil.html", {"form": form})


class CursoListView(LoginRequiredMixin, EsProfesorMixin, ListView):
    """Vista para listar los cursos de un profesor."""

    model = Curso
    template_name = "appProfesores/cursos.html"
    context_object_name = "cursos"

    def get_queryset(self) -> QuerySet[Curso]:
        """
        Obtiene el queryset de cursos del profesor actual.

        Returns:
            QuerySet[Curso]: QuerySet filtrado con los cursos del profesor.

        """
        return Curso.objects.filter(profesor=self.request.user)


class CursoCreateView(LoginRequiredMixin, EsProfesorMixin, CreateView):
    """Vista para crear un nuevo curso."""

    model = Curso
    form_class = CursoForm
    template_name = "appProfesores/create_course.html"
    success_url = reverse_lazy("appProfesores:cursos")

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """
        Procesa un formulario válido.

        Args:
            form: Formulario validado.

        Returns:
            HttpResponse: Respuesta HTTP.

        """
        form.instance.profesor = self.request.user
        messages.success(self.request, "Curso creado exitosamente.")
        return super().form_valid(form)


class CursoUpdateView(LoginRequiredMixin, EsProfesorMixin, UpdateView):
    """Vista para actualizar un curso existente."""

    model = Curso
    form_class = CursoForm
    template_name = "appProfesores/edit_course.html"

    def get_queryset(self) -> QuerySet[Curso]:
        """
        Obtiene el queryset de cursos del profesor actual.

        Returns:
            QuerySet[Curso]: QuerySet filtrado con los cursos del profesor.

        """
        return Curso.objects.filter(profesor=self.request.user)

    def get_success_url(self) -> str:
        """
        Devuelve la URL a la que redirigir después de una actualización exitosa.

        Returns:
            str: URL de redirección.

        """
        return reverse("appProfesores:curso_detalle", kwargs={"pk": self.object.pk})

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """
        Procesa un formulario válido.

        Args:
            form: Formulario validado.

        Returns:
            HttpResponse: Respuesta HTTP.

        """
        messages.success(self.request, "Curso actualizado exitosamente.")
        return super().form_valid(form)


class CursoDeleteView(LoginRequiredMixin, EsProfesorMixin, DeleteView):
    """Vista para eliminar un curso."""

    model = Curso
    template_name = "appProfesores/delete_course.html"
    success_url = reverse_lazy("appProfesores:cursos")

    def get_queryset(self) -> QuerySet[Curso]:
        """
        Obtiene el queryset de cursos del profesor actual.

        Returns:
            QuerySet[Curso]: QuerySet filtrado con los cursos del profesor.

        """
        return Curso.objects.filter(profesor=self.request.user)

    def delete(self, request: HttpRequest, *args: object, **kwargs: str) -> HttpResponse:
        """
        Elimina un curso.

        Args:
            request: Objeto HttpRequest que contiene los datos de la solicitud.
            *args: Argumentos adicionales.
            **kwargs: Argumentos adicionales con nombre.

        Returns:
            HttpResponse: Respuesta HTTP.

        """
        messages.success(self.request, "Curso eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


@login_required
def curso_detalle(request: HttpRequest, pk: int) -> HttpResponse:
    """Muestra el detalle de un curso."""
    # Verificar si el usuario es un profesor
    if not hasattr(request.user, "perfil_profesor"):
        messages.warning(request, "Solo los profesores pueden acceder a esta sección.")
        return redirect("appComunidad:index")
    curso = get_object_or_404(Curso, pk=pk, profesor=request.user)
    lecciones = curso.lecciones.all().order_by("numero_orden")
    total_estudiantes = Inscripcion.objects.filter(curso=curso).count()
    estudiantes_completados = Inscripcion.objects.filter(
        curso=curso, completado=True,
    ).count()

    context = {
        "curso": curso,
        "lecciones": lecciones,
        "total_estudiantes": total_estudiantes,
        "estudiantes_completados": estudiantes_completados,
    }
    return render(request, "appProfesores/curso_detalle.html", context)


class LeccionCreateView(LoginRequiredMixin, EsProfesorMixin, CreateView):
    """Vista para crear una nueva lección."""

    model = Leccion
    form_class = LeccionForm
    template_name = "appProfesores/create_lesson.html"

    def get_form_kwargs(self) -> dict[str, Any]:
        """
        Añade el usuario actual a los argumentos del formulario.

        Returns:
            dict[str, Any]: Argumentos para el formulario.

        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs: str) -> dict[str, Any]:
        """
        Añade el curso al contexto de la plantilla.

        Returns:
            dict[str, Any]: Contexto para la plantilla.

        """
        context = super().get_context_data(**kwargs)
        curso = get_object_or_404(
            Curso,
            pk=self.kwargs["curso_pk"],
            profesor=self.request.user,
        )
        context["curso"] = curso
        return context

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """
        Procesa un formulario válido.

        Args:
            form: Formulario validado.

        Returns:
            HttpResponse: Respuesta HTTP.

        """
        form.instance.curso = get_object_or_404(
            Curso,
            pk=self.kwargs["curso_pk"],
            profesor=self.request.user,
        )
        messages.success(self.request, "Lección creada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Devuelve la URL a la que redirigir después de una creación exitosa.

        Returns:
            str: URL de redirección.

        """
        return reverse("appProfesores:curso_detalle",
                     kwargs={"pk": self.kwargs["curso_pk"]})


class LeccionUpdateView(LoginRequiredMixin, EsProfesorMixin, UpdateView):
    """Vista para actualizar una lección existente."""

    model = Leccion
    form_class = LeccionForm
    template_name = "appProfesores/edit_lesson.html"

    def get_queryset(self) -> QuerySet[Leccion]:
        """Obtiene el queryset de lecciones del profesor actual."""
        return Leccion.objects.filter(curso__profesor=self.request.user)

    def get_form_kwargs(self) -> dict:
        """Añade el usuario actual a los argumentos del formulario."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs: str) -> dict[str, Any]:
        """Añade el curso al contexto de la plantilla."""
        context = super().get_context_data(**kwargs)
        context["curso"] = self.object.curso
        return context

    def get_success_url(self) -> str:
        """Devuelve la URL a la que redirigir después de una actualización exitosa."""
        return reverse("appProfesores:curso_detalle",
                     kwargs={"pk": self.object.curso.pk})

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """Procesa un formulario válido y muestra un mensaje de éxito."""
        messages.success(self.request, "Lección actualizada exitosamente.")
        return super().form_valid(form)

@login_required
def agregar_material(request: HttpRequest, leccion_pk: int) -> HttpResponse:
    """Agrega un nuevo material a una lección."""
    if not hasattr(request.user, "perfil_profesor"):
        messages.warning(request, "Solo los profesores pueden acceder a esta sección.")
        return redirect("appComunidad:index")

    leccion = get_object_or_404(Leccion, pk=leccion_pk, curso__profesor=request.user)

    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.leccion = leccion
            material.save()
            messages.success(request, "Material agregado exitosamente.")
            return redirect("appProfesores:leccion_detalle", pk=leccion.pk)
    else:
        form = MaterialForm()
    return render(request, "appProfesores/agregar_material.html", {
        "form": form,
        "leccion": leccion,
    })

@login_required
def eliminar_material(request: HttpRequest, material_pk: int) -> HttpResponse:
    """Elimina un material de una lección."""
    if not hasattr(request.user, "perfil_profesor"):
        messages.warning(request, "Solo los profesores pueden acceder a esta sección.")
        return redirect("appComunidad:index")

    material = get_object_or_404(
        Material,
        pk=material_pk,
        leccion__curso__profesor=request.user,
    )
    leccion = material.leccion

    if request.method == "POST":
        material.delete()
        messages.success(request, "Material eliminado exitosamente.")
        return redirect("appProfesores:leccion_detalle", pk=leccion.pk)

    return render(request, "appProfesores/eliminar_material.html", {
        "material": material,
    })

@login_required
def estudiantes_curso(request: HttpRequest, curso_pk: int) -> HttpResponse:
    """Muestra la lista de estudiantes inscritos en un curso."""
    if not hasattr(request.user, "perfil_profesor"):
        messages.warning(request, "Solo los profesores pueden acceder a esta sección.")
        return redirect("appComunidad:index")

    curso = get_object_or_404(Curso, pk=curso_pk, profesor=request.user)
    inscripciones = Inscripcion.objects.filter(curso=curso).select_related("estudiante")

    estudiantes_info = []

    for inscripcion in inscripciones:
        estudiante = inscripcion.estudiante
        total_lecciones = curso.lecciones.count()
        lecciones_completadas = ProgresoLeccion.objects.filter(
            estudiante=estudiante,
            leccion__curso=curso,
            completado=True,
        ).count()

        porcentaje = lecciones_completadas / total_lecciones * 100 if total_lecciones > 0 else 0

        estudiantes_info.append({
            "estudiante": estudiante,
            "fecha_inscripcion": inscripcion.fecha_inscripcion,
            "completado": inscripcion.completado,
            "porcentaje": porcentaje,
            "lecciones_completadas": lecciones_completadas,
            "total_lecciones": total_lecciones,
        })

    return render(request, "appProfesores/students_list.html", {
        "curso": curso,
        "estudiantes_info": estudiantes_info,
    })

@login_required
def toggle_curso_activo(request: HttpRequest, pk: int) -> JsonResponse:
    """Cambia el estado activo de un curso."""
    if not hasattr(request.user, "perfil_profesor"):
        return JsonResponse({"success": False, "message": "Acceso no autorizado"})

    if request.method == "POST":
        curso = get_object_or_404(Curso, pk=pk, profesor=request.user)

        # Parsear los datos JSON del cuerpo de la solicitud
        import json
        data = json.loads(request.body)
        active = data.get("active", False)

        # Actualizar el estado activo del curso
        curso.activo = active
        curso.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "Método no permitido"})
