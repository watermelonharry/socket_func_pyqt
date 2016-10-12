# -*- coding: utf-8 -*-

"""
Module implementing YingyanFunc.
"""

from PyQt4.QtCore import pyqtSignature,  pyqtSignal
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui

from package.gpsuploader import GpsUploader

from ui.Ui_yingyan_web import Ui_yingyan_web
import time


class YingyanFunc(QDialog, Ui_yingyan_web):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None, updateMainSignal = None, recDataSignal = None, toPickSignal = None):
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

        #upload data to BAIDU
        # self.uploader = GpsUploader(self.updateMainSignal, self.toGpsUploaderSignal)
    
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
            self.uploadGpsData('str args here')
        else:
            pass

    def uploadGpsData(self,str_arg):
        #TODO:发送至gpsuploader并启动上传
        pass

    def ExtractCommandData(self, strArg):
        strArg = str(strArg)
        data = strArg.split('=')
        argList = [data[0],data[1]]
        if str(reduce(lambda x,y: chr(ord(x)^ord(y)), list('='.join(data[:-1]) + '='))) == data[-1]:
            if data[0] == '0':
                if data[1] == 'L':      # command 1
                    argList.append(data[2])     #longitude
                    argList.append(data[3])     #latitude
                    argList.append(data[4])     #height
                    argList.append(data[5])     #speed

                    self.update_status(strArg,argList)
                else:
                    #todo: wrong heartbeat info
                    argList = None
            else:
                if data[1] == 'P':      #command 2
                    #todo: param check
                    pass
                else:
                    argList = None

                if data[1] == 'S':      #command 3
                    #todo: param set
                    pass
                else:
                    argList = None

                if data[1] == 'D':      #command 4
                    #todo: set points
                    self.SendToPickFunc(strArg)
                else:
                    argList = None
        else:
            argList = None


    def SendToPickFunc(self,strArg):
        """
        发送至pickFunc
        """
        #test
        self.updateMainSignal.emit('yinyan-to pickpiont:' + str(strArg)[:-1])

        self.toPickPointSignal.emit(strArg)