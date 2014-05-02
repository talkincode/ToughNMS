#!/usr/bin/env python
#coding=utf-8
import base
from forms import service_form
from lib import rutils
from settings import config
from lib.nagutils import nagapi
from lib.cmdhelp import help_dict


@base.route('/manage/service')
class ServiceHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name",None)
        services = nagapi.list_service(host_name)
        self.render('services.html',host_name=host_name,services=services)

@base.route('/manage/service/add')
class serviceAddHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name",None)
        form = service_form.service_add_form()
        form.host_name.set_value(host_name)
        self.render("service_form.html",
            form=form,
            commands=nagapi.list_commands(),
            help_dict=help_dict)

    @base.authenticated
    def post(self,**kwargs):
        form = service_form.service_add_form()
        if not form.validates(source=self.get_params()):
            self.render("service_form.html",
                form=form,
                commands=nagapi.list_commands(),
                help_dict=help_dict)
            return

        ret = nagapi.add_service(
            form.d.host_name,
            form.d.service_description,
            form.d.check_command,   
            use = form.d.use, 
            notifications_enabled = form.d.notifications_enabled
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/service?host_name='+form.d.host_name, permanent=False)   


@base.route('/manage/service/update')
class serviceUpdateHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        sid = self.get_argument("service_id")
        form = service_form.service_update_form()
        service = nagapi.get_service(sid)
        if not service:
            raise ValueError("service not exists")
        form.fill(service)
        form.service_id.set_value(sid)
        form.use.set_value(service.use)
        form.notifications_enabled.set_value(service.notifications_enabled)
        form.process_perf_data.set_value(service.process_perf_data)
        self.render("service_form.html",
            form=form,
            commands=nagapi.list_commands(),
            help_dict=help_dict)

    @base.authenticated
    def post(self,**kwargs):
        form = service_form.service_update_form()
        if not form.validates(source=self.get_params()):
            self.render("service_form.html",
                form=form,
                commands=nagapi.list_commands(),
                help_dict=help_dict)
            return

        ret = nagapi.update_service(
            form.d.service_id,
            form.d.service_description,
            form.d.check_command,  
            use = form.d.use,
            notifications_enabled = form.d.notifications_enabled        
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/manage/service?host_name='+form.d.host_name, permanent=False)   


@base.route('/manage/service/delete')
class ServiceDeleteHandler(base.BaseHandler):

    @base.authenticated
    def get(self, template_variables={}):
        service_id = self.get_argument("service_id")
        host_name = self.get_argument("host_name")
        if not service_id:
            raise ValueError("service_id is empty")

        ret = nagapi.del_service(service_id)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:
            self.redirect('/manage/service?host_name='+host_name, permanent=False)   

