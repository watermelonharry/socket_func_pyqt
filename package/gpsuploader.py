# -*- coding:UTF-8 -*-
import time
from PyQt4.QtCore import QThread
import threading
import requests

CONFIG_PATH = 'gps_config.dat'
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

class GpsUploader(threading.Thread):

    def __init__(self):
        super(GpsUploader, self).__init__()
        self.hello = 'hellolllll'
        self.para = self.get_ak()

    def run(self):
        print(self.hello)
        print (self.para)

        while True:
            self.test_for_upload()
            time.sleep(2)

    def get_ak(self):
        para = {}
        with open(CONFIG_PATH, 'r') as data:
            for line in data:
                temp = line.split(':')
                para[temp[0]] = temp[1][:-1]

        para['longitude'] = '120.13143165691'
        para['latitude']='30.272977524721'
        para['loc_time'] = current_unix()
        para['coord_type'] = '3'
        return para

    def upload_point(self):
        reply = requests.post(CONFIG_URL, data = self.para).json()
        if reply['status'] == 0:
            return True
        else:
            return False

    def test_for_upload(self):
        self.para['loc_time'] = current_unix()
        if self.upload_point() is False:
            print('upload fail')
        else:
            print('upload done')


if __name__ == '__main__':
    c = GpsUploader()
    c.start()


