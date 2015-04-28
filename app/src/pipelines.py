# This module contains a seris of useful pipelines

from app.lib.torhelp import pipe
from app.lib.torhelp.proxy import *
from app.lib.torhelp.session import *

from app import config


# rate limit pipe
rl_pipe = pipe.RateLimit(
    RedisProxy(config.REDIS), 20, 1, 10, 5*60, name='rate_limit')

# session read pipe
sr_pipe = pipe.SessionRead(
    RedisSessionReaderWriter(config.REDIS),
    Session,
    name='session_read')

# session write pipe
sw_pipe = pipe.SessionWrite(
    RedisSessionReaderWriter(config.REDIS),
    Session,
    name='session_write')

# session remove pipe
srm_pipe = pipe.SessionRemove(
    RedisSessionReaderWriter(config.REDIS),
    Session,
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
