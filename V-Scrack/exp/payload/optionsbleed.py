#-*-coding:utf-8-*-

import urllib3
import pyparsing as pp


pool = urllib3.PoolManager(10, cert_reqs='CERT_NONE')
showall = True


def parse_verbs():
    get = pp.Literal("GET")
    post = pp.Literal("POST")
    options = pp.Literal("OPTIONS")
    put = pp.Literal("PUT")
    patch = pp.Literal("PATCH")
    delete = pp.Literal("DELETE")
    connect = pp.Literal("CONNECT")
    trace = pp.Literal("TRACE")
    track = pp.Literal("TRACK")
    head = pp.Literal("HEAD")
    crappaton = pp.Word(pp.printables).setResultsName('bleed')
    headers = pp.ZeroOrMore(
        get | post | head | options | put | patch | delete | connect | trace | track).setResultsName('headers')
    verb = pp.Dict(pp.Group((headers + pp.ZeroOrMore(crappaton))).setResultsName('results'))
    return verb

def get_verbs(url):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = pool.request('OPTIONS', url)
        res = str(r.headers["Allow"])
        if "allow" in res:
            verbs = res + "PAPAPAPA"
            if verbs is "":
                return "EMPTY"
            else:
                return verbs.replace(',', '')
        else:
            return "ERROR"
    except Exception as e:
        return "ERROR"

def check_bleeding(url,retests):
    for i in range(retests):
        verbs=get_verbs(url)
        if (verbs == "EMPTY"):
            return "EMPTY"
        else:
            parsed_verbs = (parse_verbs().parseString(verbs)).asDict()
            if "bleed" in parsed_verbs["results"]:
                if parsed_verbs["results"]["bleed"] is "":
                    return "EMPTY"
                elif "ERROR" in parsed_verbs["results"]["bleed"]:
                    return "ERROR"
                else:
                    print('BLEEDING: '+parsed_verbs["results"]["bleed"])
                    return "BLEEDING"
    return "NO BLEEDING "

def verify(protocol,ip,port):
    url = protocol+'://'+ip+':'+str(port)+'/'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print('testing if apache HTTP OPTIONS bleed vul(CVE-2017-9798)')
    iters = 1
    checked = []
    try:
        checked = check_bleeding(url,iters)
        if checked == "BLEEDING":
            msg = 'there is apache HTTP OPTIONS bleed vul(CVE-2017-9798) on url : ' + url + ' .'
            print(msg)
            number = 'v50'
            return True,url,number,msg
        else:
            print(checked)
            msg = 'there is no apache HTTP OPTIONS bleed vul(CVE-2017-9798)'
            number = 'v0'
            return False,url,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,url,number,msg



if __name__ == '__main__':
    res = verify('http','114.141.182.13',443)
    print(res)