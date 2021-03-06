# -*- coding: utf-8 -*-

STATUS_DICT = {
    0:u'等待状态更新',
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
    4007:u'飞行器20秒后将自动返航',
    4008:u'自动返航已终止',
    4009:u'返航已终止',
    5001:u'GUIDANCE已启动',
    5002:u'GUIDANCE已终止',
    5003:u'GUIDANCE异常，请重启飞行器',
    5004:u'检测到障碍物，即将执行避障算法',
}

NOTICE_DICT = {
    0:u'无提示信息',
    1:u'确定起飞？',
    2:u'确定执行任务？',
    3:u'确定终止任务？',
    4:u'确定降落？',
    5:u'确定返航？',
    6:u'开启实时位置更新？',
    7:u'确认关闭实时位置更新？',
    8:u'确认设置飞行器当前坐标为返航点？',

    #错误提示

    10:u'飞行器未处于等待状态，\n无法设置，添加的点无效',
    11:u'飞行器未处于“轨迹点设置完成”状态,\n无法进行起飞操作',
    12:u'当前操作无效\n正在等待飞行器状态更新',
    13:u'路径已经设置\n如需再设置请重置',
    14:u'请先设置路径。',
    2101:u'飞行器未处于起飞/终止任务状态，\n无法进行开始操作',
    3101:u'飞行器未处于执行任务状态，\n无法终止任务',
    4101:u'飞行器未处于起飞/完成任务/返航状态，\n无法进行降落操作',
    5101:u'飞行器正处于执行任务/返航状态，\n无法进行返航操作',
    6101:u'飞行器未处于路径设置完成/降落状态,\n无法进行起飞操作',
    7101:u'飞行器未处于等待状态，\n无法设置返航点',

    21:u'正在等待上一条命令设置完成',
    22:u'选取点不足，请重新选择',
    23:u'设置点步骤错误',
    24:u'计算的路径点不足，请重新设置',
    25:u'确认重新发送上一条命令？',
    26:u'上一条命令设置成功，\n无需重复发送',
    27:u'确认清除上一条命令？\n清除后需要重新设置',

    29:u'确认开启服务器？',
    30:u'GPRS服务器开启成功',
    31:u'服务器未运行，无法停止',
    32:u'服务器正在运行\n请勿重复操作',
    33:u'服务器开启失败，\n请确保网络环境、参数正确',
    34:u'IP、端口设置成功',
    3401:u'参数错误，\n请输入正确的IP和端口号',
    3411:u'确认关闭服务器？\n关闭后无法远程控制飞行器',
    3412:u'飞行器未连接，\n请等待飞行器连接成功再发送',
    35:u'飞行器连接成功,\n可以进行下一步操作',
    36:u'确定清除窗口的记录？',

    71:u'错误：未收到当前坐标信息，\n请建立与飞行器的连接',
    72:u'地图加载成功，可以进行下一步操作',
    7201:u'地图加载失败，\n请确保网络正常后重启程序',
    73:u'确定清除路径设置？',
    74:u'正在等待地图加载完成，\n若长时间未完成请重启程序',

    201:u'路径设置成功\n如需设置新路径请重置后再选取点',
    202:u'设置成功',
    203:u'路径设置失败，重新发送',
    204:u'路径设置失败，请检查参数',
    205:u'参数设置失败，\n请确认飞行器处于等待状态',
    206:u'确认设置参数？',
    207:u'请输入正确的参数值',

    1001: u'起飞命令设置成功',
    1002: u'起飞命令设置失败，重新发送',
    2001: u'执行任务命令设置成功',
    2002: u'执行任务命令设置失败，重新发送',
    3001: u'终止任务命令设置成功',
    3002: u'终止任务命令设置失败，重新发送',
    4001: u'降落命令设置成功',
    4002: u'降落命令设置失败，重新发送',
    5001: u'返航命令设置成功',
    5002: u'返航命令设置失败，重新发送',
    6001: u'飞行器参数设置成功',
    6002: u'飞行器参数设置失败，\n重新发送？',
    6003: u'飞行器参数设置错误，\n请重置后重新设置',
    6004: u'飞行器参数查询失败，\n重新查询',
    6005: u'飞行器参数查询成功',
    8001:u'返航点设置成功',
    8002:u'返航点设置失败，\n重新发送命令？',

}

class PlaneStatus():
    """
    飞行器状态
    """
    def __init__(self):
        self.NO_ACCESS = 0          #等待状态更新
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