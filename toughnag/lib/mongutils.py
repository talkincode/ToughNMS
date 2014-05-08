#!/usr/bin/env python
#coding=utf-8

from pymongo import MongoClient

class MongoDB:

    def __init__(self,server="localhost",port=27017):
        self.mdb = MongoClient(server, port)

    def query_load_perfdata(self,host_name):
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        result = hostdb.find({"$or":[{"command":"check_load"},{"command":"check_local_load"}]})
        return result

    def query_swap_perfdata(self,host_name):
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        result = hostdb.find({"$or":[{"command":"check_swap"},{"command":"check_local_swap"}]})
        return result

    def query_disk_perfdata(self,host_name):
        perfdb = self.mdb['nagios_perfdata']
        hostdb = perfdb[host_name]
        result = hostdb.find({"$or":[{"command":"check_disk"},{"command":"check_local_disk"}]})
        return result        

mongodb = MongoDB()

if __name__ == '__main__':
    loaddata = mongodb.query_load_perfdata("localhost")
    swapdata = mongodb.query_swap_perfdata("localhost")
    for d in  loaddata:
        print d 

    for d in swapdata:
        print d