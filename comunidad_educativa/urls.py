"""
URL configuration for comunidad_educativa project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# Importar vistas locales
from . import views

# Configuración de manejadores de error
handler404 = "comunidad_educativa.views.handler404"
handler500 = "comunidad_educativa.views.handler500"

# Configuración de URLs
urlpatterns = [
    # Página de inicio
    path("", views.home_view, name="home"),
    
    # Panel de administración
    path('admin/', admin.site.urls),
    
    # URLs de aplicaciones
    path("comunidad/", include("appComunidad.urls")),
    path("estudiantes/", include("appEstudiantes.urls")),
    path("profesores/", include("appProfesores.urls")),
    
    # Autenticación
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    
    # Perfil de usuario
    path("profile/", views.ProfileView.as_view(), name="profile"),
    
    # Registro
    path("register/", views.register_view, name="register"),
    path("register/student/", views.register_student_view, name="register_student"),
    path("register/teacher/", views.register_teacher_view, name="register_teacher"),

    # Password reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
