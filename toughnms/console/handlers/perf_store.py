#!/usr/bin/env python
from __future__ import division
from hashlib import md5
import base
import time
import os
import sys
import re
from toughlib.permit import permit
from toughlib import utils,logger

"""
# 'process-host-perfdata' command definition
define command{
        command_name    process-host-perfdata
        command_line    curl -d "l=$LASTHOSTCHECK$&c=$SERVICECHECKCOMMAND$&h=$HOSTNAME$&d=$HOSTPERFDATA$" \
         "http://localhost:8099/perfdata/store"
}


# 'process-service-perfdata' command definition
define command{
        command_name    process-service-perfdata
        command_line    curl -d "l=$LASTSERVICECHECK$&c=$SERVICECHECKCOMMAND$&h=$HOSTNAME$&s=SERVICEDESC&d=$SERVICEPERFDATA$" \
        "http://localhost:8099/perfdata/store"
}
"""

def parse_check_load(data):
    """ load1=2.470;5.000;10.000;0; load5=1.710;4.000;6.000;0; load15=1.290;3.000;4.000;0; """
    grp = re.search('load1=(.+?);.*load5=(.+?);.*load15=(.+?);.*',data)
    return grp and  dict(
        load1=float(grp.group(1)),
        load5=float(grp.group(2)),
        load15=float(grp.group(3))
    ) or None

def parse_check_disk(data):
    """ /=7785MB;10274;11558;0;12843 """
    grp = re.search('(/.*)=(.+?)MB.*;(\d+)',data)
    if grp:
        part,usage,total = grp.groups()
        usage = int(usage) /int(total) * 100  
        return {'part':part,"usage":int(usage)}
    return None   

def parse_check_swap(data):
    """ swap=2427MB;599;299;0;2999 """
    grp = re.search('swap=(.+?)MB.*;(\d+)',data)
    if grp:
        free,total = grp.groups()
        usage = (int(total) - int(free)) /int(total) * 100  
        return {"usage":int(usage)}
    return None   

parse_funcs = {
    "check_disk": parse_check_disk,
    "check_data_disk": parse_check_disk,
    "check_local_disk": parse_check_disk,
    "check_load": parse_check_load,
    "check_local_load" : parse_check_load,
    "check_swap": parse_check_swap,
    "check_local_swap": parse_check_swap
}



@permit.route('/perfdata/store')
class HostPerfStoreHandler(base.BaseHandler):

    def get(self):
        self.post()

    def post(self):
        token = self.get_argument("token",None)
        if not token or not token in md5(self.settings.config.system.secret.encode('utf-8')).hexdigest():
            return self.render_json(code=1,msg=u"token invalid")

        command = self.get_argument("command",None)
        if not command:
            return self.render_json(code=1,msg=u"cmd invalid")

        pref_cmd = ([p for p in parse_funcs.keys() if p in command] or [None])[0]
        if not pref_cmd:
            return self.render_json(code=1,msg=u"command %s not support" % command)

        host = self.get_argument("host",None)
        if not host:
            return self.render_json(code=1,msg=u"host invalid")

        lastcheck = self.get_argument("lastcheck","")
        service = self.get_argument("service","")
        perf_data = self.get_argument("data",""),

        if not all ([lastcheck,perf_data]):
            return self.render_json(code=1,msg=u"lastcheck,perf_data invalid")

        data = dict(
            lastcheck = int(lastcheck),
            host = host,
            service = service,
            command = pref_cmd,
            data = parse_funcs[pref_cmd](perf_data)
        )
        logger.debug("perfdata_command insert to db %s"%repr(data))
        self.mongodb.add_perfdata(data)
        self.render_json(code=0,msg=u"success")










