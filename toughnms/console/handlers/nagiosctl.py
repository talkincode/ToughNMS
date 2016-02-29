#!/usr/bin/env python
#coding=utf-8
import base
from toughlib.permit import permit
from cyclone.web import authenticated



@permit.route('/nagios/ctl')
class HostHandler(base.BaseHandler):


    @authenticated
    def get(self, template_variables={}):
        self.render('nagiosctl.html') 

    @authenticated
    def post(self,**kwargs):
        def get_function(name):
            CMDS = {
                'status' : self.nagapi.status_nagios,
                'running': self.nagapi.is_running,
                'reload' : self.nagapi.reload_nagios,
                'start'  : self.nagapi.start_nagios,
                'stop'   : self.nagapi.stop_nagios,
                'restart': self.nagapi.restart_nagios,
                'verify' : self.nagapi.verify_config
            }
            return CMDS[name]
        result = get_function(self.get_argument("exec"))()
        self.render_json(code=result.code,msg=result.msg)

