"""
Modelos para la aplicación Comunidad.

Este módulo define los modelos utilizados en la aplicación Comunidad,
incluyendo Planes, Noticias, Testimonios y Mensajes de Contacto.
"""

from typing import ClassVar

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Plan(models.Model):
    """Modelo que representa un plan de suscripción."""

    class Nivel(models.TextChoices):
        """Opciones de nivel para los planes."""

        PRINCIPIANTE = "principiante", _("Principiante")
        INTERMEDIO = "intermedio", _("Intermedio")
        AVANZADO = "avanzado", _("Avanzado")

    nombre = models.CharField(_("Nombre"), max_length=100)
    descripcion = models.TextField(_("Descripción"))
    nivel = models.CharField(
        _("Nivel"),
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.PRINCIPIANTE,
    )
    precio = models.DecimalField(
        _("Precio"),
        max_digits=10,
        decimal_places=2,
    )
    duracion_meses = models.PositiveIntegerField(
        _("Duración (meses)"),
        default=1,
    )

    class Meta:
        """Metadatos del modelo Plan."""

        verbose_name = _("Plan")
        verbose_name_plural = _("Planes")

    def __str__(self) -> str:
        """Representación en cadena del plan."""
        return f"{self.nombre} - {self.get_nivel_display()}"


class Noticia(models.Model):
    """Modelo que representa una noticia en el sitio."""

    titulo = models.CharField(_("Título"), max_length=200)
    contenido = models.TextField(_("Contenido"))
    fecha_publicacion = models.DateTimeField(
        _("Fecha de publicación"),
        auto_now_add=True,
    )
    imagen = models.ImageField(
        _("Imagen"),
        upload_to="noticias/",
        blank=True,
        null=True,
    )

    class Meta:
        """Metadatos del modelo Noticia."""

        verbose_name = _("Noticia")
        verbose_name_plural = _("Noticias")
        ordering: ClassVar[list[str]] = ["-fecha_publicacion"]

    def __str__(self) -> str:
        """Representación en cadena de la noticia."""
        return self.titulo

    def get_absolute_url(self) -> str:
        """Obtiene la URL absoluta de la noticia."""
        return reverse("appComunidad:noticia_detalle", kwargs={"pk": self.pk})


class Testimonio(models.Model):
    """Modelo que representa un testimonio de un usuario."""

    nombre = models.CharField(_("Nombre"), max_length=100)
    rol = models.CharField(_("Rol o cargo"), max_length=100)
    contenido = models.TextField(_("Contenido"))
    fecha = models.DateField(_("Fecha"), auto_now_add=True)
    imagen = models.ImageField(
        _("Foto de perfil"),
        upload_to="testimonios/",
        blank=True,
        null=True,
    )

    class Meta:
        """Metadatos del modelo Testimonio."""

        verbose_name = _("Testimonio")
        verbose_name_plural = _("Testimonios")

    def __str__(self) -> str:
        """Representación en cadena del testimonio."""
        return f"{self.nombre} - {self.rol}"


class ContactoMensaje(models.Model):
    """Modelo que representa un mensaje de contacto."""

    nombre = models.CharField(_("Nombre"), max_length=100)
    email = models.EmailField(_("Correo electrónico"))
    asunto = models.CharField(_("Asunto"), max_length=200)
    mensaje = models.TextField(_("Mensaje"))
    fecha = models.DateTimeField(_("Fecha"), auto_now_add=True)
    leido = models.BooleanField(_("¿Leído?"), default=False)

    class Meta:
        """Metadatos del modelo ContactoMensaje."""

        verbose_name = _("Mensaje de Contacto")
        verbose_name_plural = _("Mensajes de Contacto")
        ordering: ClassVar[list[str]] = ["-fecha"]

    def __str__(self) -> str:
        """Representación en cadena del mensaje de contacto."""
        return f"{self.asunto} - {self.email}"
