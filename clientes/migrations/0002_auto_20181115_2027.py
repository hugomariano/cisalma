# Generated by Django 2.0.4 on 2018-11-16 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='credito_disponible',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='cliente',
            name='deuda_actual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='cliente',
            name='limite_credito',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
