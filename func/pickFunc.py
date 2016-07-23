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
    def __init__(self, parent=None,  upsignal = None,  downsignal = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.js_signal.connect(self.add_test)
        self.points = []
        self.insignal = downsignal
        self.outsignal = upsignal
        
        self.pp_webView.page().mainFrame().addToJavaScriptWindowObject("js_buffer", self)
    
    @pyqtSignature("")
    def on_pp_testbrowser_textChanged(self):
        """
        Slot documentation goes here.
        """
    #must be a slot so the JS could call the function
    @pyqtSlot(str) 
    def add_test(self, str_arg):
        self.pp_testbrowser.append(str_arg)
    
    @pyqtSlot(str)
    def receive_from_js(self, str_arg):
        
        self.add_test(str_arg)
        self.add_test(" added.")
        self.outsignal.emit(str_arg)
    
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
	    for (var i = 0; i<markers.length -1; i++){
			map.removeOverlay(markers[i]);
            pass_buffer += String(points[i].lng) + "-" +String(points[i].lat) + "|";
		}
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
        self.outsignal.emit('Loading map done...')
