#!/usr/bin/env python
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughnms import __version__


def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def run():
    local("pypy toughctl --manage -c etc/toughnms.json")

def suprun():
    local("supervisord -c etc/supervisord_test.conf")

def admlog():
    local("tail -f  /var/toughnms/toughnms.log")

def naglog():
    local("tail -f  /var/toughnms/nagios.log")

def mdblog():
    local("tail -f  /var/toughnms/mongodb.log")

def initdb():
    local("pypy toughctl --initdb -c etc/toughnms.json")

