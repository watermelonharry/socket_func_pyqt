# -*- coding:UTF-8 -*-
import time
from PyQt4.QtCore import QThread, QMutex, QMutexLocker
import threading
import requests, os
"""
基于百度鹰眼api：http://lbsyun.baidu.com/index.php?title=yingyan/api/track
"""

##config file path
CONFIG_PATH = '/'.join(os.getcwd().split('\\')) + '/websrc/gps_config.dat'
CONFIG_URL = 'http://api.map.baidu.com/trace/v2/track/addpoint'

def time_to_unix(time_str):
    """
    unix时间戳计算
    :param time_str: str 'year month day hour minute sec' in decimal
    :return: int(UNIX_TIMESTAMP)
    """
    try:
        s = time.mktime(time.strptime(time_str, '%Y %m %d %H %M %S'))
        return int(s)
    except Exception as e:
        return None

##INPUT: str or int(unix timestamp)
##output: str 'year month day hour minute sec' in decimal
def unix_to_time(unix_str):
    try:
        dt = time.localtime(int(unix_str))
        return str(' '.join([str(i) for i in dt][:6]))
    except Exception as e:
        return None

def current_unix():
    try:
        unix_str = int(time.mktime(time.localtime()))
        return unix_str
    except Exception as e:
        return None


#class GpsUploader(threading.Thread):
class GpsUploader(QThread):
    GPSMutex = QMutex()
    
    def __init__(self, updateMainSignal = None,  recSignal = None, toPickPointSignal = None):
        super(GpsUploader, self).__init__()
        self.para = {
                    'ak':None,
                    'service_id':None,
                    'latitude':None,             #wei du,double,-90.0~90.0
                    'longitude':None,            #jing du,double, -180-180.0
                    'coord_type':1,
                    'loc_time':None,            #UNIX time stamp
                    'entity_name':None}
        self.get_ak()
        self.points = []

        self.updateMainSignal = updateMainSignal
        self.recSignal = recSignal
        self.toPickPointSignal = toPickPointSignal

    #point_tuple: (longitude, latitude, unix_time)
    #the element type can be str/int/double
    def add_point(self, point_tuple):
        #get lock
        with QMutexLocker(self.GPSMutex):
            self.points.append(point_tuple)
        #release the lock

    def run(self):
        # print(self.hello)
        # print (self.para)

        #get lock
        with QMutexLocker(self.GPSMutex):
            up_count = 0
            del_count = 0
            fail_count = 0
            # fail_list = []
            if len(self.points) != 0:
                for point in self.points:
                    if self.set_point(long= point[0], lat=point[1]):
                        if self.upload_one_point():
                            up_count += 1
                            #更新取点窗口的当前坐标
                            self.toPickPointSignal.emit('IN=YY=LOC=' + str(point[0]) + '='+str(point[1]))
                        else:
                            fail_count += 1
                            # fail_list.append(point)
                    else:
                        del_count +=1
                self.points = []
                self.update_main(
                'enter-func-GpsUploader-run: ' + str(up_count) + ' uploaded, ' + str(fail_count) + ' failed, ' + str(
                    del_count) + ' deleted.')

        #release lock
        # self.points = fail_list

    #update to mainwindow
    def update_main(self,  str_arg):
        self.updateMainSignal.emit(str_arg)
        print(str_arg)

    def get_ak(self):
        try:
            with open(CONFIG_PATH, 'r') as data:
                for line in data:
                    temp = line.split(':')
                    self.para[temp[0]] = temp[1][:-1]
            self.para['loc_time'] = current_unix()
            print(self.para)
        except Exception as e:
            print('error-uploader init failed:', e.message)

    def set_point(self,long = None, lat = None, time = current_unix(), coord_type = 1):
        if long is None or lat is None:
            return False
        else:
            self.para['longitude'] = long
            self.para['latitude'] = lat
            self.para['loc_time'] = time
            self.para['coord_type'] = coord_type
            return True

    def upload_one_point(self):
        reply = requests.post(CONFIG_URL, data = self.para).json()
        if reply['status'] is 0:
            return True
        else:
            return False

    # def GtoB(self, G_lon, G_lat):
    #     """
    #     GPS坐标转换为百度坐标
    #     :param G_lon: GPS经度
    #     :param G_lat: GPS纬度
    #     :return: (百度经度,百度纬度) 或 None
    #     """
    #     try:
    #         import json
    #         import base64
    #         url = 'http://api.map.baidu.com/ag/coord/convert?from=0&to=4&x=%s&y=%s' % (str(G_lon), str(G_lat))
    #         source_code = requests.get(url)
    #         plain_text = source_code.text
    #         c = json.loads(plain_text)
    #         if c['error'] == 0:
    #             return (base64.decodestring(c['x']), base64.decodestring(c['y']))  # lat,lon in string type
    #         else:
    #             return None
    #     except Exception as e:
    #         print('error in GtoB:', e.message)
    #         return None




if __name__ == '__main__':
    test_p = [
        ('120.13143165691','30.272977524721' ),
        ('120.13143165690','30.272977524720' ),
        ('120.13143165689','30.272977524719' ),
        ('120.13143165688','30.272977524718' ),
        ('120.13143165687','30.272977524717' ),
    ]

    c = GpsUploader()
    for p in test_p:
        c.add_point(p)
    c.start()


