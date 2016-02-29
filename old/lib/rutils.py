#coding:utf-8
import logging
import sys
import md5
import time
import datetime
import decimal
import uuid
import StringIO


decimal.getcontext().prec = 11
decimal.getcontext().rounding = decimal.ROUND_UP

KEY, KLEN = '^!$#*%', 6


def encrypt(src):
    """
    >>> encrypt('nagios')
    '3040434A4556'
    """
    output = StringIO.StringIO()
    for i in range(len(src)):
        key = KEY[i % KLEN]
        ch = ord(src[i]) ^ ord(key)
        ihex = hex(ch).upper()
        if '0X' in ihex:
            ihex = ihex[2:]
        output.write(ihex)
    return output.getvalue()


def decrypt(dest):
    """
    >>> decrypt('66191C1B121D')
    '888888'
    """
    output = StringIO.StringIO()
    if len(dest) % 2 != 0:
        dest = "0" + dest
    for i in range(0, len(dest), 2):
        key = KEY[(i / 2) % KLEN]
        b = int(dest[i + 1], 16)
        b = b + 16 * int(dest[i], 16)
        b = b ^ ord(key)
        output.write(chr(b))
    return output.getvalue()

def encode(u):
    """
    >>> encode('a')
    'a'
    """
    if isinstance(u, unicode):
        try:
            u = u.encode('utf-8')
        except:
            u = u.encode('ascii')
    return u


def decode(s):
    if isinstance(s, str):
        try:
            s = s.decode('utf-8')
        except:
            s = s.decode('gbk')
    return s

def split_mline(src,wd=32,rstr='\r\n'):
    _idx = 0
    ss = []
    for c in src:
        if _idx > 0 and _idx%wd == 0:
            ss.append(rstr)
        ss.append(c)
        _idx += 1
    return ''.join(ss)


def md5hash(src):
    if isinstance(src, unicode):
        return md5.new(src.encode("utf-8")).hexdigest()
    else:
        return md5.new(src).hexdigest()



def getLogger(name, logfile=None, debug=True):
    level = debug and logging.DEBUG or logging.ERROR
    formatter = logging.Formatter(u'%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logfile:
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

log = getLogger("system")

def convtime(ctime):
    """
    >>> type(convtime('2012-01-14 00:00:00'))
    <type 'unicode'>
    >>> convtime('')
    ''
    """
    if not ctime:
        return ''
    cdate = datetime.datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
    nowdate = datetime.datetime.now()
    dt = nowdate - cdate
    secs = dt.total_seconds()

    if secs < 60:
        return u"刚刚"
    minute = int(secs / 60)
    if minute >= 1 and minute < 60:
        return u"%s分钟前" % minute

    hours = int(secs / (60 * 60))
    if hours >= 1 and hours < 24:
        return u"%s小时前" % hours

    days = int(secs / (60 * 60 * 24))
    if days >= 1 and days < 31:
        return u"%s天前" % days

    months = int(secs / (60 * 60 * 24 * 30))
    if months >= 1 and months < 12:
        return u"%s月前" % months

    years = int(secs / (60 * 60 * 24 * 365))
    return u"%s年前" % years


def fmt_second(time_total):
    """
    >>> fmt_second(100)
    '00:01:40'
    """

    def _ck(t):
        return t < 10 and "0%s" % t or t

    times = int(time_total)
    h = times / 3600
    m = times % 3600 / 60
    s = times % 3600 % 60
    return "%s:%s:%s" % (_ck(h), _ck(m), _ck(s))


def rtitle(val, wd=20):
    if not val:
        return
    if len(val) >= wd:
        return val[0:(wd - 1)] + '...'
    return val + '...'


def get_uuid():
    return uuid.uuid4().hex


def gen_numid():
    times = str(time.time())
    uid = times.replace('\.', '')
    return uid[0:10]

def get_currtime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_currdate():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def datetime2msec(dtime_str):
    _datetime =  datetime.datetime.strptime(dtime_str,"%Y-%m-%d %H:%M:%S")
    return int(time.mktime(_datetime.timetuple()))

def get_datetime(second):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(second))



if __name__ == '__main__':
    import doctest
    doctest.testmod()