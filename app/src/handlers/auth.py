import logging

from app.lib.torhelp import handler
from app.lib.torhelp import pipe
from app.lib.torhelp.users import Manager
from app.lib.torhelp.crypto import Hasher

from app import config
from app.src import jobs
from app.src import models
from app.src.pipelines import *


manager = Manager(
    proxy=MongodbProxy(config.DB['users']),
    hasher=Hasher('sha256')
)


# ============================== http post pipes ============================


class ClearPipe(pipe.Pipe):
    """ Clear the response to prevent any output to the client """

    def __call__(self, req, res):
        res.body = None
        return (req, res)


class MaybeRedirectPipe(pipe.Pipe):
    """ Redirect user if a session exists """

    def __init__(self, location, **kwargs):
        super(MaybeRedirectPipe, self).__init__(**kwargs)
        self.location = location

    def __call__(self, req, res):
        if req.session.data:
            req.handler.redirect(self.location)
        return (req, res)


class SignupUserPipe(pipe.Pipe):
    """ Create a new user in the database """

    def __call__(self, req, res):
        user, error = manager.create_user(req.body)
        if error:
            res.error = error
            req.handler.render('public/signup.html', req=req, res=res)
        else:
            res.body = user
        return (req, res)


class LoginUserPipe(pipe.Pipe):
    """ Login an existing user """

    def log_fail(self, req):
        """ log failed activity """

        # Get userkey
        users = models.User.query({'username': req.body['username']})
        userkey = users[0].key if users else None

        # Save login attempt to db
        data = {
            'ip': req.handler.request.remote_ip,
            'kind': 'login:failure',
            'userkey': userkey,
            'message': 'failed login for user `{}`'.format(req.body['username'])
        }
        config.JOBS_QUEUE.enqueue(jobs.Activity.log, data, result_ttl=0)

    def __call__(self, req, res):
        user, error = manager.authenticate_user(
            req.body['username'], req.body['password']
        )
        if error:
            res.error = error
            self.log_fail(req)
            req.handler.render('public/login.html', req=req, res=res)
        else:
            res.body = user
        return (req, res)


class LogActivityPipe(pipe.Pipe):
    """ Log auth attempts """

    def __init__(self, kind, **kwargs):
        super(LogActivityPipe, self).__init__(**kwargs)
        self.kind = kind

    def log(self, req):
        data = {
            'userkey': req.session.get('userkey') if req.session else None,
            'ip': req.handler.request.remote_ip,
            'kind': self.kind,
        }
        config.JOBS_QUEUE.enqueue(jobs.Activity.log, data, result_ttl=0)

    def __call__(self, req, res):
        self.log(req)
        return (req, res)


# ================================ pipelines ==============================

# create a rate limiter (3 reqs/s per IP, with 0 burst reqs every 0 secs)
auth_rl_pipe = pipe.RateLimit(RedisProxy(config.REDIS), 30, 1, 0, 0)


signup_get_pipeline = pipe.Pipeline(
    auth_rl_pipe,
    sr_pipe,
    MaybeRedirectPipe('/'),
    pipe.HTMLEncode('public/signup.html')
)


login_get_pipeline = pipe.Pipeline(
    auth_rl_pipe,
    sr_pipe,
    MaybeRedirectPipe('/'),
    pipe.HTMLEncode('public/login.html')
)

signup_post_pipeline = pipe.Pipeline(
    pipe.PostFormDecode(),
    SignupUserPipe(),
    sw_pipe,
    LogActivityPipe('signup:success'),
    ClearPipe(),
    MaybeRedirectPipe('/'),
)


login_post_pipeline = pipe.Pipeline(
    pipe.PostFormDecode(),
    LoginUserPipe(),
    sw_pipe,
    LogActivityPipe('login:success'),
    ClearPipe(),
    MaybeRedirectPipe('/')
)


logout_get_pipeline = pipe.Pipeline(
    auth_rl_pipe,
    sr_pipe,
    LogActivityPipe('logout:success'),
    srm_pipe,
    pipe.Redirect('/')
)


# ================================ handlers ==============================

class AuthHandler(handler.BasePipedHandler):
    Model = models.User


class SignupHandler(AuthHandler):
    GetPipeline = signup_get_pipeline
    PostPipeline = signup_post_pipeline


class LoginHandler(AuthHandler):
    GetPipeline = login_get_pipeline
    PostPipeline = login_post_pipeline


class LogoutHandler(AuthHandler):
    GetPipeline = logout_get_pipeline
