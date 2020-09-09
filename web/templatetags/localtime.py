from django import template
from django.utils import timezone
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.conf import settings
import pytz
from datetime import datetime


register = template.Library()


@register.inclusion_tag('localtime_snippet.html')
def localtime(time=None):
    if time is None:
        time = timezone.now()
    utc = time.astimezone(pytz.utc)
    return {
        'ms': int(utc.timestamp()*1000),
        'time': utc,
    }
