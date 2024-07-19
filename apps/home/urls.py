from django.urls import path, re_path, include
from . import views
from .views import index, update_event
from .admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    # The home page
<<<<<<< HEAD
    path('', views.pages, name='home'),
    path('perfil/', views.perfil, name='perfil'),
=======
    path('index/', views.index, name='index'),
>>>>>>> 58d0b0a97cd6fba154d3c77d543d8d5ca6caea11
    path('seccion/', views.seccion, name='seccion'),
    path('alumnos/<int:asignatura_id>/', views.alumnos, name='alumnos'),
    path('notasal/', views.notasal, name='notasal'),
    path('analisisnota/', views.analisisnota, name='analisisnota'),
    path('testvocacional/', views.testvocacional, name='testvocacional'),
    path('cuestionario/', views.cuestionario, name='cuestionario'),
<<<<<<< HEAD
    path('asignaturas/<int:id_añocurso>/', views.asignaturas, name='asignaturas'),
    path('guardar_calificaciones/', views.guardar_calificaciones, name='guardar_calificaciones'),
=======
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('update_event/', update_event, name='update_event'),



>>>>>>> 58d0b0a97cd6fba154d3c77d543d8d5ca6caea11

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]



