# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""
from PyQt4 import QtGui

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
    def __init__(self, parent=None,  upsignal = None,  downsignal = None, updateMainSignal = None, sendOrderSignal = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.js_signal.connect(self.ShowInTab)
        self.points = []
        self.lines = []
        self.pathPoints = []
        #输入信号
        self.toPickPointSignal = downsignal
        #输出信号
        self.fromPickPointSignal = upsignal
        #更新显示
        self.updateMainSignal = updateMainSignal
        self.toPickPointSignal.connect(self.ReiceveStrData)
        #发送socket命令
        self.sendOrderSignal = sendOrderSignal

        #存储已发送命令 用于验证发送成功
        self.orderDict={}
        import os
        self.pp_webView.setUrl(
            QtCore.QUrl(_fromUtf8("file:///" + '/'.join(os.getcwd().split('\\')) + "/websrc/pick_point_2.html")))

        self.pp_webView.page().mainFrame().addToJavaScriptWindowObject("js_buffer", self)

        self.STEP = STEP_START

        # 存储当前位置
        self.currentLoc = None



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
                order = orderId + '=D=' + str(len(self.pathPoints)) + '='
                order += '='.join([str(p[0]) + '|' + str(p[1]) for p in self.pathPoints]) + '='
                order += self.xorFormat(order)

                print(order)

                #加入字典
                self.orderDict[orderId] = order
                self.SendOrder(order)
                #改变状态
                self.STEP = STEP_SEND_WAIT
                self.ShowInTab('<sending path data:orderId-'+ str(orderId)+'>')

            else:
                self.ShowInTab('<error: not enough points>')
        else:
            self.ShowInTab('<error: wrong step>')

    def SendOrder(self,strArg):
        self.sendOrderSignal.emit(strArg)


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
        self.pathPoints = []
        self.lines = []
        self.orderDict = {}
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
        按照 起点-轨迹点-终点 生成轨迹
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
                self.pathPoints = tempPoints

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
        按照计算路径运行
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
            self.pathPoints = [(x[0],x[1]) for x in self.lines]
            self.pathPoints.append(self.lines[-1][2:])

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
    def on_pick_curLoc_btn_clicked(self):
        """
        显示当前坐标
        :return:
        """
        if self.currentLoc is not None:
            try:
                bdPoint = self.GtoB(self.currentLoc[0], self.currentLoc[1])
            except Exception as e:
                print('error in pickFunc.curLoc_btn:',e.message)


            if bdPoint is not None:
                jscript = """

                map.removeOverlay(curLocMarkers[0]);
                curLocMarkers.pop();

                var curPoint = new BMap.Point(%s);
                map.centerAndZoom(curPoint, 15);
                curmarker = new BMap.Marker(curPoint);  // 创建标注
                map.addOverlay(curmarker);               // 将标注添加到地图中
                curLocMarkers.push(curmarker);
                curmarker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画

                """ %','.join(bdPoint)
                self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)
        else:
            QtGui.QMessageBox.about(self, u'错误提示', u'未收到当前坐标信息。')

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


    #test: receive message from yingyanFunc
    def ReiceveStrData(self,strArg):
        strArg = str(strArg)
        # 内部数据收发处理
        try:
            innerData = strArg.split('=')
            if innerData[0] == 'IN':
                if innerData[1] == 'YY' and innerData[2] == 'LOC':
                    self.currentLoc = (innerData[3],innerData[4])
        except Exception as e:
            print('error in ReiceveStrData.innerData:',e.message)

        # 外部操作
        if self.STEP is STEP_SEND_WAIT:

            if self.xorFormat(strArg[:-1]) is strArg[-1]:
                data = strArg.split('=')
                orderId = data[0]

                if data[1]=='DY':
                    try:
                        # 从命令集合中删除
                        self.orderDict.pop(orderId)
                        self.ShowInTab('<send success: orderId-' + str(orderId) + '>')
                        QtGui.QMessageBox.about(self, u'发送成功', u'路径设置成功')
                    except Exception as e:
                        print('e10001')

                    #清空历史数据
                    self.STEP = STEP_START
                    self.points = []
                    self.lines = []
                    self.pathPoints = []
                    # #test
                    self.updateMainSignal.emit('pickpiont from yingyan:' + str(strArg))

                    #清除地图数据
                    self.ClearMapCovers()

                elif data[1] == 'DN':
                    #todo:设置失败
                    self.SendOrder(self.orderDict[orderId])

                elif data[1] == 'DE':
                    #todo:参数错误
                    self.ShowInTab('<error: points info error, please reset points>')
                    QtGui.QMessageBox.about(self, u'设置失败', u'路径设置失败，请检查参数。')

            else:
                #todo：返回命令校验未通过
                pass
        else:
            #todo:错误状态
            pass

    @pyqtSlot(str)
    def receive_from_js(self, str_arg):
        pass


    def processPickData(self, str_data):
        pass

    def uniqueId(self):
        """
        生成基于当前unix时间戳的唯一ID
        :return: str(unique id)
        """
        import datetime
        import time
        uniID = str(time.mktime(time.localtime()))[:-2] + str(datetime.datetime.now().microsecond / 1000)
        return str(uniID)

    def xorFormat(self, str_arg):
        """
        计算给定str的字节异或值
        :param str_arg:
        :return: char
        """
        return str(reduce(lambda x, y: chr(ord(x) ^ ord(y)), list(str(str_arg))))

    def GtoB(self, G_lon, G_lat):
        """
        GPS坐标转换为百度坐标
        基于webAPI:http://lbsyun.baidu.com/index.php?title=webapi/guide/changeposition
        :param G_lon: GPS经度
        :param G_lat: GPS纬度
        :return: (百度经度,百度纬度) 或 None
        """
        try:
            import json
            import requests
            url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=1&to=5&ak=znRegmlIFbPc0LHl1IUUnQju' % (str(G_lon), str(G_lat))
            source_code = requests.get(url)
            plain_text = source_code.text
            c = json.loads(plain_text)
            if c['status'] == 0:
                return (str(c['result'][0]['x']),str(c['result'][0]['y']))  # lat,lon in string type
            else:
                return None
        except Exception as e:
            print('error in GtoB:', e.message)
            return None