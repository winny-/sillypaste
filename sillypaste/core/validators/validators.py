from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from sillypaste.core.models import Paste


__all__ = ['validate_future_datetime', 'validate_paste_sort_key']


def validate_future_datetime(value):
    if value <= timezone.now():
        raise ValidationError(
            _('%(value)s is in the past'), params={'value': value}
        )


def validate_paste_sort_key(value):
    """Is the value a valid Paste sort key?"""
    # key = value.lstrip('-') will strip off more than one '-'.
    key = value[1:] if value[0] == '-' else value
    if key not in (f.name for f in Paste._meta.get_fields()):
        raise ValidationError(_('%(value)s is not a valid sort key.'))
