import socket
import time
import log
import threading
from PyQt4.QtCore import QObject

def current_time():
    return str(time.asctime())
QUIT_SIGNAL = 'q'
PRINT = True

class socket_server(QObject):
    def __init__(self, host = None, port = None, mode = 'TCP', print_target = None):
        self._host = host
        self._port = port
        self._mode = mode
        log.PRINT = False
        self._log = log.logfile('sserverclasstest')
        self._sock = None
        self._clients = []
        self._Event = threading.Event()
        self._Event.set()
        self._print_target = print_target #for outside print function
        self._lock = threading.Lock()

    def __str__(self):
        return 'host:%s:%s @ %s\n' %(self._host, self._port, self._mode)

    # def add_log(self, log = None, dest = None):
    #     if dest is not None:
    #         dest.append(str(log))
    #     else:
    #         print(self._log[-1])
    #     self._log.append(current_time() + '--'+ str(log))
    def add_log(self,words):
        self._lock.acquire()
        self._log.write(words)
        self._lock.release()
        #this shall be deleted
        if self._print_target != None:
            try:
                self._print_target.append(words)
            except Exception as e:
                print(str(e) +': print target error')
        ##print function in console
        if PRINT is True:
            print(words)

    def set_hostport(self, host, port):
        if self._sock != None:
            self.stop_tcp_server()
        self._host = str(host)
        self._port = int(port)
        self.add_log('change host to '+ str(host) + ':' + str(port) + '--')

##need change
    def set_mode(self, mode):
        if len(self._client) != 0 :
            self.client.close()
            self.sock.close()
            self.client = None
            self.sock = None
        self._mode  = mode
        self.add_log('change mode to '+ mode +'--')

    def start_tcp_server(self):
        self._Event.set()
        new_thread = threading.Thread(target= self.tcp_server,args=())
        new_thread.start()
        #
        self.add_log('enter function: start_tcp_server...')
        #
    def stop_tcp_server(self):
        self.add_log('enter function: stop_tcp_server...')

        # stop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # try:
        #     stop_sock.connect((self._host, self._port))
        # except Exception as e:
        #     if e.errno == 10061:
        #         pass
        # try:
        #     stop_sock.send(QUIT_SIGNAL)
        # except Exception as e:
        #     if e.errno == 10061:
        #         pass
        #     self.add_log('tcp_server stopped')
        #
        # try:
        #     stop_sock.connect((self._host, self._port))
        # except Exception as e:
        #     if e.errno == 10061:
        #         pass
        # stop_sock.close()
        self._Event.clear()
        for client in self._clients:
            client.send('server closed!')
            client.close()
        self._clients = []

        ##to end the sub process of tcp_server
        stop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            stop_sock.connect((self._host, self._port))
            stop_sock.close()
        except Exception as e:
            if e.errno == 10061:
                pass

        self._sock.close()
        self._sock = None

    def tcp_server(self):
        #
        self.add_log('enter function: tcp_server...')
        #

        if self._sock != None:
            self.add_log('error:socket server already running, stop first!')
            return False
        try:
            # Create a TCP socket
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Enable reuse address/port
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind the socket to the port
            server_address = (self._host, self._port)
            #
            self.add_log('Starting up echo server  on '+ self._host + ' port '+ str(self._port))
            #

            self._sock.bind(server_address)
            # Listen to clients, backlog argument specifies the max no. of queued connections
            self._sock.listen(10)

            self.add_log("Waiting to receive message from client.")
        except Exception as e:
            self.add_log('error '+str(e.errno)+':'+ e.strerror)
            return False

        #enter listen mode
        while self._Event.isSet():

            client, address = self._sock.accept()
            self._lock.acquire()
            self._clients.append(client)
            self._lock.release()
            #
            self.add_log('connected by '+str(address)+' from main...')
            #
            new_thread = threading.Thread(target= self.tcp_sock_process,args=(client,address, self._Event))
            new_thread.start()

        #self._sock.close()
        #
        self.add_log('socket closed')

    def tcp_sock_process(self, client, address, Event):
        #
        self.add_log('enter function: tcp_sock_process...')
        #
        #
        self.add_log('subprocess for '+str(address)+' is on the go...')
        #
        while True:
            try:
                data = client.recv(2048)
                if data[:len(QUIT_SIGNAL)] != QUIT_SIGNAL:
                    client.send('Get:')
                    client.send(data)
                    client.send('@' + str(time.asctime()) + '\n')
                    #
                    self.add_log('recv: '+ str(data)+ ' from '+ str(address))
                    #
                else:
                    self.add_log('recv: '+ str(data)+ ' from '+ str(address))
                    client.send('quit commad accept, socket closed!')
                    client.close()
                    self._lock.acquire()
                    self._clients.remove(client)
                    self._lock.release()
                    break
            except Exception as e:
                print(str(e))
                #
                self.add_log(str(e))
                #
                break
        self.add_log('send to client:'+ str(address)+'--socket closed!')





if __name__ == '__main__':
    test = socket_server(host= '10.180.61.89', port = 9876)
    print(test)
    test.start_tcp_server()
    stop_count = 10
    while stop_count != 0:
         time.sleep(5)
         test.add_log('active threading:' + str(threading.activeCount())+ '--stop count:' + str(stop_count))
         stop_count -= 1
    test.stop_tcp_server()
    test.add_log('active threading:' + str(threading.activeCount()))

    print(test)
    test.start_tcp_server()
    stop_count = 10
    while stop_count != 0:
         time.sleep(5)
         test.add_log('active threading:' + str(threading.activeCount())+ '--stop count:' + str(stop_count))
         stop_count -= 1
