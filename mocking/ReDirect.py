# -*- coding: utf-8 -*-

import socket
import threading

def GetServerIp():
    inStr = raw_input('input Server IP:PORT')


class Server():
    def __init__(self):
        self.host = '52.198.38.190'
        self.port = 9876
        self.sserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (self.host, self.port)
        self.sserver.bind(server_address)
        self.sserver.listen(5)
        print('server Listening\n')

        (client, address) = self.sserver.accept()
        print('client connected:'+ str(address))
        (schoolserver, Saddress) = self.sserver.accept()
        print('schoolserver connected:' + str(Saddress))
        t1 = ReDirectThread(dst=client, src=schoolserver)
        t2 = ReDirectThread(dst=schoolserver, src=client)
        t1.start()
        t2.start()


    def clientConnect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.close()
        except Exception as e:
            s.close()
            pass

class ReDirectThread(threading.Thread):
    def __init__(self, dst = None, src = None):
        self.dst = dst
        self.src = src
        print('ReDirectThread on the run')

    def run(self):
        while True:
            if self.src is not None:
                data = self.src.recv(2048)
                print('receive from client:' + data)

            if self.dst is not None:
                self.dst.send(data)
                print('send to school server:' + data)
        print('end recThread:' + threading.Thread.getName())

if __name__ == '__main__':
    t = Server()