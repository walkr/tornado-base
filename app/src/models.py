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

    @classmethod
    def query(cls, fltr, limit=0, offset=0):
        results = cls.Proxy.query(fltr, limit, offset)
        return [cls(**r) for r in results] if results else None


class User(BaseModel):
    """ User model """
    Proxy = MongodbProxy(config.DB['users'])

    key = StringField()
    username = StringField()
    password = StringField()
    created = IntegerField(default=lambda: int(time.time()))


class Post(BaseModel):
    """ Blog post model """
    Proxy = MongodbProxy(config.DB['posts'])

    key = StringField()
    userkey = StringField()
    title = StringField()
    content = StringField()
    timestamp = IntegerField(default=lambda: int(time.time()))
    tags = SetField(StringField())


class Comment(BaseModel):
    """ Comment model """
    Proxy = MongodbProxy(config.DB['comments'])

    key = StringField()
    userkey = StringField()
    content = StringField()
    created = IntegerField(default=lambda: int(time.time()))


class Channel(BaseModel):
    """ Chaneel/Room is an abstract model used for ws communication """

    secret = StringField()
    subscribers = SetField(StringField())


class Activity(BaseModel):
    """ Activity log """

    Proxy = MongodbProxy(config.DB['activity'])

    key = StringField()
    ip = StringField()
    kind = StringField()
    userkey = StringField()
    message = StringField()
    private = BooleanField(default=True)
