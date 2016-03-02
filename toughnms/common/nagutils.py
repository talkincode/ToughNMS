#!/usr/bin/env python
#coding=utf-8

from pynag import Model
from pynag import Control
from pynag import Parsers
from twisted.python import log
import functools

'''
nagios api utils
'''

STATUS = {0: u"正常", 1: u"警告", 2:u"严重", 3: u"未知", 255: u"未知"}
STYLE = {0: u"status_ok", 1: u"status_warn", 2: u"status_fail", 3: u"status_unknow", 255: u'status_unknow'}

def autoerror(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as err:
            log.err(err, "nagios config error")
            return Result(1, u"server error")
    return wrapper

class Result:
    def __init__(self,code=0,msg=None):
        self.code=code
        self.msg = msg

_success = Result()


##############################################################################
## nagios api 
##############################################################################

class NagiosApi:

    def __init__(self,config):
        self.nagios_bin = config.nagios.nagios_bin
        self.nagios_cfg = config.nagios.nagios_cfg
        self.nagios_service = config.nagios.nagios_service
        self.nagios_host_cfg_dir = config.nagios.nagios_host_cfg_dir
        self.nagios_host_group_cfg = config.nagios.nagios_host_group_cfg
        self.nagios_contact_cfg = config.nagios.nagios_contact_cfg

        self.process = Control.daemon(
            nagios_bin = self.nagios_bin,
            nagios_cfg = self.nagios_cfg,
            nagios_init = "service {0}".format(self.nagios_service),
            service_name = self.nagios_service
        )

    def get_stats_data(self):
        try:
            stat = Parsers.StatusDat()
            stat.parse()
            return stat['programstatus'][0]
        except:
            return None

    #--------------------hostgroup-----------------------------#

    def list_hostgroup(self):
        all_grps = Model.Hostgroup.objects.all
        all_grps = (grp for grp in all_grps if grp.hostgroup_name)
        return all_grps

    def count_hostgroup(self):
        return len(Model.Hostgroup.objects.all)

    def get_hostgroup(self,group_name):
        try:
            return Model.Hostgroup.objects.get_by_shortname(group_name)
        except KeyError,e:
            return None

    @autoerror
    def add_hostgroup(self,name,alias,members=None,sync=True):
        grp = self.get_hostgroup(name)
        if grp:
            return Result(1,u"host group is already exists")
        grp = Model.Hostgroup()
        grp.set_filename(self.nagios_host_group_cfg)
        grp.hostgroup_name = name
        grp.alias = alias
        if members:
            grp.members = members        
        grp.save()
        if sync:
            self.reload_nagios()
        return _success

    @autoerror
    def update_hostgroup(self,name,alias,members=None,sync=True,**kwargs):
        grp = self.get_hostgroup(name)
        if not grp:
            return Result(1,u"host group is not exists")
        grp.hostgroup_name = name
        grp.alias = alias
        if members:
            grp.members = members
        grp.save()
        if sync:
            self.reload_nagios()
        return _success

    @autoerror
    def del_hostgroup(self,group_name,sync=True):
        for grp in Model.Hostgroup.objects.filter(hostgroup_name=group_name):
            if grp.members:
                return Result(1,'There are members of this group')
            grp.delete()
            if sync:
                self.reload_nagios()
        return _success

    #------------------------contact-----------------------------#


    def list_contactgroup(self):
        contact_grps = Model.Contactgroup.objects.all
        return [g for g in contact_grps if g.contactgroup_name]

    def list_contact(self,contact_group=None):
        all_contact = Model.Contact.objects.all
        return [c for c in  all_contact if c.contact_name]

    def get_contact(self,contact_name):
        try:
            return Model.Contact.objects.get_by_shortname(contact_name)
        except KeyError ,e:
            return None

    @autoerror
    def add_contact(self,name,alias,email,contactgroup,sync=True,**kwargs):
        contact = self.get_contact(name)
        if contact:
            return Result(1,u"contact is already exists")
        contact = Model.Contact()
        contact.set_filename(self.nagios_contact_cfg)
        contact.use = 'generic-contact'
        contact.contact_name = name
        contact.alias = alias
        contact.email = email   
        if 'pager' in kwargs:
            contact.pager = kwargs.pop("pager")
        contact.save()
        contact.add_to_contactgroup(contactgroup)
        if sync:
            self.reload_nagios();
        return _success

    @autoerror
    def update_contact(self,name,alias,email,contactgroup,sync=True,**kwargs):
        contact = self.get_contact(name)
        if not contact:
            return Result(1,u"contact is not exists")

        for _cgrp in contact.get_effective_contactgroups():
            contact.remove_from_contactgroup(_cgrp.contactgroup_name)

        contact.alias = alias
        contact.email = email
        if 'pager' in kwargs:
            contact.pager = kwargs.pop("pager")
        contact.save()
        contact.add_to_contactgroup(contactgroup)
        if sync:
            self.reload_nagios()
        return _success

    @autoerror
    def del_contact(self,name,sync=True):
        for contact in Model.Contact.objects.filter(contact_name=name):
            contact.delete()
            if sync:
                self.reload_nagios()
        return _success


    #------------------------host-----------------------------#

    def list_host(self,group_name=None):
        if group_name:
            group = self.get_hostgroup(group_name)
            if group:
                return group.get_effective_hosts()
        all_hosts = Model.Host.objects.all
        all_hosts = (host for host in all_hosts if host.host_name)        
        return all_hosts

    def count_host(self):
        return len(Model.Host.objects.filter(register='1'))

    def get_host(self,host_name):
        try:
            return Model.Host.objects.get_by_shortname(host_name)
        except KeyError,e:
            return None

    @autoerror
    def add_host(self,group_name,host_name,alias,address,sync=True,**kwargs):
        host = self.get_host(host_name)
        if host:
            return Result(1,"host is already exists")
        group = self.get_hostgroup(group_name)
        if not group:
            return Result(1,"host group is not exists")

        host = Model.Host()
        host.set_filename("{0}/{1}.cfg".format(self.nagios_host_cfg_dir,host_name))
        host.host_name = host_name
        host.alias = alias
        host.address = address
        host.notifications_enabled = kwargs.pop('notifications_enabled',0)
        for _k,_v in kwargs.items():
            if hasattr(host,_k) and _v:
                setattr(host,_k,_v)
        host.save()
        host.add_to_hostgroup(group_name)
        if sync:
            self.reload_nagios()
        return _success

    @autoerror
    def update_host(self,group_name,host_name,alias,address,sync=True,**kwargs):
        host = self.get_host(host_name)
        if not host:
            return Result(1,"host is not exists")

        group = self.get_hostgroup(group_name)
        if not group:
            return Result(1,"host group is not exists")

        for _group in host.get_effective_hostgroups():
            host.remove_from_hostgroup(_group.hostgroup_name)

        host.use = kwargs.pop("use")
        host.host_name = host_name
        host.alias = alias
        host.address = address
        host.notifications_enabled = kwargs.pop('notifications_enabled',0)
        host.add_to_hostgroup(group.hostgroup_name)
        for _k,_v in kwargs.items():
            if hasattr(host,_k) and _v:
                setattr(host,_k,_v)
        if sync:
            self.reload_nagios()
        return _success


    def del_host(self,host_name,sync=True):
        for host in Model.Host.objects.filter(host_name=host_name):
            host.delete()
            if sync:
                self.reload_nagios()
        return _success

    #------------------------host-----------------------------#

    def list_service(self,host_name):
        host = self.get_host(host_name)
        if not host:
            return None
        services = host.get_effective_services()
        return services

    def count_service(self):
        return len(Model.Service.objects.filter(register='1'))


    def get_service(self,service_id):
        try:
            return Model.Service.objects.get_by_id(service_id)
        except KeyError,e:
            return None

    @autoerror
    def add_service(self,host_name,serv_desc,check_command,sync=True,**kwargs):
        service = Model.Service()
        service.use = kwargs.pop("use")
        service.host_name = host_name
        service.service_description = serv_desc
        service.check_command = check_command
        service.notifications_enabled = kwargs.pop('notifications_enabled',0)
        service.process_perf_data = kwargs.pop("process_perf_data",1)
        service.max_check_attempts = kwargs.pop("max_check_attempts",1)
        service.normal_check_interval = kwargs.pop("normal_check_interval",5)
        service.retry_check_interval = kwargs.pop("retry_check_interval",1)
        for _k,_v in kwargs.items():
            if hasattr(service,_k) and _v:
                setattr(service,_k,_v)        
        service.save()
        if sync:
            self.reload_nagios()
        return _success            
    
    @autoerror
    def update_service(self,sid,serv_desc,check_command,sync=True,**kwargs):
        service = self.get_service(sid)
        if not service:
            return Result(1,"service is not exists")

        service.use = kwargs.pop("use")
        service.service_description = serv_desc
        service.check_command = check_command
        service.notifications_enabled = kwargs.pop('notifications_enabled',0)
        service.process_perf_data = kwargs.pop("process_perf_data",1)
        service.max_check_attempts = kwargs.pop("max_check_attempts",1)
        service.normal_check_interval = kwargs.pop("normal_check_interval",5)
        service.retry_check_interval = kwargs.pop("retry_check_interval",1)
        for _k,_v in kwargs.items():
            if hasattr(service,_k) and _v:
                setattr(service,_k,_v)        
        service.save()
        if sync:
            self.reload_nagios()
        return _success

    @autoerror
    def del_service(self,service_id,sync=True):
        service = self.get_service(service_id)
        if service:
            service.delete()
        if sync:
            self.reload_nagios()
        return _success    

    #------------------------cmds-----------------------------#

    def list_commands(self):
        commands = Model.Command.objects.all
        return commands


    #------------------------ctl-----------------------------#
    @autoerror
    def is_running(self):
        ret = self.process.running()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err          
        return Result(0,msg)

    @autoerror
    def status_nagios(self):
        ret = self.process.status()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret==0 and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err           
        return Result(0,msg)

    @autoerror
    def reload_nagios(self):
        ret = self.process.reload()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret==0 and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err   
        return Result(0,msg)

    @autoerror
    def verify_config(self):
        ret = self.process.verify_config()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret and u"校验成功 \n %s"%out or u"校验失败 \n %s"%err
        return Result(0,msg)

    @autoerror
    def stop_nagios(self):
        ret = self.process.stop()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret==0 and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err 
        return Result(0,msg)

    @autoerror
    def start_nagios(self):
        ret = self.process.start()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret==0 and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err          
        return Result(0,msg)

    @autoerror
    def restart_nagios(self):
        ret = self.process.restart()
        out = self.process.stdout
        err = self.process.stderr
        msg = ret==0 and u"执行成功 \n %s"%out or u"执行失败 \n %s"%err      
        return Result(0,msg)



