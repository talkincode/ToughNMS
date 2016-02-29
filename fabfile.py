#!/usr/bin/env python
import sys,os
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughnms import __version__


def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def run():
    local("pypy toughctl --admin -c etc/toughnms.json")


def initdb():
    local("pypy toughctl --initdb -c etc/toughnms.json")

