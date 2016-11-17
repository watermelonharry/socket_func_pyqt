# -*- coding: utf-8 -*-

"""
Module implementing YingyanFunc.
"""

from PyQt4.QtCore import pyqtSignature,  pyqtSignal, QUrl
from PyQt4 import QtCore
_fromUtf8 = QtCore.QString.fromUtf8
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui

from package.gpsuploader import GpsUploader

from ui.Ui_yingyan_web import Ui_yingyan_web
import time
import os
STATUS_DICT = {1:u'等待状态',
               2:u'路径设置完成',
               3:u'起飞',
               4:u'执行任务',
               5:u'终止任务',
               6:u'降落',
               7:u'任务完成',
               8:u'返航'
               }

class YingyanFunc(QDialog, Ui_yingyan_web):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, updateMainSignal = None, recDataSignal = None, toPickSignal = None, sendOrderSignal = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)

        self.setupUi(self)
        #SIGNALS used to update main window
        self.updateMainSignal = updateMainSignal
        #SIGNALS used to receive data
        self.toYingyanFuncSignal = recDataSignal
        self.toYingyanFuncSignal.connect(self.ExtractCommandData)
        #发送至pickFunc
        self.toPickPointSignal= toPickSignal
        #发送socket命令
        self.sendOrderSignal = sendOrderSignal

        #故障信息存储文件
        import os
        PATH = '/'.join(os.getcwd().split('\\'))
        self.errorFile = PATH + '/ErrorInfo/BugInfo-'+'-'.join(time.ctime().split(' ')).replace(':','-',10) +'.dat'
        try:
            with open(self.errorFile, 'a') as errorFile:
                errorFile.write('<Error File created at ' + time.ctime()+'>\n')
        except Exception as e:
            print ('error in creating errorFile:' ,e.message, 'please reopen the program')

        #upload data to BAIDU
        self.uploader = GpsUploader(updateMainSignal=updateMainSignal,toPickPointSignal= toPickSignal)
        # import os
        # self.webView.setUrl(QtCore.QUrl(_fromUtf8("file:///" + '/'.join(os.getcwd().split('\\')) + "/websrc/yinyandemo/index.html")))
        #
    @pyqtSignature("")
    def on_web_emit_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.updateMainSignal.emit('emit btn clicked')

    def update_status(self, str_arg, argList):
        #the str_arg includes all data, will be processed first
        #(longitude, latitude, time) will be pass to gps_loader and upload to BAIDU
        #other info will be pass to local textbrowser
        self.web_time_label.setText(str(time.asctime()).split(' ')[3])
        if argList is not None:
            self.web_longi_label.setText(argList[2])
            self.web_lati_label.setText(argList[3])
            self.web_altitu_label.setText(argList[4])
            self.web_speed_label.setText(argList[5])
            self.web_recdata_label.setText(STATUS_DICT[int(argList[6])])
        else:
            pass

    def uploadGpsData(self,pointTuple):
        #TODO:发送至gpsuploader并启动上传
        self.uploader.add_point(pointTuple)
        self.uploader.start()

    def ExtractCommandData(self, strArg):
        strArg = str(strArg)       #去掉尾部的\r\n
        while '\r' in strArg: strArg.replace('\r','')
        while '\n' in strArg:strArg.replace('\n','')

        data = strArg.split('=')
        argList = [data[0],data[1]]
        # 校验通过
        if str(reduce(lambda x,y: chr(ord(x)^ord(y)), list('='.join(data[:-1]) + '='))) == data[-1]:
            if data[0] == '0':
                if data[1] == 'L':      # command 1
                    argList.append(data[2])     #longitude
                    argList.append(data[3])     #latitude
                    argList.append(data[4])     #height
                    argList.append(data[5])     #speed
                    argList.append(data[6])     #plane status

                    self.update_status(strArg,argList)
                    #上传至鹰眼
                    self.uploadGpsData((float(data[2]), float(data[3])))
                    #更新取点窗口的当前坐标数据，飞行器的状态数据
                    self.SendToPickFunc('IN=YY=LOC='+ str(data[2]) + '=' + str(data[3])+ '=' + str(data[6]))
                else:
                    #todo: wrong heartbeat info
                    argList = None
            else:
                if data[1] == 'P':      #command 2
                    #todo: param check
                    return
                else:
                    argList = None

                if data[1] == 'S':      #command 3
                    #todo: param set
                    return
                else:
                    argList = None

                if data[1][0] == 'D':      #command 4
                    #set points
                    self.SendToPickFunc(strArg)
                    return
                else:
                    argList = None

                if data[1] == 'E':      #命令4，飞行器发送，故障信息上传
                    #故障信息转存到文件
                    if self.SaveErrorToFile(data[:]) is True:
                        self.SendOrder(id=data[0],content='DY')
                    else:
                        self.SendOrder(id=data[0],content='DN')
                    return
                else:
                    argList = None

                if data[1] == 'C':      #命令5：飞行器控制命令回复
                    self.SendToPickFunc(strArg)
                    return
                else:
                    pass
        else:
            argList = None

    def SendOrder(self,id=None, content=None):
        """
        发送数据至socket client
        :param id: 命令的唯一标志
        :param content: 命令的内容
        :return:
        """
        orderStr = '='.join([str(id), str(content)]) + '='
        orderStr += self.xorFormat(orderStr)
        print(orderStr)
        self.sendOrderSignal.emit(orderStr)


    def SendToPickFunc(self,strArg):
        """
        发送至pickFunc
        """
        #test
        self.updateMainSignal.emit('yinyan-to pickpiont:' + str(strArg))
        self.toPickPointSignal.emit(strArg)

    def SaveErrorToFile(self,errorList):
        """
        保存故障信息到本地
        输入参数列表：[故障序号，故障类型，经度，纬度]
        本地提供：本地时间
        :return:
        """
        writeList = errorList[2:6] + [time.ctime()]
        try:
            with open(self.errorFile,'a') as errorFile:
                errorFile.write(','.join(writeList) + '\n')
                return True
        except Exception as e:
            print('error in yingyan-SaveErrorToFile:', e.message)
            return False

    def xorFormat(self, str_arg):
        return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))