from maestro.models import Producto, PresentacionxProducto, Presentacion, CatalogoxProveedor
from ventas.models import OfertaVenta
from rest_framework import serializers


class PresentacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Presentacion
        fields = ['id', 'descripcion']


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id', 'descripcion']


class PresentacionxProductoSerializer(serializers.ModelSerializer):
    presentacion = PresentacionSerializer()

    class Meta:
        model = PresentacionxProducto
        fields = ['id', 'presentacion', 'producto', 'cantidad']


# Usado para obtener el precio base del producto.
class CatalogoxProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogoxProveedor
        fields = ['id', 'precio_base', 'producto']


class ProductoPrecioVentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id', 'precio_venta', 'descripcion']


class OfertaVentaSerializer(serializers.ModelSerializer):
    presentacion_oferta = PresentacionxProductoSerializer()
    presentacion_retorno = PresentacionxProductoSerializer()
    producto_retorno = ProductoSerializer()
    producto_oferta = ProductoSerializer()

    class Meta:
        model = OfertaVenta
        fields = ['id', 'tipo', 'producto_oferta', 'presentacion_oferta', 'cantidad_oferta',
                  'producto_retorno', 'presentacion_retorno', 'retorno',
                  'fechahora_fin', 'stock_limite', 'stock_faltante']
