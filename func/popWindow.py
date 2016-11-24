# -*- coding: utf-8 -*-

from ui.Ui_poowindow import Ui_notice_window
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop

noticeDict= {
    0:u'无提示信息',
    1:u'确定起飞？',
    2:u'确定执行任务？',
    3:u'确定终止任务？',
    4:u'确定降落？',
    5:u'确定返航？',
    6:u'提示6',

    #错误提示

    10:u'飞行器未处于等待状态，\n添加的点无效',
    11:u'飞行器轨迹点未设置，\n请先设置轨迹点',
    12:u'无法设置\n正在等待飞行器状态更新',
    13:u'路径已经设置\n如需再设置请重置',
    2101:u'飞行器未处于起飞/终止任务状态，\n无法进行开始操作',
    3101:u'飞行器未处于执行任务状态，\n无法终止任务',
    4101:u'飞行器未起飞/完成任务/返航状态，\n无法进行降落操作',
    5101:u'飞行器未处于终止/完成任务/降落状态，\n无法进行返航操作',

    21:u'正在等待上一条命令设置完成',
    22:u'选取点不足，请重新选择',
    23:u'设置点步骤错误',
    24:u'计算的路径点不足，请重新设置',
    25:u'确认重新发送上一条命令？',
    26:u'上一条命令设置成功，\n无需重复发送',
    27:u'确认清除上一条命令？\n清除后需要重新设置',

    31:u'server未运行，无法停止',
    32:u'server正在运行\n请勿重复操作',

    71:u'错误：未收到当前坐标信息，\n请建立与飞行器的连接',
    72:u'地图加载成功，可以进行下一步操作',
    73:u'确定清除路径设置？',

    201:u'路径设置成功\n如需设置新路径请重置后再选取点',
    202:u'设置成功',
    203:u'路径设置失败，重新发送',
    204:u'路径设置失败，请检查参数',
    205:u'参数设置失败，\n请确认飞行器处于等待状态',
    206:u'确认设置高度和速度？',
    207:u'请输入正确的高度和速度数值',

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
    6001: u'飞行器参数设置成功',
    6002: u'飞行器参数设置失败，\n重新发送？',
    6003: u'飞行器参数设置错误，\n请重置后重新设置',
    6004: u'飞行器参数查询失败，\n重新查询',
    6005: u'飞行器参数查询成功',

}

class NoticeWindow(QDialog, Ui_notice_window):
    def __init__(self,intArg = 0):
        QDialog.__init__(self)
        self.setupUi(self)
        self.notice_content.setText(noticeDict[intArg])
        self.status = False

    def show(self, intArg = 0):
        self.notice_content.setText(noticeDict[intArg])
        QDialog.show(self)

    def exec_(self, intArg = 0):
        self.notice_content.setText(noticeDict[intArg])
        self.status = False
        QDialog.exec_(self)


    def Confirm(self, intArg = 0):
        self.exec_(intArg)

    @pyqtSignature("")
    def on_notice_true_btn_clicked(self):
        self.status = True
        self.close()

    @pyqtSignature("")
    def on_notice_cancel_btn_clicked(self):
        self.status = False
        self.close()


