#!/usr/bin/env python
#coding=utf-8
import base
from forms import host_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi,STATUS,STYLE
from lib import router


@router.route('/manage/status/hosts')
class HostHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        return self.post() 

    @base.authenticated
    def post(self, template_variables={}):
        group_name = self.get_argument("group_name",None)
        groups = nagapi.list_hostgroup()
        all_hosts = nagapi.list_host(group_name)
        self.render('host_status.html',
            curr_group=group_name,
            groups=groups,
            hosts=all_hosts,
            STATUS=STATUS,
            STYLE=STYLE
        )           