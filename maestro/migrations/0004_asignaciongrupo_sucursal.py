# Generated by Django 2.0.4 on 2018-11-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maestro', '0003_auto_20181104_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignaciongrupo',
            name='sucursal',
            field=models.ManyToManyField(to='maestro.Sucursal'),
        ),
    ]
