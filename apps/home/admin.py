from django.contrib import admin
from .models import AñoCurso, Alumno, Asignatura, Profesor, Prediccion, Calificaciones, TipoUsuario
from django.contrib import admin
from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    site_header = "Sistema de Administración"
    site_title = "Administración"
    index_title = "Panel de Control"

admin_site = MyAdminSite(name='myadmin')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'correo', 'celular']  

    def nombre_completo(self, obj):
        return f"{obj.p_nombre} {obj.apellido_pat} {obj.apellido_mat}"
    nombre_completo.short_description = 'Nombre completo'

admin.site.register(TipoUsuario)
@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'direccion', 'numero_apoderado']  

    def nombre_completo(self, obj):
        return f"{obj.p_nombre} {obj.apellido_pat} {obj.apellido_mat}"
    nombre_completo.short_description = 'Nombre completo'

admin.site.register(AñoCurso)
admin.site.register(Asignatura)
admin.site.register(Prediccion)
admin.site.register(Calificaciones)

