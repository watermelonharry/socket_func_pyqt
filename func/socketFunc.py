# -*- coding: utf-8 -*-

"""
Module implementing SocketUi.
"""

from PyQt4.QtCore import pyqtSignature, QMutex, QMutexLocker, QThread,  pyqtSignal,  SIGNAL
from PyQt4.QtGui import QDialog
from ui.Ui_socketUI import Ui_SocketUi
## log write module
from package import log  
import socket
import time

##holding the established connetion with the socket client
##only to sending back data to client from server
class clientthread(QThread):
    def __init__(self,  parent = None,  mutex = None,  client = None,  upsignal = None, resignal = None,  id = 0):
        super(clientthread,  self).__init__(parent)
        self.mutex = mutex
        self.client = client
        self.upsignal = upsignal
        self.resignal  = resignal
        self.id = id
        self.RUN_FLAG = True
        self.SEND_DATA = None
        self.SEND_FLAG = False
        
        with QMutexLocker(self.mutex):
            self.update_main('enter-client-class-INIT-'+ str(self))
    
    def __str__(self):
        return('client-id-'+ str(self.id))
    
    #show operations in GUI
    def update_main(self,  str_arg):
        self.upsignal.emit(str_arg)
        
    def run(self):
        self.RUN_FLAG = True
        
        while self.RUN_FLAG:
            if self.SEND_FLAG:
                with QMutexLocker(self.mutex):
                    self.send_back()
                    
        self.update_main('end client thread')
    
    ##implement SEND TO  CLIENT method here 
    def send_back(self):
        message = 'send from client Thread '+str(self.id)+'- function send_back = '+self.SEND_DATA
        self.SEND_FLAG = False
        self.SEND_DATA = None
        self.update_main(message)
    
    ##change the connected client
    def set_para(self,  client = None):
        self.client = client
    
    ##stop the thread
    def close(self):
        self.RUN_FLAG = False
        self.update_main('enter client func-CLOSE-')



##set the socket server and running in QThread
##accept only 1 connection with clients
##showing received data in run method
##send data to client in another thread -- self.clientThread
class sserver(QThread):
    update_signal = pyqtSignal(str)
    return_signal = pyqtSignal(str)
    
    def __init__(self,  parent =None,  mutex = None,  host = 'localhost',  port = 9876,  mode = 'TCP'):
        super(sserver,  self).__init__(parent)
        self.mutex = mutex
        self.host = host
        self.port = port
        self.mode = mode
        self.sserver = None
        self.RUN_FLAG = True
        self.clientThread = clientthread(mutex = self.mutex,  upsignal = self. update_signal, resignal = self.return_signal,  id = 111)
    
        with QMutexLocker(self.mutex):
                self.update_signal.emit('enter sserver class: '+ str(self))
    
    def __str__(self):
        return('sserver--host:'+ str(self.host)+':'+str(self.port)+'; mode-'+ self.mode)
    
    ##set socket parameters
    def setpara(self):
        pass
    
    def update_main(self,  str_arg):
        self.update_signal.emit(str_arg)
            
    def run(self):  
        self.RUN_FLAG = True
        self.clientThread.start()
        
        while self.RUN_FLAG:
            with QMutexLocker(self.mutex):
                str_arg1 = 'send from sserver Thread - still working'
                self.update_signal.emit(str_arg1)

            time.sleep(10)
        self.update_main('end sserver thread')
    
    def close(self):
        self.RUN_FLAG = False
        self.clientThread.close()
        self.update_main('enter sserver func-CLOSE-')
    
    def create_server(self):
        pass



class SocketFunc(QDialog, Ui_SocketUi):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.sock = sserver()
        self.host = 'localhost'
        self.port = 9876
        self.mode = 'TCP'
        
        self.mutex = QMutex()
        self.log = log.logfile('log_socke_func')
        if self.log is not None:
            self.log.write('enter-socketFuc-class-INIT-'+  str(self))
        
        self.sock.update_signal.connect(self. say_hi)
    
    def __str__(self):
        return('sockFunc-para:')

    def say_hi(self,  words):
        self.sock_show_tb.append(str(words))
        ##add log
        self.log.write(str(words))
        
        
    
    @pyqtSignature("")
    def on_sock_clear_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.say_hi('clear button clicked')
    
    @pyqtSignature("")
    def on_sock_getip_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('get ip button clicked')
        str_in = [str(i) for i in self.sock_ip.text().split(':')]
        self.host = str_in[0]
        self.port = int(str_in[1])
        self.say_hi('set host/port to' + ':'.join(str_in))
    
    @pyqtSignature("")
    def on_sock_start_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('start button clicked, start tcpserver with:')
        self.sock.setpara()
        self.say_hi(str(self.sock))
        self.sock.start()

    

    
    @pyqtSignature("")
    def on_sock_tcp_rbtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('tcp clicked')
        if self.sock_tcp_rbtn.isChecked():
            self.say_hi('tcp checked')
        if self.sock_udp_rbtn.isChecked():
            self.say_hi('udp checked')
    

    @pyqtSignature("")
    def on_sock_udp_rbtn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('udp clicked')
        if self.sock_tcp_rbtn.isChecked():
            self.say_hi('tcp checked')
        if self.sock_udp_rbtn.isChecked():
            self.say_hi('udp checked')
    
    @pyqtSignature("")
    def on_sock_send_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        message = str(self.sock_input_3.text())
        self.say_hi('send button clicked,data:' + message)
        self.sock.clientThread.SEND_DATA = message
        self.sock.clientThread.SEND_FLAG = True
    
    @pyqtSignature("")
    def on_sock_save_log_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('save log button clicked')
    
    @pyqtSignature("")
    def on_sock_close_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('close button clicked')
        #self.sock.stop_tcp_server()
        self.sock.close()
