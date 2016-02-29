#!/usr/bin/env python
#coding=utf-8
import base
from toughnms.console.forms import contact_form
from toughnms.console.handlers.base import MenuSys
from toughnms.console.settings import *
from toughlib.permit import permit
from cyclone.web import authenticated

class GroupHandler(base.BaseHandler):

    def get_groups(self):
        groups = self.nagapi.list_contactgroup()
        groups = [(g.contactgroup_name, g.alias) for g in groups]
        return groups


@permit.route('/contact', u"联系人管理", MenuSys, is_menu=True, order=2.0001)
class ContactHandler(GroupHandler):

    @authenticated
    def get(self, template_variables={}):
        self.post()

    @authenticated
    def post(self,**kwargs):
        all_contacts = self.nagapi.list_contact()
        self.render('contacts.html',contacts=all_contacts)     



@permit.route('/contact/add', u"联系人新增", MenuSys,  order=2.0002)
class ContactAddHandler(GroupHandler):

    @authenticated
    def get(self,template_variables={}):
        form = contact_form.contact_add_form(self.get_groups())
        self.render('base_form.html',form=form)

    @authenticated
    def post(self,**kwargs):
        form = contact_form.contact_add_form(self.get_groups())
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        ret = self.nagapi.add_contact(
            form.d.contact_name,
            form.d.alias,
            form.d.email,
            form.d.contactgroup_name,
            pager=form.d.pager
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/contact', permanent=False)

@permit.route('/contact/update', u"联系人更新", MenuSys, order=2.0003)
class ContactUpdateHandler(GroupHandler):

    @authenticated
    def get(self,template_variables={}):
        form = contact_form.contact_update_form(self.get_groups())
        contact = self.nagapi.get_contact(self.get_argument("contact_name"))
        if not contact:
            return self.render_error(msg=u"Contact not exists")
        form.fill(contact)
        _cgs = contact.get_effective_contactgroups()
        form.contactgroup_name.set_value(_cgs and _cgs[0].contactgroup_name or None)
        self.render('base_form.html',form=form)

    @authenticated
    def post(self,**kwargs):
        form = contact_form.contact_update_form(self.get_groups())
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        ret = self.nagapi.update_contact(
            form.d.contact_name,
            form.d.alias,
            form.d.email,
            form.d.contactgroup_name,
            pager=form.d.pager
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/contact', permanent=False)


@permit.route('/contact/delete', u"联系人删除", MenuSys, order=2.0004)
class ContactDeleteHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        contact_name = self.get_argument("contact_name",None)
        if not contact_name:
            raise ValueError("contact_name is empty")

        self.nagapi.del_contact(contact_name)
        self.redirect('/contact', permanent=False)




