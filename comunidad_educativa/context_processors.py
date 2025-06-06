def admin_site_info(request):
    """
    Context processor para agregar información del sitio a todas las plantillas del admin.
    """
    from django.conf import settings
    
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Panel de Administración'),
        'SITE_HEADER': getattr(settings, 'SITE_HEADER', 'Administración del Sitio'),
        'SITE_TITLE': getattr(settings, 'SITE_TITLE', 'Administración del Sitio'),
        'INDEX_TITLE': getattr(settings, 'INDEX_TITLE', 'Bienvenido al Panel de Administración'),
        'SITE_URL': getattr(settings, 'SITE_URL', '/'),
        'HAS_MODULE_PERMS': request.user.has_module_perms('auth') if hasattr(request, 'user') else False,
    }
