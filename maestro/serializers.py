from .models import Producto
from rest_framework import serializers
from datetime import date


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = ['id', 'descripcion']
