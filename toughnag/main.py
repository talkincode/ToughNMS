#!/usr/bin/env python
# -*- coding: utf-8 -*-
activate_this = '../env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
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
from lib import router

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

    app = Application()
    handler_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"handlers")
    router.load_handlers(app, handler_path=handler_path, pkg_prefix="handlers")

    server = HTTPServer(app, xheaders=True)
    server.listen(int(options.port), '0.0.0.0')
    if options.debug:
        from tornado import autoreload
        autoreload.start(IOLoop.instance())
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
