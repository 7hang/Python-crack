# coding: utf-8

import os
import re
import time
import telnetlib
from exp.lib.gla import getpassdict

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if telnet weak pass vul')
    user_list = ['root', 'admin', 'zte', 'cisco']
    psw = ['root', 'admin', 'zte', 'cisco','zte123456','zte123',' ']
    for user in user_list:
        for pass_ in psw:
            try:
                tn = telnetlib.Telnet(ip,port,timeout=3)
                time.sleep(0.5)
                os = tn.read_some()
            except Exception as e:
                continue
            user_match = b"(?i)(login|user|username)"
            pass_match = b'(?i)(password|pass)'
            login_match = b'#|\$|>'
            if re.search(user_match, os):
                try:
                    tn.write(user.encode('ascii') + b"\n")
                    tn.read_until(pass_match, timeout=1.5)
                    tn.write(pass_.encode('ascii') + b"\n")
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        msg = 'There is telnet weak pass vul on: %s , with username: %s and password: %s.' % (
                        url, user, pass_)
                        print(msg)
                        number = 'v88'
                        return True, url, number, msg
                except Exception as e:
                    pass
            else:
                try:
                    info = tn.read_until(user_match, timeout=2)
                except Exception as e:
                    continue
                if re.search(user_match, info):
                    try:
                        tn.write(user.encode('ascii') + b"\n")
                        tn.read_until(pass_match, timeout=2)
                        tn.write(pass_.encode('ascii') + b"\n")
                        login_info = tn.read_until(login_match, timeout=2)
                        tn.close()
                        if re.search(login_match, login_info):
                            msg = 'There is telnet weak pass vul on: %s , with username: %s and password: %s.' % (
                                url, user, pass_)
                            print(msg)
                            number = 'v88'
                            return True, url, number, msg
                    except Exception as e:
                        continue
                elif re.search(pass_match, info):
                    tn.read_until(pass_match, timeout=2)
                    tn.write(pass_.encode('ascii') + b"\n")
                    login_info = tn.read_until(login_match, timeout=3)
                    tn.close()
                    if re.search(login_match, login_info):
                        msg = 'There is telnet weak pass vul on: %s , with username: %s and password: %s.' % (
                            url, user, pass_)
                        print(msg)
                        number = 'v88'
                        return True, url, number, msg
                    else:
                        pass
    msg = 'Therer is no telnet weakpass vul in url:' + url + '.'
    number = 'v0'
    return False, url, number, msg


