#-*- encoding: utf-8 -*-
'''

@author: SmthEcon
'''
import datetime

class scanLog(object):
    '''
    classdocs
    '''
    global preFilename
    preFilename = 'D:/Scripts/V-Scrack/exp/scanLog '
    def __init__(self):
        pass
    
    @staticmethod
    def writeScanLog(*content):
        now = str(datetime.datetime.now())
        filename = preFilename + now.split(' ')[0] + '.log'
        with open(filename,'a') as file:
            for line in content[0]:
                file.write(now.split('.')[0] + ', ' + str(line).strip('[]') + '\n')

if __name__=='__main__':
    log = scanLog()
    log.writeScanLog('test')

