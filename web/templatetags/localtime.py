from django import template
from django.utils import timezone
import pytz


register = template.Library()


@register.inclusion_tag('localtime_snippet.html')
def localtime(time=None):
    if time is None:
        time = timezone.now()
    utc = time.astimezone(pytz.utc)
    return {'ms': int(utc.timestamp() * 1000), 'time': utc}
