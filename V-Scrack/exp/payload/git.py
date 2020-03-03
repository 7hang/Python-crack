# -*-coding:utf-8-*-

import requests


def verify(protocol, ip, port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if git information disclose vul')
    status = ''
    contentlen = ''
    dirconurl = url + '/nodirinthiswebanx4dm1n/'
    try:
        dirresponse = requests.get(dirconurl, verify=False, timeout=5)
        status = dirresponse.status_code
        gitpath = '/.git/config'
        giturl = url + gitpath.strip('\r\n')
        response = requests.get(giturl, timeout=5)
        if 'repositoryformatversion' in response.text:
            msg = 'Found /.git/config dir in url:' + giturl + ''
            print(msg)
            number = 'v37'
            return True, url, number, msg
        else:
            msg = 'Cannot found /.git/config dir in url:' + giturl + ''
            number = 'v0'
            return False, url, number, msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg