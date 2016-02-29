#!/usr/bin/env python
#coding=utf-8
import base
from toughlib.permit import permit
from toughlib import utils


@permit.route('/alerts')
class AlertQueryHandler(base.BaseHandler):
    def get(self, template_variables={}):
        return self.post()

    def post(self,*args,**kwargs):
        alert_type = self.get_argument("alert_type",None)
        begin_day = self.get_argument("begin_day",utils.get_currdate())
        end_day = self.get_argument("end_day",utils.get_currdate())
        begin_time = utils.datetime2msec("%s 00:00:00"%begin_day)
        end_time = utils.datetime2msec("%s 23:59:59"%end_day)
        query = self.mongodb.query_alert(alert_type,begin_time,end_time)
        page_data = self.get_page_data(query)
        self.render("alerts.html",page_data=page_data,**self.get_params())



