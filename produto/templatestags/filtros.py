from django import template

register = template.Library()


@register.filter("enumerate")
def enumerat(valor):
    return enumerate(valor)
