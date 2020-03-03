#-*-coding:utf-8-*-

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    print('testing if svn entries')
    status = ''
    contentlen = ''
    dirconurl = url+'/nodirinthiswebanx4dm1n/'
    try:
        dirresponse=requests.get(dirconurl, verify=False, timeout=10)
        status=dirresponse.status_code
        contentLen=dirresponse.headers['content-length']
        svnpath = '/.svn/entries'
        svnurl=url+svnpath.strip('\r\n')
        response=requests.get(svnurl, verify=False, timeout=10)
        if response.status_code!=status and response.headers['content-length']!=contentLen:
            qurl = url+'/.svn/all-wcprops'
            response2 = requests.get(qurl, verify=False, timeout=6)
            if 'svn:wc:ra_dav:version-url' in response.text:
                msg = 'Found /.svn/entries dir in url:'+qurl+' .'
                print(msg)
                number = 'v19'
                return True,url,number,msg
            else:
                pass
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg
    msg = 'Cannot found /.svn/entries dir in url:' + svnurl + ''
    number = 'v0'
    return False, url, number, msg

