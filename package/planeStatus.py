# -*- coding: utf-8 -*-

STATUS_DICT = {
    0:u'测试状态',
    1:u'等待状态',
    2:u'路径设置完成',
    3:u'起飞',
    4:u'执行任务',
    5:u'终止任务',
    6:u'降落',
    7:u'任务完成',
    8:u'返航'
               }

DEBUG_STATUS_DICT = {
    1001:u'GPRS连接成功',
    2001:u'获得飞行器控制权',
    2002:u'起飞',
    2003:u'降落',
    2004:u'返航',
    3000:u'开始执行任务',
    300:[u'正在飞往第',u'个点'],
    4001:u'路径点初始化成功',
    4002:u'路径点加载成功',
    4003:u'路径点加载失败，正在执行任务',
    4004:u'任务被终止',
    4005:u'终止任务失败，未开始执行任务',
    4006:u'任务已完成',
}

class PlaneStatus():
    """
    飞行器状态
    """
    def __init__(self):
        self.WAIT = 1               #等待
        self.POINT_SET = 2          #设置路径完成
        self.TAKE_OFF = 3           #起飞
        self.START_MISSION = 4      #执行任务
        self.ABORT_MISSION = 5      #终止任务
        self.LAND = 6               #降落
        self.FINISH_MISSION = 7     #任务完成
        self.RETURN_TO_BASE = 8     #返航

class PlaneControl():
    """
    飞行器控制命令
    """
    def __init__(self):
        self.TAKE_OFF = 1               #起飞
        self.START_MISSION = 2          #开始任务
        self.ABORT_MISSION = 3          #终止任务
        self.LAND = 4                   #降落
        self.RETURN_TO_BASE = 5         #返航