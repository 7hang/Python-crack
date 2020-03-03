# -*- coding:utf-8 -*-

import socket
import datetime
from exp.lib import gla

class Auxiliarylib():
    def __init__(self):
        pass

    def auxiliarytest(self):
        web = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        web.bind(('0.0.0.0',8088))
        web.listen(10)
        while True:
            try:
                conn,addr = web.accept()
                data = conn.recv(4096)
                data = data.decode()
                req_line = data.split("\r\n")[0]
                path = req_line.split()[1]
                route_list = path.split('/')
                html = "NO"
                if len(route_list) == 3:
                    if route_list[1] == 'add':
                        if route_list[2] not in gla.url_history:
                            gla.url_history.append(route_list[2])
                    elif route_list[1] == 'check':
                        if route_list[2] in gla.url_history:
                            gla.url_history.remove(route_list[2])
                            html = 'YES'
                else:
                    query_str = route_list[1]
                    for query_raw in gla.query_history:
                        if query_str in query_raw:
                            gla.query_history.remove(query_raw)
                            html = "YES"
                print(datetime.datetime.now().strftime('%m-%d %H:%M:%S') + " " + str(addr[0]) +' web query: ' + path)
                raw = "HTTP/1.0 200 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: %d\r\nConnection: close\r\n\r\n%s" %(len(html),html)
                raw = raw.encode("utf-8")
                conn.send(raw)
                conn.close()
            except Exception as e:
                msg = str(e)
                print(msg)
                pass
