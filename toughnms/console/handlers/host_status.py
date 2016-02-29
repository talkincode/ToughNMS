#!/usr/bin/env python
#coding=utf-8
import base
from toughnms.console.forms import host_form
from toughlib.permit import permit
from toughlib import utils,logger
from toughnms.console.handlers.base import MenuRes
from cyclone.web import authenticated
from toughnms.common.nagutils import STATUS,STYLE
from cyclone.web import authenticated


@permit.route('/status/hosts', u"主机状态", MenuRes, is_menu=True, order=7.0001)
class HostHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        return self.post() 

    @authenticated
    def post(self, template_variables={}):
        group_name = self.get_argument("group_name",None)
        groups = self.nagapi.list_hostgroup()
        all_hosts = self.nagapi.list_host(group_name)
        self.render('host_status.html',
            curr_group=group_name,
            groups=groups,
            hosts=all_hosts,
            STATUS=STATUS,
            STYLE=STYLE
        )           