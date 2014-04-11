#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

import time

from tornado import gen
from tornado import web


class BaseHandler(web.RequestHandler):
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


class SleepHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        start = time.time()
        res = yield gen.Task(time.sleep, seconds=5)
        self.write("when i sleep %f s" % (time.time() - start))
