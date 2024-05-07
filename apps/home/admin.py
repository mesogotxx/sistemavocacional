from django.contrib import admin
from .models import AñoCurso, Alumno, Asignatura, Profesor, Prediccion, Calificaciones, TipoUsuario
from django.contrib import admin
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = "Sistema de Administración"
    site_title = "Administración"
    index_title = "Panel de Control"

admin_site = MyAdminSite(name='myadmin')

admin.site.register(TipoUsuario)
admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(AñoCurso)
admin.site.register(Asignatura)
admin.site.register(Prediccion)
admin.site.register(Calificaciones)
