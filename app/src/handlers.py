import time
import json
import logging
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """ To be inherited by other handlers """

    def write_json(self, data, status_code=200):
        """ Write json data to the client """
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(status_code)
        self.write(json.dumps(data))


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html')
