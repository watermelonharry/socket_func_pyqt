# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""
from Voronoi.Voronoi import Voronoi
from Voronoi import dijkstra
from package.rectangular import Rectangular

from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4 import QtCore
_fromUtf8 = QtCore.QString.fromUtf8

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
        self.lines = None
        #输入信号
        self.toPickPointSignal = downsignal
        #输出信号
        self.fromPickPointSignal = upsignal
        #更新显示
        self.updateMainSignal = updateMainSignal
        self.toPickPointSignal.connect(self.ReiceveStrData)

        #存储已发送命令 用于验证发送成功
        self.orderDict={}
        self.WAITFLAG = False
        import os
        self.pp_webView.setUrl(
            QtCore.QUrl(_fromUtf8("file:///" + '/'.join(os.getcwd().split('\\')) + "/websrc/pick_point_2.html")))

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
        
        # self.points.append(str_arg.split('-'))
        self.pp_testbrowser.append('point added:'+str_arg)
    
    # @pyqtSlot(str)
    # #input str_arg: point number
    # def delete_one_point_js(self, str_arg):
    #
    #     delete_p = list(self.points.pop(len(self.points) -1))
    #     self.pp_testbrowser.append('point '+ str(len(self.points) +1)+' deleted:'+ str(delete_p[0]) + '-' + str(delete_p[1]))
        
    @pyqtSignature("")
    def on_pick_send_btn_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # p = self.pp_webView.page().mainFrame().documentElement().findFirst('div[id=show_data]')
        # self.js_signal.emit(p.toPlainText())
        
        #jstest
        jscript = """
        var count = markers.length;
        var pass_buffer = "";
	    for (var i = 0; i<markers.length ; i++){
			//map.removeOverlay(markers[i]);
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

    @pyqtSignature("")
    def on_pick_clear_btn_clicked(self):
        """
        清除按钮
        删除已选点 路径记录 地图显示记录
        :return:
        """
        self.pp_testbrowser.clear()
        self.WAITFLAG = False
        self.points = []
        self.lines = None

        jscript = """
        	    map.clearOverlays();
        		markers = [];
                points = [];
                p_count = 1;
                var lineMarkers = []; //路径集合
	            var linePoints = []; //路径点集合
                """
        # self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript("""document.write("hello")""")
        self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)

    @pyqtSignature("")
    def on_pick_path_btn_clicked(self):
        """
        轨迹模式按钮
        :return:
        """
        #TODO 暂时用于测试voronoi路径
        rec = Rectangular(lineList=self.lines, startPoint=self.points[0], endPoint=self.points[1])
        rec.process()
        self.lines = rec.output()


        try:
            lineData = '='.join(['|'.join(str(t) for t in x) for x in self.lines])
        except Exception as e:
            print(e.message)
        jscript = """
                var lineMarkers = [];
                var lineData = "%s";
                var lineList = lineData.split("=");
                //document.write(lineData + "<br />");
                //document.write(lineList[0] + "<br />");

                for (var i = 0; i<lineList.length ; i++){
        			var lines = lineList[i].split("|");
        			var polyline = new BMap.Polyline([
        		    new BMap.Point(parseFloat(lines[0]), parseFloat(lines[1])),
        		    new BMap.Point(parseFloat(lines[2]), parseFloat(lines[3])),
        	], {strokeColor:"red", strokeWeight:2, strokeOpacity:0.5});   //创建折线

        	        map.addOverlay(polyline);   //增加折线
        		}

        	    """ % lineData
        self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)

        pass

    @pyqtSignature("")
    def on_pick_obstacle_btn_clicked(self):
        """
        障碍模式按钮
        :return:
        """
        #TODO 暂时用于测试dijikstra路径
        dijktraPath = dijkstra.GetPath(self.lines, self.points[0], self.points[1])
        self.lines = dijktraPath

        try:
            lineData = '='.join(['|'.join(str(t) for t in x) for x in self.lines])
        except Exception as e:
            print(e.message)
        jscript = """
                    var lineMarkers = [];
                    var lineData = "%s";
                    var lineList = lineData.split("=");
                    //document.write(lineData + "<br />");
                    //document.write(lineList[0] + "<br />");

                    for (var i = 0; i<lineList.length ; i++){
            			var lines = lineList[i].split("|");
            			var polyline = new BMap.Polyline([
            		    new BMap.Point(parseFloat(lines[0]), parseFloat(lines[1])),
            		    new BMap.Point(parseFloat(lines[2]), parseFloat(lines[3])),
            	], {strokeColor:"white", strokeWeight:2, strokeOpacity:0.5});   //创建折线

            	        map.addOverlay(polyline);   //增加折线
            		}

            	    """ % lineData
        self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)

        pass

    @pyqtSignature("")
    def on_pick_showPath_btn_clicked(self):
        """
        生成轨迹按钮
        :return:
        """
        try:
            lineData = '='.join(['|'.join(str(t) for t in x) for x in self.lines])
        except Exception as e:
            print(e.message)
        jscript = """
        var lineMarkers = [];
        var lineData = "%s";
        var lineList = lineData.split("=");
        //document.write(lineData + "<br />");
        //document.write(lineList[0] + "<br />");

        for (var i = 0; i<lineList.length ; i++){
			var lines = lineList[i].split("|");
			var polyline = new BMap.Polyline([
		    new BMap.Point(parseFloat(lines[0]), parseFloat(lines[1])),
		    new BMap.Point(parseFloat(lines[2]), parseFloat(lines[3])),
	], {strokeColor:"yellow", strokeWeight:2, strokeOpacity:0.5});   //创建折线

	        map.addOverlay(polyline);   //增加折线
		}

	    """%lineData
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

    def ClearMapCovers(self):
        self.on_pick_clear_btn_clicked()


    #test: receive message from yingyanFunc
    def ReiceveStrData(self,strArg):
        # self.ShowInTab(strArg)
        if self.WAITFLAG is True:
            data = strArg.split('=')
            if data[2]=='Y':
                self.ShowInTab('send success.')
                self.WAITFLAG = False
                self.points = []
                self.lines = None
                #test
                self.updateMainSignal.emit('pickpiont from yingyan:' + str(strArg))
                self.ClearMapCovers()

    @pyqtSlot(str)
    def receive_from_js(self, str_arg):
        """处理从JS传来的点，格式化后发送到socket.send"""
        if self.WAITFLAG is False:
            self.ShowInTab(str_arg)
            self.ShowInTab(" added.")
            self.processPickData(str_arg[:-1])
            self.WAITFLAG = True
        else:
            self.ShowInTab('data sending, please wait...')


    def processPickData(self, str_data):
        orderId = self.uniqueId()

        for pointTuple in str_data.split('=')[1:]:
            plist = pointTuple.split('|')
            plongi,plati = float(plist[0]), float(plist[1])
            self.points.append((plongi,plati))

        vp = Voronoi(self.points[:])
        vp.process()
        self.lines = vp.getOutput()
        # rec = Rectangular(lineList= self.lines, startPoint =self.points[0],endPoint= self.points[1])
        # rec.process()
        # self.lines = rec.output()


        order = orderId + '=D=' + str_data +"="
        order += self.xorFormat(order)
        print(order)

        self.orderDict[orderId] = order
        self.fromPickPointSignal.emit(order)

    def uniqueId(self):
        import datetime
        import time
        uniID = str(time.mktime(time.localtime()))[:-2] + str(datetime.datetime.now().microsecond / 1000)
        return str(uniID)

    def xorFormat(self, str_arg):
        return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))