# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""
from PyQt4 import QtGui

from Voronoi.Voronoi import Voronoi
from Voronoi import dijkstra
from package.rectangular import Rectangular
import copy,time

from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4 import QtCore
_fromUtf8 = QtCore.QString.fromUtf8

from package.planeStatus import STATUS_DICT,PlaneStatus,PlaneControl, DEBUG_STATUS_DICT
from ui.Ui_debugWindow import Ui_debug_window
class DebugWindow(QDialog, Ui_debug_window):
    def __init__(self, toDebugWindowSignal = None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.ToDebugWindowSignal = toDebugWindowSignal
        self.ToDebugWindowSignal.connect(self.ExtractDebugInfo)

    def ExtractDebugInfo(self,strArg):
        strArg = str(strArg)
        statusCode = int(strArg)
        if strArg[0] == '3' and strArg[-1] != '0':
            messageList = copy.deepcopy(DEBUG_STATUS_DICT[300])
            messageList.insert(1, unicode(statusCode % 3000))
            message = u''.join(messageList)
            self.ShowInBrowser(message)

        else:
            try:
                message = DEBUG_STATUS_DICT[statusCode]
                self.ShowInBrowser(message)
            except Exception as e:
                print('error in debugwindow-exrtract:',e.message)

    def ShowInBrowser(self,strArg):
        self.debug_text_browser.append(time.ctime() + ':  ' + strArg)

    @pyqtSignature("")
    def on_debug_clear_btn_clicked(self):
        self.debug_text_browser.clear()