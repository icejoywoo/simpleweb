#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

import json

from tornado import web

from models import *


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


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


class CategoryHandler(BaseHandler):
    def get(self):
        print self.request.arguments
        # 默认显示页面
        if not self.request.arguments:
            self.render("category.html")
        # 获取全部数据
        elif "all" in self.request.arguments:
            category_json = json.dumps([i.as_dict() for i in self.db.query(Category).all()])
            self.set_header("Content-Type", "application/json")
            self.write(category_json)
        # 根据请求获取数据
        else:
            # 把arguments的value list转换为整体, 假设这里的请求都是单个的, 不会重复
            filters = {k: ''.join(v) for k, v in self.request.arguments.items()}
            data = [i.as_dict() for i in self.db.query(Category).filter_by(**filters).all()]
            self.set_header("Content-Type", "application/json")
            if len(data) == 0:
                self.write(None)
            elif len(data) == 1:
                self.write(json.dumps(data[0]))
            else:
                self.write(json.dumps(data))