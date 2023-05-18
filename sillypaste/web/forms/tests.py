from django.test import TestCase
from . import PasteForm
from sillypaste.core.models import Language
from django.utils import timezone
from datetime import timedelta


# TODO: check the sort of error text that occur in f.errors.
class TestPasteForm(TestCase):
    def test_validate_required_fields(self):
        self.assertFalse(PasteForm().is_valid())
        self.assertFalse(PasteForm({'title': 't'}).is_valid())
        self.assertFalse(PasteForm({'body': 'b'}).is_valid())
        self.assertTrue(PasteForm({'title': 't', 'body': 'b'}).is_valid())

    def test_validate_keep_trailing_nl(self):
        f = PasteForm({'title': 't', 'body': 'text\n'})
        f.is_valid()
        self.assertEqual(f.save().body, 'text\n')

    def do_not_add_trailing_nl(self):
        f = PasteForm({'title': 't', 'body': 'text'})
        f.is_valid()
        self.assertEqual(f.save().body, 'text')

    def test_validate_crlf_to_lf(self):
        f = PasteForm({'title': 't', 'body': 'a\r\nb\r\nc'})
        f.is_valid()
        self.assertEqual(f.save().body, 'a\nb\nc')

    def test_validate_random_stray_crs_left_alone(self):
        f = PasteForm({'title': 't', 'body': 'a\rb\nc'})
        f.is_valid()
        self.assertEqual(f.save().body, 'a\rb\nc')

    def test_validate_expires_never(self):
        f = PasteForm({'title': 't', 'body': 'b', 'expiry_preset': 'never'})
        f.is_valid()
        self.assertEqual(f.save().expiry, None)

    def test_validate_expires_1hour(self):
        before = timezone.now() + timedelta(hours=1)
        f = PasteForm({'title': 't', 'body': 'b', 'expiry_preset': '1hour'})
        f.is_valid()
        expiry = f.save().expiry
        after = timezone.now() + timedelta(hours=1)
        self.assertTrue(before < expiry < after)

    def test_validate_expires_1day(self):
        before = timezone.now() + timedelta(days=1)
        f = PasteForm({'title': 't', 'body': 'b', 'expiry_preset': '1day'})
        f.is_valid()
        expiry = f.save().expiry
        after = timezone.now() + timedelta(days=1)
        self.assertTrue(before < expiry < after)

    def test_validate_expires_custom_invalid_no_date_or_time(self):
        f = PasteForm({'title': 't', 'body': 'b', 'expiry_preset': 'custom'})
        self.assertFalse(f.is_valid())

    def test_validate_expires_custom_good(self):
        t = timezone.now().replace(microsecond=0) + timedelta(hours=16)
        f = PasteForm(
            {
                'title': 't',
                'body': 'b',
                'expiry_preset': 'custom',
                'custom_expiry_date': t.strftime(
                    PasteForm.CUSTOM_EXPIRY_DATE_FORMAT
                ),
                'custom_expiry_time': t.strftime(
                    PasteForm.CUSTOM_EXPIRY_TIME_FORMAT
                ),
            }
        )
        self.assertEqual(f.save().expiry, t)

    def test_validate_expires_custom_unparsable_date_and_time(self):
        f = PasteForm(
            {
                'title': 't',
                'body': 'b',
                'expiry_preset': 'custom',
                'custom_expiry_date': 'garbage',
                'custom_expiry_time': 'garbage',
            }
        )
        self.assertFalse(f.is_valid())

    def test_validate_expires_custom_unparsable__time(self):
        t = timezone.now().replace(microsecond=0) + timedelta(hours=16)
        f = PasteForm(
            {
                'title': 't',
                'body': 'b',
                'expiry_preset': 'custom',
                'custom_expiry_date': t.strftime(
                    PasteForm.CUSTOM_EXPIRY_DATE_FORMAT
                ),
                'custom_expiry_time': 'garbage',
            }
        )
        self.assertFalse(f.is_valid())

    def test_validate_expires_custom_unparsable_date(self):
        t = timezone.now().replace(microsecond=0) + timedelta(hours=16)
        f = PasteForm(
            {
                'title': 't',
                'body': 'b',
                'expiry_preset': 'custom',
                'custom_expiry_date': 'garbage',
                'custom_expiry_time': t.strftime(
                    PasteForm.CUSTOM_EXPIRY_TIME_FORMAT
                ),
            }
        )
        self.assertFalse(f.is_valid())

    def test_validate_invalid_expiry_preset(self):
        f = PasteForm({'title': 't', 'body': 'b', 'expiry_preset': 'garbage'})
        self.assertFalse(f.is_valid())

    def test_validate_invalid_language(self):
        f = PasteForm({'title': 't', 'body': 'b', 'language': '1'})
        self.assertFalse(f.is_valid())

    def test_validate_language(self):
        lang = Language.objects.create(name='Python')
        f = PasteForm({'title': 't', 'body': 'b', 'language': str(lang.pk)})
        self.assertTrue(f.is_valid())

    # TODO test creation of Form from an instance.
