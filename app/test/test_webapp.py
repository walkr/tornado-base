import unittest
from tornado.testing import AsyncHTTPTestCase

import os
import sys
import copy
import unittest
import logging


sys.path.append(os.path.dirname(__file__) + '/..')

from app import server


class WebTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return server.application

    def get_handlers(self):
        return server.routes.routes

    def post(self, url, data, encode=True, **kwargs):
        body = urlencode(data) if encode else body
        return self.fetch(url, method='POST', body=body, **kwargs)

    def post_json(self, url, data, **kwargs):
        data = json.dumps(data)
        return self.post(url, data, **kwargs)


class HTTPTest(WebTestCase):

    usernames = {
        'john', 'mike', 'jessica', 'michelle', 'vanessa',
        'tony', 'roger', 'joe', 'alex', 'dan', 'oliver'
    }

    def test_get_main(self):
        resp = self.fetch('/')
        self.assertEqual(200, resp.code)


if __name__ == '__main__':
    unittest.main()
