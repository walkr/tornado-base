# This module contains a series of rest handlers

from app.lib.torhelp.handler import BasePipedHandler
from app.lib.torhelp import pipeline

from app.src import models
from app.src import pipelines


class BaseResourceHandler(BasePipedHandler):
    GetPipeline = pipelines.common + pipeline.get
    PostPipeline = pipelines.common + pipeline.post
    DeletePipeline = pipelines.common + pipeline.delete
    PutPipeline = pipelines.common + pipeline.put


class UserHandler(BaseResourceHandler):
    Model = models.User
    Proxy = models.User.Proxy


class PostHandler(BaseResourceHandler):
    Model = models.Post
    Proxy = models.Post.Proxy


class CommentHandler(BaseResourceHandler):
    Model = models.Comment
    Proxy = models.Comment.Proxy
