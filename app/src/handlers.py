import re
import json
import tornado.web


class SecuredHandler(tornado.web.RequestHandler):
    """ Validate, don't trust input, redirections, etc """

    def set_custom_headers(self):
        """ Set some custom and security related headers """
        self.set_header('x-frame-options', 'DENY')
        self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('Server', 'Server')

    def prepare(self):
        super(SecuredHandler, self).prepare()
        self.set_custom_headers()

    def redirect(self, location):
        """ A better, more secured redirect """
        location = self._strip_domain(location)
        return super(SecuredHandler, self).redirect(location)

    @classmethod
    def _strip_domain(cls, location):
        """ Strip domain from `location`, to prevent redirection
        to an external domain """
        pattern = r'^(?:https?://)?[-a-zA-Z0-9\.:]*/?'
        stripped = re.sub(pattern, '', location)
        return '/' + stripped


class BaseHandler(SecuredHandler):
    """ To be inherited by other handlers """

    def write_json(self, data, status_code=200):
        """ Write json data to the client """
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(status_code)
        self.write(json.dumps(data))


class MainHandler(BaseHandler):
    def get(self):
        self.render('home.html')
