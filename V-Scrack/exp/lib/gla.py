# -*- coding:utf-8 -*-

import string

query_history = []
url_history = []


class getpassdict():
    def __init__(self):
        pass

    def get_pass_dict(self):
        pass_dict = []
        with open('../pass_ftp.txt','r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                pass_dict.append(line)
            f.close()
        return pass_dict

class gettag():
    def __init__(self):
        pass

    def get_tag(self):
        tag_dict = []
        with open('http_discern.ini','r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                tag_dict.append(line)
            f.close()
        return tag_dict

def str2hex(x):
    asdad = bytes(x, 'utf-8')
    return asdad.hex()

def hex_dump(buf):

    output = ''
    buf_size = len(buf)

    for i in range(0, buf_size, 16):
        output += '%08x  ' % i

        for j in range(0, 16):
            if j == 8:
                output += ' '
            if i + j >= buf_size:
                output += '   '
            else:
                output += '%02x ' % ord(buf[i + j])

        output += ' '

        for j in range(0, 16):
            if i + j >= buf_size:
                output += ' '
            else:
                if (buf[i + j] in string.printable) and (not buf[i + j].isspace()):
                    output += '%c' % buf[i + j]
                else:
                    output += '.'

        output += '\n'
    return output