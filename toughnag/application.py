#!/usr/bin/env python
#coding=utf-8

import types
from tornado import web
from tornado.websocket import WebSocketHandler
from tornado.options import options
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from mako.lookup import TemplateLookup
from handlers.base import BaseHandler
from handlers.base import PageNotFoundHandler
from lib import rutils
from lib.mongutils import mongodb
from settings import config


class Application(web.Application):
    app_urls = [(r'/favicon.ico', web.StaticFileHandler,
                {'path': "/static/favicon.ico"}),
                ('.*', PageNotFoundHandler), ]

    def __init__(self):
        super(Application, self).__init__(self.app_urls, **config)

        self.mongodb = mongodb

        self.cache = CacheManager(**parse_cache_config_options({
            'cache.type': 'file',
            'cache.data_dir': './tmp/cache/data',
            'cache.lock_dir': './tmp/cache/lock'
        }))

        self.tp_lookup = TemplateLookup(directories=['./templates'],
                                        default_filters=['decode.utf8'],
                                        input_encoding='utf-8',
                                        output_encoding='utf-8',
                                        encoding_errors='replace',
                                        module_directory="./tmp")
        
        self.logging = rutils.getLogger("server", "./server.log",debug=options.debug)



    def _get_host_handlers(self, request):
        host = request.host.lower().split(':')[0]
        handlers = (i for p, h in self.handlers for i in h if p.match(host))
        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]
        return handlers




