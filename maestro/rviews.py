from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics


class ProductosListView(generics.ListAPIView):
    serializer_class = ProductoSerializer

    def get_queryset(self):
        if 'q' in self.request.GET:
            queryset = Producto.objects.filter(descripcion__icontains=self.request.GET['q'])
        else:
            queryset = Producto.objects.all()
        return queryset
