import os
import sys
import json

from tornado.testing import AsyncHTTPTestCase, AsyncHTTPClient

sys.path.append(os.path.dirname(__file__) + '/..')
from app import server

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class WebTestCase(AsyncHTTPTestCase):

    def get_app(self):
        app = server.application
        for index, urlspec in enumerate(app.handlers[0][1]):
            try:
                urlspec.handler_class.GetPipeline.pop('rate_limit')
                urlspec.handler_class.GetPipeline.pop('authenticate')
            except (AttributeError, TypeError):
                pass
        return app

    def get_handlers(self):
        return server.routes.routes

    # GET =========================================================

    @property
    def client(self):
        return AsyncHTTPClient(self.io_loop)

    def get(self, url, qparams=None, **kwargs):
        url = url + '?' + urlencode(qparams) if qparams else url
        return self.fetch(url, method='GET', **kwargs)

    def json_get(self, url, key=None, qparams=None):
        url = url + '/' + key if key else url
        resp = self.get(url, qparams=qparams)
        return resp

    # POST =========================================================

    def post(self, url, data, encode=True, **kwargs):
        body = urlencode(data) if encode else data
        resp = self.fetch(url, method='POST', body=body, **kwargs)
        return resp

    def json_post(self, url, data, **kwargs):
        data = bytes(json.dumps(data), 'utf-8')
        return self.post(url, data, encode=False, **kwargs)

    # DELETE =========================================================

    def delete(self, url):
        return self.fetch(url, method='DELETE')
