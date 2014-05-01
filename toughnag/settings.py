#!/usr/bin/env python
#coding=utf-8
import yaml

CFG_FILE = 'config.yaml'


def read_config():
    with open(CFG_FILE) as cf:
        return yaml.load(cf)

config = read_config()

def update(**cfg):
    config.update(cfg)
    yaml.dump(config, open(CFG_FILE,'w'), default_flow_style=False)

if __name__ == '__main__':
    update(test=True)