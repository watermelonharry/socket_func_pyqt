# -*- coding: utf-8 -*-

from ui.Ui_poowindow import Ui_notice_window
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop

noticeDict= {
    1:u'确定起飞？',
    2:u'提示2',
    3:u'提示3',
    4:u'提示',
    5:u'提示4',
    6:u'提示5',
}

class NoticeWindow(QDialog, Ui_notice_window):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.status = False

    def show(self, intArg):
        self.notice_content.setText(noticeDict[intArg])
        QDialog.show(self)

    def exec_(self, intArg):
        self.notice_content.setText(noticeDict[intArg])
        self.status = False
        QDialog.exec_(self)


    def Confirm(self, intArg):
        self.exec_(intArg)

    @pyqtSignature("")
    def on_notice_true_btn_clicked(self):
        self.status = True
        self.close()

    @pyqtSignature("")
    def on_notice_cancel_btn_clicked(self):
        self.status = False
        self.close()


