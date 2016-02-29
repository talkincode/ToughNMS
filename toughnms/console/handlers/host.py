#!/usr/bin/env python
#coding=utf-8
import base
from toughnms.console.forms import host_form
from toughnms.console.handlers.base import MenuRes

from toughlib.permit import permit
from cyclone.web import authenticated

@permit.route('/host', u"主机管理", MenuRes, is_menu=True, order=3.0001)
class HostHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        self.post()

    @authenticated
    def post(self,**kwargs):
        group_name = self.get_argument("group_name",None)
        all_hosts = self.nagapi.list_host(group_name)
        groups = self.nagapi.list_hostgroup()
        self.render('hosts.html',
            curr_group=group_name,
            hosts=all_hosts,
            groups=groups
        )     

@permit.route('/host/add', u"主机新增", MenuRes, order=3.0002)
class HostAddHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        groups = self.nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_add_form(groups)
        self.render('base_form.html',form=form)

    @authenticated
    def post(self,**kwargs):
        groups = self.nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_add_form(groups)
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        ret = self.nagapi.add_host(
            form.d.group_name,
            form.d.host_name,
            form.d.alias,
            form.d.address,
            use = form.d.use,
            notifications_enabled = form.d.notifications_enabled
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/host', permanent=False)


@permit.route('/host/update', u"主机更新", MenuRes, order=3.0003)
class HostUpdateHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        groups = self.nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_update_form(groups)
        host = self.nagapi.get_host(self.get_argument("host_name"))
        if not host:
            raise ValueError("host not exists")
        form.fill(host)
        _hgs = host.get_effective_hostgroups()
        form.group_name.set_value(_hgs and _hgs[0].hostgroup_name or None)
        form.use.set_value(host.use)
        self.render("base_form.html", form=form)

    @authenticated
    def post(self,**kwargs):
        groups = self.nagapi.list_hostgroup()
        groups = [(g.hostgroup_name,g.alias) for g in groups]
        form = host_form.host_update_form(groups)
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        ret = self.nagapi.update_host(
            form.d.group_name,
            form.d.host_name,
            form.d.alias,
            form.d.address,
            use = form.d.use, 
            notifications_enabled = form.d.notifications_enabled           
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/host', permanent=False)

@permit.route('/host/delete', u"主机删除", MenuRes, order=3.0004)
class HostDeleteHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name")
        if not host_name:
            raise ValueError("host_name is empty")

        self.nagapi.del_host(host_name)
        self.redirect('/host', permanent=False)

