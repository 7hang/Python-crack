# -*- coding:utf-8 -*-

import http.client

httpClient = None

try:
    httpClient = http.client.HTTPSConnection('10.11.20.139', 443, timeout=30)
    httpClient.request('GET', '')

    response = httpClient.getresponse()

    print(response.getheaders())
    print('aaaaaaaaaaaaa')
    print('bbbbbbbbb')

    print(response.read())
except Exception as e:
    print(e)
finally:
    if httpClient:
        httpClient.close()









