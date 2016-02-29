#!/usr/bin/python
#coding=utf-8
from __future__ import division
import os
import sys
import re
import logging
from optparse import OptionParser
from pymongo import MongoClient

'''
# 'process-host-perfdata' command definition
define command{
        command_name    process-host-perfdata
        command_line    /path/perfdata_handler.py -l "$LASTHOSTCHECK$" -h "$HOSTNAME$" -d "$HOSTPERFDATA$"
        }


# 'process-service-perfdata' command definition
define command{
        command_name    process-service-perfdata
        command_line    /path/perfdata_handler.py -l "$LASTSERVICECHECK$" -h "$HOSTNAME$" -s "$SERVICEDESC$" -d "$SERVICEPERFDATA$"
        }
'''

def getLogger(name, logfile=None, debug=True):
    level = debug and logging.DEBUG or logging.ERROR
    formatter = logging.Formatter(u'%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logfile:
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

mdb = MongoClient('localhost', 27017)
log = getLogger("nagios_perfdata","/var/log/nagios/nagios_perfdata.log",True)

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

def process_data(options):
    _pref_cmd = [p for p in parse_funcs.keys() if p in options.command]
    if not _pref_cmd:
        log.debug("perfdata_command do nothing of %s"%options.command)
        return 
    _cmd = str(_pref_cmd[0])
    db = mdb['nagios_perfdata']
    coll = db[str(options.host)]
    data = dict(
        lastcheck = int(options.lastcheck),
        host = options.host,
        service = options.service,
        command = _cmd,
        data = parse_funcs[_cmd](options.data)
    )
    log.debug("perfdata_command insert to db %s"%repr(data))
    coll.insert(data)


if __name__ == "__main__":
    log.debug("perfdata_command: "+" ".join(sys.argv))
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-l", "--lastcheck",dest="lastcheck", help="lastcheck sec")
    parser.add_option("-H", "--host", dest="host",help="host name")
    parser.add_option("-s", "--service",dest="service", help="service desc")
    parser.add_option("-c", "--command",dest="command", help="command desc")
    parser.add_option("-d", "--data",dest="data", help="pref data")
    (options, args) = parser.parse_args()
    if not options.lastcheck and not options.host and not options.data:
        parser.error("incorrect number of arguments")
    else:
        try:
            process_data(options)
        except:
            log.exception("perfdata_command execute error")
