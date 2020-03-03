#-*- coding: utf-8 -*-

import dns.resolver
import dns.zone

def verify(protocol,ip,port):
    url = ip+':'+str(port)
    print('testing if dns zone transfer vul')
    try:
        dnsResolver = dns.resolver.Resolver()
        dnsResolver.timeout = 6
        ns = dnsResolver.query(url, 'NS')
        if ns:
            for domain_dns in ns:
                xfr = dns.query.xfr(str(domain_dns), url, timeout=6, lifetime=6)
                if dns.zone.from_xfr(xfr):
                    msg = 'There is dns zone transfer vul on url: ' + url + ' .'
                    print(msg)
                    number = 'v123'
                    return True, url, number, msg
                else:
                    pass
    except Exception as e:
        print(str(e))
    msg = 'There is no dns zone transfer vul.'
    number = 'v0'
    return False, url, number, msg