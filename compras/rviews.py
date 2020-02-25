from .serializers import ProductoSerializer, PresentacionxProductoSerializer, PrecioTentativoSerializer
from rest_framework import generics
from maestro.models import CatalogoxProveedor, Producto, PresentacionxProducto


class ProductosListView(generics.ListAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        if 'q' in self.request.GET:
            queryset = Producto.objects.filter(descripcion__icontains=self.request.GET['q'])
        else:
            queryset = Producto.objects.all()
        return queryset


class PresentacionxProductoListView(generics.ListAPIView):
    serializer_class = PresentacionxProductoSerializer

    def get_queryset(self):
        queryset = PresentacionxProducto.objects.filter(producto__in=self.kwargs['producto'].split(','))\
            .order_by('producto')
        return queryset


class PrecioTentativoView(generics.ListAPIView):
    serializer_class = PrecioTentativoSerializer

    def get_queryset(self):
        try:
            queryset = CatalogoxProveedor.objects.filter(presentacionxproducto=self.kwargs['pk'])
        except CatalogoxProveedor.DoesNotExist:
            queryset = CatalogoxProveedor.objects.none()
        return queryset
