#!/usr/bin/env python
#coding=utf-8
import base
from toughnms.console.forms import group_form
from toughlib.permit import permit
from toughnms.console.handlers.base import MenuRes
from cyclone.web import authenticated


@permit.route('/group', u"主机分组管理", MenuRes, is_menu=True, order=3.0001)
class GroupHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        all_grps = self.nagapi.list_hostgroup()
        self.render('groups.html', groups=all_grps)


@permit.route('/group/add', u"主机分组新增", MenuRes, order=3.0002)
class GroupAddHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        form = group_form.group_add_form()
        self.render('base_form.html',form=form)

    @authenticated
    def post(self,**kwargs):
        form = group_form.group_add_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        ret = self.nagapi.add_hostgroup(form.d.hostgroup_name,form.d.alias)
        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else:
            self.redirect('/group', permanent=False)


@permit.route('/group/update', u"主机分组更新", MenuRes, order=3.0003)
class GroupUpdateHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        form = group_form.group_update_form()
        group = self.nagapi.get_hostgroup(self.get_argument("group_name"))
        if not group:
            raise ValueError("group not exists")
        form.fill(group)
        self.render("base_form.html", form=form)

    @authenticated
    def post(self,**kwargs):
        form = group_form.group_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        group = self.nagapi.get_hostgroup(form.d.hostgroup_name)
        if not group:
            raise ValueError("group not exists")

        ret = self.nagapi.update_hostgroup(form.d.hostgroup_name,form.d.alias)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:            
            self.redirect('/group', permanent=False)

@permit.route('/group/delete', u"主机分组新增", MenuRes, order=3.0004)
class GroupDeleteHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        group_name = self.get_argument("group_name")
        if not group_name:
            raise ValueError("group_name is empty")

        ret = permit.nagapi.del_hostgroup(group_name)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:
            self.redirect('/group', permanent=False)

