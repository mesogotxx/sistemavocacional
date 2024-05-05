from django.db import models
from django.contrib.auth.models import User


class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    p_nombre = models.CharField(max_length=45, verbose_name='Primer nombre')
    s_nombre = models.CharField(max_length=45, blank=True, null=True, verbose_name='Segundo nombre')
    apellido_pat = models.CharField(max_length=45, verbose_name='Apellido paterno')
    apellido_mat = models.CharField(max_length=45, verbose_name='apellido materno')
    fecha_nac = models.DateField()
    fecha_ingreso = models.DateField()
    direccion = models.CharField(max_length=45, blank=True, null=True, verbose_name='Dirección')
    numero_apoderado = models.IntegerField(blank=True, null=True, verbose_name='Celular apoderado')
    
    def __str__(self):
        return f"{self.p_nombre} {self.apellido_pat} {self.apellido_mat}"
    
    
class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    p_nombre = models.CharField(max_length=45, verbose_name='Primer nombre')
    s_nombre = models.CharField(max_length=45, blank=True, null=True, verbose_name='Segundo nombre')
    apellido_pat = models.CharField(max_length=45, verbose_name='Apellido paterno')
    apellido_mat = models.CharField(max_length=45, verbose_name='Aperllido materno')
    correo = models.CharField(max_length=45, verbose_name='Correo')
    celular = models.IntegerField(blank=True, null=True, verbose_name='Celular')

    def __str__(self):
        return f"{self.p_nombre} {self.apellido_pat} {self.apellido_mat}"
    
class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    nombre_asig = models.CharField(max_length=45, verbose_name='Asignatura')
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, verbose_name='Profesor')

    def __str__(self):
        return self.nombre_asig

class Calificaciones(models.Model):
    id_calificaciones = models.AutoField(primary_key=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Calificacion')
    fecha = models.DateField()
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, verbose_name='Asignatura')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name='Alumno')

    def __str__(self):
        return f"{self.calificacion} - {self.asignatura} - {self.alumno}"

class Prediccion(models.Model):
    id_prediccion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    sugerencia = models.CharField(max_length=45, blank=True, null=True, verbose_name='Sugerencia')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, verbose_name='Alumno')

    def __str__(self):
        return f"{self.fecha} - {self.alumno}"


