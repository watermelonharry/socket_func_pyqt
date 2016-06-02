# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\DemoSocket\socket_func_pyqt\ui\yingyan_web.ui'
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

class Ui_yingyan_web(object):
    def setupUi(self, yingyan_web):
        yingyan_web.setObjectName(_fromUtf8("yingyan_web"))
        yingyan_web.resize(1280, 720)
        yingyan_web.setMinimumSize(QtCore.QSize(1280, 720))
        yingyan_web.setSizeGripEnabled(True)
        self.webView = QtWebKit.QWebView(yingyan_web)
        self.webView.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("https://passport.baidu.com/v2/?login&fr=old&login&u=http://yingyan.baidu.com/track.html?i=107208")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.web_fresh_btn = QtGui.QPushButton(yingyan_web)
        self.web_fresh_btn.setGeometry(QtCore.QRect(30, 500, 75, 23))
        self.web_fresh_btn.setObjectName(_fromUtf8("web_fresh_btn"))
        self.web_emit_btn = QtGui.QPushButton(yingyan_web)
        self.web_emit_btn.setGeometry(QtCore.QRect(120, 500, 75, 23))
        self.web_emit_btn.setObjectName(_fromUtf8("web_emit_btn"))
        self.web_group_box = QtGui.QGroupBox(yingyan_web)
        self.web_group_box.setGeometry(QtCore.QRect(20, 530, 211, 171))
        self.web_group_box.setAutoFillBackground(True)
        self.web_group_box.setObjectName(_fromUtf8("web_group_box"))
        self.web_time_label = QtGui.QLabel(self.web_group_box)
        self.web_time_label.setGeometry(QtCore.QRect(80, 35, 101, 20))
        self.web_time_label.setObjectName(_fromUtf8("web_time_label"))
        self.web_const_time_label = QtGui.QLabel(self.web_group_box)
        self.web_const_time_label.setGeometry(QtCore.QRect(30, 40, 54, 12))
        self.web_const_time_label.setObjectName(_fromUtf8("web_const_time_label"))
        self.web_test_label = QtGui.QLabel(self.web_group_box)
        self.web_test_label.setGeometry(QtCore.QRect(30, 80, 54, 12))
        self.web_test_label.setObjectName(_fromUtf8("web_test_label"))

        self.retranslateUi(yingyan_web)
        QtCore.QObject.connect(self.web_fresh_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.reload)
        QtCore.QMetaObject.connectSlotsByName(yingyan_web)

    def retranslateUi(self, yingyan_web):
        yingyan_web.setWindowTitle(_translate("yingyan_web", "Dialog", None))
        self.web_fresh_btn.setText(_translate("yingyan_web", "刷新", None))
        self.web_emit_btn.setText(_translate("yingyan_web", "emit", None))
        self.web_group_box.setTitle(_translate("yingyan_web", "DATA", None))
        self.web_time_label.setText(_translate("yingyan_web", "None", None))
        self.web_const_time_label.setText(_translate("yingyan_web", "TIME:", None))
        self.web_test_label.setText(_translate("yingyan_web", "FOR TEST", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    yingyan_web = QtGui.QDialog()
    ui = Ui_yingyan_web()
    ui.setupUi(yingyan_web)
    yingyan_web.show()
    sys.exit(app.exec_())

