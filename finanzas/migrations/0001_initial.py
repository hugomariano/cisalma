# Generated by Django 2.0.4 on 2018-10-29 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maestro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuentaCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion', models.CharField(choices=[('1', '7 DIAS'), ('2', '14 DIAS'), ('3', '21 DIAS'), ('4', '30 DIAS')], max_length=1)),
                ('estado', models.CharField(choices=[('1', 'PENDIENTE'), ('2', 'PAGADO')], max_length=1)),
                ('tipo', models.CharField(choices=[('1', 'CREDITO'), ('2', 'CONTADO')], max_length=1)),
                ('fechahora_caducidad', models.DateTimeField(blank=True, null=True)),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('monto_amortizado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion', models.CharField(choices=[('1', '7 DIAS'), ('2', '14 DIAS'), ('3', '21 DIAS'), ('4', '30 DIAS')], max_length=1)),
                ('estado', models.CharField(choices=[('1', 'PENDIENTE'), ('2', 'PAGADO'), ('3', 'CANCELADO')], max_length=1)),
                ('tipo', models.CharField(choices=[('1', 'CREDITO'), ('2', 'CONTADO')], max_length=1)),
                ('fechahora_caducidad', models.DateTimeField()),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('monto_amortizado', models.DecimalField(decimal_places=2, max_digits=8)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleJornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('1', 'INGRESO'), ('2', 'EGRESO')], max_length=1)),
                ('is_espontaneo', models.BooleanField(default=False)),
                ('target', models.IntegerField(blank=True, null=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fechahora', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('asignado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechahora_inicio', models.DateTimeField(auto_now_add=True)),
                ('fechahora_fin', models.DateTimeField(blank=True, null=True)),
                ('monto_actual', models.DecimalField(decimal_places=2, max_digits=8)),
                ('monto_apertura', models.DecimalField(decimal_places=2, max_digits=8)),
                ('monto_cierre', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('asignado_fin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='asignado_fin', to=settings.AUTH_USER_MODEL)),
                ('asignado_inicio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asignado_inicio', to=settings.AUTH_USER_MODEL)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Caja')),
            ],
        ),
        migrations.CreateModel(
            name='PagoCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechahora', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('1', 'EFECTIVO'), ('2', 'DEPOSITO'), ('3', 'CHEQUE')], max_length=1)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('banco', models.CharField(blank=True, choices=[('1', 'BANCO DE CRÉDITO DEL PERÚ'), ('2', 'BANCO CONTINENTAL'), ('3', 'BANCO DE LA NACIÓN')], max_length=1, null=True)),
                ('codigo', models.CharField(blank=True, max_length=150, null=True)),
                ('asignado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('cuentacliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finanzas.CuentaCliente')),
            ],
        ),
        migrations.CreateModel(
            name='PagoProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechahora', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('1', 'EFECTIVO'), ('2', 'DEPOSITO'), ('3', 'CHEQUE')], max_length=1)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('banco', models.CharField(choices=[('1', 'BANCO DE CRÉDITO DEL PERÚ'), ('2', 'BANCO CONTINENTAL'), ('3', 'BANCO DE LA NACIÓN')], max_length=1)),
                ('codigo', models.CharField(max_length=150)),
                ('asignado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('cuentaproveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finanzas.CuentaProveedor')),
            ],
        ),
        migrations.AddField(
            model_name='detallejornada',
            name='jornada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finanzas.Jornada'),
        ),
    ]
