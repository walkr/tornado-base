# Initialize database
import os
import rethinkdb as r

os.sys.path.append(os.getcwd())
from app import config


def catch_err(fun, *args, **kwargs):
    try:
        fun(*args, **kwargs)
    except Exception as e:
        print('Exception encountered: {}'.format(e))


# Create database
catch_err(lambda: r.db_create(config.DBNAME).run(config.DBCON))
tables = [
    'users', 'post', 'comments', 'messages', 'sessions',
    'activity', 'sms', 'settings', 'feedback',
]


# Create tables
for table in tables:
    catch_err(
        lambda: r.db(config.DBNAME).table_create(
            table, primary_key='key'
        ).run(config.DBCON)
    )
