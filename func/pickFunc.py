# -*- coding: utf-8 -*-

"""
Module implementing PickPoint_func.
"""
from PyQt4 import QtGui

from Voronoi.Voronoi import Voronoi
from Voronoi import dijkstra
from package.rectangular import Rectangular
import copy

from PyQt4.QtCore import pyqtSignature,  pyqtSignal,  pyqtSlot, QEventLoop
from PyQt4.QtGui import QDialog,  QMessageBox
from PyQt4 import QtCore
_fromUtf8 = QtCore.QString.fromUtf8

from ui.Ui_pick_point import Ui_PickPoint
from popWindow import NoticeWindow
from package.planeStatus import STATUS_DICT,PlaneStatus,PlaneControl

STEP_START = 1
STEP_GET_POINT =2
STEP_SEND_WAIT = 3
STEP_SEND_FIN = 4
STEP_SEND_FAIL = 5

planeStatus = PlaneStatus()
planeControl = PlaneControl()


class PickPointfunc(QDialog, Ui_PickPoint):
    """
    Class documentation goes here.
    """


    js_signal = pyqtSignal(str)
    def __init__(self, parent=None,  upsignal = None,  downsignal = None, updateMainSignal = None, sendOrderSignal = None, toDebugWindowSingal = None):
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
        #发送到debug窗口
        self.toDebugWindowSingal = toDebugWindowSingal

        #存储已发送命令 用于验证发送成功
        self.orderDict={}
        # import os
        # self.pp_webView.setUrl(
        #     QtCore.QUrl(_fromUtf8("file:///" + '/'.join(os.getcwd().split('\\')) + "/websrc/pick_point_2.html")))

        self.pp_webView.page().mainFrame().addToJavaScriptWindowObject("js_buffer", self)

        ##设置点的步骤
        self.ORDER_STEP = STEP_START
        ##飞行器的状态
        self.PLANE_STATUS = None

        # 存储当前位置
        self.currentLoc = None
        self.curBdLoc = None



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
    def ConfirmByJs(self, strArg):
        self.Confirm(13)

    @pyqtSlot(str)
    #input str_arg: longi-lati
    def add_one_point_js(self, str_arg):


        #todo: debug 时注意
        if self.PLANE_STATUS is planeStatus.WAIT:
            if self.ORDER_STEP is STEP_START:
                self.ShowInTab('point added:'+str_arg)

                self.points.append(tuple(float(x) for x in str_arg.split('|')))
            else:
                self.ShowInTab('<error:waiting for former progress to be finished>')
                self.Confirm(21)
        elif self.PLANE_STATUS is not None:
            self.Confirm(10)
        else:
            self.Confirm(12)

    
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
        if self.PLANE_STATUS is planeStatus.WAIT:
            if self.ORDER_STEP is STEP_GET_POINT:
                if len(self.lines) >= 1:
                    #TODO：生成、发送命令

                    orderId = self.uniqueId()
                    orderContent = 'Z=D=' + str(len(self.pathPoints)) + '='
                    orderContent += '='.join([str(p[0]) + '|' + str(p[1]) for p in self.CalculatePoints(self.pathPoints)])

                    #加入字典
                    self.RecordOrder(orderId, orderContent)
                    self.SendOrder(id = orderId, content= orderContent)
                    #改变状态
                    self.ORDER_STEP = STEP_SEND_WAIT
                    self.ShowInTab('<sending path data:orderId-'+ str(orderId)+'>')

                else:
                    self.ShowInTab('<error: not enough points>')
                    self.Confirm(24)
            elif self.ORDER_STEP is STEP_SEND_WAIT:
                self.ShowInTab('<error: wrong step>')
                self.Confirm(21)
            elif self.ORDER_STEP is STEP_START:
                self.ShowInTab(u'<error: 步骤错误>')
                self.Confirm(11)
        else:
            self.Confirm(10)

    @pyqtSignature("")
    def on_pick_resend_btn_clicked(self):
        """
        重新发送
        :return:
        """
        if self.Confirm(25) is True:
            if len(self.orderDict) > 0:
                for k,v in self.orderDict.items():
                    self.SendOrder(id=k, content=v)
            else:
                self.Confirm(26)
        else:
            pass

    @pyqtSignature("")
    def on_pick_reset_order_btn_clicked(self):
        """
        清除上一条命令
        :return:
        """
        if self.Confirm(27) is True:
            self.ORDER_STEP = STEP_START
            self.orderDict = {}

    def CalculatePoints(self, pointsList):
        """
        输入路径点，输出差值
        :param pointsList:
        :return:
        """
        resultList = []
        if self.curBdLoc is not None:
            formerPoint = self.curBdLoc
            for singlePoint in pointsList:
                cLongi = 1000000.0 * (float(singlePoint[0]) - float(formerPoint[0]))
                clati = 1000000.0 * (float(singlePoint[1]) - float(formerPoint[1]))
                formerPoint = singlePoint
                resultList.append((str(cLongi), str(clati)))
        if len(resultList) > 0 :
            return resultList
        else:
            print('error in pickFunc-CalculatePoint: not enough points')
            QtGui.QMessageBox.about(self, u'错误', u'计算失败，路径点不足')
            return None


    def SendOrder(self,id=None, content=None):
        """
        发送数据至socket client
        :param id: 命令的唯一标志
        :param content: 命令的内容
        :return:
        """
        orderStr = '='.join([str(id), str(content)]) + '='
        orderStr += self.xorFormat(orderStr)
        print(orderStr)
        self.sendOrderSignal.emit(orderStr)


    @pyqtSignature("")
    def on_pick_clear_btn_clicked(self):
        """
        清除按钮
        删除已选点 路径记录 地图显示记录
        :return:
        """
        if self.Confirm(73) is True:
            self.pp_testbrowser.clear()
            self.WAITFLAG = False
            self.points = []
            self.pathPoints = []
            self.lines = []
            self.orderDict = {}
            self.ORDER_STEP = STEP_START
            self.PLANE_STATUS = planeStatus.WAIT

            jscript = """
                    map.clearOverlays();
                    markers = [];
                    points = [];
                    p_count = 1;
                    var lineMarkers = []; //路径集合
                    var linePoints = []; //路径点集合
                    SET_FLAG = 1;
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
        if self.PLANE_STATUS is planeStatus.WAIT:
            if self.ORDER_STEP is STEP_START:
                if len(self.points) >2:
                    #处理轨迹点
                    tempPoints = copy.deepcopy(self.points)
                    tempPoints = tempPoints[0:1] + tempPoints[2:] + tempPoints[1:2]

                    #生成路径
                    self.lines = map(lambda x:x[0]+x[1], zip(tempPoints[:-1],tempPoints[1:]))
                    self.pathPoints = tempPoints

                    #改变步骤状态
                    self.ORDER_STEP = STEP_GET_POINT

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
                            SET_FLAG = 0;

                            """ % lineData
                    self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)


                else:
                    self.ShowInTab('<error: not enough points')
                    self.Confirm(22)


            else:
                self.ShowInTab('<error: wrong step>')
                self.Confirm(23)
        else:
            self.Confirm(11)


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

        if self.PLANE_STATUS is planeStatus.WAIT:
            if self.ORDER_STEP is STEP_START and len(self.points) >2:
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
                self.ORDER_STEP = STEP_GET_POINT

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
                            SET_FLAG = 0;

                            """ % lineData
                self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)
            elif len(self.points) <=2:
                self.ShowInTab('<error: not enough points>')
                self.Confirm(22)
            elif self.ORDER_STEP is not STEP_START:
                self.ShowInTab('<error: wrong step>')
                self.Confirm(23)
            else:
                self.ShowInTab('<error: something wrong>')
        else:
            self.Confirm(11)

    @pyqtSignature("")
    def on_pick_curLoc_btn_clicked(self):
        """
        显示当前坐标
        :return:
        """
        if self.currentLoc is not None:
            try:
                self.curBdLoc = self.GtoB(self.currentLoc[0], self.currentLoc[1])
            except Exception as e:
                print('error in pickFunc.curLoc_btn:',e.message)
                self.curBdLoc = None


            if self.curBdLoc is not None:
                jscript = """

                map.removeOverlay(curLocMarkers[0]);
                curLocMarkers.pop();

                var curPoint = new BMap.Point(%s);
                map.centerAndZoom(curPoint, 19);
                curmarker = new BMap.Marker(curPoint);  // 创建标注
                map.addOverlay(curmarker);               // 将标注添加到地图中
                curLocMarkers.push(curmarker);
                curmarker.setAnimation(BMAP_ANIMATION_BOUNCE); //跳动的动画

                """ %','.join(self.curBdLoc)
                self.pp_webView.page().mainFrame().documentElement().evaluateJavaScript(jscript)
        else:
            self.Confirm(71)

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
        self.Confirm(72)

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
        """
        槽函数，处理接收数据
        :param strArg:
        :return:
        """
        strArg = str(strArg)
        # 内部数据收发处理
        try:
            innerData = strArg.split('=')
            if innerData[0] == 'IN':
                if innerData[1] == 'YY' and innerData[2] == 'LOC':
                    self.currentLoc = (innerData[3],innerData[4])
                    self.PLANE_STATUS = int(innerData[5])
                    self.pick_status_label.setText(STATUS_DICT[self.PLANE_STATUS])
                if innerData[2] == 'T':
                    self.SendToDebugWindow(innerData[3])
        except Exception as e:
            print('error in ReiceveStrData.innerData:',e.message)

        # 外部数据收发操作
        if self.ORDER_STEP is STEP_SEND_WAIT:

            #校验通过
            if self.xorFormat(strArg[:-1]) == strArg[-1]:
                data = strArg.split('=')
                data = data[:1] + data[2:]
                orderId = data[0]
                #todo：加入其他命令
                #确认接收的命令在字典中
                if orderId in self.orderDict:
                    #3.2 设置路径命令回复
                    if data[1]=='D':
                        if data[2] == 'Y':
                            if self.RemoveOrder(orderId) is True:
                                self.Confirm(201)

                                #清空历史数据
                                self.ORDER_STEP = STEP_START
                                self.points = []
                                self.lines = []
                                self.pathPoints = []
                                # #test
                                # self.updateMainSignal.emit('pickpiont from yingyan:' + str(strArg))

                                #清除地图数据
                                # self.ClearMapCovers()
                        if data[2] == 'N':
                            if self.Confirm(203) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                            else:
                                ##不重新发送
                                pass

                        if data[2] == 'E':
                            #todo:参数错误
                            self.ShowInTab('<error: points info error, please reset points>')
                            self.Confirm(204)
                    #5 控制命令回复
                    if data[1] == 'C':
                        #起飞
                        if data[2] == '1' and data[3] == 'Y':
                            self.Confirm(1001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == '1' and data[3] == 'N':
                            if self.Confirm(1002) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                            else:
                                pass
                        #执行任务
                        if data[2] == '2' and data[3] == 'Y':
                            self.Confirm(2001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == '2' and data[3] == 'N':
                            if self.Confirm(2002) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                        #终止任务
                        if data[2] == '3' and data[3] == 'Y':
                            self.Confirm(3001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == '3' and data[3] == 'N':
                            if self.Confirm(3002) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                        #降落
                        if data[2] == '4' and data[3] == 'Y':
                            self.Confirm(4001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == '4' and data[3] == 'N':
                            if self.Confirm(4002) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                        #返航
                        if data[2] == '5' and data[3] == 'Y':
                            self.Confirm(5001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == '5' and data[3] == 'N':
                            if self.Confirm(5002) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                    #2 参数查询命令回复
                    if data[1] == 'P':
                        if data[2] =='N':
                            if self.Confirm(6004) is True:
                                self.SendOrder(orderId, self.orderDict[orderId])
                        else:
                            #设置参数显示
                            self.pp_param_height.setText(data[2])
                            self.pp_param_speed.setText(data[3])
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                            self.Confirm(6005)

                    #3.1 参数设置命令回复
                    if data[1] == 'S':
                        if data[2] == 'Y':
                            self.Confirm(6001)
                            self.RemoveOrder(orderId)
                            self.ORDER_STEP = STEP_START
                        if data[2] == 'N':
                            if self.Confirm(6002) is True:
                                #再次发送
                                self.SendOrder(orderId, self. orderDict[orderId])
                            else:
                                #不重新发送
                                pass
                        if data[2] == 'E':
                            if self.Confirm(6003) is True:
                                #重新设置
                                pass
                            else:
                                #不重新设置
                                pass

                    # #6 飞行器调试信息
                    # if data[1] =='T':
                    #     self.SendToDebugWindow(data[2])

                else:
                    k, v = self.orderDict.items()
                    self.SendOrder(k,v)

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
        计算给定str的字节异或值s
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

    def RecordOrder(self,strOrderId, strOrderContent):
        """
        记录已发送命令到字典
        :param strOrderId: 命令唯一id
        :param strOrderContent: 命令内容
        :return:
        """
        try:
            self.orderDict[strOrderId] = strOrderContent
        except Exception as e:
            print('e10002:',e.message)

    def RemoveOrder(self,strOrderId):
        """
        删除已存储的，发送成功的命令
        :param strOrderId: 命令唯一ID
        :return: True or False
        """
        try:
            self.orderDict.pop(strOrderId)
            self.ShowInTab('<send success: orderId-' + str(strOrderId) + '>')
            return True
        except Exception as e:
            print('e10001:',e.message)
            return False

    def SendToDebugWindow(self,strArg):
        self.toDebugWindowSingal.emit(strArg)

    """
    飞行器控制按钮
    """
    def Confirm(self,intArg):
        """
        确认窗口
        :param intArg:
        :return:确定返回True， 取消返回False
        """
        chooseWindow = NoticeWindow()
        chooseWindow.Confirm(intArg)
        return chooseWindow.status

    @pyqtSignature("")
    def on_pick_takeoff_btn_clicked(self):
        """
        起飞按钮
        """
        self.ShowInTab(u'起飞 button clicked')
        if self.Confirm(1) is True:
            if self.PLANE_STATUS is planeStatus.POINT_SET:
                if self.ORDER_STEP == STEP_START:
                    orderId = self.uniqueId()
                    orderContent = 'Z=C=1'
                    self.SendOrder(orderId, orderContent)
                    self.RecordOrder(orderId,orderContent)
                    self.ORDER_STEP = STEP_SEND_WAIT
                else:
                    self.Confirm(21)
            else:
                self.Confirm(11)


    @pyqtSignature("")
    def on_pick_startMission_btn_clicked(self):
        """
        执行任务按钮
        """
        # TODO: not implemented yet
        self.ShowInTab('startMission button clicked')
        if self.Confirm(2) is True:
            if self.PLANE_STATUS is planeStatus.TAKE_OFF or self.PLANE_STATUS is planeStatus.ABORT_MISSION:
                if self.ORDER_STEP == STEP_START:
                    orderId = self.uniqueId()
                    orderContent = 'Z=C=2'
                    self.SendOrder(orderId, orderContent)
                    self.RecordOrder(orderId,orderContent)
                    self.ORDER_STEP = STEP_SEND_WAIT
                else:
                    self.Confirm(21)
            else:
                self.Confirm(2101)


    @pyqtSignature("")
    def on_pick_abortMission_btn_clicked(self):
        """
        终止任务按钮
        """
        # TODO: not implemented yet
        self.ShowInTab('abortMission button clicked')
        if self.Confirm(3) is True:
            if self.PLANE_STATUS is planeStatus.START_MISSION:
                if self.ORDER_STEP == STEP_START:
                    orderId = self.uniqueId()
                    orderContent = 'Z=C=3'
                    self.SendOrder(orderId, orderContent)
                    self.RecordOrder(orderId,orderContent)
                    self.ORDER_STEP = STEP_SEND_WAIT
                else:
                    self.Confirm(21)
            else:
                self.Confirm(3101)


    @pyqtSignature("")
    def on_pick_land_btn_clicked(self):
        """
        降落按钮
        """
        # TODO: not implemented yet
        self.ShowInTab('land button clicked')
        if self.Confirm(4) is True:
            if self.PLANE_STATUS is planeStatus.WAIT or self.PLANE_STATUS is planeStatus.START_MISSION:
                self.Confirm(4101)
            else:

                if self.ORDER_STEP == STEP_START:
                    orderId = self.uniqueId()
                    orderContent = 'Z=C=4'
                    self.SendOrder(orderId, orderContent)
                    self.RecordOrder(orderId,orderContent)
                    self.ORDER_STEP = STEP_SEND_WAIT
                else:
                    self.Confirm(21)


    @pyqtSignature("")
    def on_pick_return_btn_clicked(self):
        """
        返航按钮
        """
        self.ShowInTab('returnToBase button clicked')
        if self.Confirm(5) is True:
            if self.PLANE_STATUS is planeStatus.FINISH_MISSION or self.PLANE_STATUS is planeStatus.ABORT_MISSION or self.PLANE_STATUS is planeStatus.LAND:
                if self.ORDER_STEP == STEP_START:
                    orderId = self.uniqueId()
                    orderContent = 'Z=C=5'
                    self.SendOrder(orderId, orderContent)
                    self.RecordOrder(orderId,orderContent)
                    self.ORDER_STEP = STEP_SEND_WAIT
                else:
                    self.Confirm(21)
            else:
                self.Confirm(5101)


    """
    飞行器参数查询和设置
    """
    @pyqtSignature("")
    def on_pick_param_check_btn_clicked(self):
        """
        参数查询按钮
        :return:
        """
        self.ShowInTab(u'参数查询按钮 clicked')
        if self.ORDER_STEP == STEP_START:
            orderId = self.uniqueId()
            self.SendOrder(self.uniqueId(), content='Z=P')
            self.ORDER_STEP = STEP_SEND_WAIT
            self.RecordOrder(orderId,'Z=P')
        else:
            self.Confirm(21)

    @pyqtSignature("")
    def on_pick_param_set_btn_clicked(self):
        """
        参数设置按钮
        只能在飞行器等待状态下设置
        :return:
        """
        if self.PLANE_STATUS is planeStatus.WAIT:
            if self.Confirm(206) is True:
                #todo: 获取高度和速度，校验参数，发送命令
                height = str(self.pp_param_height.text())
                speed = str(self.pp_param_speed.text())
                try:
                    height = float(height)
                    speed = float(speed)

                    #发送命令
                    if self.ORDER_STEP is STEP_START:
                        orderId = self.uniqueId()
                        orderContent = 'Z=S='+str(height)+'='+str(speed)

                        self.SendOrder(orderId, orderContent)
                        self.RecordOrder(orderId, orderContent)
                        self.ORDER_STEP = STEP_SEND_WAIT
                    else:
                        self.Confirm(21)
                except Exception as e:
                    self.Confirm(207)
                    self.ShowInTab('error in param_set:',e.message)
        else:
            ## 提示飞行器处于等待状态
            self.Confirm(205)