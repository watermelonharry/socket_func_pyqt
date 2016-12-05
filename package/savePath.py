# -*- coding: utf-8 -*-
"""
用于记录、添加、删除轨迹点
"""
import os
class pathSaver():
    def __init__(self,path = None, filename = None):
        if filename is None:
            self.fileName = 'path_config.dat'
        else:
            self.fileName = str(filename)

        if path is None:
            self.savePath = '/'.join(os.getcwd().split('\\')) + '/websrc/path_config.dat'
        else:
            self.savePath = str(path) + '/'+ self.fileName

    def __str__(self):
        return 'pathSaver init'

    def LoadPath(self):
        """
        从文件中读取路径点坐标信息，格式化后返回点坐标列表
        :return:
        """
        try:
            pathFile = open(self.savePath,'r')
            pathList = pathFile.readlines()
            pathList = self.preProcess(pathList)
            return pathList
        except Exception as e:
            print('error in pathSaver-LoadPath:',e.message)
            return None

    def preProcess(self,strList):
        if len(strList) is 0:
            return None
        pathList = []
        for lines in strList:
            noEnterLine = ''.join(lines.split('\n'))
            pathStr = noEnterLine.split('|')
            pathList.append(tuple(pathStr))
        return pathList

    def ClearRecord(self):
        """
        删除文件中的点坐标
        :return:True / False
        """
        try:
            pathFile = open(self.savePath, 'w')
            pathFile.write('')
            pathFile.close()
            return True
        except Exception as e:
            print('error in pathSaver-ClearRecord', e.message)
            return False

    def addOnePoint(self,pointTup):
        """
        在文件中追加一个当前坐标点
        :param pointTup: (longitude,latitude)
        :return: True / False
        """
