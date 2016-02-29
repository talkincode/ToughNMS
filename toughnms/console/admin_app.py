#!/usr/bin/env python
#coding:utf-8
import sys
import os
import time
import importlib
import cyclone.web
from twisted.python import log
from twisted.internet import reactor
from mako.lookup import TemplateLookup
from sqlalchemy.orm import scoped_session, sessionmaker
from toughlib import logger, utils, dispatch
from toughlib.dbengine import get_engine
from toughlib.permit import permit, load_events, load_handlers
from toughlib import db_session as session
from toughlib import db_cache as cache
from toughlib import dispatch
from toughlib.dbutils import make_db
from toughnms.console import models
from toughnms.console.handlers import host_perf
from toughnms.console.settings import *
from toughnms.common.nagutils import NagiosApi
from toughnms.common.mongodb import MongoDB
import toughnms

class HttpServer(cyclone.web.Application):
    def __init__(self, config=None, dbengine=None, **kwargs):

        self.config = config

        settings = dict(
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            template_path=os.path.join(os.path.dirname(toughnms.__file__), "views"),
            static_path=os.path.join(os.path.dirname(toughnms.__file__), "static"),
            xsrf_cookies=True,
            config=self.config,
            debug=self.config.system.debug,
            xheaders=True,
        )

        self.tp_lookup = TemplateLookup(
            directories=[settings['template_path']],
            default_filters=['decode.utf8'],
            input_encoding='utf-8',
            output_encoding='utf-8',
            encoding_errors='ignore',
            module_directory="/tmp/toughnms"
        )

        self.db_engine = dbengine or get_engine(config)
        self.db = scoped_session(sessionmaker(bind=self.db_engine, autocommit=False, autoflush=False))
        self.session_manager = session.SessionManager(settings["cookie_secret"], self.db_engine, 600)
        self.mcache = cache.CacheManager(self.db_engine)
        self.nagapi = NagiosApi(self.config)
        self.mongodb = MongoDB(self.config.database.mongodb_url,self.config.database.mongodb_port)

        self.aes = utils.AESCipher(key=self.config.system.secret)

        # cache event init
        dispatch.register(self.mcache)

        # app init_route
        load_handlers(handler_path=os.path.join(os.path.abspath(os.path.dirname(__file__))),
            pkg_prefix="toughnms.console", excludes=['base','webserver','radius'])

        self.init_route_permit()

        # app event init
        # event_params= dict(dbengine=self.db_engine, mcache=self.mcache, aes=self.aes)
        # load_events(os.path.join(os.path.abspath(os.path.dirname(toughnms.manage.events.__file__))),
        #     "toughnms.manage.events", excludes=[],event_params=event_params)


        # for g in self.nagapi.list_hostgroup():
        #     for host in g.get_effective_hosts():
        #         permit.add_route(host_perf.HostPerfDataHandler, 
        #             r"/gperfdata?group_name=%s&host_name=%s"%(g.hostgroup_name,host.host_name),
        #             utils.safeunicode(host.alias),
        #             MenuRes,
        #             is_menu=True,
        #             order=7.0005)
        cyclone.web.Application.__init__(self, permit.all_handlers, **settings)

    def init_route_permit(self):
        with make_db(self.db) as conn:
            try:
                oprs = conn.query(models.TlOperator)
                for opr in oprs:
                    if opr.operator_type > 0:
                        for rule in self.db.query(models.TlOperatorRule).filter_by(operator_name=opr.operator_name):
                            permit.bind_opr(rule.operator_name, rule.rule_path)
                    elif opr.operator_type == 0:  # 超级管理员授权所有
                        permit.bind_super(opr.operator_name)
            except Exception as err:
                logger.error("init route error , %s" % str(err))

def run(config, dbengine):
    app = HttpServer(config, dbengine)
    reactor.listenTCP(int(config.admin.port), app, interface=config.admin.host)

