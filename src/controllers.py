#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    """
    index page
    """
    def get(self):
        self.render("index.html")


class DefaultHandler(BaseHandler):
    """
    default handler to look up the template named "${name}.html"
    """
    def get(self, name):
        self.render("%s.html" % name)
