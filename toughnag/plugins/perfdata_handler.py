#!/usr/bin/env python
#coding=utf-8
import os
import sys
import time
import bisect
import itertools
from datetime import datetime
from optparse import OptionParser
import logging

def getLogger(name, logfile=None, debug=False):
    level = debug and logging.DEBUG or logging.ERROR
    formatter = logging.Formatter(u'%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

log = getLogger("nagios_perfdata","/var/log/nagios/nagios_perfdata.log",True)

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

default_data_dir = '/var/log/nagios/statdata/'

class PerfData:
    def __init__(self, db_name):
        self.db_name = db_name
        self.fp_index = open(os.path.join(default_data_dir, db_name + '.index'), 'a')
        self.fp_data_for_append = open(os.path.join(default_data_dir, db_name + '.db'), 'a')

    def append_data(self, data, record_time=datetime.now()):
        def check_args():
            if not data:
                raise ValueError('data is null') 
            if not isinstance(data, basestring):
                raise ValueError('data is not string') 
            if data.find('\r') != -1 or data.find('\n') != -1:
                raise ValueError('data contains linesep') 
        check_args()
        record_time = time.mktime(record_time.timetuple()) 
        data = '%s\t%s%s' % (record_time, data, os.linesep)
        offset = self.fp_data_for_append.tell()
        self.fp_data_for_append.write(data)
        self.fp_index.write('%s\t%s%s' % (record_time, offset, os.linesep))
        self.fp_index.close()
        self.fp_data_for_append.close()
        

def process_data(options):
    if options.service:
        db = PerfData('%s-service'%(options.host))
        db.append_data('%s\t%s\t%s\t%s'%(options.lastcheck,options.host,options.service,options.data))
    else:
        db = PerfData(options.host)
        db.append_data('%s\t%s\t%s'%(options.lastcheck,options.host,options.data))



if __name__ == "__main__":
    log.info("process_data:"+" ".join(sys.argv))
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-l", "--lastcheck",dest="lastcheck", help="lastcheck sec")
    parser.add_option("-H", "--host", dest="host",help="host name")
    parser.add_option("-s", "--service",dest="service", help="service desc")
    parser.add_option("-d", "--data",dest="data", help="pref data")
    (options, args) = parser.parse_args()
    if not options.lastcheck and not options.host and not options.data:
        parser.error("incorrect number of arguments")
    else:
        process_data(options)
