from django.contrib.auth.decorators import user_passes_test
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def superuser_required(view_func):
    """
    Decorador para vistas que requieren privilegios de superusuario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='admin:login',
        redirect_field_name=None
    )
    return actual_decorator(view_func)

@superuser_required
def dashboard_stats(request):
    """
    Vista para mostrar estadísticas en el dashboard del administrador.
    """
    from django.db.models import Count, Q
    from datetime import timedelta
    from django.utils import timezone
    import json
    
    # Obtener el conteo total de usuarios
    user_count = User.objects.count()
    
    # Obtener el conteo de usuarios activos en los últimos 30 días
    active_users = User.objects.filter(
        last_login__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Obtener estadísticas de los últimos 7 días
    today = timezone.now().date()
    date_range = [today - timedelta(days=x) for x in range(6, -1, -1)]
    
    # Obtener el conteo de nuevos usuarios por día
    new_users_data = []
    for date in date_range:
        count = User.objects.filter(
            date_joined__date=date
        ).count()
        new_users_data.append({
            'date': date.strftime('%a, %b %d'),
            'count': count
        })
    
    # Obtener el conteo de inicios de sesión por día
    login_data = []
    for date in date_range:
        count = User.objects.filter(
            last_login__date=date
        ).count()
        login_data.append({
            'date': date.strftime('%a, %b %d'),
            'count': count
        })
    
    # Obtener conteos adicionales (ejemplo: estudiantes, profesores, cursos)
    # Ajusta según tus modelos
    try:
        from appEstudiantes.models import Estudiante
        student_count = Estudiante.objects.count()
    except ImportError:
        student_count = 0
    
    try:
        from appProfesores.models import Profesor
        teacher_count = Profesor.objects.count()
    except ImportError:
        teacher_count = 0
    
    try:
        from appCursos.models import Curso
        course_count = Curso.objects.count()
    except ImportError:
        course_count = 0
    
    context = {
        'title': 'Panel de Administración',
        'user_count': user_count,
        'active_users': active_users,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'new_users_data': json.dumps(new_users_data),
        'login_data': json.dumps(login_data),
        'opts': User._meta,
        'is_popup': False,
        'is_nav_sidebar_enabled': True,
        'available_apps': request.user.get_all_permissions(),
    }
    
    return TemplateResponse(request, 'admin/dashboard_stats.html', context)
