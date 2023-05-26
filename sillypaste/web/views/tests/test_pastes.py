from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.http import HttpResponseRedirect
from .. import ListPastes


def prepare_request(url, query={}, user=None):
    req = RequestFactory().get('/all', query)
    req.user = AnonymousUser() if user is None else user
    return req


class TestListPastes(TestCase):
    def test_cleans_bad_sort_key(self):
        req = prepare_request('/all', {'sort': 'BADKEY'})
        view = ListPastes()
        view.setup(req)
        out = view.get(req)
        self.assertIsInstance(out, HttpResponseRedirect)
        self.assertURLEqual(out.url, '/all')

    def test_keeps_good_sort_key(self):
        req = prepare_request('/all', {'sort': 'author'})
        view = ListPastes()
        view.setup(req)
        out = view.get(req)
        self.assertNotIsInstance(out, HttpResponseRedirect)

    def test_keeps_good_rev_sort_key(self):
        req = prepare_request('/all', {'sort': '-author'})
        view = ListPastes()
        view.setup(req)
        out = view.get(req)
        self.assertNotIsInstance(out, HttpResponseRedirect)
