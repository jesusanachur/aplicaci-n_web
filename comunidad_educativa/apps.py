from django.apps import AppConfig
from django.contrib import admin

class ComunidadEducativaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comunidad_educativa'
    
    def ready(self):
        # Configuración personalizada del admin
        admin.site.site_header = "Panel de Administración"
        admin.site.site_title = "Sitio de Administración"
        admin.site.index_title = "Bienvenido al Panel de Administración"
