#!/usr/bin/env python
#coding=utf-8
import base

from forms import group_form
from lib import rutils
from lib.nagutils import nagapi
from lib import router

@router.route('/manage/group')
class GroupHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        all_grps = nagapi.list_hostgroup()
        self.render('groups.html',groups=all_grps)        


@router.route('/manage/group/add')
class GroupAddHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        form = group_form.group_add_form()
        self.render('base_form.html',form=form)

    @base.authenticated
    def post(self,**kwargs):
        form = group_form.group_add_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        ret = nagapi.add_hostgroup(form.d.hostgroup_name,form.d.alias)
        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else:
            self.redirect('/manage/group', permanent=False) 


@router.route('/manage/group/update')
class GroupUpdateHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        form = group_form.group_update_form()
        group = nagapi.get_hostgroup(self.get_argument("group_name"))
        if not group:
            raise ValueError("group not exists")
        form.fill(group)
        self.render("base_form.html", form=form)

    @base.authenticated
    def post(self,**kwargs):
        form = group_form.group_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        group = nagapi.get_hostgroup(form.d.hostgroup_name)
        if not group:
            raise ValueError("group not exists")

        ret = nagapi.update_hostgroup(form.d.hostgroup_name,form.d.alias)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:            
            self.redirect('/manage/group', permanent=False)         

@router.route('/manage/group/delete')
class GroupDeleteHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        group_name = self.get_argument("group_name")
        if not group_name:
            raise ValueError("group_name is empty")

        ret = nagapi.del_hostgroup(group_name)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:
            self.redirect('/manage/group', permanent=False)         

