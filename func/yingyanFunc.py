# -*- coding: utf-8 -*-

"""
Module implementing YingyanFunc.
"""

from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog
from PyQt4 import QtGui

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
    
    @pyqtSignature("")
    def on_web_emit_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.upsignal.emit('emit btn clicked')
        
        self.upsignal.emit('awake from 5 secs sleep')
    
    def update_status(self, str_arg):
        #str will be processed first
        self.web_time_label.setText(str(time.asctime()))
        self.web_test_label.setText(str_arg)
