# Generated by Django 2.0.4 on 2018-10-29 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='AccionxVista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Accion')),
            ],
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionAccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accionxvista', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.AccionxVista')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='CatalogoxProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_tentativo', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('precio_base', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('nivel', models.SmallIntegerField()),
                ('padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maestro.Categoria')),
                ('padre_total', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='padretotal', to='maestro.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('ruc', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Impuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('abreviatura', models.CharField(max_length=10)),
                ('porcentaje', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PrecioxProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fechahora', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='PresentacionxProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Presentacion')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('precio_compra', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('utilidad_monetaria', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('ruc', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=150)),
                ('responsable', models.CharField(max_length=150)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='TipoComprobante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=150)),
                ('codigo_sunat', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Vista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Modulo')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='catalogo',
            field=models.ManyToManyField(to='maestro.Sucursal'),
        ),
        migrations.AddField(
            model_name='producto',
            name='categorias',
            field=models.ManyToManyField(to='maestro.Categoria'),
        ),
        migrations.AddField(
            model_name='producto',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Empresa'),
        ),
        migrations.AddField(
            model_name='presentacionxproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Producto'),
        ),
        migrations.AddField(
            model_name='precioxproveedor',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Producto'),
        ),
        migrations.AddField(
            model_name='precioxproveedor',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Proveedor'),
        ),
        migrations.AddField(
            model_name='catalogoxproveedor',
            name='presentacionxproducto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='maestro.PresentacionxProducto'),
        ),
        migrations.AddField(
            model_name='catalogoxproveedor',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Producto'),
        ),
        migrations.AddField(
            model_name='catalogoxproveedor',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maestro.Proveedor'),
        ),
        migrations.AddField(
            model_name='caja',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Sucursal'),
        ),
        migrations.AddField(
            model_name='almacen',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Sucursal'),
        ),
        migrations.AddField(
            model_name='accionxvista',
            name='vista',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='maestro.Vista'),
        ),
    ]