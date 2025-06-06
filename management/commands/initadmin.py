from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superusuario ya existe.'))
            return

        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Cambia esto en producción

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Superusuario creado con éxito. Usuario: {username}, Contraseña: {password}')
        )
        self.stdout.write(self.style.WARNING('¡IMPORTANTE! Cambia la contraseña del administrador después del primer inicio de sesión.'))
