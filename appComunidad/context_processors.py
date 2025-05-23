"""Procesadores de contexto personalizados para la aplicación appComunidad."""


from django.http import HttpRequest


def user_redirect_processor(request: HttpRequest) -> dict[str, str]:
    """
    Procesador de contexto para determinar la URL de redirección después del login.

    Args:
        request: La solicitud HTTP.

    Returns:
        dict: Diccionario con la URL de redirección.

    """
    redirect_url = "appComunidad:index"  # URL por defecto

    if hasattr(request.user, "perfil_estudiante"):
        redirect_url = "appEstudiantes:dashboard"
    elif hasattr(request.user, "perfil_profesor"):
        redirect_url = "appProfesores:dashboard"

    return {
        "login_redirect_url": redirect_url,
    }
