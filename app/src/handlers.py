import time
import json
import logging
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """ To be inherited by other handlers """

    def set_custom_headers(self):
        """ Set some custom and security related headers """
        self.set_header('x-frame-options', 'DENY')
        self.set_header('x-xss-protection', '1; mode=block')

    def prepare(self):
        super(BaseHandler, self).prepare()
        self.set_custom_headers()

    def write_json(self, data, status_code=200):
        """ Write json data to the client """
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(status_code)
        self.write(json.dumps(data))


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html')
