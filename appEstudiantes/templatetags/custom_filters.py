"""Filtros personalizados para plantillas de la aplicación de Estudiantes."""
from typing import Any, Protocol, TypeVar

from django import template

register = template.Library()

# Type variables for generic types
K = TypeVar("K")
V = TypeVar("V")


class HasId(Protocol):
    """Protocolo para objetos que tienen un atributo id."""

    id: int

@register.filter
def get_item(dictionary: dict[K, V] | None, key: K) -> V | None:
    """
    Obtiene un valor de un diccionario por su clave.

    Args:
        dictionary: Diccionario del cual obtener el valor.
        key: Clave del valor a obtener.

    Returns:
        El valor asociado a la clave o None si no existe.

    """
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def select_attr(items: list[Any] | None, attr_value: str) -> list[Any]:
    """
    Filtra una lista de objetos por un atributo con valor True.

    Args:
        items: Lista de objetos a filtrar.
        attr_value: Nombre del atributo a verificar.

    Returns:
        Lista filtrada de objetos que tienen el atributo en True.

    """
    if items is None:
        return []
    return [item for item in items if hasattr(item, attr_value) and getattr(item, attr_value)]


@register.filter
def filter_lecciones_curso(
    progreso_lecciones: list[Any] | None, curso: HasId | None,
) -> list[Any]:
    """
    Filtra las lecciones completadas para un curso específico.

    Args:
        progreso_lecciones: Lista de objetos ProgresoLeccion o None
        curso: Objeto que tiene un atributo 'id' o None

    Returns:
        Lista de ProgresoLeccion filtrados por curso y completados

    """
    if not progreso_lecciones or not curso:
        return []
    return [pl for pl in progreso_lecciones if pl.leccion.curso_id == curso.id and pl.completado]


@register.filter
def filter_completadas(progreso_lecciones: list[Any] | None) -> list[Any]:
    """
    Filtra las lecciones completadas.

    Args:
        progreso_lecciones: Lista de objetos ProgresoLeccion o None

    Returns:
        Lista de ProgresoLeccion completados

    """
    if not progreso_lecciones:
        return []
    return [pl for pl in progreso_lecciones if pl.completado]
