#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-10

__author__ = 'icejoywoo'

import os

import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

url_routers = [
    (r"/", IndexHandler),
]

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application(url_routers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()