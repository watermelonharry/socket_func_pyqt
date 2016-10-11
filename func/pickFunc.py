# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""

from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot
from PyQt4.QtGui import QDialog,  QMessageBox

from ui.Ui_pick_point import Ui_PickPoint


class PickPointfunc(QDialog, Ui_PickPoint):
    """
    Class documentation goes here.
    """
    js_signal = pyqtSignal(str)
    def __init__(self, parent=None,  upsignal = None,  downsignal = None, updateMainSignal = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.js_signal.connect(self.ShowInTab)
        self.points = []
        self.insignal = downsignal
        self.outsignal = upsignal
        self.updateMainSignal = updateMainSignal
        self.insignal.connect(self.ReiceveStrData)

        #存储已发送命令 用于验证发送成功
        self.orderDict={}
        
        self.pp_webView.page().mainFrame().addToJavaScriptWindowObject("js_buffer", self)
    
    @pyqtSignature("")
    def on_pp_testbrowser_textChanged(self):
        """
        Slot documentation goes here.
        """
    #must be a slot so the JS could call the function
    @pyqtSlot(str) 
    def ShowInTab(self, str_arg):
        self.pp_testbrowser.append(str_arg)
    
    @pyqtSlot(str)
    #input str_arg: longi-lati
    def add_one_point_js(self, str_arg):
        
        self.points.append(str_arg.split('-'))
        self.pp_testbrowser.append('point '+ str(len(self.points))+' added:'+str_arg)
    
    @pyqtSlot(str)
    #input str_arg: point number
    def delete_one_point_js(self, str_arg):
        
        delete_p = list(self.points.pop(len(self.points) -1))
        self.pp_testbrowser.append('point '+ str(len(self.points) +1)+' deleted:'+ str(delete_p[0]) + '-' + str(delete_p[1]))
        
    @pyqtSignature("")
    def on_pp_button_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        p = self.pp_webView.page().mainFrame().documentElement().findFirst('div[id=show_data]')
        self.js_signal.emit(p.toPlainText())
        
        #jstest
        jscript = """
        var count = markers.length;
        var pass_buffer = "";
	    for (var i = 0; i<markers.length ; i++){
			map.removeOverlay(markers[i]);
            pass_buffer += String(points[i].lng) + "|" +String(points[i].lat) + "=";
		}
		pass_buffer = String(markers.length) + "=" + pass_buffer
		markers = [];
        points = [];
        p_count = 1;
        
        js_buffer.receive_from_js(pass_buffer);
        """
        
        #self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript("""document.write("hello")""")
        self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)
    
    @pyqtSignature("bool")
    def on_pp_webView_loadFinished(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        #QMessageBox.about(self,u"success", "<loading map finished>\n<ready for next operation>")
        self.updateMainSignal.emit('Loading map done...')

    #test: receive message from yingyanFunc
    def ReiceveStrData(self,strArg):
        self.pp_testbrowser.append(strArg)

    @pyqtSlot(str)
    def receive_from_js(self, str_arg):
        """处理从JS传来的点，格式化后发送到socket.send"""
        self.ShowInTab(str_arg)
        self.ShowInTab(" added.")
        self.processPickData(str_arg[:-1])

    def processPickData(self, str_data):
        orderId = self.uniqueId()
        order = orderId + '=D=' + str_data +"="
        order += self.xorFormat(order)
        print(order)

        self.orderDict[orderId] = order
        self.outsignal.emit(order)

    def uniqueId(self):
        import datetime
        import time
        uniID = str(time.mktime(time.localtime()))[:-2] + str(datetime.datetime.now().microsecond / 1000)
        return str(uniID)

    def xorFormat(self, str_arg):
        return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))