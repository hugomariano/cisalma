from .models import AsignacionGrupo


def format_categories(categorias):
    contenedor = []
    profundidad = -1
    for c in categorias:
        if c.nivel == 1:
            contenedor.append([c.descripcion])
            profundidad += 1
        else:
            contenedor[profundidad].append(c.descripcion)
    return contenedor


def empresa_list(user):
    asig_grupo = AsignacionGrupo.objects.get(usuario=user)
    sucursales = asig_grupo.sucursal.all()
    empresas = []
    for s in sucursales:
        empresas.append(s.empresa_id)
    return empresas
