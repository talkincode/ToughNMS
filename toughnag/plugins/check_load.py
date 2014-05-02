#!/usr/bin/env python
#coding=utf-8

import os,sys
from pynag.Plugins import simple as Plugin

np =Plugin()
np.add_arg("l","load-file","Enter a load average file", required=None)
np.activate()

if np['load-file']:
    load_file = np['load-file']
else:
    load_file ="/proc/loadavg"

if not os.path.isfile(load_file):
    np.nagios_exit(np.UNKNOWN,"Missing Load average file %s"% load_file)

current_load = os.popen("cat %s"% load_file).readline().split()

np.add_perfdata("1min", current_load[0])
np.add_perfdata("5min", current_load[1])
np.add_perfdata("15min", current_load[2])

np.check_range(current_load[0])