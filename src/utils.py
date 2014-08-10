#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uredirect-py
#   by Naoki Rinmous <sukareki@gmail.com>
#   published under WTFPL


# Utility Functions

import json
import md5
import os.path
import random

def createUrlHash(url):
    m = md5.new()
    m.update(url)
    return m.hexdigest()

def generateId(length):
    list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    str = ''
    for i in range(0, length):
        str += list[random.randint(0, len(list) - 1)]
    return str

def getStaticPath():
    return os.path.join(os.path.dirname(__file__), 'static')

def readConfig(path):
    with open('config.json', 'rb') as f:
        config = json.load(f)

    config['db_host'] = config.get('host', 'localhost')
    config['db_port'] = config.get('port', 6379)
    config['db_id']   = config.get('db', 0)
    config['db_reversedb']   = config.get('reversedb', 0)

    config['http_port']   = config.get('http_port', 80)

    config['deflen']   = config.get('deflen', 6)
    config['prefix']   = config.get('prefix', 'http://localhost:8080/')

    return config
