#!/usr/bin/env python
# coding=utf-8
from autobahn.twisted import choosereactor
choosereactor.install_optimal_reactor(False)
from twisted.python import log
from toughlib import config as iconfig
from toughlib.dbengine import get_engine
from toughnms.common import initdb as init_db
from toughlib import dispatch,logger
from twisted.internet import reactor
from hashlib import md5
import argparse
import sys
import os

reactor.suggestThreadPoolSize(60)

def update_timezone(config):
    try:
        if 'TZ' not in os.environ:
            os.environ["TZ"] = config.system.tz
        time.tzset()
    except:
        pass

def check_env(config):
    try:
        backup_path = config.database.backup_path
        if not os.path.exists(backup_path):
            os.system("mkdir -p  %s" % backup_path)
        if not os.path.exists("/var/toughnms"):
            os.system("mkdir -p /var/toughnms")
    except Exception as err:
        import traceback
        traceback.print_exc()

def run_initdb(config):
    init_db.update(config)


def run():
    log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-manage', '--manage', action='store_true', default=False, dest='manage', help='run manage')
    parser.add_argument('-initdb', '--initdb', action='store_true', default=False, dest='initdb', help='run initdb')
    parser.add_argument('-port', '--port', type=int, default=0, dest='port', help='admin port')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, dest='debug', help='debug option')
    parser.add_argument('-x', '--xdebug', action='store_true', default=False, dest='xdebug', help='xdebug option')
    parser.add_argument('-c', '--conf', type=str, default="/etc/toughnms.json", dest='conf', help='config file')
    args = parser.parse_args(sys.argv[1:])

    config = iconfig.find_config(args.conf)
    syslog = logger.Logger(config)
    dbengine = get_engine(config)
    dispatch.register(syslog)

    with open("/var/toughnms/token","wb") as tf:
        tf.write(md5(config.system.secret.encode('utf-8')).hexdigest())

    update_timezone(config)
    check_env(config)

    if args.debug or args.xdebug:
        config.defaults.debug = True

    if args.port > 0:
        config.server.port = int(args.port)

    if args.manage:
        from toughnms.console import admin_app
        admin_app.run(config,dbengine)
        reactor.run()

    if args.initdb:
        init_db.update(get_engine(config))

