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
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_web_halt_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        print('halt btn clicked')
        time.sleep(5)
        print('awake from 5 secs sleep')
