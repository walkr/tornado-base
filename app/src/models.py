import time
from app.lib.torhelp.model import *
# This module contains all the models used in the app

from app.lib.torhelp.proxy import MongodbProxy
from app import config


class BaseModel(Model):
    """ The base model to be inherited """
    Proxy = None

    def is_valid(self):
        return True


class User(BaseModel):
    """ User model """
    Proxy = MongodbProxy(config.DB['users'])

    key = CharField()
    username = CharField()
    password = CharField()
    created = IntegerField(default=lambda: int(time.time()))


class Post(BaseModel):
    """ Blog post model """
    Proxy = MongodbProxy(config.DB['posts'])

    key = CharField()
    userkey = CharField()
    title = CharField()
    content = CharField()
    timestamp = IntegerField(default=lambda: int(time.time()))
    tags = SetField(CharField())


class Comment(BaseModel):
    """ Comment model """
    Proxy = MongodbProxy(config.DB['comments'])

    key = CharField()
    userkey = CharField()
    content = CharField()
    created = IntegerField(default=lambda: int(time.time()))


class Channel(BaseModel):
    """ Chaneel/Room is an abstract model used for ws communication """

    secret = CharField()
    subscribers = SetField(CharField())
