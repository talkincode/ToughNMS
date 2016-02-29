#!/usr/bin/env python
#coding=utf-8
import base
from lib import router
from dbbaks import db_config
import os

@router.route('/manage/dbbaks')
class DbbaksHandler(base.BaseHandler):
    def get(self, template_variables={}):
        name = self.get_argument("name")
        if name not in db_config:
            self.render_error(msg=u"数据库备份不存在")

        dbconf = db_config[name]

        flist = os.listdir(dbconf['path'])
        flist.sort(reverse=True)

        self.render("dbbaks.html",flist=flist[:60],dbconf=dbconf)



