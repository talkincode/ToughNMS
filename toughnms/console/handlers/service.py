#!/usr/bin/env python
#coding=utf-8
import base
from toughnms.console.forms import service_form
from toughnms.console.handlers.base import MenuSys
from toughlib.permit import permit
from toughnms.common.cmdhelp import help_dict
from cyclone.web import authenticated

@permit.route('/service', u"服务管理", MenuSys, order=4.0001)
class ServiceHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name",None)
        services = self.nagapi.list_service(host_name) or []
        self.render('services.html',host_name=host_name,services=services)

@permit.route('/service/add', u"服务新增", MenuSys, order=4.0002)
class serviceAddHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        host_name = self.get_argument("host_name",None)
        form = service_form.service_add_form()
        form.host_name.set_value(host_name)
        self.render("service_form.html",
            form=form,
            commands=self.nagapi.list_commands(),
            help_dict=help_dict)

    @authenticated
    def post(self,**kwargs):
        form = service_form.service_add_form()
        if not form.validates(source=self.get_params()):
            self.render("service_form.html",
                form=form,
                commands=self.nagapi.list_commands(),
                help_dict=help_dict)
            return

        ret = self.nagapi.add_service(
            form.d.host_name,
            form.d.service_description,
            form.d.check_command,   
            use = form.d.use, 
            notifications_enabled = form.d.notifications_enabled,
            max_check_attempts = form.d.max_check_attempts,
            normal_check_interval = form.d.normal_check_interval or 5,
            retry_check_interval = form.d.retry_check_interval or 1
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/service?host_name='+form.d.host_name, permanent=False)


@permit.route('/service/update', u"服务更新", MenuSys, order=4.0003)
class serviceUpdateHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        sid = self.get_argument("service_id")
        form = service_form.service_update_form()
        service = self.nagapi.get_service(sid)
        if not service:
            raise ValueError("service not exists")
        form.fill(service)
        form.service_id.set_value(sid)
        form.use.set_value(service.use)
        form.notifications_enabled.set_value(service.notifications_enabled)
        form.process_perf_data.set_value(service.process_perf_data)
        self.render("service_form.html",
            form=form,
            commands=self.nagapi.list_commands(),
            help_dict=help_dict)

    @authenticated
    def post(self,**kwargs):
        form = service_form.service_update_form()
        if not form.validates(source=self.get_params()):
            self.render("service_form.html",
                form=form,
                commands=self.nagapi.list_commands(),
                help_dict=help_dict)
            return

        ret = self.nagapi.update_service(
            form.d.service_id,
            form.d.service_description,
            form.d.check_command,  
            use = form.d.use,
            notifications_enabled = form.d.notifications_enabled,     
            process_perf_data = form.d.process_perf_data,
            max_check_attempts = form.d.max_check_attempts,
            normal_check_interval = form.d.normal_check_interval or 5,
            retry_check_interval = form.d.retry_check_interval or 1
        )

        if ret.code > 0:
            self.render_error(msg=ret.msg)
        else: 
            self.redirect('/service?host_name='+form.d.host_name, permanent=False)


@permit.route('/service/delete', u"服务删除", MenuSys, order=4.0004)
class ServiceDeleteHandler(base.BaseHandler):

    @authenticated
    def get(self, template_variables={}):
        service_id = self.get_argument("service_id")
        host_name = self.get_argument("host_name")
        if not service_id:
            raise ValueError("service_id is empty")

        ret = self.nagapi.del_service(service_id)
        if ret.code > 0:
            self.render_error(msg=ret.msg) 
        else:
            self.redirect('/service?host_name='+host_name, permanent=False)

