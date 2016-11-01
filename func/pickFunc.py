# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""
from Voronoi.Voronoi import Voronoi
from Voronoi import dijkstra
from package.rectangular import Rectangular
import copy

from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4 import QtCore
_fromUtf8 = QtCore.QString.fromUtf8

from ui.Ui_pick_point import Ui_PickPoint

STEP_START = 1
STEP_GET_POINT =2
STEP_SEND_WAIT = 3
STEP_SEND_FAIL = 4

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

        self.STEP = STEP_START



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
        if self.STEP is STEP_START:
            self.ShowInTab('point added:'+str_arg)

            self.points.append(tuple(float(x) for x in str_arg.split('|')))
        else:
            self.ShowInTab('<error:waiting for former progress to be finished>')
    
    # @pyqtSlot(str)
    # #input str_arg: point number
    # def delete_one_point_js(self, str_arg):
    #
    #     delete_p = list(self.points.pop(len(self.points) -1))
    #     self.ShowInTab('point '+ str(len(self.points) +1)+' deleted:'+ str(delete_p[0]) + '-' + str(delete_p[1]))
        
    @pyqtSignature("")
    def on_pick_send_btn_clicked(self):
        """
        确定按钮，按下后发送轨迹命令,等待接收飞行器回复
        要求当前状态处于 STEP_GET_POINT
        完成后属性变为 STEP_SEND_WAIT

        """

        if self.STEP is STEP_GET_POINT:
            if len(self.lines) >= 1:
                #TODO：生成、发送命令

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


            else:
                self.ShowInTab('<error: not enough points>')
        else:
            self.ShowInTab('<error: wrong step>')



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
        self.STEP = STEP_START

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
        要求当前状态处于 STEP_START
        完成后属性变为 STEP_GET_POINT
        :return:
        """
        if self.STEP is STEP_START:
            if len(self.points) >2:
                #处理轨迹点
                tempPoints = copy.deepcopy(self.points)
                tempPoints = tempPoints[0:1] + tempPoints[2:] + tempPoints[1:2]

                #生成路径
                self.lines = map(lambda x:x[0]+x[1], zip(tempPoints[:-1],tempPoints[1:]))

                #改变步骤状态
                self.STEP = STEP_GET_POINT

                #路径显示
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


            else:
                self.ShowInTab('<error: not enough points')


        else:
            self.ShowInTab('<error: wrong step>')


    @pyqtSignature("")
    def on_pick_obstacle_btn_clicked(self):
        """
        障碍模式按钮
        起点-终点-障碍点
        要求当前状态处于 STEP_START
        完成后属性变为 STEP_GET_POINT
        :return:
        """


        if self.STEP is STEP_START and len(self.points) >2:
            self.ShowInTab('<calculating>')
            #计算维诺图
            vp = Voronoi(self.points[:])
            vp.process()
            self.lines = vp.getOutput()

            #路径初筛
            rec = Rectangular(lineList=self.lines, startPoint=self.points[0], endPoint=self.points[1])
            rec.process()
            self.lines = rec.output()

            #dijkstra筛选
            self.lines = dijkstra.GetPath(self.lines, self.points[0], self.points[1])

            #改变步骤状态
            self.STEP = STEP_GET_POINT

            #显示到地图
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
        elif len(self.points) <=2:
            self.ShowInTab('<error: not enough points>')
        elif self.STEP is not STEP_START:
            self.ShowInTab('<error: wrong step>')
        else:
            self.ShowInTab('<error: something wrong>')


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
        # """处理从JS传来的点，格式化后发送到socket.send"""
        # if self.WAITFLAG is False:
        #     self.ShowInTab(str_arg)
        #     self.ShowInTab(" added.")
        #     self.processPickData(str_arg[:-1])
        #     self.WAITFLAG = True
        # else:
        #     self.ShowInTab('data sending, please wait...')
        pass


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
