# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\DemoSocket\socket_func_pyqt\ui\socketUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SocketUi(object):
    def setupUi(self, SocketUi):
        SocketUi.setObjectName(_fromUtf8("SocketUi"))
        SocketUi.resize(807, 432)
        SocketUi.setSizeGripEnabled(True)
        self.sock_show_tb = QtGui.QTextBrowser(SocketUi)
        self.sock_show_tb.setGeometry(QtCore.QRect(140, 140, 451, 261))
        self.sock_show_tb.setObjectName(_fromUtf8("sock_show_tb"))
        self.sock_getip_btn = QtGui.QPushButton(SocketUi)
        self.sock_getip_btn.setGeometry(QtCore.QRect(30, 180, 75, 23))
        self.sock_getip_btn.setObjectName(_fromUtf8("sock_getip_btn"))
        self.sock_start_btn = QtGui.QPushButton(SocketUi)
        self.sock_start_btn.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.sock_start_btn.setObjectName(_fromUtf8("sock_start_btn"))
        self.label = QtGui.QLabel(SocketUi)
        self.label.setGeometry(QtCore.QRect(152, 26, 91, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.sock_tcp_rbtn = QtGui.QRadioButton(SocketUi)
        self.sock_tcp_rbtn.setGeometry(QtCore.QRect(450, 20, 89, 16))
        self.sock_tcp_rbtn.setChecked(True)
        self.sock_tcp_rbtn.setObjectName(_fromUtf8("sock_tcp_rbtn"))
        self.sock_udp_rbtn = QtGui.QRadioButton(SocketUi)
        self.sock_udp_rbtn.setEnabled(False)
        self.sock_udp_rbtn.setGeometry(QtCore.QRect(450, 40, 89, 16))
        self.sock_udp_rbtn.setObjectName(_fromUtf8("sock_udp_rbtn"))
        self.label_3 = QtGui.QLabel(SocketUi)
        self.label_3.setGeometry(QtCore.QRect(190, 100, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.sock_send_btn = QtGui.QPushButton(SocketUi)
        self.sock_send_btn.setGeometry(QtCore.QRect(110, 95, 75, 23))
        self.sock_send_btn.setObjectName(_fromUtf8("sock_send_btn"))
        self.sock_clear_btn = QtGui.QPushButton(SocketUi)
        self.sock_clear_btn.setGeometry(QtCore.QRect(30, 270, 75, 23))
        self.sock_clear_btn.setObjectName(_fromUtf8("sock_clear_btn"))
        self.sock_save_log_btn = QtGui.QPushButton(SocketUi)
        self.sock_save_log_btn.setEnabled(True)
        self.sock_save_log_btn.setGeometry(QtCore.QRect(30, 300, 75, 23))
        self.sock_save_log_btn.setCheckable(False)
        self.sock_save_log_btn.setObjectName(_fromUtf8("sock_save_log_btn"))
        self.sock_close_btn = QtGui.QPushButton(SocketUi)
        self.sock_close_btn.setGeometry(QtCore.QRect(30, 240, 75, 23))
        self.sock_close_btn.setObjectName(_fromUtf8("sock_close_btn"))
        self.sock_quit_btn = QtGui.QPushButton(SocketUi)
        self.sock_quit_btn.setGeometry(QtCore.QRect(30, 330, 75, 23))
        self.sock_quit_btn.setObjectName(_fromUtf8("sock_quit_btn"))
        self.sock_ip = QtGui.QLineEdit(SocketUi)
        self.sock_ip.setGeometry(QtCore.QRect(250, 20, 191, 31))
        self.sock_ip.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sock_ip.setObjectName(_fromUtf8("sock_ip"))
        self.sock_input_3 = QtGui.QLineEdit(SocketUi)
        self.sock_input_3.setGeometry(QtCore.QRect(220, 90, 371, 31))
        self.sock_input_3.setObjectName(_fromUtf8("sock_input_3"))

        self.retranslateUi(SocketUi)
        QtCore.QObject.connect(self.sock_quit_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), SocketUi.close)
        QtCore.QMetaObject.connectSlotsByName(SocketUi)

    def retranslateUi(self, SocketUi):
        SocketUi.setWindowTitle(_translate("SocketUi", "GPRS服务", None))
        self.sock_getip_btn.setText(_translate("SocketUi", "获取ip", None))
        self.sock_start_btn.setText(_translate("SocketUi", "开启服务", None))
        self.label.setText(_translate("SocketUi", "设定ip 端口:", None))
        self.sock_tcp_rbtn.setText(_translate("SocketUi", "TCP", None))
        self.sock_udp_rbtn.setText(_translate("SocketUi", "UDP", None))
        self.label_3.setText(_translate("SocketUi", "输入", None))
        self.sock_send_btn.setText(_translate("SocketUi", "发送", None))
        self.sock_clear_btn.setText(_translate("SocketUi", "clear", None))
        self.sock_save_log_btn.setText(_translate("SocketUi", "SQLLLL", None))
        self.sock_close_btn.setText(_translate("SocketUi", "关闭服务", None))
        self.sock_quit_btn.setText(_translate("SocketUi", "quit", None))
        self.sock_ip.setText(_translate("SocketUi", "10.180.61.89:9876", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SocketUi = QtGui.QDialog()
    ui = Ui_SocketUi()
    ui.setupUi(SocketUi)
    SocketUi.show()
    sys.exit(app.exec_())

