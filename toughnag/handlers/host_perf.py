#!/usr/bin/env python
#coding=utf-8
import base
from forms import host_form
from lib import rutils
from settings import config
from lib import router

@router.route('/manage/perfdata')
class HostHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name")
        loaddata = self.mongodb.query_load_perfdata(host_name)
        swapdata = self.mongodb.query_swap_perfdata(host_name)
        diskdata = self.mongodb.query_disk_perfdata(host_name)

        _disk_usage = { int(d['lastcheck'])*1000:str(d['data']['usage']) for d in diskdata}

        self.render("host_perf.html",
            host_name=host_name,
            loaddata=loaddata,
            swapdata=swapdata,
            disk_usage=_disk_usage
        )
        

    @base.authenticated
    def post(self, template_variables={}):
        pass         