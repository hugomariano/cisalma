from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import Compra, DetalleCompra
from maestro.models import Producto, Categoria, Sucursal, Almacen, Proveedor
from .models import Stock, Kardex
from clientes.models import Cliente
# Model import<--

# Utils import-->
from maestro.utils import empresa_list
# Utils import<--


class DetalleCompraForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_pedido', 'total']


class DetalleCompraOfertaForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_pedido']


class StockFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StockFiltroForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['categoria'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['almacen'] = forms.ModelChoiceField(queryset=Almacen.objects.filter(
            sucursal__empresa__in=empresa_list(user)), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['almacen'].empty_label = None


class KardexFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(KardexFiltroForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['categoria'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['almacen'] = forms.ModelChoiceField(queryset=Almacen.objects.filter(
            sucursal__empresa__in=empresa_list(user)), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['almacen'].empty_label = None
        self.fields['tipo'] = forms.ChoiceField(choices=Kardex.TIPO_MOVIMIENTO_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                    attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fecha_inicio'] = forms.CharField(required=False,
                                                      widget=forms.TextInput(
                                                          attrs={'id': 'fecha_inicio', 'placeholder': 'Inicio',
                                                                 'class': 'form-control'}))
        self.fields['fecha_fin'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(
                                                       attrs={'id': 'fecha_fin', 'placeholder': 'Fin',
                                                              'class': 'form-control'}))


class RecepcionFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RecepcionFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None


class EntregaFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(EntregaFiltroForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['cliente'].empty_label = None


class KardexReportFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(KardexReportFiltroForm, self).__init__(*args, **kwargs)
        self.fields['productos'] = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False,
                                                          widget=forms.Select(
                                                              attrs={'class': 'default-select2 form-control'}))
        self.fields['productos'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                         widget=forms.Select(
                                                             attrs={'class': 'default-select2 form-control'}))
        self.fields['sucursal'].empty_label = None

        self.fields['date_inicio'] = forms.CharField(required=True,
                                                     widget=forms.TextInput(
                                                         attrs={'id': 'date_inicio', 'placeholder': 'Inicio',
                                                                'class': 'form-control'}))
        self.fields['date_fin'] = forms.CharField(required=True,
                                                  widget=forms.TextInput(
                                                      attrs={'id': 'date_fin', 'placeholder': 'Fin',
                                                             'class': 'form-control'}))


class StockCambioForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(StockCambioForm, self).__init__(*args, **kwargs)
        self.fields['stock'] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Stock Nuevo'}),
                                                  required=True)
        self.fields['producto'] = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'prod_inp'}), required=True)
