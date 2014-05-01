#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import os
import sys
if platform.system() == 'Windows':
    reload(sys)
    sys.setdefaultencoding('gbk')

import logging
import importlib
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.options import options, define
from application import Application


define('appdir', type=str, default=os.path.abspath(os.path.dirname(__file__)))
define('debug', type=bool, default=True)
define('port', type=int, default=9000)

def main():
    os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
    path = os.path.dirname(os.path.abspath(__file__))
    if path not in sys.path:
        sys.path.insert(0, path)

    parse_command_line()
    if options.debug:
        logging.info('Starting server at port %s in debug mode' % options.port)
    else:
        logging.info('Starting server at port %s' % options.port)

    hds = set(os.path.splitext(it)[0] for it in os.listdir('./handlers'))
    hds = [it for it in hds if it not in ('__init__', 'base','.svn','.DS_Store')]
    hdmodules = []
    for hd in hds:
        try:
            _hd = 'handlers.%s' % hd
            logging.info('load_module %s'%_hd)
            hdmodules.append(importlib.import_module(_hd))
        except:
            logging.exception("load_module error ")
            continue

    app = Application()
    app.load_module(hdmodules)

    server = HTTPServer(app, xheaders=True)
    server.listen(int(options.port), '0.0.0.0')
    if options.debug:
        from tornado import autoreload
        autoreload.start(IOLoop.instance())
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
