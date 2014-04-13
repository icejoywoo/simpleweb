#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-4-11

__author__ = 'wujiabin'

import json

from tornado import web
from tornado import escape

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
        # 默认显示页面
        if not self.request.arguments:
            # 获取无父节点的分类
            parents = self.db.query(Category).filter_by(parent_id=None).all()
            self.render("category.html", parents=parents)
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

    def post(self):
        kvargs = {k: ''.join(v) for k, v in self.request.arguments.items()}
        name = escape.to_unicode(kvargs["name"])
        try:
            c = self.db.query(Category).filter_by(name=name).one()
        except:
            c = Category(name)
        if kvargs["parent_id"]:
            parent_id = int(kvargs["parent_id"])
            c.parent_id = parent_id
        # 注意session的使用
        try:
            self.db.add(c)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()
        # redirect到原来的页面
        self.redirect("/category")


class MethodHandler(BaseHandler):

    def get(self):
        # 默认显示页面
        if not self.request.arguments:
            # 获取无父节点的分类
            self.render("method.html")
        # 获取全部数据
        elif "all" in self.request.arguments:
            method_json = json.dumps([i.as_dict() for i in self.db.query(Method).all()])
            self.set_header("Content-Type", "application/json")
            self.write(method_json)

    def post(self):
        if "all" in self.request.arguments:
            method_json = json.dumps([i.as_dict() for i in self.db.query(Method).all()])
            self.set_header("Content-Type", "application/json")
            self.write(method_json)
        else:
            kvargs = {k: escape.to_unicode(''.join(v)) for k, v in self.request.arguments.items()}
            m = Method(kvargs["name"], kvargs["description"])

            # 注意session的使用
            try:
                self.db.add(m)
                self.db.commit()
            except:
                self.db.rollback()
                raise
            finally:
                self.db.close()

    def delete(self, _id):
        m = self.db.query(Method).filter_by(id=_id).one()
        # 注意session的使用
        try:
            self.db.delete(m)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def put(self, _id):
        kvargs = {k: escape.to_unicode(''.join(v)) for k, v in self.request.arguments.items()}
        print kvargs
        m = self.db.query(Method).filter_by(id=_id).one()
        m.name = kvargs["name"]
        m.description = kvargs["description"]
        # 注意session的使用
        try:
            self.db.add(m)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()


class SampleHandler(BaseHandler):

    def get(self):
        if "all" in self.request.arguments:
            samples = self.db.query(Sample).all()
            print samples[1].category
            data = [i.as_dict() for i in samples]
            sample_json = json.dumps(data)
            self.set_header("Content-Type", "application/json")
            self.write(sample_json)
        else:
            self.render("sample.html")

    def post(self):
        if "all" in self.request.arguments:
            sample_json = json.dumps([i.as_dict() for i in self.db.query(Sample).all()])
            self.set_header("Content-Type", "application/json")
            self.write(sample_json)

    def put(self, _id):
        kvargs = {k: escape.to_unicode(''.join(v)) for k, v in self.request.arguments.items()}
        print kvargs
        s = self.db.query(Sample).filter_by(id=_id).one()
        s.labeled_result = kvargs["labeled_result"]
        # 注意session的使用
        try:
            self.db.add(s)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def delete(self, _id):
        s = self.db.query(Sample).filter_by(id=_id).one()
        # 注意session的使用
        try:
            self.db.delete(s)
            self.db.commit()
        except:
            self.db.rollback()
            raise
        finally:
            self.db.close()
