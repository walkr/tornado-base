import logging
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import config
from app.src import routes


application = tornado.web.Application(routes.routes, **config.TORNADO)

if __name__ == "__main__":
    define('port', default=8001, type=int)
    tornado.options.parse_command_line()
    logging.info(
        'Starting server [port={}] [debug={}]'.format(
            options.port, config.TORNADO['debug']))

    application.listen(options.port, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
