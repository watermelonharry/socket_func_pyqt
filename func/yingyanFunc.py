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
                errorFile.write('<Error File created at ' + time.ctime() + '>')
        except Exception as e:
            print ('error in creating errorFile:' ,e.message, 'please reopen the program')

        #upload data to BAIDU
        self.uploader = GpsUploader(updateMainSignal=updateMainSignal,toPickPointSignal= toPickSignal)
        import os
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("file:///" + '/'.join(os.getcwd().split('\\')) + "/websrc/yinyandemo/index.html")))
    
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

        self.web_recdata_label.setText(str_arg)

        if argList is not None:
            self.web_longi_label.setText(argList[2])
            self.web_lati_label.setText(argList[3])
            self.web_altitu_label.setText(argList[4])
            self.web_speed_label.setText(argList[5])
        else:
            pass

    def uploadGpsData(self,pointTuple):
        #TODO:发送至gpsuploader并启动上传
        self.uploader.add_point(pointTuple)
        self.uploader.start()

    def ExtractCommandData(self, strArg):
        strArg = str(strArg)
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

                    self.update_status(strArg,argList)
                    #todo: 上传至鹰眼
                    self.uploadGpsData((float(data[2]), float(data[3])))
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
                    #todo: set points
                    self.SendToPickFunc(strArg)
                    return
                else:
                    argList = None

                if data[1] == 'E':      #命令4，飞行器发送，故障信息上传
                    #todo: 故障信息转存到文件
                    self.SaveErrorToFile(data[2:6])
                    return
                else:
                    argList = None
        else:
            argList = None

    def SendOrder(self,strArg):
        self.sendOrderSignal.emit(strArg)


    def SendToPickFunc(self,strArg):
        """
        发送至pickFunc
        """
        #test
        self.updateMainSignal.emit('yinyan-to pickpiont:' + str(strArg)[:-1])
        self.toPickPointSignal.emit(strArg)

    def SaveErrorToFile(self,errorList):
        """
        保存故障信息到本地
        输入参数列表：[故障序号，故障类型，经度，纬度]
        本地提供：本地时间
        :return:
        """
        writeList = errorList + [time.ctime()]
        try:
            with open(self.errorFile,'a') as errorFile:
                errorFile.write(','.join(writeList) + '\n')
        except Exception as e:
            print('error in yingyan-SaveErrorToFile:', e.message)

