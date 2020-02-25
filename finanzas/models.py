from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from maestro.models import Caja, Proveedor
from clientes.models import Cliente


class Jornada(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT)
    fechahora_inicio = models.DateTimeField(auto_now_add=True)
    fechahora_fin = models.DateTimeField(null=True, blank=True)
    asignado_inicio = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado_inicio', )
    asignado_fin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado_fin', blank=True, null=True)
    monto_actual = models.DecimalField(max_digits=8, decimal_places=2)
    monto_apertura = models.DecimalField(max_digits=8, decimal_places=2)
    monto_cierre = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estado = models.BooleanField(default=True)


class DetalleJornada(models.Model):
    TIPO_CHOICES = (
        ('1', 'INGRESO'),
        ('2', 'EGRESO'),
    )
    jornada = models.ForeignKey(Jornada, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    is_espontaneo = models.BooleanField(default=False)
    target = models.IntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fechahora = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)


class CuentaCliente(models.Model):
    DURACION_CHOICES = (
        ('1', '7 DIAS'),
        ('2', '14 DIAS'),
        ('3', '21 DIAS'),
        ('4', '30 DIAS'),
    )
    ESTADO_CHOICES = (
        ('1', 'PENDIENTE'),
        ('2', 'PAGADO'),
    )
    TIPO_CHOICES = (
        ('1', 'CONTADO'),
        ('2', 'CREDITO'),
    )
    duracion = models.CharField(max_length=1, choices=DURACION_CHOICES)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    fechahora_caducidad = models.DateTimeField(blank=True, null=True)
    monto_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_amortizado = models.DecimalField(max_digits=8, decimal_places=2)
    monto_deuda = models.DecimalField(max_digits=8, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)


class PagoCliente(models.Model):
    TIPO_CHOICES = (
        ('1', 'EFECTIVO'),
        ('2', 'DEPOSITO'),
        ('3', 'CHEQUE'),
    )
    BANCO_CHOICES = (
        ('0', 'NO APLICA'),
        ('1', 'BANCO CONTINENTAL'),
        ('2', 'BANCO DE CRÉDITO DEL PERÚ'),
        ('3', 'BANCO DE LA NACIÓN'),
    )
    fechahora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    cuentacliente = models.ForeignKey(CuentaCliente, on_delete=models.PROTECT)
    recibo = models.CharField(max_length=50, blank=True, null=True)
    banco = models.CharField(max_length=1, choices=BANCO_CHOICES, blank=True, null=True)
    codigo = models.CharField(max_length=150, blank=True, null=True)
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)


class CuentaProveedor(models.Model):
    DURACION_CHOICES = (
        ('1', '7 DIAS'),
        ('2', '14 DIAS'),
        ('3', '21 DIAS'),
        ('4', '30 DIAS'),
    )
    ESTADO_CHOICES = (
        ('1', 'PENDIENTE'),
        ('2', 'PAGADO'),
        ('3', 'CANCELADO'),
    )
    TIPO_CHOICES = (
        ('1', 'CONTADO'),
        ('2', 'CREDITO'),
    )
    duracion = models.CharField(max_length=1, choices=DURACION_CHOICES)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    fechahora_caducidad = models.DateTimeField()
    monto_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_amortizado = models.DecimalField(max_digits=8, decimal_places=2)
    monto_deuda = models.DecimalField(max_digits=8, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)


class PagoProveedor(models.Model):
    TIPO_CHOICES = (
        ('1', 'EFECTIVO'),
        ('2', 'DEPOSITO'),
        ('3', 'CHEQUE'),
    )
    BANCO_CHOICES = (
        ('0', 'NO APLICA'),
        ('1', 'BANCO CONTINENTAL'),
        ('2', 'BANCO DE CRÉDITO DEL PERÚ'),
        ('3', 'BANCO DE LA NACIÓN'),
    )
    fechahora = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    cuentaproveedor = models.ForeignKey(CuentaProveedor, on_delete=models.PROTECT)
    banco = models.CharField(max_length=1, choices=BANCO_CHOICES)
    codigo = models.CharField(max_length=150)
    recibo = models.CharField(max_length=50)
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)
