from . import validate_future_datetime, validate_paste_sort_key
from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz


class TestValidatoFutureDatetime(TestCase):
    def test_past(self):
        with self.assertRaises(ValidationError):
            t = datetime(1980, 1, 1, 19, 1, 0, 0, pytz.UTC)
            validate_future_datetime(timezone.localtime(t))

    def test_future(self):
        t = datetime(2100, 1, 1, 19, 1, 0, 0, pytz.UTC)
        self.assertIsNone(validate_future_datetime(timezone.localtime(t)))


class TestValidatePasteSortKey(TestCase):
    def test_empty(self):
        with self.assertRaises(ValidationError):
            validate_paste_sort_key('')

    def test_wrong_type(self):
        with self.assertRaises(ValidationError):
            validate_paste_sort_key(42)

    def test_unknown_key(self):
        with self.assertRaises(ValidationError):
            validate_paste_sort_key('whoknows')

    def test_valid_id(self):
        self.assertIsNone(validate_paste_sort_key('id'))
