# Generated by Django 2.0.4 on 2018-11-21 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentacliente',
            name='monto_deuda',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cuentaproveedor',
            name='monto_deuda',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuentacliente',
            name='tipo',
            field=models.CharField(choices=[('1', 'CONTADO'), ('2', 'CREDITO')], max_length=1),
        ),
        migrations.AlterField(
            model_name='cuentaproveedor',
            name='tipo',
            field=models.CharField(choices=[('1', 'CONTADO'), ('2', 'CREDITO')], max_length=1),
        ),
        migrations.AlterField(
            model_name='pagocliente',
            name='banco',
            field=models.CharField(blank=True, choices=[('0', 'NO APLICA'), ('1', 'BANCO CONTINENTAL'), ('2', 'BANCO DE CRÉDITO DEL PERÚ'), ('3', 'BANCO DE LA NACIÓN')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='pagoproveedor',
            name='banco',
            field=models.CharField(choices=[('0', 'NO APLICA'), ('1', 'BANCO CONTINENTAL'), ('2', 'BANCO DE CRÉDITO DEL PERÚ'), ('3', 'BANCO DE LA NACIÓN')], max_length=1),
        ),
    ]
