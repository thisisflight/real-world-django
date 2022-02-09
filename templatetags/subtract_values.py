from django import template

register = template.Library()


@register.simple_tag
def subtract(first_arg, second_arg):
    return int(first_arg) - int(second_arg)
