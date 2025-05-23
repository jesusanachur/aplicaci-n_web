"""
Modelos para la aplicación de Profesores.

Este módulo contiene todos los modelos necesarios para la gestión de profesores,
cursos, lecciones, materiales y evaluaciones en la plataforma educativa.
"""
from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from appComunidad.models import Plan


class PerfilProfesor(models.Model):
    """Modelo que almacena información adicional del profesor."""

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_profesor")
    foto = models.ImageField(upload_to="perfil_profesores/", default="default_profile.png")
    biografia = models.TextField()
    especialidad = models.CharField(max_length=100)
    anos_experiencia = models.PositiveIntegerField(default=0)
    titulo_academico = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        """Configuraciones adicionales del modelo PerfilProfesor."""

        verbose_name: ClassVar[str] = "Perfil de Profesor"
        verbose_name_plural: ClassVar[str] = "Perfiles de Profesores"

    def __str__(self) -> str:
        """Representación en cadena del perfil del profesor."""
        return f"Profesor: {self.usuario.get_full_name() or self.usuario.username}"

class Curso(models.Model):
    """Modelo que representa un curso en la plataforma."""

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cursos_creados")
    nivel_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="cursos")
    fecha_creacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="cursos/", blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        """Metadatos para el modelo Curso."""

        verbose_name: ClassVar[str] = "Curso"
        verbose_name_plural: ClassVar[str] = "Cursos"
        ordering: ClassVar[list[str]] = ["-fecha_creacion"]

    def __str__(self) -> str:
        """Representación en cadena del curso."""
        return self.titulo

    def get_absolute_url(self) -> str:
        """Obtiene la URL absoluta para la vista de detalle del curso."""
        return reverse("appProfesores:curso_detalle", kwargs={"pk": self.pk})

class Leccion(models.Model):
    """Modelo que representa una lección dentro de un curso."""

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="lecciones")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido = models.TextField()
    numero_orden = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    duracion_minutos = models.PositiveIntegerField(default=30)

    class Meta:
        """Metadatos para el modelo Leccion."""

        verbose_name: ClassVar[str] = "Lección"
        verbose_name_plural: ClassVar[str] = "Lecciones"
        ordering: ClassVar[list[str]] = ["curso", "numero_orden"]
        unique_together: ClassVar[tuple[str, str]] = ("curso", "numero_orden")

    def __str__(self) -> str:
        """Representación en cadena de la lección."""
        return f"{self.curso.titulo} - Lección {self.numero_orden}: {self.titulo}"

    def get_absolute_url(self) -> str:
        """Obtiene la URL absoluta para la vista de detalle de la lección."""
        return reverse("appProfesores:leccion_detalle", kwargs={"pk": self.pk})

class Material(models.Model):
    """Modelo que representa un material de apoyo para una lección."""

    TIPO_CHOICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ("documento", "Documento"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("presentacion", "Presentación"),
        ("ejercicio", "Ejercicio"),
    )

    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="materiales")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default="")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to="materiales/")
    fecha_subida = models.DateTimeField(default=timezone.now)

    class Meta:
        """Metadatos para el modelo Material."""

        verbose_name: ClassVar[str] = "Material"
        verbose_name_plural: ClassVar[str] = "Materiales"
        ordering: ClassVar[list[str]] = ["leccion", "fecha_subida"]

    def __str__(self) -> str:
        """Representación en cadena del material."""
        return f"{self.titulo} ({self.get_tipo_display()}) - {self.leccion.titulo}"

    def get_tipo_icon(self) -> str:
        """
        Obtiene el ícono de Font Awesome correspondiente al tipo de material.

        Returns:
            str: Clase CSS de Font Awesome para el ícono.

        """
        icons: dict[str, str] = {
            "documento": "fa-file-alt",
            "video": "fa-video",
            "audio": "fa-headphones",
            "presentacion": "fa-file-powerpoint",
            "ejercicio": "fa-tasks",
        }
        return icons.get(self.tipo, "fa-file")

class Evaluacion(models.Model):
    """Modelo que representa una evaluación para una lección."""

    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name="evaluaciones")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    puntaje_maximo = models.PositiveIntegerField(default=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        """Metadatos para el modelo Evaluacion."""

        verbose_name: ClassVar[str] = "Evaluación"
        verbose_name_plural: ClassVar[str] = "Evaluaciones"

    def __str__(self) -> str:
        """Representación en cadena de la evaluación."""
        return f"Evaluación: {self.titulo} - {self.leccion.titulo}"

class Pregunta(models.Model):
    """Modelo que representa una pregunta dentro de una evaluación."""

    TIPO_CHOICES: ClassVar[tuple[tuple[str, str], ...]] = (
        ("opcion_multiple", "Opción Múltiple"),
        ("verdadero_falso", "Verdadero/Falso"),
        ("texto_libre", "Texto Libre"),
        ("completar", "Completar"),
    )

    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE, related_name="preguntas")
    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    puntaje = models.PositiveIntegerField(default=10)

    class Meta:
        """Metadatos para el modelo Pregunta."""

        verbose_name: ClassVar[str] = "Pregunta"
        verbose_name_plural: ClassVar[str] = "Preguntas"

    def __str__(self) -> str:
        """Representación en cadena de la pregunta."""
        return f"{self.enunciado[:50]}... ({self.get_tipo_display()})"

class Opcion(models.Model):
    """Modelo que representa una opción para una pregunta de opción múltiple."""

    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")
    texto = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)

    class Meta:
        """Metadatos para el modelo Opcion."""

        verbose_name: ClassVar[str] = "Opción"
        verbose_name_plural: ClassVar[str] = "Opciones"

    def __str__(self) -> str:
        """Representación en cadena de la opción."""
        return f"{self.texto} - {'Correcta' if self.es_correcta else 'Incorrecta'}"

