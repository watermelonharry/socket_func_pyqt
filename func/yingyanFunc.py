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
        self.webView.setUrl(QUrl('‪file:///C:/yinyandemo/index.html'))
        self.upsignal.emit('awake from 5 secs sleep')
    
    def update_status(self, str_arg):
        #the str_arg includes all data, will be processed first
        #(longitude, latitude, time) will be pass to gps_loader and upload to BAIDU
        #other info will be pass to local textbrowser 
        self.web_time_label.setText(str(time.asctime()).split(' ')[3])
        self.web_recdata_label.setText(str_arg)
        self.web_longi_label.setText(str_arg)
        self.web_lati_label.setText(str_arg)
        self.web_altitu_label.setText(str_arg)
    
