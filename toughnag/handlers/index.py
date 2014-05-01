#!/usr/bin/env python
#coding=utf-8
import base

@base.route('/')
class IndexHandler(base.BaseHandler):
    def get(self, template_variables={}):
        self.redirect('/manage', permanent=False) 



