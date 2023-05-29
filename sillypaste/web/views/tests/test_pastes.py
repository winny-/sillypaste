from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpResponsePermanentRedirect,
)
from django.http.response import Http404
from .. import ListPastes, show_paste, show_raw


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


class TestViewPaste(TestCase):

    fixtures = ['one-paste']

    def test_404_missing_paste(self):
        req = prepare_request('/123')
        self.assertRaises(Http404, lambda: show_paste(req, 123))

    def test_get_paste(self):
        req = prepare_request('/1')
        out = show_paste(req, 1)
        self.assertIsInstance(out, HttpResponse)
        self.assertEqual(out.status_code, 200)

    def test_get_raw_paste(self):
        req = prepare_request('/1/raw')
        out = show_raw(req, 1)
        self.assertIsInstance(out, HttpResponse)
        self.assertEqual(out.status_code, 200)
        self.assertIn('text/plain', out.headers['content-type'])

    def test_raw_routing(self):
        out = self.client.get('/1/raw/')
        self.assertEqual(out.status_code, 200, "GET /1/raw/")
        out = self.client.get('/1/raw')
        self.assertIsInstance(out, HttpResponsePermanentRedirect)
        self.assertEqual(out.url, '/1/raw/')
