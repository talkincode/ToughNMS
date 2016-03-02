#!/usr/bin/env python
# coding:utf-8
from hashlib import md5
from toughlib import utils,logger
from toughnms.console.handlers.base import BaseHandler, MenuSys
from toughlib.permit import permit
from toughnms.console import models
from cyclone.web import authenticated
from toughlib.mail import send_mail as sendmail
from email.mime.text import MIMEText
from email import Header

@permit.route(r"/sendmail", u"发送邮件", MenuSys, order=6.0000)
class SendMailHandler(BaseHandler):

    def send_mail(self, mailto, topic, content):
        smtp_server = self.get_param_value("smtp_server",'127.0.0.1')
        from_addr = self.get_param_value("smtp_from")
        smtp_port = int(self.get_param_value("smtp_port",25))
        smtp_user = self.get_param_value("smtp_user",None)
        smtp_pwd = self.get_param_value("smtp_pwd",None)
        return sendmail(server=smtp_server, port=smtp_port,user=smtp_user, password=smtp_pwd, 
            from_addr=from_addr, mailto=mailto, topic=topic, content=content)

    def get(self):
        token = self.get_argument("token",None)
        if not token or  token not in md5(self.settings.config.system.secret.encode('utf-8')).hexdigest():
            return self.render_json(code=1,msg=u"token invalid")

        mailto = self.get_argument('mailto')
        topic = self.get_argument('topic')
        ctx = self.get_argument('content')
        logger.info("sendmail: %s %s %s"% (mailto, utils.safeunicode(topic), utils.safeunicode(ctx)))
        self.send_mail(mailto, topic, ctx).addCallbacks(logger.info,logger.error)
        self.mongodb.add_mail_alert(mailto,ctx)
        self.render_json(code=0,msg="mail send done")

        




