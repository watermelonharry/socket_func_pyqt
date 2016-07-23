# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\Demo\ui\pick_point.ui'
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

class Ui_PickPoint(object):
    def setupUi(self, PickPoint):
        PickPoint.setObjectName(_fromUtf8("PickPoint"))
        PickPoint.resize(887, 632)
        PickPoint.setSizeGripEnabled(True)
        self.pp_webView = QtWebKit.QWebView(PickPoint)
        self.pp_webView.setGeometry(QtCore.QRect(0, 0, 891, 631))
        self.pp_webView.setUrl(QtCore.QUrl(_fromUtf8("file:///C:/local/pick_point_2.html")))
        self.pp_webView.setObjectName(_fromUtf8("pp_webView"))
        self.pp_testbrowser = QtGui.QTextBrowser(PickPoint)
        self.pp_testbrowser.setGeometry(QtCore.QRect(480, 510, 401, 121))
        self.pp_testbrowser.setObjectName(_fromUtf8("pp_testbrowser"))
        self.pp_button = QtGui.QPushButton(PickPoint)
        self.pp_button.setGeometry(QtCore.QRect(390, 600, 75, 23))
        self.pp_button.setObjectName(_fromUtf8("pp_button"))

        self.retranslateUi(PickPoint)
        QtCore.QMetaObject.connectSlotsByName(PickPoint)

    def retranslateUi(self, PickPoint):
        PickPoint.setWindowTitle(_translate("PickPoint", "Dialog", None))
        self.pp_button.setText(_translate("PickPoint", "get", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PickPoint = QtGui.QDialog()
    ui = Ui_PickPoint()
    ui.setupUi(PickPoint)
    PickPoint.show()
    sys.exit(app.exec_())

