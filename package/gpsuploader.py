# -*- coding:UTF-8 -*-
import time
from PyQt4.QtCore import QThread
import threading

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


class GpsUploader(threading.Thread):

    def __init__(self):
        super(GpsUploader, self).__init__()
        self.hello = 'hellolllll'

    def run(self):
        print(self.hello)


if __name__ == '__main__':
    c = GpsUploader()
    c.start()

