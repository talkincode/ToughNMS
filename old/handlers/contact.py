#!/usr/bin/env python
#coding=utf-8
import base
from forms import contact_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi
from lib import router

@router.route('/manage/contact')
class ContactHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        self.post()

    @base.authenticated
    def post(self,**kwargs):
        all_contacts = nagapi.list_contact()
        self.render('contacts.html',contacts=all_contacts)     


def get_groups():
    groups = nagapi.list_contactgroup()
    groups = [(g.contactgroup_name,g.alias) for g in groups]
    return groups

@router.route('/manage/contact/add')
class ContactAddHandler(base.BaseHandler):

    @base.authenticated
    def get(self,template_variables={}):
        form = contact_form.contact_add_form(get_groups())
        self.render('base_form.html',form=form)

    @base.authenticated
    def post(self,**kwargs):
        form = contact_form.contact_add_form(get_groups())
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        ret = nagapi.add_contact(
            form.d.contact_name,
            form.d.alias,
            form.d.email,
            form.d.contactgroup_name,
            pager=form.d.pager
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/contact', permanent=False)

@router.route('/manage/contact/update')
class ContactUpdateHandler(base.BaseHandler):

    @base.authenticated
    def get(self,template_variables={}):
        form = contact_form.contact_update_form(get_groups())
        contact = nagapi.get_contact(self.get_argument("contact_name"))
        if not contact:
            return self.render_error(msg=u"Contact not exists")
        form.fill(contact)
        _cgs = contact.get_effective_contactgroups()
        form.contactgroup_name.set_value(_cgs and _cgs[0].contactgroup_name or None)
        self.render('base_form.html',form=form)

    @base.authenticated
    def post(self,**kwargs):
        form = contact_form.contact_update_form(get_groups())
        if not form.validates(source=self.get_params()):
            return self.render("base_form.html", form=form)

        ret = nagapi.update_contact(
            form.d.contact_name,
            form.d.alias,
            form.d.email,
            form.d.contactgroup_name,
            pager=form.d.pager
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/contact', permanent=False)


@router.route('/manage/contact/delete')
class ContactDeleteHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        contact_name = self.get_argument("contact_name",None)
        if not contact_name:
            raise ValueError("contact_name is empty")

        nagapi.del_contact(contact_name)
        self.redirect('/manage/contact', permanent=False)     




