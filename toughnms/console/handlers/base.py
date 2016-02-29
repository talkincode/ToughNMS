#!/usr/bin/env python
# coding:utf-8

import json
import cyclone.auth
import cyclone.escape
import cyclone.web
from mako.template import Template
from hashlib import md5
from twisted.python import log
from toughlib import utils
from toughlib.paginator import Paginator
from toughlib.permit import permit
from cyclone.util import ObjectDict
import logging
import urllib
import urlparse
from toughnms.console.settings import *
from toughnms import __version__ as sys_version



class BaseHandler(cyclone.web.RequestHandler):
    url_pattern = None
    
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    # def check_xsrf_cookie(self):
    #     pass

    def initialize(self):
        self.tp_lookup = self.application.tp_lookup
        self.nagapi = self.application.nagapi
        self.db = self.application.db()
        self.mongodb = self.application.mongodb
        if self.settings.debug:
            log.msg("[debug] :: %s request body: %s" % (self.request.path, self.request.body))
        
    def on_finish(self):
        self.db.close()
        
    def get_error_html(self, status_code=500, **kwargs):
        return self.render_json(code=1, msg=u"%s:server error" % status_code)

    def render(self, template_name, **template_vars):
        html = self.render_string(template_name, **template_vars)
        self.write(html)

    def render_error(self, **template_vars):
        tpl = "error.html"
        html = self.render_string(tpl, **template_vars)
        self.write(html)

    def _write(self, resp):
        if self.settings.debug:
            log.msg("[debug] :: %s response body: %s" % (self.request.path, resp))
        self.write(resp)

    def render_json(self, **template_vars):
        if not template_vars.has_key("code"):
            template_vars["code"] = 0
        resp = json.dumps(template_vars, ensure_ascii=False)
        self._write(resp)

    def render_string(self, template_name, **template_vars):
        template_vars["xsrf_form_html"] = self.xsrf_form_html
        template_vars["current_user"] = self.current_user
        template_vars["request"] = self.request
        template_vars["handler"] = self
        template_vars["utils"] = utils
        template_vars['sys_version'] = sys_version
        template_vars["permit"] = permit
        template_vars["menu_icons"] = MENU_ICONS
        template_vars["all_menus"] = permit.build_menus(order_cats=ADMIN_MENUS)
        mytemplate = self.tp_lookup.get_template(template_name)
        return mytemplate.render(**template_vars)

    def render_from_string(self, template_string, **template_vars):
        template = Template(template_string)
        return template.render(**template_vars)

    def make_sign(self, secret, params=[]):
        """ make sign
        :param params: params list
        :return: :rtype:
        """
        _params = [utils.safestr(p) for p in params if p is not None]
        _params.sort()
        _params.insert(0, secret)
        strs = ''.join(_params)
        # if self.settings.debug:
        #     log.msg("sign_src = %s" % strs, level=logging.DEBUG)
        mds = md5(utils.safestr(strs)).hexdigest()
        return mds.upper()

    def check_sign(self, secret, msg):
        """ check message sign
        :param msg: dict type  data
        :return: :rtype: boolean
        """
        if "sign" not in msg:
            return False
        sign = msg['sign']
        params = [msg[k] for k in msg if k != 'sign']
        local_sign = self.make_sign(secret, params)
        if self.settings.debug:
            log.msg("[debug] :::::::: remote_sign = %s ,local_sign = %s" % (sign, local_sign), level=logging.DEBUG)
        return sign == local_sign


    def get_page_data(self, query):
        page_size = self.application.settings.get("page_size", 10)
        page = int(self.get_argument("page", 1))
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data



    def get_page_url(self, page, form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" % (form_id.strip(), page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''

        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)


    def get_current_user(self):
        username = self.get_secure_cookie("opr_name")
        if not username: return None
        ipaddr = self.get_secure_cookie("opr_login_ip")
        opr_type = int(self.get_secure_cookie("opr_type"))
        login_time = self.get_secure_cookie("opr_login_time")

        user = ObjectDict()
        user.username = username
        user.ipaddr = ipaddr
        user.opr_type = opr_type
        user.login_time = login_time
        return user

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


    def get_param_value(self, name, defval=None):
        val = self.db.query(models.TlParam.param_value).filter_by(param_name = name).scalar()
        return val or defval


    def export_file(self, filename, data):
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename=' + filename)
        self.write(data.xls)
        self.finish()