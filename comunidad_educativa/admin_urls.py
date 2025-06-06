from django.urls import path, include
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .admin_views import dashboard_stats

# Obtener el admin_site personalizado
admin_site = admin.site

# Configurar el título del sitio de administración
admin.site.site_header = 'Panel de Administración'
admin.site.site_title = 'Sitio de Administración'
admin.site.index_title = 'Bienvenido al Panel de Administración'

def admin_view(view, cacheable=False):
    """
    Decorador para vistas del admin que requiere permisos de superusuario.
    """
    def wrapper(*args, **kwargs):
        return admin_site.admin_view(view)(*args, **kwargs)
    wrapper.admin_site = admin_site
    
    # Usar el login_url correcto
    login_url = getattr(settings, 'LOGIN_URL', 'admin:login')
    
    return never_cache(login_required(
        user_passes_test(
            lambda u: u.is_active and u.is_staff,
            login_url=login_url
        )(view)
    ))

# Vistas personalizadas del admin
urlpatterns = [
    # Redirigir la raíz del admin al índice del admin
    path('', admin_site.admin_view(admin_site.index), name='index'),
    
    # Incluir las URLs de autenticación
    path('login/', admin_site.login, name='login'),
    path('logout/', admin_site.logout, name='logout'),
    
    # Dashboard de estadísticas
    path('dashboard/', admin_view(dashboard_stats), name='dashboard_stats'),
    
    # Incluir las URLs de las aplicaciones del admin
    path('appComunidad/', include('appComunidad.urls')),
    path('appEstudiantes/', include('appEstudiantes.urls')),
    path('appProfesores/', include('appProfesores.urls')),
]

# Incluir las URLs del admin por defecto
urlpatterns += [
    path('', include(admin_site.urls)),
]
