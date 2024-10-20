from django import template

register = template.Library()

@register.filter(name='zip_lists')
def zip_lists(a, b):
    """Zips two lists together."""
    return zip(a, b)
