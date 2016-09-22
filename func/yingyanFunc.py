# -*- coding: utf-8 -*-

"""
Module implementing YingyanFunc.
"""

from PyQt4.QtCore import pyqtSignature,  QUrl
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui

from package.gpsuploader import GpsUploader

from ui.Ui_yingyan_web import Ui_yingyan_web
import time


class YingyanFunc(QDialog, Ui_yingyan_web):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None,  upsignal = None,  downsignal = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        #SIGNALS used to update main window
        self.upsignal = upsignal
        #SIGNALS used to receive data
        self.downsignal = downsignal
        self.downsignal.connect(self.update_status)
        #upload data to BAIDU
        self.uploader = GpsUploader(upsignal, downsignal)
    
    @pyqtSignature("")
    def on_web_emit_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.upsignal.emit('emit btn clicked')
        
        self.upsignal.emit('awake from 5 secs sleep')
    
    def update_status(self, str_arg):
        #the str_arg includes all data, will be processed first
        #(longitude, latitude, time) will be pass to gps_loader and upload to BAIDU
        #other info will be pass to local textbrowser


        self.web_time_label.setText(str(time.asctime()).split(' ')[3])

        argList = self.ExtractCommandData(str_arg)
        self.web_recdata_label.setText(str_arg)

        if argList is not None:
            self.web_longi_label.setText(argList[2])
            self.web_lati_label.setText(argList[3])
            self.web_altitu_label.setText(argList[4])
        else:
            pass

    def ExtractCommandData(self, strArg):
        data = strArg.split('=')
        argList = [data[0],data[1]]
        if str(reduce(lambda x,y: chr(ord(x)^ord(y)), list('='.join(data[:-1]) + '='))) == data[-1]:
            if data[0] == '0':
                if data[1] == 'L':      # command 1
                    argList.append(data[2])     #longitude
                    argList.append(data[3])     #latitude
                    argList.append(data[4])     #height
                    argList.append(data[5])     #speed
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
                    pass
                else:
                    argList = None
        else:
            argList = None

        return argList