import tornado.web


class Module(tornado.web.UIModule):
    """ General purpose module rendering """

    def render(self, filepath, **kwargs):
        return self.render_string(filepath, **kwargs)
