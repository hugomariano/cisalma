from django.shortcuts import redirect, HttpResponse
from django.views.generic import DetailView, ListView, TemplateView, RedirectView

# Extra python features-->
from maestro.mixin import BasicEMixin
# Extra python features<--

# Model import-->
from clientes.models import Cliente, ContactosCliente
# Model import<--

# Forms import-->
from .forms import ClienteForm, ContactoForm, ClienteFiltroForm, ContactoFiltroForm
# Forms import<--
# Utils import-->
from maestro.utils import empresa_list
# Utils import<--


# Create your views here.
class ClienteListView(BasicEMixin, ListView):

    template_name = 'clientes/cliente-list.html'
    model = Cliente
    nav_name = 'nav_cliente'
    view_name = 'cliente'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_filtro'] = ClienteFiltroForm(self.request.GET)
        return context

    def get_queryset(self):
        documento = self.request.GET.get('documento', False)
        descripcion = self.request.GET.get('descripcion', False)
        tipo = self.request.GET.getlist('tipo')
        if documento != '' and documento is not False:
            query = Cliente.objects.filter(documento__icontains=documento)
        elif descripcion != '' and descripcion is not False:
            query = Cliente.objects.filter(descripcion__icontains=descripcion)
        else:
            query = Cliente.objects.all()
        if len(tipo) > 0:
            query = query.filter(tipo__in=tipo)
        query = query.filter(empresa__in=empresa_list(self.request.user))
        return query


class ClienteDetailView(BasicEMixin, DetailView):

    template_name = 'clientes/cliente-detail.html'
    model = Cliente
    nav_name = 'nav_cliente'
    view_name = 'cliente'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contactos'] = ContactosCliente.objects.filter(cliente=self.kwargs['pk'])
        return context


class ClienteEditView(BasicEMixin, TemplateView):

    template_name = 'clientes/cliente-edit.html'
    nav_name = 'nav_cliente'
    view_name = 'cliente'
    action_name = 'editar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = ClienteForm(user=self.request.user)
        else:
            cliente = Cliente.objects.get(pk=self.kwargs['pk'])
            context['object'] = ClienteForm(instance=cliente, user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = ClienteForm(request.POST, user=self.request.user)
        else:
            cliente = Cliente.objects.get(pk=self.kwargs['pk'])
            form = ClienteForm(request.POST, instance=cliente, user=self.request.user)
        if form.is_valid():
            cliente = form.save(commit=False)
            if form.cleaned_data['tipo'] == '1':
                cliente.documento = cliente.dni
                cliente.descripcion = cliente.nombres + ' ' + cliente.apellidos
            else:
                cliente.documento = cliente.ruc
                cliente.descripcion = cliente.razon_social
            cliente.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/clientes/cliente/'+str(cliente.id))


class ContactoListView(BasicEMixin, ListView):

    template_name = 'clientes/contacto-list.html'
    model = ContactosCliente
    nav_name = 'nav_contacto'
    view_name = 'contacto'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacto_filtro'] = ContactoFiltroForm(self.request.GET, user=self.request.user)
        return context

    def get_queryset(self):
        dni = self.request.GET.get('dni', False)
        descripcion = self.request.GET.get('descripcion', False)
        cliente = self.request.GET.getlist('cliente')
        if dni != '' and dni is not False:
            query = ContactosCliente.objects.filter(dni__icontains=dni)
        elif descripcion != '' and descripcion is not False:
            query = ContactosCliente.objects.filter(descripcion__icontains=descripcion)
        else:
            query = ContactosCliente.objects.all()
        if len(cliente) > 0:
            query = query.filter(cliente__in=cliente)
        return query


class ContactoDetailView(BasicEMixin, DetailView):

    template_name = 'clientes/contacto-detail.html'
    model = ContactosCliente
    nav_name = 'nav_contacto'
    view_name = 'contacto'
    action_name = 'leer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactoEditView(BasicEMixin, TemplateView):

    template_name = 'clientes/contacto-edit.html'
    nav_name = 'nav_contacto'
    view_name = 'contacto'
    action_name = 'editar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['pk'] == 0:
            context['object'] = ContactoForm(self.request.GET, user=self.request.user)
        else:
            contacto = ContactosCliente.objects.get(pk=self.kwargs['pk'])
            context['object'] = ContactoForm(instance=contacto, user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 0:
            form = ContactoForm(request.POST, user=self.request.user)
        else:
            contacto = ContactosCliente.objects.get(pk=self.kwargs['pk'])
            form = ContactoForm(request.POST, instance=contacto, user=self.request.user)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.descripcion = contacto.nombres + ' ' + contacto.apellidos
            contacto.save()
        else:
            return HttpResponse(form.errors)
        return redirect('/clientes/contacto/'+str(contacto.id))
