#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-10

__author__ = 'icejoywoo'

import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from config import *

define("port", default=8888, help="listen on the given port", type=int)

engine = create_engine('sqlite:///:memory:', echo=True)


class Application(tornado.web.Application):
    def __init__(self, args, **kwargs):
        tornado.web.Application.__init__(self, args, **kwargs)
        self.db = scoped_session(sessionmaker(bind=engine))

if __name__ == "__main__":
    application = Application(url_routers, **settings)
    tornado.options.parse_command_line(sys.argv)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    if settings['debug']:  # debug log in dev mode
        logging.getLogger().setLevel(logging.DEBUG)
    tornado.ioloop.IOLoop.instance().start()