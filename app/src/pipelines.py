# This module contains a seris of useful pipelines

from app.lib.torhelp import pipe
from app.lib.torhelp.proxy import *
from app.lib.torhelp.session import *
from app.src import util
from app import config


# rate limit pipe
rl_proxy = RedisProxy(pipe.RateLimit.RateLimitModel, config.REDIS)
rl_conf = pipe.RateLimit.RateLimitConfig(20, 1, 10, 5*60)
rl_pipe = pipe.RateLimit(rl_proxy, rl_conf, name='rate_limit')

# session proxy
sess_proxy = util.make_proxy_for_table(Session, 'sessions')

# session read pipe
sr_pipe = pipe.SessionRead(
    SessionReaderWriter(sess_proxy),
    name='session_read')

# session write pipe
sw_pipe = pipe.SessionWrite(
    SessionReaderWriter(sess_proxy),
    name='session_write')

# session remove pipe
srm_pipe = pipe.SessionRemove(
    SessionReaderWriter(sess_proxy),
    name='session_remove')

# authorize pipe
authorize_pipe = pipe.Authorize(name='authorize')


# a common pipeline to be used across handlers
common = pipe.Pipeline(
    rl_pipe,
    sr_pipe,
    pipe.Authenticate(name='authenticate'),
)


# simple pipeline for showing html pages
html = lambda filepath: pipe.Pipeline(pipe.HTMLEncode(filepath, name='html'))
