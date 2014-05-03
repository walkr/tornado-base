import tornado.web
from src.handlers import MainHandler


routes = [
    (r'/', MainHandler),
    (r'/static/(.+)', tornado.web.StaticFileHandler),
]