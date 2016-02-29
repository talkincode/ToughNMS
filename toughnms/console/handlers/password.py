#!/usr/bin/env python
# coding:utf-8

from toughlib import utils
from toughnms.console.handlers.base import BaseHandler, MenuSys
from toughlib.permit import permit
from toughnms.console import models
from toughnms.console.handlers import password_forms
from cyclone.web import authenticated
from hashlib import md5

###############################################################################
# password update
###############################################################################

@permit.route(r"/password", u"密码修改", MenuSys, order=1.0000)
class PasswordUpdateHandler(BaseHandler):

    @authenticated
    def get(self):
        form = password_forms.password_update_form()
        form.fill(tra_user=self.get_secure_cookie("tra_user"))
        return self.render("base_form.html", form=form)

    @authenticated
    def post(self):
        form = password_forms.password_update_form()
        if not form.validates(source=self.get_params()):
            self.render("base_form.html", form=form)
            return
        if form.d.tra_user_pass != form.d.tra_user_pass_chk:
            self.render("base_form.html", form=form, msg=u'确认密码不一致')
            return
        opr = self.db.query(models.TlOperator).filter_by(operator_name=form.d.tra_user).first()
        opr.operator_pass = md5(form.d.tra_user_pass).hexdigest()

        ops_log = models.TlOperateLog()
        ops_log.operator_name = self.get_secure_cookie("tra_user")
        ops_log.operate_ip = self.get_secure_cookie("tra_login_ip")
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)修改密码' % (self.get_secure_cookie("tra_user"),)
        self.db.add(ops_log)

        self.db.commit()
        self.redirect("/")


