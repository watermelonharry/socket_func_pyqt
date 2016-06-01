# -*- coding: utf-8 -*-
import os
import time

PATH = None
PRINT = True

class logfile(object):
    def __init__(self, name = 'log', mode = 'a'):
        self._file = None
        self._filename = name+'-'+ self.gettime() +'.dat'
        self._mode = 'a'

    def __str__(self):
        print('name:' + self._filename + '; mode:' + self._mode)

    def write(self, loglist):
        self.open()

        if self._file:
            if type(loglist) == type(['a']) or type(loglist) == type(('a','b')):
                for lines in loglist:
                    self._file.write(time.ctime()+'--'+ str(lines)+'\n')
            else:
                self._file.write(time.ctime()+'--'+ str(loglist)+'\n')
        else:
            self.say('creat file first!')

        self.done()

    def done(self):
        self._file.close()
        self.say('log wrote, file closed.')

    def open(self):
        try:
            self._file = open(self._filename, self._mode)
            self.say('log file opened')
        except Exception as e:
            self._file = None
            self.say(str(e))

    def changemod(self, mode = 'w+'):
        self.done()
        self._mode = mode
        try:
            self._file = open(self._filename, self._mode)
            self.say('log file creat')
        except Exception as e:
            self._file = None
            self.say(str(e))

    def say(self,words):
        if PRINT:
            print(words)

    def gettime(self):
        t = time.gmtime()
        return ('-'.join([str(i) for i in [t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec]]))

if __name__ == '__main__':
    log = logfile(name = 'hello')
    log.write('test-1')
    log.write(['list-1', 'list-2'])
    log.write([1234, 'list-2'])

    log.write('test-222')
    log.write(['list-222', 'list-222'])
    log.write([111232, 'list-123123'])