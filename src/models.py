#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-10

__author__ = 'icejoywoo'

import motor

from config import *


def get_client():
    # MotorClient takes the same constructor arguments as MongoClient
    client = motor.MotorClient(**mongodb_config)
    return client

if __name__ == "__main__":
    def a(args, **kwargs):
        print args, kwargs
    client = get_client()
    print client.alive(callback=a)
