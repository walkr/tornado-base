import os
import sys
import redis
import rq
import rethinkdb
import logging

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(os.path.dirname(ROOT_DIR))

from app.src import uimodules


# ==========================================================
# TORNADO SETTINGS
# ==========================================================
TORNADO = dict(
    template_path=os.path.join(ROOT_DIR, 'www/templates'),
    static_path=os.path.join(ROOT_DIR, 'www/static'),
    ui_modules=uimodules,
    login_url='/user/login',
    cookie_secret='cookie-secret-change-this',
    xsrf_cookies=True,
    debug=True,
)


# ==========================================================
# DATABASE & SECURITY SETTINGS
# ==========================================================
DBNAME = 'appname'
ENV = os.environ.get('APPNAME_ENV')

# Local
if ENV in ['local', None]:
    DBCON = rethinkdb.connect()
    TORNADO['debug'] = True
    TORNADO['xsrf_cookies'] = False

# Production
else:
    DBCON = rethinkdb.connect(host='YOUR-SQL-PRIVATE-IP')

if ENV is None:
    logging.warning('* APPNAME_ENV var not set. Defaulting to local.')


# ==========================================================
# REDIS CONNECTION + rq QUEUES
# ==========================================================
REDIS = redis.Redis()
JOBS_QUEUE = rq.Queue(connection=REDIS)


# ==========================================================
# TWILIO SETTINGS
# ==========================================================
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_NUMBER = ''
