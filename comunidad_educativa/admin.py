from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.db.models import Count, Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import json

# Importa tus modelos aquí
try:
    from appEstudiantes.models import Estudiante
except ImportError:
    Estudiante = None

try:
    from appProfesores.models import Profesor
except ImportError:
    Profesor = None

try:
    from appCursos.models import Curso
except ImportError:
    Curso = None

# Clase personalizada para el modelo User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    # Personalizar los campos mostrados en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

# Clase personalizada para el modelo Group
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users_count')
    search_fields = ('name',)
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = 'Usuarios'

class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Administración"
    site_title = "Sitio de Administración"
    index_title = "Bienvenido al Panel de Administración"
    
    def get_urls(self):
        from .admin_views import dashboard_stats
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-stats/', self.admin_view(dashboard_stats), name='dashboard-stats'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        """
        Override del método index para incluir estadísticas en el dashboard.
        """
        extra_context = extra_context or {}
        
        # Obtener estadísticas básicas
        extra_context.update({
            'user_count': User.objects.count(),
            'student_count': Estudiante.objects.count() if Estudiante else 0,
            'teacher_count': Profesor.objects.count() if Profesor else 0,
            'course_count': Curso.objects.count() if Curso else 0,
        })
        
        return super().index(request, extra_context)
    
    def get_app_list(self, request, app_label=None):
        """
        Devuelve una lista ordenada de todas las aplicaciones instaladas.
        """
        app_dict = self._build_app_dict(request)
        
        # Ordenar las aplicaciones
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Ordenar los modelos dentro de cada aplicación
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
            
            # Añadir iconos personalizados para cada aplicación
            app_icons = {
                'auth': 'people',
                'sites': 'public',
                'estudiantes': 'school',
                'profesores': 'person',
                'cursos': 'menu_book',
            }
            
            app['icon'] = app_icons.get(app['app_label'], 'apps')
        
        return app_list
    
    def each_context(self, request):
        """
        Agrega contexto adicional a todas las páginas del admin.
        """
        context = super().each_context(request)
        context.update({
            'site_header': self.site_header,
            'site_title': self.site_title,
            'site_url': '/',
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
        })
        return context

# Crear y configurar el admin personalizado
admin_site = CustomAdminSite(name='custom_admin')

# Registrar los modelos en el admin personalizado
admin_site.register(User, CustomUserAdmin)
admin_site.register(Group, CustomGroupAdmin)

# Configurar el sitio de administración por defecto
admin.site = admin_site
admin.sites.site = admin_site

# Asegurarse de que el sitio esté registrado
if not admin.site.is_registered(User):
    admin.site.register(User, CustomUserAdmin)
if not admin.site.is_registered(Group):
    admin.site.register(Group, CustomGroupAdmin)
