from django import forms

from django.forms import ModelChoiceField

# Model import-->
from maestro.models import Empresa,Sucursal, Almacen, Categoria, Presentacion, Producto,\
    PresentacionxProducto, Proveedor, CatalogoxProveedor, Caja, Grupo
from maestro.utils import empresa_list
from django.contrib.auth.models import User
# Model import<--


class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'})
        }


class SucursalForm(forms.ModelForm):

    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].empty_label = None


class AlmacenForm(forms.ModelForm):

    class Meta:
        model = Almacen
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AlmacenForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'].empty_label = None


class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'sucursal': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CajaForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'].empty_label = None


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['descripcion', 'padre']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'padre': forms.Select(attrs={'class': 'default-select2 form-control'})
        }


class PresentacionForm(forms.ModelForm):

    class Meta:
        model = Presentacion
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['descripcion', 'empresa', 'utilidad_monetaria']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'}),
            'utilidad_monetaria': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['empresa'].empty_label = None


class ProductoCategoriaForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['categorias']
        widgets = {
            'categorias': forms.SelectMultiple(attrs={'class': 'multiple-select2 form-control'})
        }


class ProductoPresentacionForm(forms.ModelForm):

    class Meta:
        model = PresentacionxProducto
        fields = ['presentacion', 'cantidad']


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'default-select2 form-control'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['empresa'] = forms.ModelChoiceField(queryset=Empresa.objects.filter(id__in=empresa_list(user)),
                                                        required=False, widget=forms.Select(
                                                            attrs={'class': 'default-select2 form-control'}))
        self.fields['empresa'].empty_label = None


class CatalogoProveedorForm(forms.ModelForm):

    class Meta:
        model = CatalogoxProveedor
        fields = ['producto']


class ProductoFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ProductoFiltroForm, self).__init__(*args, **kwargs)
        self.fields['categoria'] = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['categoria'].empty_label = None


class CatalogoFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CatalogoFiltroForm, self).__init__(*args, **kwargs)
        self.fields['sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.all(), required=False,
                                                         widget=forms.SelectMultiple(
                                                             attrs={'class': 'multiple-select2 form-control'}))
        self.fields['sucursal'].empty_label = None


class CatalogoProveedorFiltroForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CatalogoProveedorFiltroForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'] = forms.ModelChoiceField(queryset=Proveedor.objects.filter(
            empresa__in=empresa_list(user)), required=False,
                                                          widget=forms.SelectMultiple(
                                                              attrs={'class': 'multiple-select2 form-control'}))
        self.fields['proveedor'].empty_label = None


class UsuarioForm(forms.ModelForm):

    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all(), required=True,
                                   widget=forms.Select(attrs={'class': 'default-select2 form-control'}))

    sucursal = forms.ModelMultipleChoiceField(queryset=Sucursal.objects.all(), required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'default-select2 form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['grupo'].empty_label = None
