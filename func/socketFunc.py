# -*- coding: utf-8 -*-
##20160603-1455
"""
Module implementing SocketUi.
"""
import os
CONFIG_PATH = '/'.join(os.getcwd().split('\\')) + '/websrc/socket_config.dat'

from PyQt4.QtCore import pyqtSignature, QMutex, QMutexLocker, QThread,  pyqtSignal,  SIGNAL
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui
from ui.Ui_socketUI import Ui_SocketUi

##yingyan_web UI
from yingyanFunc import YingyanFunc
from pickFunc import PickPointfunc
from debugWindow import DebugWindow
from popWindow import NoticeWindow

## log write module
from package import log
import socket
import time

##set the socket server and running in QThread
##accept only 1 connection with clients
##showing received data in run method
##send data to client in another thread -- self.clientThread
class sserver(QThread):
    # update_signal = pyqtSignal(str)
    return_signal = pyqtSignal(str)

    def __init__(self,  parent =None,  mutex = None,  host = 'localhost',  port = 9876,  mode = 'TCP',
                 upMainSig = None,  recSignal = None, readySignal = None):
        super(sserver,  self).__init__(parent)
        self.mutex = mutex
        self.host = host
        self.port = port
        self.mode = mode
        self.sserver = None
        self.RUN_FLAG = True
        self.client = None
        self.updateMain = upMainSig
        self.recDataSignal = recSignal
        self.readySignal = readySignal

        with QMutexLocker(self.mutex):
            self.updateMain.emit('new socket server- '+ str(self))

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
        self.updateMain.emit(str_arg)

    ##what the THREAD mainly do
    def run(self):
        print('serverRun')
        self.update_main('success in sock-run')

        self.RUN_FLAG = True
        self.create_server()

        while self.RUN_FLAG and self.sserver is not None:
            if self.process_data() is False:
                self.connectOneClient()

        print('serverEnd')
        self.update_main('success in end-sserver-thread')


    ##triggered from dialog button, set the RUN_FLAG to stop thread, and eliminate the socket/client
    def close(self):
        self.RUN_FLAG = False
        if self.client is not None:
            try:
                self.client.send('<SERVER CLOSED NOW>')
                self.client.close()
            except Exception as e:
                pass
        else:
            self.clientConnect()
        if self.sserver is not None:
            try:
                self.sserver.close()
            except Exception as e:
                pass
        self.client = None
        self.sserver = None
        #self.clientConnect()
        self.update_main('enter-sserver-func-CLOSE-')

    def clientConnect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            s.close()
        except Exception as e:
            s.close()
            pass
            # print('error in server-close-clientConnect:',e.message)

    ##process recv data here
    def process_data(self):
        if self.client is False or self.client is None:
            return False
        try:
            data = self.client.recv(2048)
            if len(data) == 0:
                self.update_main('enter-sserver-func-PROCDATA-CLOSE BY CLIENT-0')
                self.client.close()
                self.client = None
                return False
            else:
                #implement received data PROCESSING here
                self.recDataSignal.emit(data)
                self.update_main('enter-sserver-func-PROCDATA-recv:'+str(data))
            #self.client.send('GET')
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
            self.sserver.listen(5)
            self.update_main('enter-sserver-func-CREATESERVER-' + str(self))
            self.readySignal.emit('Y')
        except Exception as e:
            self.update_main('enter-sserver-func-CREATESERVER-error-' + str(e))
            self.sserver = None
            self.RUN_FLAG = False
            self.readySignal.emit('N')
            return
        self.connectOneClient()

    ##accept connection from client if there's no connection alive
    def connectOneClient(self):
        if self.RUN_FLAG and self.sserver is not None:
            (client,  address) = self.sserver.accept()
            self.client = client
            # self.send_data('-connected-')
            #self.Confirm(35)
            self.update_main('enter-sserver-func-CREATESERVER-connected-client:'+ str(address))

    ##send data to client, mainly triggered by SEND_BUTTON in main window
    def send_data(self, str_arg):
        str_arg = str(str_arg)
        if self.client is not None:
            self.client.send(str_arg)
            self.update_main('enter-sserver-func-SENDDATA-sucess:' + str_arg)
        else:
            self.update_main('enter-sserver-func-SENDDATA-error:NO CONNECTION')

    def Confirm(self,intArg):
        """
        确认窗口
        :param intArg:
        :return:确定返回True， 取消返回False
        """
        noticeWindow = NoticeWindow()
        noticeWindow.Confirm(intArg)
        return noticeWindow.status

class SocketFunc(QDialog, Ui_SocketUi):
    """
    Class documentation goes here.
    """
    updateMainSignal = pyqtSignal(str)

    toPickPointSignal = pyqtSignal(str)
    fromPickPointSignal =  pyqtSignal(str)

    toYingyanFuncSignal = pyqtSignal(str)
    fromYingyanFuncSignal = pyqtSignal(str)

    toSocketfuncSignal = pyqtSignal(str)
    fromSocketfuncSignal = pyqtSignal(str)

    toDebugWindowSignal = pyqtSignal(str)

    # 调用该信号会进行发送socket信息操作
    sendOrderSignal = pyqtSignal(str)
    # 来自server的成功信号
    serverCreateSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.sock = sserver(upMainSig=self.updateMainSignal,recSignal=self.fromSocketfuncSignal, readySignal = self.serverCreateSignal)
        self.SERVER_RUN = False
        self.host = 'localhost'
        self.port = 9876
        self.mode = 'TCP'

        ##地图加载完成标志
        self.LOAD_FINISH = False

        self.mutex = QMutex()
        self.log = log.logfile('log')
        self.orderDict = {}
        if self.log is not None:
            with QMutexLocker(self.mutex):
                self.log.write('enter-socketFuc-class-INIT-'+  str(self))

        self.updateMainSignal.connect(self.say_hi)
        self.fromSocketfuncSignal.connect(self.sockToYingyan)
        #try to make sub dialog constant
        self.YingyanDailog = YingyanFunc(updateMainSignal=self.updateMainSignal, recDataSignal=self.toYingyanFuncSignal, toPickSignal= self.toPickPointSignal, sendOrderSignal= self.sendOrderSignal)

        self.PickPointDialog = PickPointfunc(upsignal=self.fromPickPointSignal, downsignal=self.toPickPointSignal, updateMainSignal = self.updateMainSignal, sendOrderSignal= self.sendOrderSignal, toDebugWindowSingal = self.toDebugWindowSignal)
        #todo:发送到socket的信号统一为sendOrderSignal
        #self.fromPickPointSignal.connect(self.processPickData)

        self.sendOrderSignal.connect(self.SendOrder)

        #调试窗口
        self.debugWindow = DebugWindow(self.toDebugWindowSignal)
        self.ReadConfigFromFile()

        #server成功建立
        self.serverCreateSignal.connect(self.ServerCreated)

    def __str__(self):
        return('sockFunc-para:')

    def ServerCreated(self,strArg):
        if str(strArg) == 'Y':
            self.SERVER_RUN = True
            self.Confirm(30)
        else:
            self.SERVER_RUN = False
            self.Confirm(33)

    def ReadConfigFromFile(self):
        """
        从文件读取上次host:port设置
        :return:
        """
        configList = None
        try:
            with open(CONFIG_PATH, 'r') as config:
                configList = config.readlines()
        except Exception as e:
            print('error in socketFunc-ReadConfig:',e.message)

        if configList is not None:
            try:
                addrs = configList[0].replace('\n','')
                ip,port = addrs.split(':')
                self.port = int(port)
                self.host = ip
                self.sock_ip_text.setText(addrs)
            except Exception as e:
                self.port = 9876
                self.host = 'localhost'
                self.sock_ip_text.setText('localhost:9876')

    def SaveConfigToFile(self):
        """
        将上次设置保存到文件
        :return:
        """
        saveConfig = str(self.host) +':'+str(self.port)+ '\n'
        try:
            configList = None
            with open(CONFIG_PATH,'r') as config:
                configList = config.readlines()
                if len(configList) > 0:
                    configList[0] = saveConfig
                else:
                    configList.append(saveConfig)
            with open(CONFIG_PATH,'w') as config:
                if configList is not None:
                    config.writelines(configList)
        except Exception as e:
            print('error in socketFunc-saveConfig:', e.message)



    def sockToYingyan(self,message):
        """将sock接收的数据转发到yinyan窗口"""
        self.toYingyanFuncSignal.emit(message)

    def say_hi(self,  words):
        ##show in the info area in dialog
        if str(words) == 'Loading map done':
            self.LOAD_FINISH = True
        try:
            self.sock_show_tb.append(str(words))
        except Exception as e:
            self.sock_show_tb.append('<ERROR: invalid input from client>')
        ##add log
        with QMutexLocker(self.mutex):
            self.log.write(str(words))

    # def processPickData(self,  str_data):
    #     """处理来自pickPoint窗口的格式化数据（转发至socket.send）"""
    #     self.sock.send_data(str_data)
    #     self.say_hi(str_data)

    def SendOrder(self,str_data):
        """
        发送至socket 的 client
        :param str_data:
        :return:
        """
        self.sock.send_data(str_data)

    def uniqueId(self):
        import datetime
        import time
        uniID = str(time.mktime(time.localtime()))[:-2] + str(datetime.datetime.now().microsecond / 1000)
        return str(uniID)
    
    def xorFormat(self, str_arg):
        return str(reduce(lambda x,y: chr(ord(x)^ord(y)), list(str_arg)))

    def Confirm(self,intArg):
        """
        确认窗口
        :param intArg:
        :return:确定返回True， 取消返回False
        """
        noticeWindow = NoticeWindow()
        noticeWindow.Confirm(intArg)
        return noticeWindow.status

    """
    按钮
    """
    @pyqtSignature("")
    def on_sock_clear_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            self.say_hi('clear button clicked')
            if self.Confirm(36) is True:
                self.sock_show_tb.clear()
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_getip_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.LOAD_FINISH is True:
            self.say_hi('get ip button clicked')
            try:
                str_in = [str(i) for i in self.sock_ip_text.text().split(':')]
                self.host = str_in[0]
                self.port = int(str_in[1])
                self.sock.setpara(host = self.host,  port = self.port)
                self.say_hi('set host:port to ' + ':'.join(str_in))
                self.Confirm(34)
            except Exception as e:
                self.Confirm(3401)
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_tcp_rbtn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            self.say_hi('tcp clicked')
            if self.sock_tcp_rbtn.isChecked():
                self.say_hi('tcp checked')
            if self.sock_udp_rbtn.isChecked():
                self.say_hi('udp checked')
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_udp_rbtn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            self.say_hi('udp clicked')
            if self.sock_tcp_rbtn.isChecked():
                self.say_hi('tcp checked')
            if self.sock_udp_rbtn.isChecked():
                self.say_hi('udp checked')
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_send_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            message = str(self.sock_input_3.text())
            self.say_hi('send button clicked,data:' + message)
            self.sock.send_data(message)
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_yingyan_web_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            self.say_hi('yingyan_web button clicked')

            ##show SQLLL window
            self.YingyanDailog.show()

            self.say_hi('trace monitoring window create')
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_pickPoint_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            self.say_hi('pick point btn button clicked')
            ##show SQLLL window
            self.PickPointDialog.show()
            self.say_hi('pickpoint window create')
        else:
            self.Confirm(74)
    @pyqtSignature("")
    def on_sock_start_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            if self.SERVER_RUN is False:
                if self.Confirm(29) is True:
                    self.say_hi('start button clicked, start tcpserver with:')
                    # self.sock.setpara()
                    self.say_hi(str(self.sock))
                    try:
                        self.sock.start()
                        # self.SERVER_RUN = True
                        # self.Confirm(30)
                    except Exception as e:
                        self.say_hi('error in socket-start:', e.message)
                        self.SERVER_RUN = False
                        self.Confirm(33)
                    finally:
                        self.SaveConfigToFile()
            else:
                self.Confirm(32)
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_close_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.LOAD_FINISH is True:
            if self.SERVER_RUN is True and self.Confirm(3411) is True:
                self.say_hi('close button clicked')
                #self.sock.stop_tcp_server()
                self.sock.close()
                self.sock = sserver(host= self.host, port = self.port,
                                    upMainSig=self.updateMainSignal, recSignal=self.fromSocketfuncSignal,
                                    readySignal=self.serverCreateSignal)
                self.SERVER_RUN = False
            else:
                self.Confirm(31)
        else:
            self.Confirm(74)

    @pyqtSignature("")
    def on_sock_debug_btn_clicked(self):
        """
        调试信息窗口
        :return:
        """
        if self.LOAD_FINISH is True:
            self.debugWindow.show()
        else:
            self.Confirm(74)

    def xorFormat(self, str_arg):
        return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))

    @pyqtSignature("")
    def on_sock_test_btn_clicked(self):

        """
        测试按钮
        """
        if self.LOAD_FINISH is True:
            pass
        else:
            self.Confirm(74)
        #测试路径设置的回复解析
        # self.updateMainSignal.emit('test btn clicked')
        # testStr = '123456=DY='
        # self.sockToYingyan(testStr + self.xorFormat(testStr))



        # ##测试点上传：
        # import random
        # d = random.randint(-100,100)
        # e = random.randint(-100, 100)
        #
        # longi = 120.1314001 + d/10000.0
        # lati= 30.2729001 + e/10000.0
        #
        # longi = 120.12017068
        # lati = 30.26618533
        #
        #
        # teststr = '0=L='+ str(longi) + '=' + str(lati) + '=20.12=1.0=1='
        # teststr += self.xorFormat(teststr)
        # self.sockToYingyan(teststr)
        # print('send to yingyan:'+teststr)
        #
        # # ## 故障信息测试
        # # errorTestStr = '19191919=E=X=Y=longi=lati='
        # # errorTestStr += self.xorFormat(errorTestStr)
        # # self.sockToYingyan(errorTestStr)

        # ##调试窗口
        # self.toDebugWindowSignal.emit('1001')
        # self.toDebugWindowSignal.emit('2001')
        # self.toDebugWindowSignal.emit('3000')
        # self.toDebugWindowSignal.emit('3001')
        # self.toDebugWindowSignal.emit('3003')

