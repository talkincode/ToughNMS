#!/usr/bin/env python
#coding=utf-8
import base
import time
from forms import host_form
from lib import rutils
from settings import config
from lib import router
from lib.nagutils import nagapi,STATUS,STYLE


@router.route('/manage/perfdata')
class HostPerfDataHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        return self.post(template_variables)
        
    @base.authenticated
    def post(self, template_variables={}):
        day_code = self.get_argument("day_code",rutils.get_currdate())
        begin_time = rutils.datetime2msec("%s 00:00:00"%day_code)
        end_time = rutils.datetime2msec("%s 23:59:59"%day_code)
        self.logging.info("query perfdata %s -- %s"%(begin_time,end_time))
        group_name = self.get_argument("group_name",None)
        groups = nagapi.list_hostgroup()
        all_hosts = nagapi.list_host(group_name)
        host_name = self.get_argument("host_name")
        host = nagapi.get_host(host_name)
        self.render("host_perf.html",
            groups=groups,
            group_name=group_name,
            host_name=host_name,
            host=host,
            day_code=day_code,
            begin_time=begin_time, 
            end_time=end_time,
            STATUS=STATUS,
            STYLE=STYLE
        )

@router.route('/manage/perfdata/hosts')
class HostPerfHostsHandler(base.BaseHandler):
    @base.authenticated
    def get(self,*args,**kwargs):
        group_name = self.get_argument("group_name",None)
        hosts = nagapi.list_host(group_name)
        host_data = [{"host_name":h.host_name,"host_desc":h.alias} for h in hosts ]
        self.render_json(data=host_data)


@router.route('/manage/perfdata/swap_usage')
class HostPerfSwapHandler(base.BaseHandler):
    @base.authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        swapdata = self.mongodb.query_swap_perfdata(host_name,begin_time,end_time)
        _data = [ [d['lastcheck']*1000,d['data']['usage']] for d in swapdata if d['data']]
        self.render_json(data=[{"data":_data}])


@router.route('/manage/perfdata/disk_usage')
class HostPerfDiskHandler(base.BaseHandler):
    @base.authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        diskdata = self.mongodb.query_disk_perfdata(host_name,begin_time,end_time)
        _data = [ [d['lastcheck']*1000,d['data']['usage']] for d in diskdata if d['data']]
        self.render_json(data=[{"data":_data}])        

@router.route('/manage/perfdata/load_perf')
class HostPerfLoadHandler(base.BaseHandler):
    @base.authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        loaddata = self.mongodb.query_load_perfdata(host_name,begin_time,end_time)   

        load1 = {"name":u"1分钟负载","data":[]}
        load5 = {"name":u"5分钟负载","data":[]}
        load15 = {"name":u"15分钟负载","data":[]}

        for d in loaddata:
            load1["data"].append([d['lastcheck']*1000,d['data']['load1']])
            load5["data"].append([d['lastcheck']*1000,d['data']['load5']])
            load15["data"].append([d['lastcheck']*1000,d['data']['load15']])

        self.render_json(data=[load1,load5,load15])
             








