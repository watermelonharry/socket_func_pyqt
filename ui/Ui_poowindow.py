# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\socket_func_pyqt\ui\poowindow.ui'
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

class Ui_notice_window(object):
    def setupUi(self, notice_window):
        notice_window.setObjectName(_fromUtf8("notice_window"))
        notice_window.resize(319, 119)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        notice_window.setFont(font)
        notice_window.setSizeGripEnabled(False)
        self.notice_content = QtGui.QLabel(notice_window)
        self.notice_content.setGeometry(QtCore.QRect(40, 20, 251, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.notice_content.setFont(font)
        self.notice_content.setAlignment(QtCore.Qt.AlignCenter)
        self.notice_content.setObjectName(_fromUtf8("notice_content"))
        self.notice_true_btn = QtGui.QPushButton(notice_window)
        self.notice_true_btn.setGeometry(QtCore.QRect(30, 70, 93, 28))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.notice_true_btn.setFont(font)
        self.notice_true_btn.setObjectName(_fromUtf8("notice_true_btn"))
        self.notice_cancel_btn = QtGui.QPushButton(notice_window)
        self.notice_cancel_btn.setEnabled(True)
        self.notice_cancel_btn.setGeometry(QtCore.QRect(200, 70, 93, 28))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.notice_cancel_btn.setFont(font)
        self.notice_cancel_btn.setObjectName(_fromUtf8("notice_cancel_btn"))

        self.retranslateUi(notice_window)
        QtCore.QMetaObject.connectSlotsByName(notice_window)

    def retranslateUi(self, notice_window):
        notice_window.setWindowTitle(_translate("notice_window", "提示", None))
        self.notice_content.setText(_translate("notice_window", "无", None))
        self.notice_true_btn.setText(_translate("notice_window", "确定", None))
        self.notice_cancel_btn.setText(_translate("notice_window", "取消", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    notice_window = QtGui.QDialog()
    ui = Ui_notice_window()
    ui.setupUi(notice_window)
    notice_window.show()
    sys.exit(app.exec_())

