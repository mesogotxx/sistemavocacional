from django.urls import path, re_path, include
from . import views
from .views import index, update_event
from .admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    # The home page
    path('index/', views.index, name='index'),
    path('seccion/', views.seccion, name='seccion'),
    path('alumnos/<int:asignatura_id>/', views.alumnos, name='alumnos'),
    path('notasal/', views.notasal, name='notasal'),
    path('analisisnota/', views.analisisnota, name='analisisnota'),
    path('testvocacional/', views.testvocacional, name='testvocacional'),
    path('cuestionario/', views.cuestionario, name='cuestionario'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('update_event/', update_event, name='update_event'),




    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]



