#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import importlib
import logging
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

def route(url_pattern):
    def handler_wapper(cls):
        assert (issubclass(cls, RequestHandler) or issubclass(cls, WebSocketHandler))
        setattr(cls,'url_pattern',url_pattern)
        return cls
    return handler_wapper

def load_handlers(app, handler_path=None,pkg_prefix=None, 
                  excludes=('__init__', 'base','.svn','.DS_Store'),**options):

    def find_handlers():
        hds = set(os.path.splitext(it)[0] for it in os.listdir(handler_path))
        hds = [it for it in hds if it not in excludes]
        for hd in hds:
            try:
                _hd = '%s.%s' % (pkg_prefix,hd)
                logging.info('load_module %s'%_hd)
                yield importlib.import_module(_hd)
            except:
                logging.exception("load_module error ")
                continue

    for module in find_handlers():
        assert isinstance(module,types.ModuleType)
        host_pattern = options.get('host_pattern', '.*$')

        # 处理加载 RequestHandler 和路由规则
        cls_valid = lambda cls: type(cls) is types.TypeType \
                 and (issubclass(cls, RequestHandler)
                 or issubclass(cls,WebSocketHandler))  # 是否有效

        url_valid = lambda cls: hasattr(cls, 'url_pattern') and cls.url_pattern  # 是否拥有 url 规则
        mod_attrs = (getattr(module, i) for i in dir(module) if not i.startswith('_'))
        valid_handlers = [(i.url_pattern, i) for i in mod_attrs if cls_valid(i) and url_valid(i)]

        # 处理完毕载入
        app.add_handlers(host_pattern, valid_handlers)
        app.logging.info(valid_handlers)



