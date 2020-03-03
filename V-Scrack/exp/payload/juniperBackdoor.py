#pxssh模块不支持Windows系统
# -*- coding:utf-8 -*-

import re
from pexpect import pxssh

def connectSSH(host,user,password):
    try:
        ssh = pxssh.pxssh()
        ssh.login(host,user,password,login_timeout=15,auto_prompt_reset = False)
        return ssh
    except Exception as e:
        print("There is no juniperBackdoor on %s" %host)

def verify(protocol,ip,port):
    host = ip
    user = "root"
    password = "<<< %s(un='%s') = %u"
    try:
        theSSH = connectSSH(host,user,password)
        if theSSH:
            before = theSSH.before
            try:
                theSSH.logout()
            except:
                pass
            isval = re.search('Remote Management Console', before)
            if isval:
                msg = 'There is juniperBackdoor on this'
                print(msg)
                number = 'v14'
                return True, host,number,msg
            else:
                msg = 'safe'
                number = 'v0'
                return False, host,number,msg
        else:
            msg = 'connect ssh failed'
            number = 'v0'
            return False, host,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,host,number,msg
