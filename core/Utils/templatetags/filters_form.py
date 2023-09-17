from django import template

register = template.Library()


@register.simple_tag
def search_fields(request):
    return ('search',)
