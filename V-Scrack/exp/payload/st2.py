#coding:utf-8

from exp.lib.st2fun import ex_struts


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if struts2 remote code exection vul')
    try:
        res=ex_struts(ip,port,protocol)
        result = res.run()
        if len(result) > 0:
            for key in result:
                msg = 'There is struts2 remote code exection vul on url: ' +result[key]+ ' with payload: ' +key+ ' .'
                print(msg)
                number = 'v34'
                return True,url,number,msg
        else:
            msg = 'There is no struts2 remote code exection vul'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg