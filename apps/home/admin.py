from django.contrib import admin
from .models import Alumno, Asignatura, Profesor, Prediccion, Calificaciones

admin.site.register(Alumno)
admin.site.register(Asignatura)
admin.site.register(Profesor)
admin.site.register(Prediccion)
admin.site.register(Calificaciones)
