#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-10

__author__ = 'icejoywoo'

import logging
import os
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from controllers import *

define("port", default=8888, help="listen on the given port", type=int)

url_routers = [
    (r"/", IndexHandler),
]

settings = {
    "cookie_secret": "61eJJFuYh7EQnp2XdTP1o/VooETzKXQAGaYdkL5gEmG=",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application(url_routers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line(sys.argv)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    if settings['debug']:  # debug log in dev mode
        logging.getLogger().setLevel(logging.DEBUG)
    tornado.ioloop.IOLoop.instance().start()