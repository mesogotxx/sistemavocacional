# Generated by Django 4.2.9 on 2024-05-06 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id_tipousuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='tipo_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.tipousuario'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profesor',
            name='tipo_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.tipousuario'),
            preserve_default=False,
        ),
    ]
