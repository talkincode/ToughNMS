#!/usr/bin/env python
# coding:utf-8
import cyclone.auth
import cyclone.escape
import cyclone.web
import base
from toughnms.console.forms import config_forms
from toughnms.console.handlers.base import MenuSys
from toughnms.console.settings import *
from toughlib.permit import permit
from cyclone.web import authenticated
from toughnms.console import models
from toughlib import dispatch,db_cache
import ConfigParser

@permit.route(r"/config", u"参数配置管理", MenuSys, order=1.0011, is_menu=True)
class ConfigHandler(base.BaseHandler):
    @authenticated
    def get(self):
        active = self.get_argument("active", "default")
        default_form = config_forms.default_form()
        default_form.fill(self.settings.config.system)
        database_form = config_forms.database_form()
        database_form.fill(self.settings.config.database)
        nagios_form = config_forms.nagios_form()
        nagios_form.fill(self.settings.config.nagios)

        mail_form = config_forms.mail_form()
        fparam = {}
        for p in self.db.query(models.TlParam):
            fparam[p.param_name] = p.param_value

        for form in (mail_form,):
            form.fill(fparam)

        self.render("config.html",
                    active=active,
                    default_form=default_form,
                    database_form=database_form,
                    mail_form=mail_form,
                    nagios_form=nagios_form
                    )

@permit.route(r"/config/default/update", u"默认配置", MenuSys, order=1.0022)
class DefaultHandler(base.BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config.system.debug = self.get_argument("debug")
        config.system.tz = self.get_argument("tz")
        config.update()
        self.redirect("/config?active=default")


@permit.route(r"/config/database/update", u"数据库配置", MenuSys, order=1.0023)
class DatabaseHandler(base.BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config.database.echo = self.get_argument("echo")
        config.database.dbtype = self.get_argument("dbtype")
        config.database.dburl = self.get_argument("dburl")
        config.database.pool_size = self.get_argument("pool_size")
        config.database.pool_recycle = self.get_argument("pool_recycle")
        config.database.backup_path = self.get_argument("backup_path")
        config.update()

        self.redirect("/config?active=database")


@permit.route(r"/config/nagios/update", u"nagios配置", MenuSys, order=1.0024)
class NagiosHandler(base.BaseHandler):
    @cyclone.web.authenticated
    def post(self):
        config = self.settings.config
        config.nagios.nagios_bin = self.get_argument("nagios_bin")
        config.nagios.nagios_service = self.get_argument("nagios_service")
        config.nagios.nagios_cfg = self.get_argument("nagios_cfg")
        config.nagios.nagios_host_group_cfg = self.get_argument("nagios_host_group_cfg")
        config.nagios.nagios_contact_cfg = self.get_argument("nagios_contact_cfg")
        config.nagios.nagios_host_cfg_dir = self.get_argument("nagios_host_cfg_dir")
        config.update()

        self.redirect("/config?active=nagios")

@permit.route("/param/update", u"系统参数更新", MenuSys, order=1.0025)
class ParamUpdateHandler(base.BaseHandler):

    @cyclone.web.authenticated
    def post(self):
        active = self.get_argument("active", "syscfg")
        for param_name in self.get_params():
            if param_name in ("active", "submit"):
                continue

            param = self.db.query(models.TlParam).filter_by(param_name=param_name).first()
            if not param:
                param = models.TlParam()
                param.param_name = param_name
                param.param_value = self.get_argument(param_name)
                self.db.add(param)
            else:
                param.param_value = self.get_argument(param_name)

            dispatch.pub(db_cache.CACHE_SET_EVENT,param.param_name,param.param_value,600, async=True)

        self.db.commit()
        self.redirect("/config?active=%s" % active)

