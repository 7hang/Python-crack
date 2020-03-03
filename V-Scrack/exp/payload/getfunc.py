# -*- coding:utf-8 -*-

from exp.lib.Lpayload import Lpayload
from exp.lib.protocolparse import protocoparse

class func():
    def __init__(self):
        pass

    def getresult(self,protocol,ip,port,tag):
        p = protocoparse()
        l = Lpayload()
        ras = []
        #(protocol,ip,port) = p.protocolset(ip,port)
        fun_name = "verify"
        if protocol == 'http':
            if tag == 'None':
                payloads = l.getpayload(protocol,port,tag='http')
            else:
                payloads = l.getpayload(protocol,port,tag=tag)
        elif protocol == 'https':
            if tag == 'None':
                payloads = l.getpayload(protocol,port,tag='https')
            else:
                payloads = l.getpayload(protocol,port,tag=tag)
        else:
            if tag == 'None':
                payloads = l.getpayload(protocol,port,tag='None')
            else:
                payloads = l.getpayload(protocol,port,tag=tag)
        for mod in payloads:
            ra = l.getfun(mod,fun_name)(protocol,ip,port)
            ras.append((ra[0],ra[1],ra[2],ra[3]))
        return ras

