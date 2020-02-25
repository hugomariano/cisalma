from django import template

register = template.Library()


@register.filter(name='categoria_colorpick')
def categoria_colorpick(value):
    if value == 0:
        color = 'alert-primary'
    elif value == 1:
        color = 'alert-info'
    elif value == 2:
        color = 'alert-dark'
    elif value == 3:
        color = 'alert-secondary'
    else:
        color = 'alert-light'
    return color
