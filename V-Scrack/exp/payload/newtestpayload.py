import sys
from exp.lib import include
from exp.lib.Lpayload import Lpayload
from exp.lib.protocolparse import protocoparse
from exp.lib.httpparse import httpparse

def verify(protocol,ip,port):
    if ip:
        msg = "very nice"
        return True,ip,msg
    else:
        #print "OH ,NO"
        return False,ip,port



