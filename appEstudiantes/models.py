"""Modelos para la aplicación de Estudiantes."""
from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from appComunidad.models import Plan
from appProfesores.models import Curso, Leccion, Material


class PerfilEstudiante(models.Model):
    """
    Modelo que representa el perfil de un estudiante.

    Almacena información adicional sobre los estudiantes, como su foto de perfil,
    biografía, plan de suscripción e idioma nativo.
    """

    usuario: ClassVar[models.OneToOneField] = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil_estudiante",
    )
    foto: ClassVar[models.ImageField] = models.ImageField(
        upload_to="perfil_estudiantes/",
        default="default_profile.png",
    )
    biografia: ClassVar[models.TextField] = models.TextField(blank=True, default="")
    plan: ClassVar[models.ForeignKey] = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    fecha_inscripcion: ClassVar[models.DateTimeField] = models.DateTimeField(
        default=timezone.now,
    )
    idioma_nativo: ClassVar[models.CharField] = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        """Representación en cadena del perfil del estudiante."""
        return f"Perfil de {self.usuario.username}"


class Inscripcion(models.Model):
    """Modelo que representa la inscripción de un estudiante a un curso."""

    estudiante: ClassVar[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inscripciones",
    )
    curso: ClassVar[models.ForeignKey] = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name="estudiantes_inscritos",
    )
    fecha_inscripcion: ClassVar[models.DateTimeField] = models.DateTimeField(
        default=timezone.now,
    )
    completado: ClassVar[models.BooleanField] = models.BooleanField(default=False)

    class Meta:
        """Metadatos para la clase Inscripcion."""

        unique_together = ("estudiante", "curso")
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self) -> str:
        """Representación en cadena de la inscripción."""
        return f"{self.estudiante.username} - {self.curso.titulo}"


class ProgresoLeccion(models.Model):
    """Modelo que rastrea el progreso de un estudiante en una lección."""

    estudiante: ClassVar[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="progreso_lecciones",
    )
    leccion: ClassVar[models.ForeignKey] = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name="progreso_estudiantes",
    )
    completado: ClassVar[models.BooleanField] = models.BooleanField(default=False)
    fecha_inicio: ClassVar[models.DateTimeField] = models.DateTimeField(auto_now_add=True)
    fecha_completado: ClassVar[models.DateTimeField] = models.DateTimeField(
        null=True,
        blank=True,
    )
    notas: ClassVar[models.TextField] = models.TextField(blank=True, default="")

    class Meta:
        """Metadatos para la clase ProgresoLeccion."""

        unique_together = ("estudiante", "leccion")
        verbose_name = "Progreso de Lección"
        verbose_name_plural = "Progreso de Lecciones"

    def __str__(self) -> str:
        """Representación en cadena del progreso de la lección."""
        return f"{self.estudiante.username} - {self.leccion.titulo}"

    def marcar_completado(self) -> None:
        """Marca la lección como completada y registra la fecha de finalización."""
        self.completado = True
        self.fecha_completado = timezone.now()
        self.save()


class Comentario(models.Model):
    """Modelo que representa un comentario realizado por un estudiante en una lección."""

    estudiante: ClassVar[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    leccion: ClassVar[models.ForeignKey] = models.ForeignKey(
        Leccion,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    contenido: ClassVar[models.TextField] = models.TextField()
    fecha: ClassVar[models.DateTimeField] = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadatos para la clase Comentario."""

        verbose_name: ClassVar[str] = "Comentario"
        verbose_name_plural: ClassVar[str] = "Comentarios"
        ordering: ClassVar[list[str]] = ["-fecha"]

    def __str__(self) -> str:
        """Representación en cadena del comentario."""
        return f"Comentario de {self.estudiante.username} en {self.leccion.titulo}"


class MaterialDescargado(models.Model):
    """Modelo que registra los materiales descargados por los estudiantes."""

    estudiante: ClassVar[models.ForeignKey] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="materiales_descargados",
    )
    material: ClassVar[models.ForeignKey] = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="descargas",
    )
    fecha_descarga: ClassVar[models.DateTimeField] = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadatos para la clase MaterialDescargado."""

        unique_together = ("estudiante", "material")
        verbose_name = "Material Descargado"
        verbose_name_plural = "Materiales Descargados"

    def __str__(self) -> str:
        """Representación en cadena del material descargado."""
        return f"{self.estudiante.username} - {self.material.titulo}"
