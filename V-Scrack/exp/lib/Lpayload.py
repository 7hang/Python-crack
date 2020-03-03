# -*- coding:utf-8 -*-

import configparser
from exp.lib import include
import sys

class Lpayload():
    def __init__(self):
        pass

    def getpayload(self,protocol,port,tag):
        pays = []
        newpays = []
        payload =[]
        cf = configparser.ConfigParser()
        cf.read(include.scan_rule_dir)
        items = cf.items(tag)
        pays = items[0][1]
        for pay in enumerate(pays.split(",")):
            payload.append(pay[1])
        if int(port) == 443 or protocol == 'https':
            newitems = cf.items("ssl")
            newpays = newitems[0][1]
            for newpay in enumerate(newpays.split(",")):
                payload.append(newpay[1])
        else:
            pass
        if protocol in ['http','https'] and tag != 'http':
        #if tag in ['iis','apache','nginx','tomcat','activemq','jetty','axis'] and protocol in ['http','https']:
            new2items = cf.items(protocol)
            new2pays = new2items[0][1]
            for new2pay in enumerate(new2pays.split(",")):
                payload.append(new2pay[1])
        else:
            pass
        return payload

    def getfun(self,module_name,fun_name):
        try:
            module = __import__(module_name)
            return getattr(module,fun_name)
        except ImportError as e:
            pass
