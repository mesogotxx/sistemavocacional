# Generated by Django 4.2.9 on 2024-05-20 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_tipousuario_alumno_tipo_usuario_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumno',
            options={'verbose_name_plural': 'Alumnos'},
        ),
        migrations.AlterModelOptions(
            name='asignatura',
            options={'verbose_name_plural': 'Asignaturas'},
        ),
        migrations.AlterModelOptions(
            name='añocurso',
            options={'verbose_name_plural': 'Cursos'},
        ),
        migrations.AlterModelOptions(
            name='calificaciones',
            options={'verbose_name_plural': 'Calificaciones'},
        ),
        migrations.AlterModelOptions(
            name='prediccion',
            options={'verbose_name_plural': 'Predicciones'},
        ),
        migrations.AlterModelOptions(
            name='profesor',
            options={'verbose_name_plural': 'Profesores'},
        ),
        migrations.AlterModelOptions(
            name='tipousuario',
            options={'verbose_name_plural': 'Tipo Usuarios'},
        ),
        migrations.RemoveField(
            model_name='asignatura',
            name='profesor',
        ),
        migrations.AddField(
            model_name='profesor',
            name='asignaturas',
            field=models.ManyToManyField(blank=True, related_name='profesores', to='home.asignatura'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='apellido_mat',
            field=models.CharField(max_length=45, verbose_name='Apellido materno'),
        ),
    ]
