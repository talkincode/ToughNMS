#!/usr/bin/env python
#coding=utf-8
import base
from forms import host_form
from lib import rutils
from settings import config


@base.route('/manage/perfdata')
class HostHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name")
        loaddata = self.mongodb.query_load_perfdata(host_name)
        swapdata = self.mongodb.query_swap_perfdata(host_name)
        diskdata = self.mongodb.query_disk_perfdata(host_name)
        self.render("host_perf.html",
            loaddata=loaddata,
            swapdata=swapdata,
            diskdata=diskdata
        )
        

    @base.authenticated
    def post(self, template_variables={}):
        pass         