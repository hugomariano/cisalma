from maestro.models import Producto, PresentacionxProducto
from .serializers import PresentacionxProductoSerializer, ProductoPrecioVentaSerializer, OfertaVentaSerializer
from rest_framework import generics
from maestro.models import CatalogoxProveedor, PresentacionxProducto, Sucursal
from ventas.models import OfertaVenta
from almacen.models import Stock
from rest_framework.response import Response
from django.db.models import Sum


class ProductoDetailsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        presentacionxproducto = PresentacionxProducto.objects.filter(producto__in=self.kwargs['producto']
                                                                     .split(',')).order_by('producto')
        producto = Producto.objects.filter(pk__in=self.kwargs['producto'].split(',')).order_by('id')
        ofertaventa = OfertaVenta.objects.filter(producto_oferta__in=self.kwargs['producto']
                                                 .split(','), sucursal=self.kwargs['sucursal']
                                                 ).order_by('producto_oferta')
        context = {
            "request": request,
        }

        presentacionserializer = PresentacionxProductoSerializer(presentacionxproducto, many=True, context=context)
        productoserializer = ProductoPrecioVentaSerializer(producto, many=True, context=context)
        ofertaventaserializer = OfertaVentaSerializer(ofertaventa, many=True, context=context)

        response = {'presentacion': presentacionserializer.data, 'precio':  productoserializer.data,
                    'oferta': ofertaventaserializer.data}

        return Response(response)


class ValidarStockView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        presentacionxproducto = PresentacionxProducto.objects.get(pk=self.kwargs['presentacion'])
        stock = Stock.objects.filter(almacen__sucursal=Sucursal.objects.get(pk=self.kwargs['sucursal']))
        stock = stock.filter(producto=presentacionxproducto.producto_id)
        stock = stock.annotate(Sum('cantidad'))
        cantidad_stock = 0
        for s in stock:
            cantidad_stock = s.cantidad__sum
            break
        cantidad_pedido = int(self.kwargs['cantidad'])
        cantidad_stock_presentacion = cantidad_stock // presentacionxproducto.cantidad
        if cantidad_pedido > cantidad_stock_presentacion:
            response = {'status': 0, 'stock': cantidad_stock_presentacion, 'maximo':  cantidad_stock_presentacion}
        else:
            response = {'status': 1, 'stock': cantidad_stock_presentacion, 'maximo': cantidad_pedido}
        return Response(response)
