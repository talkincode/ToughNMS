#!/usr/bin/env python
#coding=utf-8
import base
from db_models import OmsHost,OmsHostGroup
from forms import host_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi


CMDS = {
    'status': nagapi.status_nagios,
    'running': nagapi.is_running,
    'reload': nagapi.reload_nagios,
    'start': nagapi.start_nagios,
    'stop': nagapi.stop_nagios,
    'restart': nagapi.restart_nagios,
    'verify': nagapi.verify_config
}

@base.route('/manage/nagios/ctl')
class HostHandler(base.BaseHandler):
    @base.authenticated
    def get(self, template_variables={}):
        self.render('nagiosctl.html') 

    @base.authenticated
    def post(self,**kwargs):
        _exec = self.get_argument("exec")
        cmd = CMDS[_exec]
        result = cmd()
        self.render_json(code=result.code,msg=result.msg)

