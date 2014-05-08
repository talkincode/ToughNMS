#!/usr/bin/env python
#coding=utf-8
import base
from lib import router

@router.route('/')
class IndexHandler(base.BaseHandler):
    def get(self, template_variables={}):
        self.redirect('/manage', permanent=False) 



