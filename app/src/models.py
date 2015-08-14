# This module contains all the models used in the app

import time

from app.lib.torhelp.model import *
from app.src import util


class BaseModel(Model):
    """ The base model to be inherited """
    Proxy = None

    def is_valid(self):
        return True

    @classmethod
    def query(cls, fltr, limit=0, offset=0):
        results = cls.Proxy.query(fltr, limit, offset)
        return [cls(**r) for r in results] if results else None

    def save(self):
        data = self.Proxy.post(self)
        self.key = data.key


class User(BaseModel):
    """ User model """

    key = StringField()
    username = StringField()
    password = StringField()
    fullname = StringField()
    image = StringField()
    created = IntegerField(default=lambda: int(time.time()))


class Post(BaseModel):
    """ Blog post model """

    key = StringField()
    userkey = StringField()
    title = StringField()
    content = StringField()
    timestamp = IntegerField(default=lambda: int(time.time()))
    tags = SetField(StringField())


class Comment(BaseModel):
    """ Comment model """

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

    key = StringField()
    ip = StringField()
    kind = StringField()
    userkey = StringField()
    message = StringField()
    private = BooleanField(default=True)


User.Proxy = util.make_proxy_for_table(User, 'users')
Post.Proxy = util.make_proxy_for_table(Post, 'post')
Comment.Proxy = util.make_proxy_for_table(Comment, 'comments')
Activity.Proxy = util.make_proxy_for_table(Activity, 'activity')
