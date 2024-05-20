from django.urls import path, re_path
from apps.home import views
from .admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    # The home page
    path('', views.perfil, name='home'),
    path('seccion/', views.seccion, name='seccion'),
    path('alumnos/', views.alumnos, name='alumnos'),
    path('notas/', views.notas, name='notas'),
    path('testvocacional/', views.testvocacional, name='testvocacional'),
    path('cuestionario/', views.cuestionario, name='cuestionario'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
