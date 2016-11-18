# -*- coding: utf-8 -*-

from ui.Ui_poowindow import Ui_notice_window
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop

noticeDict= {
    1:u'确定起飞？',
    2:u'确定执行任务？',
    3:u'确定终止任务？',
    4:u'确定降落？',
    5:u'确定返航？',
    6:u'提示6',

    #错误提示
    11:u'飞行器未处于等待状态，\n无法设置',
    2101:u'飞行器轨迹点未设置，\n请先设置轨迹点',
    3101:u'飞行器未处于执行任务状态，\n无法终止任务',
    4101:u'飞行器未处于终止/完成任务状态，\n无法进行降落操作',
    5101:u'飞行器未处于终止/完成任务状态，\n无法进行返航操作',

    21:u'正在等待上一条命令传输完成',
    22:u'选取点不足，请重新选择',
    23:u'设置点步骤错误',
    24:u'计算的路径点不足，请重新设置',

    71:u'错误：未收到当前坐标信息，\n请建立与飞行器的连接',
    72:u'地图加载成功，可以进行下一步操作',
    73:u'确定清除路径设置？',

    201:u'路径设置成功',
    202:u'设置成功',
    203:u'路径设置失败，重新发送',
    204:u'路径设置失败，请检查参数',

    1001: u'起飞命令设置成功',
    1002: u'起飞命令设置失败，重新发送',
    2001: u'执行任务命令设置成功',
    2002: u'执行任务命令设置失败，重新发送',
    3001: u'终止任务命令设置成功',
    3002: u'终止任务命令设置失败，重新发送',
    4001: u'降落命令设置成功',
    4002: u'降落命令设置失败，重新发送',
    5001: u'返航命令设置成功',
    5002: u'返航命令设置失败，重新发送',

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


