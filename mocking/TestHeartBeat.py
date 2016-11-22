# -*- coding: utf-8 -*-

import socket
import time


def uniqueId():
    """
    生成基于当前unix时间戳的唯一ID
    :return: str(unique id)
    """
    import datetime
    import time
    uniID = str(time.mktime(time.localtime()))[:-2] + str(datetime.datetime.now().microsecond / 1000)
    return str(uniID)

def xorFormat(str_arg):
    """
    计算给定str的字节异或值
    :param str_arg:
    :return: char
    """
    return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))

def startConnect(host = None, port = None):
    strArg = raw_input('default or ip:port?\n')
    if len(strArg) > 5:
        host,port = strArg.split(':')
    if host is None and port is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 9876))
            print('connected-localhost:9876')
            return s
        except Exception as e:
            print(e.message)
            return None
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            print('connected-%s:%s') %(host, str(port))
            return s
        except Exception as e:
            print(e.message)
            return None

def sendHeartBeat(s):
    if s is not None:
        c = raw_input('send heart beat order? y/n ')
        startLongi = 120.13143165691
        startLati = 30.272977524721
        startStatus = 1
        count = 0

        while c != 'n':
            if c == 'y':
                order = 'H=L=%s=%s=20.12=1.0=%s=' %(str(startLongi + count*0.00001),str(startLati + count*0.00001),str((startStatus+count)%9))
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
            c = raw_input('send heartbeat order? y/n or input longitude and latitude\n')

        print('end heartBeat')

def SendDebugInfo(s):
    if s is not None:
        startDebug = 1
        c = raw_input('send debug order? y/n ')
        while c != 'n':
            if c=='y':
                if startDebug < 3:
                    order = uniqueId() + '=T=' + str(startDebug) + '001='
                    order += xorFormat(order)
                    s.send(order)
                    print(order)
                else:
                    num = '000' + str(startDebug-3)
                    num = '3' + num[-3:] + '='
                    print(num)
                    order = uniqueId() + '=T=' + num
                    order += xorFormat(order)
                    s.send(order)
                    print(order)
            c = raw_input('send debug order? y/n ')
            startDebug = startDebug + 1 if startDebug < 17 else 1
        print('end debug info')
    print('no connect')

if __name__ == '__main__':
    s = startConnect()
    choose = raw_input('select test order:\n'
                       '1: heartBeat\n'
                       '2: debug info\n'
                       '0: end test\n')

    while choose != '0':
        if choose == '1':
            sendHeartBeat(s)
        if choose == '2':
            SendDebugInfo(s)

        choose = raw_input('select test order:\n'
                           '1: heartBeat\n'
                           '2: debug info\n'
                           '0: end test\n')
    s.close()
    print('<end connection>')