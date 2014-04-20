#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-12

__author__ = 'icejoywoo'

import os

from controllers import *

# urls routers config
url_routers = [
    # 分类管理
    (r"/category", CategoryHandler),

    # 方法管理
    (r"/method", MethodHandler),
    (r"/method/([0-9]+)", MethodHandler),

    # 样本管理
    (r"/sample", SampleHandler),
    (r"/sample/([0-9]+)", SampleHandler),

    # jsonp测试
    (r"/jsonp", JsonpHandler),
    (r"/chat/socket", ChatSocketHandler),

    # default
    (r"/", IndexHandler),
    (r"/([^/]*)", DefaultHandler),
]

# tornado config
settings = {
    "cookie_secret": "35ehsFuYh7EQn42XdTP1o/VooETzKXQAFaYdkL5gEmG=",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

# mongodb config
# http://api.mongodb.org/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
mongodb_config = {
    "host": "localhost",
    "port": 27071,
}