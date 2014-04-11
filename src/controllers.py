#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")
