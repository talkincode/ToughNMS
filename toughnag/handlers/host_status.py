#!/usr/bin/env python
#coding=utf-8
import base
from db_models import OmsHost,OmsHostGroup
from forms import host_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi

STATUS = {0:u"正常",1:u"警告",2:u"严重",3:u"未知"}
STYLE = {0:u"status_ok",1:u"status_warn",2:u"status_fail",3:u"status_unknow"}

@base.route('/manage/status/hosts')
class HostHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        group_name = self.get_argument("group_name",None)
        all_hosts = nagapi.list_host(group_name)
        self.render('host_status.html',hosts=all_hosts,STATUS=STATUS,STYLE=STYLE)   