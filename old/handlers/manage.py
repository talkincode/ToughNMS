#!/usr/bin/env python
#coding=utf-8
import base
import settings
from base import authenticated
from lib import rutils
from lib.nagutils import nagapi
from lib import router

@router.route('/manage')
class IndexHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        statsdata = nagapi.get_stats_data()
        self.render('index.html',statsdata=statsdata)

@router.route('/manage/login')
class LoginHandler(base.BaseHandler):

    def get(self, template_variables={}):
        self.render("login.html")

    def post(self, *args, **kwargs):
        next = self.get_argument("next", "/")
        username = self.get_argument("username")
        password = self.get_argument("password")
        if not username or not password:
            self.render_json(code=1, msg=u"登录失败，不允许空数据")
        else:
            if settings.read_config()['admin_name'] == username and \
               settings.read_config()['admin_pwd'] == rutils.encrypt(password):
                self.set_secure_cookie("username", username, expires_days=1)
                self.set_secure_cookie("logintime", rutils.get_currtime(), expires_days=1)
                self.render_json(msg=u"ok")
            else:
                self.render_json(code=1, msg=u"登录失败，用户密码不符合")

@router.route('/manage/logout')
class LogoutHandler(base.BaseHandler):

    def get(self, template_variables={}):
        self.clear_all_cookies()
        self.redirect("/manage/login", permanent=False)