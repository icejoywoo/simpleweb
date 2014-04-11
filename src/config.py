#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-12

__author__ = 'icejoywoo'

import os

from controllers import *

# urls routers config
url_routers = [
    (r"/sleep", SleepHandler),
    (r"/", IndexHandler),
    (r"/([^/]*)", DefaultHandler),
]

# tornado config
settings = {
    "cookie_secret": "61ehsFuYh7EQn42XdTP1o/VooETzKXQAFaYdkL5gEmG=",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

# mongodb config
# http://api.mongodb.org/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient
mongodb_config = {
    "host": "localhost",
    "port": 27071
}