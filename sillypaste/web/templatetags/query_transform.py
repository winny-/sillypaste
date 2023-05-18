from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """
    Easy way to modify a query from a template.

    See https://stackoverflow.com/a/24658162/2720026
    """
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v

    return updated.urlencode()
