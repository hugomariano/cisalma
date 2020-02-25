# Generated by Django 2.0.4 on 2018-11-04 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maestro', '0002_grupo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Grupo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='asignacionaccion',
            name='usuario',
        ),
        migrations.AddField(
            model_name='asignacionaccion',
            name='grupo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maestro.Grupo'),
            preserve_default=False,
        ),
    ]
