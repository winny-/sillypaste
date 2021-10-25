from . import validate_future_datetime
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
