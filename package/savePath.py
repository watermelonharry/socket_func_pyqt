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
            self.savePath = '/'.join(str(path).split('\\')) + '/'+ self.fileName

        folderPath = '/'.join(self.savePath.split('/')[:-1])
        if os.path.exists(folderPath) is False:
            print('error in savePath.init: can not find folder path, creating now.')
            os.makedirs(folderPath)

        try:
            file = open(self.savePath,'r')
            file.close()
        except Exception as e:
            print('error in savePath.init: can not find pathFile, creating now.')
            file = open(self.savePath, 'w')
            file.write('')
            file.close()

        self.IS_EMPTY = self.IsEmpty()

    def __str__(self):
        return 'pathSaver init'

    def LoadPath(self):
        """
        从文件中读取路径点坐标信息，格式化后返回点坐标列表
        :return: None / 路径点list：[('p1x','p1y'), ('p2x','p2y')]
        """
        if self.IS_EMPTY:
            return None
        else:
            try:
                pathFile = open(self.savePath,'r')
                pathList = pathFile.readlines()
                pathList = self.Translate(pathList)
                return pathList
            except Exception as e:
                print('error in pathSaver-LoadPath:',e.message)
                return None

    def Translate(self,strList):
        """
        转换文件中的坐标数据为指定的坐标点数据
        :param strList: ['p1x|p1y\n', 'p2x|p2y\n']
        :return: [('p1x','p1y'), ('p2x','p2y')]
        """
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
            self.IS_EMPTY = True
            return True
        except Exception as e:
            print('error in pathSaver-ClearRecord', e.message)
            return False

    def addOnePoint(self,pointTup):
        """
        在文件中追加一个当前坐标点
        :param pointTup: ('longitude','latitude')
        :return: True / False
        """
        try:
            strPoint = tuple(str(x) for x in pointTup)
        except Exception as e:
            print('error in savePath.addOnePoint: invalid point type')
            return False
        try:
            with open(self.savePath, 'a') as pFile:
                pFile.write('|'.join(strPoint) + '\n')

            self.IS_EMPTY = False
            return True
        except Exception as e:
            print('error in savePath.addOnePoint:',e.message)
            return False

    def IsEmpty(self):
        """
        判断已保存路径点是否为空
        :return: True / False
        """
        try:
            pathFile = open(self.savePath,'r')
            pathList = pathFile.readlines()
            if len(pathList) == 0:
                return True
            else:
                return False
        except Exception as e:
            return True

if __name__ == '__main__':
    tSaver = pathSaver(path = 'C:\\Users\\Harry\\Documents\\PyQtProjects\\socket_func_pyqt\\test')
    tSaver = pathSaver(path='C:\\Users\\Harry\\Documents\\PyQtProjects\\socket_func_pyqt\\test', filename= 'test_path.dat')
    tSaver.addOnePoint(('1231231','11231231'))
    tSaver.addOnePoint(('2123131','31231231'))
    tSaver.addOnePoint((231231,'31231231'))
    tSaver.addOnePoint((1.231231,2.31231))
    tSaver.ClearRecord()
    tSaver.addOnePoint(('1231231','11231231'))
    tSaver.addOnePoint(('2123131','31231231'))
    tSaver.addOnePoint((231231,'31231231'))
    tSaver.addOnePoint((1.231231,2.31231))
    pp = tSaver.LoadPath()
    print(pp)
