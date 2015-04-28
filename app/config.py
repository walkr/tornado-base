import os
import sys
import redis
import pymongo
import rq

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(ROOT_DIR))

from app.src import uimodules


TORNADO = dict(
    template_path=os.path.join(ROOT_DIR, 'www/templates'),
    static_path=os.path.join(ROOT_DIR, 'www/static'),
    ui_modules=uimodules,
    login_url='/user/login',
    cookie_secret='cookie-secret-change-this',
    xsrf_cookies=True,
    debug=True,
)


DB = pymongo.MongoClient()['tornado_base']
REDIS = redis.Redis()
JOBS_QUEUE = rq.Queue(connection=REDIS)
