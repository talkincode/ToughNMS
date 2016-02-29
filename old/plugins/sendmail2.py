#!/usr/local/bin/python
#coding:utf-8

from __future__ import unicode_literals
import sys,os
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.Header import Header
from pymongo import MongoClient
mdb = MongoClient('localhost', 27017)
def save2logdb(mailto,content):
    db = mdb['nagios_alerts']
    coll = db['alerts']
    data = dict(
        alert_type = 'mail',
        target = mailto,
        content = content,
        sendtime = time.time()   
    ) 
    coll.insert(data)

def decode(s):
    if isinstance(s, str):
        try:
            s = s.decode('utf-8')
        except:
            s = s.decode('gbk')
    return s

def sendmail(mailto,topic,content):
    #print 'mailto',mailto,topic,content
    topic = topic.replace("\\n","<br>")
    content = content.replace("\\n","<br>")
    fromaddr = 'xxx@163.com'
    toaddr = 'xxx@163.com'
    mail = MIMEText(content, 'html', 'utf-8')
    mail['Subject'] = Header("[Alert]:%s"%topic,'utf-8')
    mail['From'] = "notify <%s>"%fromaddr
    mail['To'] = "%s,%s"%(toaddr,mailto)
    mail["Accept-Language"]="zh-CN"
    mail["Accept-Charset"]="ISO-8859-1,utf-8"
    try:
        serv = smtplib.SMTP()
        #serv.set_debuglevel(True)
        serv.connect('smtp.163.com')
        serv.login('xxx@163.com','xxx')
        serv.sendmail(fromaddr, [toaddr,mailto], mail.as_string())
        serv.quit()
        print "Successfully sent email"
    except Exception,e:
        print "Error: unable to send email %s"%str(e)

    try:
        save2logdb(mailto,content)
    except:
        print 'error for save mail '


if __name__ == '__main__':
    print sys.argv
    mailto,topic,content = sys.argv[1],sys.argv[2],sys.argv[3]
    sendmail(mailto,decode(topic),decode(content))
