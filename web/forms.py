from django.utils import timezone
from datetime import timedelta, datetime
from django import forms
from django.core.exceptions import ValidationError
from core.models import Paste, Language
from core.validators import validate_future_datetime
from django.db.models.functions import Lower
import pytz


class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['expiry', 'title', 'language', 'body']

    EXPIRY_CHOICES_NO_CUSTOM = [
        ('never', 'Never'),
        ('1hour', '1 Hour'),
        ('1day', '1 Day'),
    ]
    EXPIRY_CHOICES = EXPIRY_CHOICES_NO_CUSTOM + [('custom', 'Custom')]
    expiry_preset = forms.ChoiceField(choices=EXPIRY_CHOICES, initial='1day')
    custom_expiry_date = forms.DateField(required=False)
    custom_expiry_time = forms.TimeField(required=False)


    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None:
            kwargs.update(initial={
                # XXX: Is there a better way to write this?
                'custom_expiry_date': instance.expiry.strftime("%Y-%m-%d") if instance.expiry else None,
                'custom_expiry_time': instance.expiry.strftime("%H:%M:%S") if instance.expiry else None,
                'expiry_preset': 'custom' if instance.expiry else 'never',
            })
        super().__init__(*args, **kwargs)
        self.fields['language'].queryset = Language.objects.order_by(Lower('name'))

    def clean(self, *args, **kwargs):
        ep = self.cleaned_data['expiry_preset']
        if ep  == '1day':
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
            raise RuntimeError(f'expiry_preset {expiry_preset} not recognized')
