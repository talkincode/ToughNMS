#!/usr/local/bin/python
#coding:utf-8

import sys,os
import syslog
import MySQLdb
syslog.openlog('sendsms')

def decode(s):
    if isinstance(s, str):
        try:
            s = s.decode('utf-8')
        except:
            s = s.decode('gbk')
    return s


def sendsms(mobile,content):
    syslog.syslog(u"send sms {0} {1}".format(mobile,content))
    conn = MySQLdb.connect(
            host="172.16.50.20",
            user="lingyadb",
            passwd='lingyadb',
            db="mas",
            charset="gbk"
    )
    cursor = conn.cursor()
    params = {'mobile':mobile,'content':content}
    sql = u'''insert into api_mt_lingya01
                (SM_ID,
                SRC_ID,
                MOBILES,
                CONTENT,
                IS_WAP,
                URL,
                SM_TYPE,
                MSG_FMT,
                TP_PID,
                TP_UDHI,
                FEE_USER_TYPE)
            values
                (0,96531,"{mobile}","{content}",0,"",0,0,0,0,0)'''.format(**params)
    syslog.syslog(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    mobile,content = sys.argv[1],sys.argv[2]
    sendsms(mobile,decode(content))
