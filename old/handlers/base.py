#!/usr/bin/env python
# coding=utf-8

import json
import functools
import urlparse
import urllib
from logging import DEBUG
import tornado.web
from mako.template import Template
from tornado import options
from tornado.websocket import WebSocketHandler
from lib.paginator import Paginator
from tornado.httpclient import AsyncHTTPClient
from lib import rutils
from lib.nagutils import nagapi
import settings
import dbbaks

def authenticated(method):
    """ 管理登陆校验装饰器 """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest': # jQuery 等库会附带这个头
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'code': 1, 'msg': u'您的会话已过期，请重新登录！'}))
                return
            if self.request.method in ("GET", "POST", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urllib.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise tornado.web.HTTPError(403)
        else:
            # execute method and process error
            try:
                return method(self, *args, **kwargs)
            except Exception,e:
                self.logging.exception("server process error")
                if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest': # jQuery 等库会附带这个头
                    self.set_header('Content-Type', 'application/json; charset=UTF-8')
                    self.write(json.dumps({'code': 1, 'msg': u'服务器处理失败,请稍后再试！'}))
                else:
                    self.render_error(msg=u"服务器处理失败,请稍后再试")
    return wrapper



class BaseHandler(tornado.web.RequestHandler):
    url_pattern = None

    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.logging = self.application.logging
        self.mongodb = self.application.mongodb

    def get_error_html(self, status_code=500, **kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.render_json(code=1, msg=u"%s:服务器处理失败，请联系管理员" % status_code)
        self.logging.exception("server error")
        if status_code == 404:
            return self.render_string("error.html", msg=u"404:页面不存在")
        elif status_code == 403:
            return self.render_string("error.html", msg=u"403:非法的请求")
        elif status_code == 500:
            return self.render_string("error.html", msg=u"500:服务器处理失败，请联系管理员")
        else:
            return self.render_string("error.html", msg=u"%s:服务器处理失败，请联系管理员" % status_code)

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def render_form(self, template_name="base_form.html", **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)        

    def render_error(self, **template_vars):
        tpl = "error.html"
        html = self.render_string(tpl, **template_vars)
        self.write(html)

    def render_json(self, **template_vars):
        if not template_vars.has_key("code"):
            template_vars["code"] = 0
        resp = json.dumps(template_vars, ensure_ascii=False)
        self.write(resp)


    def render_string(self, template_name, **template_vars):
        template_vars["xsrf_form_html"] = self.xsrf_form_html
        template_vars["current_user"] = self.current_user
        template_vars["login_time"] = self.get_secure_cookie("logintime")
        template_vars["request"] = self.request
        template_vars["handler"] = self
        template_vars["utils"] = rutils
        template_vars["system_name"] = settings.config["system_name"]
        template_vars["server_base"] = settings.config["server_base"]
        template_vars["groups"] = [g for g in nagapi.list_hostgroup()]
        template_vars['dbbaks'] = dbbaks.db_config
        mytemplate = self.application.tp_lookup.get_template(template_name)
        return mytemplate.render(**template_vars)

    def render_from_string(self, template_string, **template_vars):
        template = Template(template_string)
        return template.render(**template_vars)

    def get_page_data(self, query):
        page_size = self.application.settings.get("page_size",20)
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).skip(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''

        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)



    def get_params(self):
        arguments = self.request.arguments
        params = {}
        for k, v in arguments.items():
            if len(v) == 1:
                params[k] = v[0]
            else:
                params[k] = v
        return params

    def get_params_obj(self, obj):
        arguments = self.request.arguments
        for k, v in arguments.items():
            if len(v) == 1:
                if type(v[0]) == str:
                    setattr(obj, k, v[0].decode('utf-8', ''))
                else:
                    setattr(obj, k, v[0])
            else:
                if type(v) == str:
                    setattr(obj, k, v.decode('utf-8'))
                else:
                    setattr(obj, k, v)
        return obj

    def get_current_user(self):
        username = self.get_secure_cookie("username")
        if not username: return None
        user = self.get_user(username)
        return user

    def get_user(self, username):
        return settings.read_config().get('admin_name') == username and username or None


class PageNotFoundHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)

