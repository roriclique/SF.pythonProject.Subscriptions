from django import template

register = template.Library()


@register.filter()
def censor(value):
    for i in value.split():
        if i == 'radish':
            value = value.replace(i[1:6], "*" * len(i))
    return value