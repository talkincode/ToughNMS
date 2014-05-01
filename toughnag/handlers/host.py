#!/usr/bin/env python
#coding=utf-8
import base
from db_models import OmsHost,OmsHostGroup
from forms import host_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi

@base.route('/manage/host')
class HostHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        group_name = self.get_argument("group_name",None)
        all_hosts = nagapi.list_host(group_name)
        self.render('hosts.html',hosts=all_hosts)     

@base.route('/manage/host/add')
class HostAddHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        groups = nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_add_form(groups)
        self.render('base_form.html',form=form)

    @base.authenticated
    def post(self,**kwargs):
        groups = nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_add_form(groups)
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        ret = nagapi.add_host(
            form.d.group_name,
            form.d.host_name,
            form.d.alias,
            form.d.address,
            use = form.d.use
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/host', permanent=False) 


@base.route('/manage/host/update')
class HostUpdateHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        groups = nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_update_form(groups)
        host = nagapi.get_host(self.get_argument("host_name"))
        if not host:
            raise ValueError("host not exists")
        form.fill(host)
        _hgs = host.get_effective_hostgroups()
        form.group_name.set_value(_hgs and _hgs[0].hostgroup_name or None)
        form.use.set_value(host.use)
        self.render("base_form.html", form=form)

    @base.authenticated
    def post(self,**kwargs):
        groups = nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_update_form(groups)
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        ret = nagapi.update_host(
            form.d.group_name,
            form.d.host_name,
            form.d.alias,
            form.d.address,
            use = form.d.use            
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/host', permanent=False)   

@base.route('/manage/host/delete')
class HostDeleteHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name")
        if not host_name:
            raise ValueError("host_name is empty")

        nagapi.del_host(host_name)
        self.redirect('/manage/host', permanent=False)     

