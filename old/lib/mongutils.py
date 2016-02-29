#!/usr/bin/env python
#coding=utf-8
import datetime
import time
from pymongo import MongoClient
import logging

class MongoDB:

    def __init__(self,server="localhost",port=27017):
        self.mdb = MongoClient(server, port)

    def default_start_end(self):
        day_code = datetime.datetime.now().strftime("%Y-%m-%d")
        begin = datetime.datetime.strptime("%s 00:00:00"%day_code,"%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime("%s 23:59:59"%day_code,"%Y-%m-%d %H:%M:%S")
        return time.mktime(begin.timetuple()),time.mktime(end.timetuple())

    def query_load_perfdata(self,host_name,begin_time,end_time):
        if not begin_time or not end_time:
            begin_time,end_time = self.default_start_end()
        else:
            begin_time,end_time = int(begin_time),int(end_time)
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        param = {
            "$or":[{"command":"check_load"},{"command":"check_local_load"}],
            "lastcheck":{"$gte":begin_time,"$lte":end_time}
        }
        logging.info(param)
        result = hostdb.find(param)
        return result

    def query_swap_perfdata(self,host_name,begin_time,end_time):
        if not begin_time or not end_time:
            begin_time,end_time = self.default_start_end()   
        else:
            begin_time,end_time = int(begin_time),int(end_time)     
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        param = {
            "$or":[{"command":"check_swap"},{"command":"check_local_swap"}],
             "lastcheck":{"$gte":begin_time,"$lte":end_time}
        }
        result = hostdb.find(param)
        return result

    def query_disk_perfdata(self,host_name,begin_time,end_time):
        if not begin_time or not end_time:
            begin_time,end_time = self.default_start_end()       
        else:
            begin_time,end_time = int(begin_time),int(end_time)
             
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        param = {
            "$or":[{"command":"check_disk"},{'command':'check_data_disk'},{"command":"check_local_disk"}],
            "lastcheck":{"$gte":begin_time,"$lte":end_time}
        }
        result = hostdb.find(param)
        return result       


    def query_alert(self,alert_type,begin_time,end_time):
        if not begin_time or not end_time:
            begin_time,end_time = self.default_start_end()       
        else:
            begin_time,end_time = int(begin_time),int(end_time)     

        alertdb = self.mdb['nagios_alerts']['alerts']
        param = {"sendtime":{"$gte":begin_time,"$lte":end_time}} 
        if alert_type:
            param['alert_type'] = alert_type

        return alertdb.find(param)

mongodb = MongoDB()



