from django import forms

# Model import-->
from django.forms import ModelChoiceField
from maestro.models import Empresa
from clientes.models import Cliente, ContactosCliente
# Model import<--

from maestro.utils import empresa_list


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['tipo', 'telefono', 'correo', 'ruc', 'dni', 'razon_social', 'nombres', 'apellidos', 'empresa']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['empresa'] = forms.ModelChoiceField(queryset=Empresa.objects.filter(
            id__in=empresa_list(user)), widget=forms.Select(attrs={'class': 'default-select2 form-control'}))
        self.fields['empresa'].empty_label = None
        self.fields['tipo'].empty_label = None


class ContactoForm(forms.ModelForm):

    class Meta:
        model = ContactosCliente
        fields = ['cliente', 'nombres', 'apellidos',
                  'dni', 'cargo', 'telefono', 'correo', 'cargo']
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ContactoForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        required=False,
                                                        widget=forms.Select(
                                                            attrs={'class': 'default-select2 form-control'}))
        self.fields['cliente'].empty_label = None


class ClienteFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ClienteFiltroForm, self).__init__(*args, **kwargs)
        self.fields['tipo'] = forms.ChoiceField(choices=Cliente.TIPO_CHOICES, required=False,
                                                widget=forms.SelectMultiple(
                                                    attrs={'class': 'multiple-select2 form-control'}))
        self.fields['documento'] = forms.CharField(required=False,
                                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['descripcion'] = forms.CharField(required=False,
                                                     widget=forms.TextInput(attrs={'class': 'form-control'}))


class ContactoFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ContactoFiltroForm, self).__init__(*args, **kwargs)
        self.fields['cliente'] = forms.ModelChoiceField(queryset=Cliente.objects.filter(empresa__in=empresa_list(user)),
                                                        required=False,
                                                        widget=forms.SelectMultiple(
                                                            attrs={'class': 'multiple-select2 form-control'}))
        self.fields['cliente'].empty_label = None
        self.fields['dni'] = forms.CharField(required=False,
                                             widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields['descripcion'] = forms.CharField(required=False,
                                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
