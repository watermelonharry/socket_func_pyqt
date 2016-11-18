# -*- coding: utf-8 -*-

from ui.Ui_poowindow import Ui_notice_window
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop

noticeDict= {
    1:u'确定起飞？',
    2:u'提示2',
    3:u'提示3',
    4:u'提示4',
    5:u'提示5',
    6:u'提示6',

    #错误提示
    11:u'飞行器未处于等待状态，无法设置',

    21:u'正在等待上一条命令传输完成',
    22:u'选取点不足，请重新选择',
    23:u'设置点步骤错误',
    24:u'计算的路径点不足，请重新设置',

    71:u'错误：未收到当前坐标信息，请建立与飞行器的连接',
    72:u'地图加载成功，可以进行下一步操作',
    73:u'确定清除路径设置？'
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


