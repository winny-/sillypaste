from django.utils import timezone
from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError
from core.models import Paste, Language
from core.validators import validate_future_datetime
from django.db.models.functions import Lower


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
    custom_expiry = forms.DateTimeField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['language'].queryset = Language.objects.order_by(Lower('name'))

    def clean(self, *args, **kwargs):
        ep = self.cleaned_data['expiry_preset']
        if ep  == '1day':
            self.cleaned_data['expiry'] = timezone.now() + timedelta(days=1)
        elif ep == '1hour':
            self.cleaned_data['expiry'] = timezone.now() + timedelta(hours=1)
        elif ep == 'custom':
            if 'custom_expiry' not in self.cleaned_data or not self.cleaned_data['custom_expiry']:
                raise ValidationError('Custom expiry selected but no datetime provided.')
            ce = self.cleaned_data['custom_expiry']
            validate_future_datetime(ce)
            self.cleaned_data['expiry'] = ce
        elif ep == 'never':
            self.cleaned_data['expiry'] = None
        else:
            raise RuntimeError(f'expiry_preset {expiry_preset} not recognized')
