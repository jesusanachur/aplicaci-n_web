from django.db import migrations

def create_admin_permissions(apps, schema_editor):
    """
    Crea los permisos personalizados para el panel de administración.
    """
    from django.contrib.auth.management import create_permissions
    from django.apps import apps as django_apps
    
    # Asegurarse de que los permisos estén creados
    for app_config in django_apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

class Migration(migrations.Migration):
    # Eliminamos la dependencia que causa el error
    dependencies = [
        # No hay dependencias necesarias
    ]

    operations = [
        migrations.RunPython(create_admin_permissions, reverse_code=migrations.RunPython.noop),
    ]
