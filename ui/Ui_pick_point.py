# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Harry\Documents\PyQtProjects\DemoSocket\socket_func_pyqt\ui\pick_point.ui'
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
        PickPoint.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        PickPoint.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        PickPoint.setSizeGripEnabled(True)
        self.pp_webView = QtWebKit.QWebView(PickPoint)
        self.pp_webView.setGeometry(QtCore.QRect(0, 0, 891, 631))
        self.pp_webView.setMouseTracking(True)
        self.pp_webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pp_webView.setUrl(QtCore.QUrl(_fromUtf8("file:///C:/local/pick_point_2.html")))
        self.pp_webView.setObjectName(_fromUtf8("pp_webView"))
        self.pp_testbrowser = QtGui.QTextBrowser(PickPoint)
        self.pp_testbrowser.setGeometry(QtCore.QRect(480, 510, 401, 121))
        self.pp_testbrowser.setObjectName(_fromUtf8("pp_testbrowser"))
        self.pick_send_btn = QtGui.QPushButton(PickPoint)
        self.pick_send_btn.setGeometry(QtCore.QRect(390, 510, 75, 23))
        self.pick_send_btn.setObjectName(_fromUtf8("pick_send_btn"))
        self.pick_clear_btn = QtGui.QPushButton(PickPoint)
        self.pick_clear_btn.setGeometry(QtCore.QRect(390, 540, 75, 23))
        self.pick_clear_btn.setObjectName(_fromUtf8("pick_clear_btn"))
        self.pick_refresh_btn = QtGui.QPushButton(PickPoint)
        self.pick_refresh_btn.setGeometry(QtCore.QRect(390, 570, 75, 23))
        self.pick_refresh_btn.setObjectName(_fromUtf8("pick_refresh_btn"))
        self.pick_path_btn = QtGui.QPushButton(PickPoint)
        self.pick_path_btn.setGeometry(QtCore.QRect(300, 510, 75, 23))
        self.pick_path_btn.setObjectName(_fromUtf8("pick_path_btn"))
        self.pick_obstacle_btn = QtGui.QPushButton(PickPoint)
        self.pick_obstacle_btn.setGeometry(QtCore.QRect(300, 540, 75, 23))
        self.pick_obstacle_btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.pick_obstacle_btn.setObjectName(_fromUtf8("pick_obstacle_btn"))

        self.retranslateUi(PickPoint)
        QtCore.QObject.connect(self.pick_refresh_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.pp_webView.reload)
        QtCore.QMetaObject.connectSlotsByName(PickPoint)

    def retranslateUi(self, PickPoint):
        PickPoint.setWindowTitle(_translate("PickPoint", "地图选点", None))
        self.pick_send_btn.setText(_translate("PickPoint", "确定", None))
        self.pick_clear_btn.setText(_translate("PickPoint", "清除", None))
        self.pick_refresh_btn.setText(_translate("PickPoint", "刷新", None))
        self.pick_path_btn.setText(_translate("PickPoint", "轨迹模式", None))
        self.pick_obstacle_btn.setText(_translate("PickPoint", "障碍模式", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PickPoint = QtGui.QDialog()
    ui = Ui_PickPoint()
    ui.setupUi(PickPoint)
    PickPoint.show()
    sys.exit(app.exec_())

