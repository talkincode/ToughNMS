#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
sys.path.insert(0,os.path.split(__file__)[0])
sys.path.insert(0,os.path.abspath(os.path.pardir))
from toughnms.console import models
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import md5
from sqlalchemy.sql import text as _sql
import datetime
import logging

def init_db(db):

    params = [
        ('system_name',u'系统名称',u'ToughNMS管理控制台'),
        ('smtp_server', u'SMTP服务器地址', u'smtp.mailgun.org'),
        ('smtp_port', u'SMTP服务器端口', u'25'),
        ('smtp_user', u'SMTP用户名', u'service@toughradius.org'),
        ('smtp_pwd', u'SMTP密码', u'service2015'),
        ('smtp_sender', u'SMTP发送人名称', u'运营中心'),
        ('smtp_from', u'SMTP邮件发送地址', u'service@toughradius.org'),
    ]


    for p in params:
        param = models.TlParam()
        param.param_name = p[0]
        param.param_desc = p[1]
        param.param_value = p[2]
        db.add(param)

    opr = models.TlOperator()
    opr.id = 1
    opr.node_id = 1
    opr.operator_name = u'admin'
    opr.operator_type = 0
    opr.operator_pass = md5('root').hexdigest()
    opr.operator_desc = 'admin'
    opr.operator_status = 0
    db.add(opr)


    db.commit()
    db.close()


def update(db_engine):
    print 'starting update database...'
    metadata = models.get_metadata(db_engine)
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    print 'update database done'
    db = scoped_session(sessionmaker(bind=db_engine, autocommit=False, autoflush=True))()
    init_db(db)
