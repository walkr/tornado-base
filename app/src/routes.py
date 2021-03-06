# Here is the route mapping for the app

import tornado.web
from app.src.handlers import auth, ws, web, rest


routes = [
    (r'/', web.HomeHandler),
    (r'/(about|privacy|terms)', web.PublicHandler),
    (r'/signup', auth.SignupHandler),
    (r'/login', auth.LoginHandler),
    (r'/logout', auth.LogoutHandler),
    (r'/channel/(.+)', web.ChannelHandler),
    (r'/ws/(.+)', ws.ChatHandler),
    (r'/v1/users\.json/?(.+)?', rest.UserHandler),
    (r'/v1/posts\.json/?(.+)?', rest.PostHandler),
    (r'/v1/comments\.json/?(.+)?', rest.CommentHandler),
    (r'/static/(.+)', tornado.web.StaticFileHandler),
]
