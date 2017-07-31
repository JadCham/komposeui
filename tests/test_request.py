from django.test import TestCase
from django.test.client import RequestFactory
from webapp.views import *


class TestRequest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_existence(self):
        response = index(self.factory.get('/'))
        self.assertEqual(response.status_code, 200, "GET / failed status code")

    def test_upload_simple(self):
        response = index(self.factory.post('/', {"input_text": "version: 2"}, content_type="application/json"))
        self.assertEqual(response.status_code, 200, "POST / failed status code")
