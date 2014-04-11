#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-12

__author__ = 'icejoywoo'

from tornado import ioloop, httpclient
import functools


class MyTask(object):

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def callback(self, response):
        try:
            self.gen.send(response)
        except StopIteration:
            pass

    def run(self, gen):
        self.gen = gen
        partail_func = functools.partial(self.func, *self.args, **self.kwargs)
        partail_func(callback=self.callback)


def myengine(func):
    def _(*args, **kwargs):
        task_generator = func(*args, **kwargs)
        task = task_generator.next()
        task.run(task_generator)
    return _

@myengine
def download(url):
    http_client = httpclient.AsyncHTTPClient()
    response = yield MyTask(http_client.fetch, url)
    print 'response.length =', len(response.body)
    ioloop.IOLoop.instance().stop()

download("http://www.baidu.com/")
ioloop.IOLoop.instance().start()