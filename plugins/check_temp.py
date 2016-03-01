#!/usr/bin/env python
#coding:utf-8
import re
import os
import sys
import syslog
from optparse import OptionParser

syslog.openlog("nagios_plugin")

tmp = '''
coretemp-isa-0005
Adapter: ISA adapter
Core 2:       +40.0°C  (high = +84.0°C, crit = +94.0°C)

coretemp-isa-0004
Adapter: ISA adapter
Core 2:       +46.0°C  (high = +84.0°C, crit = +94.0°C)

coretemp-isa-0003
Adapter: ISA adapter
Core 1:       +43.0°C  (high = +84.0°C, crit = +94.0°C)

coretemp-isa-0002
Adapter: ISA adapter
Core 1:       +49.0°C  (high = +84.0°C, crit = +94.0°C)

coretemp-isa-0001
Adapter: ISA adapter
Core 0:       +43.0°C  (high = +84.0°C, crit = +94.0°C)

coretemp-isa-0000
Adapter: ISA adapter
Core 0:       +47.0°C  (high = +84.0°C, crit = +94.0°C)
'''

def check_cputemp(wval,cval):
    def get_state(tval):
        if tval < wval:
            return 0
        if tval > wval and tval < cval:
            return 1
        if tval > cval:
            return 2

    output_str = {
        0 : 'check OK;',
        1 : 'check Wanning;',
        2 : 'check Crit;',
        3 : 'check Unknow;'
    }

    outputs = []
    status = 0

    for line in os.popen("sensors").readlines():
    # for line in tmp.split('\n'):
        syslog.syslog("check_cputemp line %s"%line)
        grp = re.search('(Core\s\d+):\s+\+(\d+\.*\d+)',line)
        if not grp:
            continue
        _core_no,_temp = grp.groups()
        _status =  get_state(float(_temp))
        if _status > status:
            status = _status
        _out = ','.join([_core_no,_temp,str(_status)])
        outputs.append(_out)

    if not outputs :
        raise ValueError('no sensors data')

    _outstr = ';'.join(outputs)
    return status,output_str[status] + _outstr + '|' + _outstr



if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-c", "--warn",dest="warn", help="warn value")
    parser.add_option("-w", "--crit", dest="crit",help="crit value")
    (options, args) = parser.parse_args()
    if not options.warn and not options.crit:
        parser.error("incorrect number of arguments")
        sys.exit(3)
    else:
        try:
            status,output =  check_cputemp(int(options.warn),int(options.crit))
            print output
            sys.exit(status)
        except Exception ,e:
            print 'Unknow check %s'%e
            sys.exit(3)
        