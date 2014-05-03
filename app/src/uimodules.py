import tornado.web


class Item(tornado.web.UIModule):
    def render(self, pile):
        item = {}
        return self.render_string('modules/entry.html', item=item)