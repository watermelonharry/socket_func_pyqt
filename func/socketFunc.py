# -*- coding: utf-8 -*-
##20160603-1455
"""
Module implementing SocketUi.
"""

from PyQt4.QtCore import pyqtSignature, QMutex, QMutexLocker, QThread,  pyqtSignal,  SIGNAL
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui
from ui.Ui_socketUI import Ui_SocketUi
##yingyan_web UI
from yingyanFunc import YingyanFunc

## log write module
from package import log
import socket
import time

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
        self.client = None

        with QMutexLocker(self.mutex):
            self.update_signal.emit('enter-sserver-class- '+ str(self))

    def __str__(self):
        return('sserver-host:'+ str(self.host)+':'+str(self.port)+'; mode-'+ self.mode)

    ##set socket parameters
    def setpara(self, host = None,  port = None,  mode = None):
        if self.sserver is not None:
            self.update_main('enter-sserver-func-SETPARA-error-STOP SERVER FIRST')
        else:
            if host is not None:
                self.host = host
            if port is not None:
                self.port = port
            if mode is not None:
                self.mode = mode
            self.update_main('enter-sserver-func-SETPARA-sucess-SET ' + str(self))


    ##show server messages in main window
    def update_main(self,  str_arg):
        self.update_signal.emit(str_arg)

    ##what the THREAD mainly do
    def run(self):
        self.RUN_FLAG = True
        self.create_server()

        while self.RUN_FLAG:
            if self.process_data() is False:
                self.listen()
        self.update_main('end-sserver-thread')

    ##triggered from dialog button, set the RUN_FLAG to stop thread, and eliminate the socket/client
    def close(self):
        self.RUN_FLAG = False
        if self.client is not None:
            self.client.send('<SERVER CLOSED NOW>')
            self.client.close()
        if self.sserver is not None:
            self.sserver.close()
        self.client = None
        self.sserver = None
        self.update_main('enter-sserver-func-CLOSE-')


    ##process recv data here
    def process_data(self):
        try:
            data = self.client.recv(2048)
            #implement received data PROCESSING here
            self.return_signal.emit(data)

            self.update_main('enter-sserver-func-PROCDATA-recv:'+str(data))
            self.client.send('GET')
            return True
        except Exception as e:
            ##closed by remote client
            self.update_main('enter-sserver-func-PROCDATA-CLOSE BY CLIENT')
            self.client = None
            return False

    ##create a new socket server instance and make it listen, accept client connection in FUNCTION: self.listen()
    def create_server(self):
        if self.sserver is not None:
            self.update_main('enter-sserver-func-CREATESERVER-eror-CLOSE SERVER FIRST')
            return

        try:
            self.sserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_address = (self.host, self.port)
            self.sserver.bind(server_address)
            self.sserver.listen(1)
            self.update_main('enter-sserver-func-CREATESERVER-' + str(self))
        except Exception as e:
            self.update_main('enter-sserver-func-CREATESERVER-error-' + str(e))
            self.sserver = None
            self.RUN_FLAG = False
            return
        self.listen()

    ##accept connection from client if there's no connection alive
    def listen(self):
        if self.RUN_FLAG and self.sserver is not None:
            (client,  address) = self.sserver.accept()
            self.client = client
            self.update_main('enter-sserver-func-CREATESERVER-connected-client:'+ str(address))

    ##send data to client, mainly triggered by SEND_BUTTON in main window
    def send_data(self, str_arg):
        if self.client is not None:
            self.client.send(str_arg)
            self.update_main('enter-sserver-func-SENDDATA-sucess')
        else:
            self.update_main('enter-sserver-func-SENDDATA-error:NO CONNECTION')

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
        #try to make sub dialog constant
        self.web_dailog = YingyanFunc(upsignal = self.sock.update_signal,  downsignal = self.sock.return_signal)

    def __str__(self):
        return('sockFunc-para:')

    def say_hi(self,  words):
        ##show in the info area in dialog
        try:
            self.sock_show_tb.append(str(words))
        except Exception as e:
            self.sock_show_tb.append('<ERROR: invalid input from client>')
        ##add log
        self.log.write(str(words))



    @pyqtSignature("")
    def on_sock_clear_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.say_hi('clear button clicked')
        self.sock_show_tb.clear()

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
        self.sock.setpara(host = self.host,  port = self.port)
        self.say_hi('set host/port to ' + ':'.join(str_in))

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
        self.sock.send_data(message)

    @pyqtSignature("")
    def on_sock_save_log_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('SQLLL button clicked')

        ##show SQLLL window
        self.web_dailog.show()

        self.say_hi('sql window create')


    @pyqtSignature("")
    def on_sock_close_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.say_hi('close button clicked')
        #self.sock.stop_tcp_server()
        self.sock.close()