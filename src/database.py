#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uredirect-py
#   by Naoki Rinmous <sukareki@gmail.com>
#   published under WTFPL


# Redis Connection & Data Controller

import redis
import utils

class Database:

    # Class Initializator
    def __init__(self, config):
        self.deflen = config['deflen']
        self.r = redis.StrictRedis(host = config['db_host'], port = config['db_port'], db = config['db_id'])
        self.rr = redis.StrictRedis(host = config['db_host'], port = config['db_port'], db = config['db_reversedb'])

    def lookupId(self, id):
        return self.r.get(id)

    def lookupUrl(self, url):
        return self.rr.get(utils.createUrlHash(url))

    def createRecord(self, url):
        # Lookup if exists
        reverse = self.lookupUrl(url)
        if reverse:
            # Return id if exists
            return reverse
        else:
            # Create if not exists, or generate another id
            newid = utils.generateId(self.deflen)
            while not self.r.setnx(newid, url):
                newid = utils.generateId(self.deflen)
            # Create reverse link
            self.rr.set(utils.createUrlHash(url), newid)
            # Return the new id
            return newid
