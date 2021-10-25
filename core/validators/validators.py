from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


__all__ = ['validate_future_datetime']


def validate_future_datetime(value):
    if value <= timezone.now():
        raise ValidationError(
            _('%(value)s is in the past'), params={'value': value}
        )
