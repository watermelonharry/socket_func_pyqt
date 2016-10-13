# -*- coding:UTF-8 -*-
import time
from PyQt4.QtCore import QThread, QMutex, QMutexLocker
import threading
import requests, os

##config file path
CONFIG_PATH = '/'.join(os.getcwd().split('\\')) + '/websrc/gps_config.dat'
CONFIG_URL = 'http://api.map.baidu.com/trace/v2/track/addpoint'
##input : str 'year month day hour minute sec' in decimal
##return : int(UNIX_TIMESTAMP)


def time_to_unix(time_str):
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
    
    def __init__(self, upsignal = None,  downsignal = None):
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

        self.upsignal = upsignal
        self.downsignal = downsignal

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
            fail_list = []
            for point in self.points:
                if self.set_point(*point):
                    if self.upload_one_point():
                        up_count += 1
                    else:
                        fail_count += 1
                        fail_list.append(point)
                else:
                    del_count +=1
        #release lock
        self.points = fail_list
        self.update_main('enter-func-GpsUploader-run: '+str(up_count)+' uploaded, '+ str(fail_count)+ ' failed, '+ str(del_count)+ ' deleted.')

    #update to mainwindow
    def update_main(self,  str_arg):
        self.upsignal.emit(str_arg)
        print(str_arg)

    def get_ak(self):
        try:
            with open(CONFIG_PATH, 'r') as data:
                for line in data:
                    temp = line.split(':')
                    self.para[temp[0]] = temp[1][:-1]

            #test data
            self.para['longitude'] = '120.13143165691'
            self.para['latitude']='30.272977524721'
            self.para['loc_time'] = current_unix()
            self.para['coord_type'] = '3'
            print(self.para)
        except Exception as e:
            print('error-uploader init failed.')

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


