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
        self.web_fresh_btn.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.web_fresh_btn.setObjectName(_fromUtf8("web_fresh_btn"))
        self.web_halt_btn = QtGui.QPushButton(yingyan_web)
        self.web_halt_btn.setGeometry(QtCore.QRect(100, 10, 75, 23))
        self.web_halt_btn.setObjectName(_fromUtf8("web_halt_btn"))

        self.retranslateUi(yingyan_web)
        QtCore.QObject.connect(self.web_fresh_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.reload)
        QtCore.QMetaObject.connectSlotsByName(yingyan_web)

    def retranslateUi(self, yingyan_web):
        yingyan_web.setWindowTitle(_translate("yingyan_web", "Dialog", None))
        self.web_fresh_btn.setText(_translate("yingyan_web", "刷新", None))
        self.web_halt_btn.setText(_translate("yingyan_web", "HALT 5s", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    yingyan_web = QtGui.QDialog()
    ui = Ui_yingyan_web()
    ui.setupUi(yingyan_web)
    yingyan_web.show()
    sys.exit(app.exec_())

