# -*- coding: utf-8 -*-

import socket
import time


def xorFormat(str_arg):
    """
    计算给定str的字节异或值
    :param str_arg:
    :return: char
    """
    return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))

def startConnect(host = None, port = None):
    if host is None and port is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 9876))
            print('connected')
            return s
        except Exception as e:
            print(e.message)
            return None
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print('connected')
            return s
        except Exception as e:
            print(e.message)
            return None

def sendHeartBeat():
    s = startConnect()
    if s is not None:
        c = raw_input('send order? y/n')
        startLongi = 120.13143165691
        startLati = 30.272977524721
        startStatus = 1
        count = 0

        while c != 'n':
            if c == 'y':
                order = '0=L=%s=%s=20.12=1.0=%s=' %(str(startLongi + count*0.00001),str(startLati + count*0.00001),str((startStatus+count)%9))
                order += xorFormat(order)
                s.send(order)
                print (order)
                count += 1
            else:
                try:
                    c = c.split(' ')
                    order = '0=L=%s=%s=20.12=1.0=%s=' % (str(c[0]), str(c[1]), str(1))
                    order += xorFormat(order)
                    s.send(order)
                    print (order)
                except Exception as e:
                    print(e.message)
            c = raw_input('send order? y/n or input longitude and latitude')

        s.close()
        print('end connection')

if __name__ == '__main__':
    sendHeartBeat()
