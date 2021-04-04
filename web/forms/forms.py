from django.utils import timezone
from datetime import timedelta, datetime
from django import forms
from django.core.exceptions import ValidationError
from core.models import Paste
from core.validators import validate_future_datetime
import pytz


__all__ = ['PasteForm']


class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['expiry', 'title', 'language', 'body']

    CUSTOM_EXPIRY_DATE_FORMAT = '%Y-%m-%d'
    CUSTOM_EXPIRY_TIME_FORMAT = '%H:%M:%S'

    EXPIRY_CHOICES_NO_CUSTOM = [
        ('never', 'Never'),
        ('1hour', '1 Hour'),
        ('1day', '1 Day'),
    ]
    EXPIRY_CHOICES = EXPIRY_CHOICES_NO_CUSTOM + [('custom', 'Custom')]

    expiry_preset = forms.ChoiceField(choices=EXPIRY_CHOICES, initial='1day', required=False)
    custom_expiry_date = forms.DateField(required=False)
    custom_expiry_time = forms.TimeField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None:  # Populate the form based on instance data.
            custom_expiry_date = custom_expiry_time = None
            expiry_preset = 'never'
            if instance.expiry:
                custom_expiry_date = instance.expiry.strftime(
                    self.CUSTOM_EXPIRY_DATE_FORMAT
                )
                custom_expiry_time = instance.expiry.strftime(
                    self.CUSTOM_EXPIRY_TIME_FORMAT
                )
                expiry_preset = 'custom'
            kwargs.update(initial={
                'custom_expiry_date': custom_expiry_date,
                'custom_expiry_time': custom_expiry_time,
                'expiry_preset': expiry_preset,
            })
        super().__init__(*args, **kwargs)
        self.fields['body'].strip = False  # Leave whitespace alone.

    def clean_body(self, *args, **kwargs):
        """Convert CRLF to LF in the body."""
        body = self.cleaned_data['body']
        return body.replace('\r\n', '\n')

    def clean(self, *args, **kwargs):
        ep = self.cleaned_data.get('expiry_preset')
        if not ep or ep == '1day':  # Default to 1day.
            self.cleaned_data['expiry'] = timezone.now() + timedelta(days=1)
        elif ep == '1hour':
            self.cleaned_data['expiry'] = timezone.now() + timedelta(hours=1)
        elif ep == 'custom':
            if self.cleaned_data.get('custom_expiry_date') is None:
                raise ValidationError('Custom expiry selected but no date provided.')
            elif self.cleaned_data.get('custom_expiry_time') is None:
                raise ValidationError('Custom expiry selected but no time provided.')
            time = self.cleaned_data['custom_expiry_time']
            date = self.cleaned_data['custom_expiry_date']
            ce = datetime.combine(date, time)
            utc = pytz.utc.localize(ce)
            validate_future_datetime(utc)
            self.cleaned_data['expiry'] = utc
        elif ep == 'never':
            self.cleaned_data['expiry'] = None
        else:
            raise ValidationError(f'expiry_preset {ep} not recognized')
