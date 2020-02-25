from django import forms
from django.forms import ModelChoiceField

# Model import-->
from compras.models import Compra, DetalleCompra
from maestro.models import Producto, Proveedor, TipoComprobante, Impuesto, Almacen
# Model import<--
# Utils import-->
from maestro.utils import empresa_list
# Utils import<--


class CompraCreateForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['proveedor', 'almacen']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'almacen': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CompraCreateForm, self).__init__(*args, **kwargs)
        self.fields['almacen'] = forms.ModelChoiceField(queryset=Almacen.objects.filter(
            sucursal__empresa__in=empresa_list(user)), widget=forms.Select(
            attrs={'class': 'default-select2 form-control'}))
        self.fields['almacen'].empty_label = None
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.filter(
            empresa__in=empresa_list(user)), widget=forms.Select(attrs={'class': 'default-select2 form-control'}))
        self.fields['proveedor'].empty_label = None


class CompraEditForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['tipo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CompraEditForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].empty_label = None
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices]


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion_pedido', 'precio']
        widgets = {
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
        }

    def __init__(self, *args, **kwargs):
        has_data = kwargs.pop('has_data')
        proveedor = kwargs.pop('proveedor')
        super(DetalleCompraForm, self).__init__(*args, **kwargs)
        if has_data:
            self.fields['producto'] = forms.ModelChoiceField(
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'default-select2 form-control producto'}),
            )
            self.fields['producto'].empty_label = None
            self.fields['cantidad_presentacion_pedido'] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
            self.fields['precio'] = forms.DecimalField(
                widget=forms.NumberInput(attrs={'class': 'form-control precio', 'step': '.01'})
            )
        else:
            self.fields['producto'] = forms.ModelChoiceField(
                required=False,
                queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
                widget=forms.Select(attrs={'class': 'form-control producto'}),
            )
            self.fields['cantidad_presentacion'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
            self.fields['precio'] = forms.DecimalField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control precio', 'step': '.01'})
            )


class DetalleCompraRecepcionForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['cantidad_presentacion_entrega', 'total_final', 'is_checked']


# Sirve para el modal de agregar un no deseado a la compra.
class DetalleCompraNoDeseadoForm(forms.ModelForm):

    class Meta:
        model = DetalleCompra
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion_entrega', 'total_final']
        widgets = {
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
        }

    def __init__(self, *args, **kwargs):
        proveedor = kwargs.pop('proveedor')
        super(DetalleCompraNoDeseadoForm, self).__init__(*args, **kwargs)
        self.fields['producto'] = forms.ModelChoiceField(
            required=False,
            queryset=Producto.objects.filter(catalogoxproveedor__proveedor=proveedor),
            widget=forms.Select(attrs={'class': 'default-select2 form-control producto_nopedido'}),
        )
        self.fields['producto'].empty_label = None
        self.fields['cantidad_presentacion_entrega'] = forms.IntegerField(
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control cantidad_presentacion_entrega_nopedido'})
        )
        self.fields['total_final'] = forms.IntegerField(
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control total_final_nopedido'})
        )


# Sirve para guardar el detallecompra (tanto deseados y no deseados)
# class DetalleCompraForm(forms.ModelForm):
#
#     class Meta:
#         model = DetalleCompra
#         fields = ['cantidad_presentacion_entrega', 'total_final']
#
#     def __init__(self, *args, **kwargs):
#         super(DetalleCompraForm, self).__init__(*args, **kwargs)
#         self.fields['cantidad_presentacion_entrega'] = forms.IntegerField(
#             widget=forms.NumberInput(attrs={'class': 'form-control cantidad_presentacion_entrega_nopedido'})
#         )
#         self.fields['total_final'] = forms.IntegerField(
#             widget=forms.NumberInput(attrs={'class': 'form-control total_final_nopedido'})
#         )


class CompraFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CompraFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None
        self.fields['estado'] = forms.ChoiceField(choices=Compra.ESTADO_CHOICES, required=False,
                                                  widget=forms.SelectMultiple(
                                                      attrs={'class': 'multiple-select2 form-control'}))
        self.fields['tipo'] = forms.ChoiceField(choices=Compra.TIPO_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                      attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fechahora_creacion1'] = forms.CharField(required=False, widget=forms.TextInput(
                                                               attrs={'id': 'fechahora_creacion1',
                                                                      'placeholder': 'Inicio',
                                                                      'class': 'form-control'}))
        self.fields['fechahora_creacion2'] = forms.CharField(required=False, widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_creacion2',
                                                                        'placeholder': 'Fin',
                                                                        'class': 'form-control'}))
        self.fields['total_final1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Mínimo'}),
                                                       required=False)
        self.fields['total_final2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Máximo'}),
                                                       required=False)


class ImpuestoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ImpuestoForm, self).__init__(*args, **kwargs)
        self.fields['impuesto'] = forms.ModelChoiceField(queryset=Impuesto.objects.all(), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['impuesto'].empty_label = None


class CompraRecepcionForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'estado_select form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CompraRecepcionForm, self).__init__(*args, **kwargs)
        self.fields['estado'].choices = [i for i in self.fields['estado'].choices if i[0] in ['2', '3']]
