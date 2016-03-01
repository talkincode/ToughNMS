#!/usr/bin/env python
#coding=utf-8
import base
import time
from toughnms.console.forms import host_form
from toughlib.permit import permit
from toughlib import utils,logger
from toughnms.console.handlers.base import MenuRes
from cyclone.web import authenticated
from toughnms.common.nagutils import STATUS,STYLE
from cyclone.web import authenticated

@permit.route('/perfdata', u"主机性能监控", MenuRes, is_menu=False, order=7.0001)
class HostPerfDataHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        return self.post(template_variables)
        
    @authenticated
    def post(self, template_variables={}):
        day_code = self.get_argument("day_code",utils.get_currdate())
        begin_time = utils.datetime2msec("%s 00:00:00"%day_code)
        end_time = utils.datetime2msec("%s 23:59:59"%day_code)
        logger.info("query perfdata %s -- %s"%(begin_time,end_time))
        group_name = self.get_argument("group_name",None)
        groups = self.nagapi.list_hostgroup()
        all_hosts = self.nagapi.list_host(group_name)
        host_name = self.get_argument("host_name",None)
        host = self.nagapi.get_host(host_name)
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

@permit.route('/perfdata/hosts')
class HostPerfHostsHandler(base.BaseHandler):
    @authenticated
    def get(self,*args,**kwargs):
        group_name = self.get_argument("group_name",None)
        hosts = self.nagapi.list_host(group_name)
        host_data = [{"host_name":h.host_name,"host_desc":h.alias} for h in hosts ]
        self.render_json(data=host_data)


@permit.route('/perfdata/swap_usage')
class HostPerfSwapHandler(base.BaseHandler):
    @authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        swapdata = self.mongodb.query_swap_perfdata(host_name,begin_time,end_time)
        _data = [ [d['lastcheck']*1000,d['data']['usage']] for d in swapdata if d['data']]
        self.render_json(data=[{"data":_data}])


@permit.route('/perfdata/disk_usage')
class HostPerfDiskHandler(base.BaseHandler):
    @authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        diskdata = self.mongodb.query_disk_perfdata(host_name,begin_time,end_time)
        _data = [ (d['lastcheck']*1000,d['data'].get('part',"/"), d['data']['usage']) for d in diskdata if d['data']]
        parts = {}
        for lastcheck,part,usage in _data:
            if part not in parts:
                parts[part] = {'name':part,'data':[]}
            _part_data = parts[part]
            _part_data['data'].append([lastcheck,usage])

        self.render_json(data=parts.values())    

@permit.route('/perfdata/load_perf')
class HostPerfLoadHandler(base.BaseHandler):
    @authenticated
    def post(self, template_variables={}):
        host_name = self.get_argument("host_name")
        begin_time = self.get_argument("begin_time") 
        end_time = self.get_argument("end_time") 
        loaddata = self.mongodb.query_load_perfdata(host_name,begin_time,end_time)   

        load1 = {"name":u"1分钟负载","data":[]}
        load5 = {"name":u"5分钟负载","data":[]}
        load15 = {"name":u"15分钟负载","data":[]}

        for d in loaddata:
            _last_check = d['lastcheck']*1000
            _data = d.get('data')
            _load1 = _data['load1'] if _data is not None else 0
            _load5 = _data['load5'] if _data is not None else 0
            _load15 = _data['load15'] if _data is not None else 0
            load1["data"].append([_last_check,_load1])
            load5["data"].append([_last_check,_load5])
            load15["data"].append([_last_check,_load15])

        self.render_json(data=[load1,load5,load15])
             

@permit.route('/perfdata/store')
class HostPerfStoreHandler(base.BaseHandler):

    def get(self):
        token = self.get_argument("token",None)
        if not token or token not in self.settings.config.system.secret:
            return self.render_json(code=1,msg=u"token invalid")

        








