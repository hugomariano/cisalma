from django.db import models
from maestro.models import Producto, Almacen, TipoComprobante
from compras.models import DetalleCompra
from ventas.models import DetalleVenta


# Create your models here.
class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)


class Kardex(models.Model):
    TIPO_MOVIMIENTO_CHOICES = (
        (1, 'ENTRADA'),
        (2, 'SALIDA')
    )
    TIPO_DETALLE_CHOICES = (
        (1, 'COMPRA'),
        (2, 'VENTA'),
        (3, 'REEMBOLSO COMPRA'),
        (4, 'REEMBOLSO VENTA'),
    )

    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo_movimiento = models.CharField(max_length=1, choices=TIPO_MOVIMIENTO_CHOICES)
    tipo_detalle = models.CharField(max_length=1, choices=TIPO_DETALLE_CHOICES)
    cantidad = models.IntegerField()
    cantidad_entrada = models.IntegerField(blank=True, null=True)
    cantidad_salida = models.IntegerField(blank=True, null=True)
    precio_unitario_entrada = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    precio_unitario_salida = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_entrada = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    total_salida = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cantidad_saldo = models.IntegerField()
    precio_unitario_saldo = models.DecimalField(max_digits=8, decimal_places=2)
    total_saldo = models.DecimalField(max_digits=8, decimal_places=2)
    detallecompra = models.ForeignKey(DetalleCompra, on_delete=models.PROTECT, blank=True, null=True)
    detalleventa = models.ForeignKey(DetalleVenta, on_delete=models.PROTECT, blank=True, null=True)
    fechahora = models.DateTimeField(auto_now_add=True)
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.PROTECT, null=True, blank=True)
    serie_comprobante = models.CharField(max_length=10, null=True, blank=True)
    numero_comprobante = models.CharField(max_length=10, null=True, blank=True)

