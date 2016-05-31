# coding: utf-8
import sys
from PyQt4 import QtGui
from func.socketFunc import SocketFunc
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SocketFunc()
    myapp.show()
    sys.exit(app.exec_())
