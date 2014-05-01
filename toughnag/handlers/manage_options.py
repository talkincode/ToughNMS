#!/usr/bin/env python
#coding=utf-8
import base
import settings
from base import authenticated
from lib import rutils
from forms.options_form import option_update_form,passwd_update_form


@base.route('/manage/option')
class OptionsHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        form = option_update_form()
        form.fill(settings.config.copy())
        self.render("base_form.html",form=form)

    def post(self, *args, **kwargs):
        form = option_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        cfg = form.d.copy()
        del cfg['submit']
        settings.update(**cfg)
        self.redirect('/manage', permanent=False)        


@base.route('/manage/passwd')
class PasswdHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        form = passwd_update_form()
        cfg = settings.config.copy()
        param = dict(
            admin_name=cfg['admin_name'],
            admin_pwd = "",
            admin_pwd_chk = "",
        )
        form.fill(param)
        self.render("base_form.html",form=form)

    def post(self, *args, **kwargs):
        form = passwd_update_form()

        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return

        if form.d.admin_pwd != form.d.admin_pwd_chk:
            self.render("base_form.html", form=form,msg=u"确认密码不匹配")
            return

        settings.update(admin_pwd=rutils.encrypt(form.d.admin_pwd))
        self.redirect('/manage', permanent=False)    

