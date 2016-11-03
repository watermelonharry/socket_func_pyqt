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
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        yingyan_web.setFont(font)
        yingyan_web.setSizeGripEnabled(True)
        self.webView = QtWebKit.QWebView(yingyan_web)
        self.webView.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Agency FB"))
        self.webView.setFont(font)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.web_fresh_btn = QtGui.QPushButton(yingyan_web)
        self.web_fresh_btn.setGeometry(QtCore.QRect(50, 695, 75, 23))
        self.web_fresh_btn.setObjectName(_fromUtf8("web_fresh_btn"))
        self.web_emit_btn = QtGui.QPushButton(yingyan_web)
        self.web_emit_btn.setGeometry(QtCore.QRect(170, 695, 75, 23))
        self.web_emit_btn.setObjectName(_fromUtf8("web_emit_btn"))
        self.web_group_box = QtGui.QGroupBox(yingyan_web)
        self.web_group_box.setGeometry(QtCore.QRect(20, 550, 281, 141))
        self.web_group_box.setAutoFillBackground(True)
        self.web_group_box.setObjectName(_fromUtf8("web_group_box"))
        self.web_time_label = QtGui.QLabel(self.web_group_box)
        self.web_time_label.setGeometry(QtCore.QRect(80, 20, 100, 12))
        self.web_time_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.web_time_label.setObjectName(_fromUtf8("web_time_label"))
        self.web_const_time_label = QtGui.QLabel(self.web_group_box)
        self.web_const_time_label.setGeometry(QtCore.QRect(30, 20, 54, 12))
        self.web_const_time_label.setObjectName(_fromUtf8("web_const_time_label"))
        self.web_recdata_label = QtGui.QLabel(self.web_group_box)
        self.web_recdata_label.setGeometry(QtCore.QRect(30, 110, 171, 12))
        self.web_recdata_label.setObjectName(_fromUtf8("web_recdata_label"))
        self.label = QtGui.QLabel(self.web_group_box)
        self.label.setGeometry(QtCore.QRect(30, 40, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.web_group_box)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.web_group_box)
        self.label_3.setGeometry(QtCore.QRect(30, 80, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.web_longi_label = QtGui.QLabel(self.web_group_box)
        self.web_longi_label.setGeometry(QtCore.QRect(80, 40, 100, 12))
        self.web_longi_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.web_longi_label.setObjectName(_fromUtf8("web_longi_label"))
        self.web_lati_label = QtGui.QLabel(self.web_group_box)
        self.web_lati_label.setGeometry(QtCore.QRect(80, 60, 100, 12))
        self.web_lati_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.web_lati_label.setObjectName(_fromUtf8("web_lati_label"))
        self.web_altitu_label = QtGui.QLabel(self.web_group_box)
        self.web_altitu_label.setGeometry(QtCore.QRect(80, 80, 100, 12))
        self.web_altitu_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.web_altitu_label.setObjectName(_fromUtf8("web_altitu_label"))
        self.webView.raise_()
        self.web_group_box.raise_()
        self.web_fresh_btn.raise_()
        self.web_emit_btn.raise_()

        self.retranslateUi(yingyan_web)
        QtCore.QObject.connect(self.web_fresh_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webView.reload)
        QtCore.QMetaObject.connectSlotsByName(yingyan_web)

    def retranslateUi(self, yingyan_web):
        yingyan_web.setWindowTitle(_translate("yingyan_web", "轨迹监控", None))
        self.web_fresh_btn.setText(_translate("yingyan_web", "刷新", None))
        self.web_emit_btn.setText(_translate("yingyan_web", "emit", None))
        self.web_group_box.setTitle(_translate("yingyan_web", "DATA", None))
        self.web_time_label.setText(_translate("yingyan_web", "None", None))
        self.web_const_time_label.setText(_translate("yingyan_web", "TIME:", None))
        self.web_recdata_label.setText(_translate("yingyan_web", "received data", None))
        self.label.setText(_translate("yingyan_web", "LONGI:", None))
        self.label_2.setText(_translate("yingyan_web", "LATI:", None))
        self.label_3.setText(_translate("yingyan_web", "ALTIT:", None))
        self.web_longi_label.setText(_translate("yingyan_web", "None", None))
        self.web_lati_label.setText(_translate("yingyan_web", "None", None))
        self.web_altitu_label.setText(_translate("yingyan_web", "None", None))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    yingyan_web = QtGui.QDialog()
    ui = Ui_yingyan_web()
    ui.setupUi(yingyan_web)
    yingyan_web.show()
    sys.exit(app.exec_())

