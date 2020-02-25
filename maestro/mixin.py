from django.contrib.auth.mixins import UserPassesTestMixin
from maestro.models import AccionxVista, AsignacionAccion, AsignacionGrupo
from django.http import HttpResponseRedirect


class BasicEMixin(UserPassesTestMixin):
    """
    View mixin which provides sorting for ListView.
    """
    nav_main = None
    nav_name = None
    login_url = '/maestro/acceso'
    view_name = None
    action_name = None

    def get_context_data(self, *args, **kwargs):
        context = super(BasicEMixin, self).get_context_data(*args, **kwargs)
        a_grupo = AsignacionGrupo.objects.get(usuario=self.request.user.id)
        context.update({
            'nav_main': self.nav_main,
            'nav_name': self.nav_name,
            'user_name': self.request.user.username,
            'grupo_name': a_grupo.grupo.descripcion
        })
        return context

    def test_func(self):
        accionxvista = AccionxVista.objects.get(accion__descripcion=self.action_name,
                                                vista__descripcion=self.view_name)
        a_grupo = AsignacionGrupo.objects.get(usuario=self.request.user.id)
        try:
            AsignacionAccion.objects.get(grupo=a_grupo.grupo_id, accionxvista=accionxvista.id)
            response = True
        except AsignacionAccion.DoesNotExist:
            response = False
        return response

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return HttpResponseRedirect('/maestro/denied')
        return super().dispatch(request, *args, **kwargs)

