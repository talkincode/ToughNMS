#!/usr/bin/env python
#coding=utf-8

import types
from tornado import web
from tornado.websocket import WebSocketHandler
from tornado.options import options
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from mako.lookup import TemplateLookup
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from handlers.base import BaseHandler
from handlers.base import PageNotFoundHandler
from lib import rutils
from settings import config
import db_models


class Application(web.Application):
    app_urls = [(r'/favicon.ico', web.StaticFileHandler,
                {'path': "/static/favicon.ico"}),
                ('.*', PageNotFoundHandler), ]

    def __init__(self):
        super(Application, self).__init__(self.app_urls, **config)

        db_models.engine = create_engine(config['db_url'],echo=config['db_echo'],convert_unicode=True)

        self.db = scoped_session(sessionmaker(
            bind=db_models.engine,
            autocommit=False,
            autoflush=False
        ))


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


    def load_module(self, modules, **options):
        for module in modules:
            assert isinstance(module,types.ModuleType)
            host_pattern = options.get('host_pattern', '.*$')

            # 处理加载 RequestHandler 和路由规则
            cls_valid = lambda cls: type(cls) is types.TypeType \
                     and (issubclass(cls, BaseHandler)
                     or issubclass(cls,WebSocketHandler))  # 是否有效

            url_valid = lambda cls: hasattr(cls, 'url_pattern') and cls.url_pattern  # 是否拥有 url 规则
            mod_attrs = (getattr(module, i) for i in dir(module) if not i.startswith('_'))
            valid_handlers = [(i.url_pattern, i) for i in mod_attrs if cls_valid(i) and url_valid(i)]

            # 处理完毕载入
            self.add_handlers(host_pattern, valid_handlers)
            self.logging.info(valid_handlers)

    def _get_host_handlers(self, request):
        host = request.host.lower().split(':')[0]
        handlers = (i for p, h in self.handlers for i in h if p.match(host))
        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]
        return handlers




