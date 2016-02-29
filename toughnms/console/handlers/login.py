#!/usr/bin/env python
# coding:utf-8
from hashlib import md5
from toughnms.console.handlers.base import BaseHandler
from toughlib.permit import permit
from toughlib import utils
from toughnms.console import models

@permit.route(r"/login")
class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        uname = self.get_argument("username")
        upass = self.get_argument("password")
        if not uname:
            return self.render_json(code=1, msg=u"请填写用户名")
        if not upass:
            return self.render_json(code=1, msg=u"请填写密码")
        enpasswd = md5(upass.encode()).hexdigest()

        opr = self.db.query(models.TlOperator).filter(
            models.TlOperator.operator_name == uname,
            models.TlOperator.operator_pass == enpasswd
        ).first()

        if not opr:
            return self.render_json(code=1, msg=u"用户名密码不符")

        if opr.operator_status == 1:
            return self.render_json(code=1, msg=u"该操作员账号已被停用")

        self.set_secure_cookie("opr_name", uname, expires_days=None)
        self.set_secure_cookie("opr_login_time", utils.get_currtime(), expires_days=None)
        self.set_secure_cookie("opr_login_ip", self.request.remote_ip, expires_days=None)
        self.set_secure_cookie("opr_type", str(opr.operator_type), expires_days=None)


        if opr.operator_type in (1,):
            for rule in self.db.query(models.TlOperatorRule).filter_by(operator_name=uname):
                permit.bind_opr(rule.operator_name, rule.rule_path)

        ops_log = models.TlOperateLog()
        ops_log.operator_name = uname
        ops_log.operate_ip = self.request.remote_ip
        ops_log.operate_time = utils.get_currtime()
        ops_log.operate_desc = u'操作员(%s)登陆' % (uname,)
        self.db.add(ops_log)
        self.db.commit()

        self.render_json(code=0, msg="ok")

