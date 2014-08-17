#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uredirect-py
#   by Naoki Rinmous <sukareki@gmail.com>
#   published under WTFPL


# HTTP Frontend Server
#   simply place it behind nginx

import os.path
import re
from tornado.ioloop import IOLoop
from tornado.template import Template
#from tornado.util import raise_exc_info
from tornado.web import Application, HTTPError, RequestHandler, StaticFileHandler, url
import utils

class Server:
    class CustomRequestHandler(RequestHandler):
        def write_error(self, status_code, **kwargs):
            self.render('./static/error.html');

    class LookupHandler(CustomRequestHandler):
        def initialize(self, db, restrict):
            self.db = db
            self.restrict = restrict
        def get(self, id):
            url = self.db.lookupId(id)
            if url:
                if self.restrict:
                    self.render('./static/restricted.html', url = url)
                else:
                    self.redirect(url)
            else:
                self.render('./static/null.html')

    class DisplayHandler(CustomRequestHandler):
        def initialize(self, db, prefix):
            self.db = db
            self.urlprefix = prefix
        def get(self, id):
            local = self.urlprefix + id
            rlocal = self.urlprefix + 'r/' + id
            url = self.db.lookupId(id)
            if url:
                self.render('./static/show.html', local = local, url = url, rlocal = rlocal)
            else:
                self.render('./static/null.html')

    class CommitHandler(CustomRequestHandler):
        def initialize(self, db, prefix):
            self.db = db
            self.urlpartten = re.compile('^((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)$')
            self.urlprefix = prefix
        def get(self):
            self.render('commit.html')
        def post(self):
            url = self.get_argument('url', '')
            if not url:
                raise HTTPError(400)
            if len(url) > 255:
                raise HTTPError(400)
            if not self.urlpartten.match(url):
                raise HTTPError(400)
            self.redirect(self.urlprefix + self.db.createRecord(url) + '/show')

    class StaticHandler(StaticFileHandler):
        def initialize(self, path):
            self.dirname, self.filename = os.path.split(path)
            super(Server.StaticHandler, self).initialize(self.dirname)

        def get(self, path=None, include_body=True):
            # Ignore 'path'.
            super(Server.StaticHandler, self).get(self.filename, include_body)

        def write_error(self, status_code, **kwargs):
            self.render('./static/error.html');

    def __init__(self, config, db):
        self.app = self.createApplication(db, config['prefix'])
        self.app.listen(config['http_port'])
        IOLoop.current().start()

    def createApplication(self, db, prefix):
        return Application([
            # Front page
            url(r"^/$", self.StaticHandler, {'path': './static/index.html'}),

            # Commit interface
            url(r"^/new$", self.CommitHandler, dict(db = db, prefix = prefix)),

            # Redirect & Display
            url(r"^/([A-Z,a-z,0-9]{6})$", self.LookupHandler, dict(db = db, restrict = False)),
            url(r"^/([A-Z,a-z,0-9]{6})/show$", self.DisplayHandler, dict(db = db, prefix = prefix)),

            # Restricted Redirect (R-18, etc.)
            url(r"^/r/([A-Z,a-z,0-9]{6})$", self.LookupHandler, dict(db = db, restrict = True)),

            # Reject with 404
            url(r"^/(.*)", self.StaticHandler, {'path': './static/null.html'})
        ])
