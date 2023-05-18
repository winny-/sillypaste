from django.test import TestCase
from django.template import Template, Context
from datetime import datetime
from . import localtime  # noqa: F401


# TODO also test the human readable time format.
class TestLocaltimeTemplateTag(TestCase):

    TEMPLATE_NOW = Template('{% load localtime %} {% localtime %}')
    TEMPLATE_SPECIFIED_TIME = Template(
        '{% load localtime %} {% localtime t %}'
    )

    def test_now(self):
        rendered = self.TEMPLATE_NOW.render(Context())
        expected_seconds = str(
            int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
        )[:-2]
        self.assertIn(f'data-utc-ms="{expected_seconds}', rendered)

    def test_specified_time(self):
        n = datetime(2020, 1, 1, 19, 20)
        rendered = self.TEMPLATE_SPECIFIED_TIME.render(Context({'t': n}))
        expected_seconds = str(int((n - datetime(1970, 1, 1)).total_seconds()))
        self.assertIn(f'data-utc-ms="{expected_seconds}', rendered)
