import os
import sys


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
