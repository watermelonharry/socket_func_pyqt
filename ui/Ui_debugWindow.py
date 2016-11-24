# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\socket_func_pyqt\ui/debugWindow.ui'
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

class Ui_debug_window(object):
    def setupUi(self, debug_window):
        debug_window.setObjectName(_fromUtf8("debug_window"))
        debug_window.resize(539, 430)
        debug_window.setSizeGripEnabled(True)
        self.groupBox = QtGui.QGroupBox(debug_window)
        self.groupBox.setGeometry(QtCore.QRect(17, 14, 501, 401))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.debug_text_browser = QtGui.QTextBrowser(self.groupBox)
        self.debug_text_browser.setGeometry(QtCore.QRect(20, 70, 461, 321))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.debug_text_browser.setFont(font)
        self.debug_text_browser.setObjectName(_fromUtf8("debug_text_browser"))
        self.debug_clear_btn = QtGui.QPushButton(self.groupBox)
        self.debug_clear_btn.setGeometry(QtCore.QRect(50, 30, 93, 28))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Microsoft YaHei UI"))
        self.debug_clear_btn.setFont(font)
        self.debug_clear_btn.setObjectName(_fromUtf8("debug_clear_btn"))

        self.retranslateUi(debug_window)
        QtCore.QMetaObject.connectSlotsByName(debug_window)

    def retranslateUi(self, debug_window):
        debug_window.setWindowTitle(_translate("debug_window", "调试信息", None))
        self.groupBox.setTitle(_translate("debug_window", "调试信息", None))
        self.debug_clear_btn.setText(_translate("debug_window", "清除", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    debug_window = QtGui.QDialog()
    ui = Ui_debug_window()
    ui.setupUi(debug_window)
    debug_window.show()
    sys.exit(app.exec_())

