#-*- encoding: utf-8 -*-
'''

@author: SmthEcon
'''
import datetime

class exceptionLog(object):

    global filename
    filename='../exp/exceptionLog.txt'

    def __init__(self):
        pass
        
    @staticmethod
    def write(message):
        now = str(datetime.datetime.now())
        with open(filename,'a') as file:
            file.write(now.split('.')[0] + ' '+ message + '\n')
        
if __name__=='__main__':
    el = exceptionLog()
    el.write('123456')
        
