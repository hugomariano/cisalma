from django import forms
from django.forms import ModelChoiceField

# Model import-->
from maestro.models import Sucursal, Producto, PresentacionxProducto, Impuesto
from ventas.models import OfertaVenta, Venta, DetalleVenta
from clientes.models import Cliente
from finanzas.models import CuentaCliente
from maestro.utils import empresa_list
# Model import<--


class OfertaVentaForm(forms.ModelForm):

    fechahora_inicio = forms.DateTimeField(widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M %p',
                                                                      attrs={'class': 'form-control'}),
                                           input_formats=['%d/%m/%Y %I:%M %p'])
    fechahora_fin = forms.DateTimeField(widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M %p',
                                                                   attrs={'class': 'form-control'}),
                                        input_formats=['%d/%m/%Y %I:%M %p'])

    class Meta:
        model = OfertaVenta
        fields = ['sucursal', 'tipo', 'tipo_duracion', 'producto_oferta',
                  'presentacion_oferta', 'cantidad_oferta', 'producto_retorno',
                  'presentacion_retorno', 'retorno', 'fechahora_inicio', 'fechahora_fin', 'stock_limite']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'tipo_duracion': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'producto_oferta': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'presentacion_oferta': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'cantidad_oferta': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto_retorno': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'presentacion_retorno': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'retorno': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_limite': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(OfertaVentaForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), widget=forms.Select(attrs={'class': 'default-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices if i[0] in ['1', '2', '3']]
        self.fields['tipo_duracion'].choices = [i for i in self.fields['tipo_duracion'].choices if i[0] in ['1', '2']]
        self.fields['producto_oferta'].empty_label = None
        self.fields['presentacion_oferta'].empty_label = None
        self.fields['producto_retorno'].empty_label = None
        self.fields['presentacion_retorno'].empty_label = None


class VentaCreateForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['cliente', 'sucursal']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'default-select2 form-control', 'id': 'cliente'}),
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VentaCreateForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        required=False, widget=forms.Select(
                                                            attrs={'class': 'default-select2 form-control'}))
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), widget=forms.Select(attrs={'class': 'default-select2 form-control'}))
        self.fields['sucursal'].empty_label = None


class VentaFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VentaFiltroForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        required=False, widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['cliente'].empty_label = None
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None
        self.fields['estado'] = forms.ChoiceField(choices=Venta.ESTADO_ENVIO_CHOICES, required=False,
                                                  widget=forms.SelectMultiple(
                                                      attrs={'class': 'multiple-select2 form-control'}))
        self.fields['tipo_pago'] = forms.ChoiceField(choices=Venta.TIPO_PAGO_CHOICES, required=False,
                                                     widget=forms.SelectMultiple(
                                                         attrs={'class': 'multiple-select2 form-control'}))
        self.fields['estado_pago'] = forms.ChoiceField(choices=Venta.ESTADO_PAGO_CHOICES, required=False,
                                                       widget=forms.SelectMultiple(
                                                         attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fechahora_creacion1'] = forms.CharField(required=False,
                                                             widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_creacion1',
                                                                        'placeholder': 'Inicio',
                                                                        'class': 'form-control'}))
        self.fields['fechahora_creacion2'] = forms.CharField(required=False,
                                                             widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_creacion2',
                                                                        'placeholder': 'Fin',
                                                                        'class': 'form-control'}))
        self.fields['total1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Mínimo'}),
                                                 required=False)
        self.fields['total2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Máximo'}),
                                                 required=False)


class VentaEditForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['tipo', 'cliente']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'cliente': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user')
        super(VentaEditForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        widget=forms.Select(
                                                            attrs={'class': 'default-select2 form-control'}))
        self.fields['tipo'].empty_label = None
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices if i[0] in ['1', '2']]


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'presentacionxproducto', 'cantidad_presentacion_pedido']
        widgets = {
            'presentacionxproducto': forms.HiddenInput(attrs={'class': 'presentacionxproducto'}),
            'cantidad_unidad': forms.HiddenInput(attrs={'class': 'cantidad_unidad'}),
        }

    def __init__(self, *args, **kwargs):
        has_data = kwargs.pop('has_data')
        sucursal = kwargs.pop('sucursal')
        super(DetalleVentaForm, self).__init__(*args, **kwargs)
        if has_data:
            self.fields['producto'] = forms.ModelChoiceField(
                queryset=Producto.objects.filter(catalogo=sucursal),
                widget=forms.Select(attrs={'class': 'default-select2 form-control producto'}),
            )
            self.fields['producto'].empty_label = None
            self.fields['cantidad_presentacion_pedido'] = forms.IntegerField(
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )
        else:
            self.fields['producto'] = forms.ModelChoiceField(
                required=False,
                queryset=Producto.objects.filter(catalogo=sucursal),
                widget=forms.Select(attrs={'class': 'form-control producto'}),
            )
            self.fields['cantidad_presentacion_pedido'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control cantidadpresentacion'})
            )


class ImpuestoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ImpuestoForm, self).__init__(*args, **kwargs)
        self.fields['impuesto'] = forms.ModelChoiceField(queryset=Impuesto.objects.all(), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['impuesto'].empty_label = None


class VentaEntregaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['estado']
        widgets = {
            'estado': forms.Select(attrs={'class': 'estado_select form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(VentaEntregaForm, self).__init__(*args, **kwargs)
        self.fields['estado'].choices = [i for i in self.fields['estado'].choices if i[0] in ['2', '3']]


class DetalleVentaEntregaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cantidad_presentacion_entrega', 'is_checked']


class VentaDescuentoAdicionalForm(forms.ModelForm):

    class Meta:
        model = DetalleVenta
        fields = ['descuento_adicional']
        widgets = {
            'descuento_adicional': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
        }
