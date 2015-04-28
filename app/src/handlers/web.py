# This module contains web/browser handlers

from app.lib.torhelp import pipe
from app.lib.torhelp import handler
from app.lib.torhelp import pipeline

from app.src import models
from app.src import pipelines


class HTMLView(handler.BasePipedHandler):
    """ Inherit this handler """


class HomeHandler(HTMLView):
    """ Display the homepage """

    Model = models.Post
    Proxy = models.Post.Proxy
    GetPipeline = pipeline.get.clone(encode=pipe.HTMLEncode('home.html'))


class PublicHandler(HTMLView):
    """ Serve public pages """

    class PublicPipe(pipe.Pipe):
        def __call__(self, req, res):
            filepath = 'public/{}.html'.format(req.args[0])
            return pipe.HTMLEncode(filepath)(req, res)

    GetPipeline = pipe.Pipeline(PublicPipe())


class ChannelHandler(HTMLView):
    """ Serve the chat/channel page """

    GetPipeline = pipelines.html('channel.html')
