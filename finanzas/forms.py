from django import forms
from django.forms import ModelChoiceField

# Model import-->
from maestro.models import Caja, Proveedor
from clientes.models import Cliente
from finanzas.models import DetalleJornada, Jornada, CuentaCliente, CuentaProveedor, PagoCliente, PagoProveedor
from ventas.models import Venta
from compras.models import Compra
# Model import<--
from maestro.utils import empresa_list


class JornadaFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(JornadaFiltroForm, self).__init__(*args, **kwargs)
        self.fields['caja'] = forms.ModelChoiceField(queryset=Caja.objects.filter(
            sucursal__empresa__in=empresa_list(user)), required=False,
                                                     widget=forms.SelectMultiple(
                                                         attrs={'class': 'multiple-select2 form-control'}))
        self.fields['caja'].empty_label = None
        self.fields['fechahora_inicio1'] = forms.CharField(required=False,
                                                           widget=forms.TextInput(
                                                               attrs={'id': 'fechahora_inicio1',
                                                                      'placeholder': 'Inicio',
                                                                      'class': 'form-control'}))
        self.fields['fechahora_inicio2'] = forms.CharField(required=False,
                                                           widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_inicio2',
                                                                        'placeholder': 'Fin',
                                                                        'class': 'form-control'}))
        self.fields['monto1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Mínimo'}),
                                                 required=False)
        self.fields['monto2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Máximo'}),
                                                 required=False)


class DetalleJornadaCreateForm(forms.ModelForm):

    class Meta:
        model = DetalleJornada
        fields = ['tipo', 'monto', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(DetalleJornadaCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices if i[0] in ['1', '2']]


class JornadaCreateForm(forms.ModelForm):

    class Meta:
        model = Jornada
        fields = ['caja', 'monto_apertura']
        widgets = {
            'caja': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'monto_apertura': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(JornadaCreateForm, self).__init__(*args, **kwargs)
        self.fields['caja'] = forms.ModelChoiceField(queryset=Caja.objects.filter(
            sucursal__empresa__in=empresa_list(user)),
                                                     widget=forms.Select(
                                                         attrs={'class': 'default-select2 form-control'}))
        self.fields['caja'].empty_label = None


class CuentaClienteFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CuentaClienteFiltroForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        required=False, widget=forms.SelectMultiple(
                                                         attrs={'class': 'multiple-select2 form-control'}))
        self.fields['cliente'].empty_label = None
        self.fields['duracion'] = forms.ChoiceField(choices=CuentaCliente.DURACION_CHOICES, required=False,
                                                    widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['estado'] = forms.ChoiceField(choices=CuentaCliente.DURACION_CHOICES, required=False,
                                                  widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['tipo'] = forms.ChoiceField(choices=CuentaCliente.DURACION_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fechahora_caducidad1'] = forms.CharField(required=False,
                                                              widget=forms.TextInput(
                                                               attrs={'id': 'fechahora_caducidad1',
                                                                      'placeholder': 'Inicio',
                                                                      'class': 'form-control'}))
        self.fields['fechahora_caducidad2'] = forms.CharField(required=False,
                                                              widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_caducidad2',
                                                                        'placeholder': 'Fin',
                                                                        'class': 'form-control'}))
        self.fields['monto_amortizado1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Mínimo'}),
                                                            required=False)
        self.fields['monto_amortizado2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Máximo'}),
                                                            required=False)
        self.fields['monto_total2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Máximo'}),
                                                       required=False)
        self.fields['monto_total2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Máximo'}),
                                                       required=False)


class PagoClienteCreateForm(forms.ModelForm):

    class Meta:
        model = PagoCliente
        fields = ['tipo', 'monto', 'banco', 'codigo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'banco': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PagoClienteCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices if i[0] in ['1', '2', '3']]
        self.fields['banco'].choices = [i for i in self.fields['banco'].choices if i[0] in ['0', '1', '2', '3']]


class CuentaProveedorFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CuentaProveedorFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                          widget=forms.SelectMultiple(
                                                         attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None
        self.fields['duracion'] = forms.ChoiceField(choices=CuentaProveedor.DURACION_CHOICES, required=False,
                                                    widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['estado'] = forms.ChoiceField(choices=CuentaProveedor.DURACION_CHOICES, required=False,
                                                  widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['tipo'] = forms.ChoiceField(choices=CuentaProveedor.DURACION_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                        attrs={'class': 'multiple-select2 form-control'}))
        self.fields['fechahora_caducidad1'] = forms.CharField(required=False,
                                                              widget=forms.TextInput(
                                                               attrs={'id': 'fechahora_caducidad1',
                                                                      'placeholder': 'Inicio',
                                                                      'class': 'form-control'}))
        self.fields['fechahora_caducidad2'] = forms.CharField(required=False,
                                                              widget=forms.TextInput(
                                                                 attrs={'id': 'fechahora_caducidad2',
                                                                        'placeholder': 'Fin',
                                                                        'class': 'form-control'}))
        self.fields['monto_amortizado1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Mínimo'}),
                                                            required=False)
        self.fields['monto_amortizado2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                            'placeholder': 'Máximo'}),
                                                            required=False)
        self.fields['monto_total1'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Mínimo'}),
                                                       required=False)
        self.fields['monto_total2'] = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Máximo'}),
                                                       required=False)


class PagoProveedorCreateForm(forms.ModelForm):

    class Meta:
        model = PagoProveedor
        fields = ['tipo', 'monto', 'banco', 'codigo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'banco': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PagoProveedorCreateForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].choices = [i for i in self.fields['tipo'].choices if i[0] in ['1', '2', '3']]
        self.fields['banco'].choices = [i for i in self.fields['banco'].choices if i[0] in ['0', '1', '2', '3']]


class PagoVentaForm(forms.ModelForm):

    duracion = forms.ChoiceField(choices=CuentaCliente.DURACION_CHOICES, required=False,
                                 widget=forms.Select(
                                     attrs={'class': 'default-select2 form-control'}))
    pago = forms.FloatField(required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'pago_inp',
                                                            'readonly': 'readonly'}))
    recibo = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    caja = forms.ModelChoiceField(queryset=Caja.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'default-select2 form-control'}))

    class Meta:
        model = Venta
        fields = ['tipo_pago', 'tipo_comprobante', 'serie_comprobante', 'numero_comprobante']
        widgets = {
            'tipo_pago': forms.Select(attrs={'class': 'default-select2 form-control tipo_pago'}),
            'tipo_comprobante': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'serie_comprobante': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_comprobante': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(PagoVentaForm, self).__init__(*args, **kwargs)
        self.fields['caja'].empty_label = None


class PagoCompraForm(forms.ModelForm):

    duracion = forms.ChoiceField(choices=CuentaProveedor.DURACION_CHOICES, required=False,
                                 widget=forms.Select(
                                     attrs={'class': 'default-select2 form-control'}))
    pago = forms.FloatField(required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'pago_inp',
                                                            'readonly': 'readonly'}))
    recibo = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    caja = forms.ModelChoiceField(queryset=Caja.objects.all(), required=True,
                                  widget=forms.Select(attrs={'class': 'default-select2 form-control'}))

    class Meta:
        model = Compra
        fields = ['tipo_pago', 'tipo_comprobante', 'serie_comprobante', 'numero_comprobante']
        widgets = {
            'tipo_pago': forms.Select(attrs={'class': 'default-select2 form-control tipo_pago'}),
            'tipo_comprobante': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'serie_comprobante': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_comprobante': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(PagoCompraForm, self).__init__(*args, **kwargs)
        self.fields['caja'].empty_label = None
