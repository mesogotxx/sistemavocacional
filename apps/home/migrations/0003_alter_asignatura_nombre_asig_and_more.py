# Generated by Django 4.2.9 on 2024-05-05 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_alumno_apellido_mat_alter_alumno_apellido_pat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='nombre_asig',
            field=models.CharField(max_length=45, verbose_name='Asignatura'),
        ),
        migrations.AlterField(
            model_name='asignatura',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.profesor', verbose_name='Profesor'),
        ),
        migrations.AlterField(
            model_name='calificaciones',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.alumno', verbose_name='Alumno'),
        ),
        migrations.AlterField(
            model_name='calificaciones',
            name='asignatura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.asignatura', verbose_name='Asignatura'),
        ),
        migrations.AlterField(
            model_name='calificaciones',
            name='calificacion',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Calificacion'),
        ),
        migrations.AlterField(
            model_name='prediccion',
            name='alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.alumno', verbose_name='Alumno'),
        ),
        migrations.AlterField(
            model_name='prediccion',
            name='sugerencia',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Sugerencia'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='apellido_mat',
            field=models.CharField(max_length=45, verbose_name='Aperllido materno'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='apellido_pat',
            field=models.CharField(max_length=45, verbose_name='Apellido paterno'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='celular',
            field=models.IntegerField(blank=True, null=True, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='correo',
            field=models.CharField(max_length=45, verbose_name='Correo'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='p_nombre',
            field=models.CharField(max_length=45, verbose_name='Primer nombre'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='s_nombre',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Segundo nombre'),
        ),
    ]
