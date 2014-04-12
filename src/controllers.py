#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

from tornado import web


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db()


class IndexHandler(BaseHandler):
    """
    index page
    """
    def get(self):
        print self.db
        self.render("index.html")


class DefaultHandler(BaseHandler):
    """
    default handler to look up the template named "${name}.html"
    """
    def get(self, name):
        self.render("%s.html" % name)

