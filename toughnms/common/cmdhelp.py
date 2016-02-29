#!/usr/bin/env python
#coding=utf-8

help_dict = {
   "check-host-alive":{
     "desc":u"主机存活状态",
     "example":"check-host-alive",
     "perfdata":0
   },
   "check_local_disk":{
      "desc":u"本地磁盘",
      "example":"check_local_disk!20%!10%!/",
      "perfdata":1
   },
   "check_local_load":{
      "desc":u"本地主机负载",
      "example":"check_local_load!5.0,4.0,3.0!10.0,6.0,4.0",
      "perfdata":1
   },
   "check_local_procs":{
      "desc":u"本地主机进程",
      "example":"check_local_procs!250!400!RSZDT",
      "perfdata":0
   },
   "check_local_users":{
      "desc":u"本地主机登陆",
      "example":"check_local_users!20!50",
      "perfdata":0
   },
   "check_local_swap":{
      "desc":u"本地主机交换分区",
      "example":"check_local_swap!20!10",
      "perfdata":1
   },
   "check_ftp":{
      "desc":u"ftp服务",
      "example":"check_ftp!21",
      "perfdata":0
   },  
   "check_snmp":{
      "desc":u"snmp服务",
      "example":"check_snmp",
      "perfdata":0
   },  
   "check_http":{
      "desc":u"HTTP服务",
      "example":"check_http",
      "perfdata":0
   },       
   "check_ping":{
      "desc":u"主机ping",
      "example":"check_ping!100.0,20%!500.0,60%",
      "perfdata":1
   }        
}


