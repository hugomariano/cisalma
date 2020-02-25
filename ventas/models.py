from django.db import models
from maestro.models import Sucursal, TipoComprobante, Producto, PresentacionxProducto, Impuesto
from clientes.models import Cliente
from django.contrib.auth.models import User


# Create your models here.
class Venta(models.Model):
    ESTADO_ENVIO_CHOICES = (
        ('1', 'GENERADO'),
        # ('2', 'CONVERTIDO A PEDIDO'),
        ('3', 'VENTA'),
        ('4', 'ANULADO'),
        ('5', 'OCUPADO'),
    )
    ESTADO_PAGO_CHOICES = (
        ('1', 'EN DEUDA'),
        ('2', 'PAGADO'),
    )
    TIPO_PAGO_CHOICES = (
        ('1', 'CONTADO'),
        ('2', 'CREDITO'),
    )
    TIPO_CHOICES = (
        ('1', 'VENTA DIRECTA'),
    )
    asignado = models.ForeignKey(User, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    estado = models.CharField(max_length=1, choices=ESTADO_ENVIO_CHOICES, default=1)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default=1)
    tipo_pago = models.CharField(max_length=1, choices=TIPO_PAGO_CHOICES, default=1)
    estado_pago = models.CharField(max_length=1, choices=ESTADO_PAGO_CHOICES, default=1)
    fechahora_creacion = models.DateTimeField(auto_now_add=True)
    tipo_comprobante = models.ForeignKey(TipoComprobante, on_delete=models.PROTECT, null=True, blank=True)
    serie_comprobante = models.CharField(max_length=10, null=True, blank=True)
    numero_comprobante = models.CharField(max_length=10, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True, null=True)
    impuesto_monto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_pagado = models.BooleanField(default=False)
    is_entregado = models.BooleanField(default=False)


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    presentacionxproducto = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT)
    cantidad_presentacion_pedido = models.IntegerField(blank=True, null=True)
    cantidad_presentacion_entrega = models.IntegerField(blank=True, null=True)
    cantidad_unidad_pedido = models.IntegerField(blank=True, null=True)
    cantidad_unidad_entrega = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    sub_total = models.DecimalField(max_digits=8, decimal_places=2)
    descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    impuesto = models.ManyToManyField(Impuesto)
    impuesto_monto = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    descuento_adicional = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=8, decimal_places=2)
    is_oferta = models.BooleanField(default=False)
    is_nodeseado = models.BooleanField(default=True)
    is_checked = models.BooleanField(default=False)


class OfertaVenta(models.Model):
    TIPO_DURACION_CHOICES = (
        ('1', 'TEMPORAL'),
        ('2', 'PERMANENTE'),
    )
    TIPO_CHOICES = (
        ('1', 'PRODUCTO'),
        ('2', 'DESCUENTO MONETARIO'),
        ('3', 'DESCUENTO PORCENTUAL'),
    )
    is_active = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    tipo_duracion = models.CharField(max_length=1, choices=TIPO_DURACION_CHOICES)
    producto_oferta = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto_oferta_venta')
    presentacion_oferta = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                            related_name='presentacion_oferta_venta')
    cantidad_oferta = models.IntegerField()
    cantidad_unidad_oferta = models.IntegerField(blank=True, null=True)
    producto_retorno = models.ForeignKey(Producto, on_delete=models.PROTECT, blank=True, null=True,
                                         related_name='producto_retorno_venta')
    presentacion_retorno = models.ForeignKey(PresentacionxProducto, on_delete=models.PROTECT,
                                             related_name='presentacion_retorno_venta', blank=True, null=True)
    retorno = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    fechahora_inicio = models.DateTimeField(blank=True, null=True)
    fechahora_fin = models.DateTimeField(blank=True, null=True)
    stock_limite = models.IntegerField(blank=True, null=True)
    stock_faltante = models.IntegerField(blank=True, null=True)
