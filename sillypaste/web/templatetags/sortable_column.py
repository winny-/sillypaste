from django import template


register = template.Library()


@register.inclusion_tag('sortable_column_snippet.html')
def sortable_column(request, pretty_name, identifier, default=False):
    current = request.GET.get('sort', identifier if default else None)
    return {
        'pretty_name': pretty_name,
        'identifier': identifier,
        'request': request,
        'selected': identifier == current,
    }
