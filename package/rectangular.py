# -*- coding: utf-8 -*-

"""
用于约束路径集合，在指定区域内
输入线段集合，起点、终点坐标。
输出线段集合
"""
from math import sqrt
import copy

class Rectangular:
    def __init__(self,lineList = None, startPoint = None , endPoint = None):
        self.lines = lineList
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.resLines = []

    def process(self):
        startRecord = []
        endRecord = []
        lineDict = {}
        for i in range(0,len(self.lines)):
            lineDict[i] = self.lines[i]
            # 计算起始点到线段的投影点和距离
            crossPoint, distance = self.pointOnLine(*(self.startPoint + self.lines[i]))
            if crossPoint is not None:
                startRecord.append((distance, crossPoint, i))
            # 计算终点到线段的投影点和距离
            crossPoint, distance = self.pointOnLine(*(self.endPoint + self.lines[i]))
            if crossPoint is not None:
                endRecord.append((distance, crossPoint, i))



        #按照距离排序
        if startRecord is not None and len(startRecord) != 0:
            try:
                startRecord.sort(key = lambda x:x[0])

                # 取出最近的投影点，更新lines数组
                record = startRecord[0]
                pointOnLine = record[1]
                oldLineKey = record[2]
                oldLine = lineDict.pop(oldLineKey)

                self.resLines.append(self.startPoint + pointOnLine)
                self.resLines += self.createNewLine(pointOnLine, oldLine)
            except Exception as e:
                print('error in rectangular.process:', e.message)

        # 按照距离排序
        if endRecord is not None and len(endRecord) != 0:
            try:
                endRecord.sort(key = lambda x:x[0])

                # 取出最近的投影点，更新lines数组
                record = endRecord[0]
                pointOnLine = record[1]
                oldLineKey = record[2]
                oldLine = lineDict.pop(oldLineKey)

                self.resLines.append(self.endPoint + pointOnLine)
                self.resLines += self.createNewLine(pointOnLine, oldLine)
            except Exception as e:
                print('error in rectangular.process:', e.message)

        for (k, v) in lineDict.items():
            self.resLines.append(v)

    def output(self):
        return self.resLines

    def createNewLine(self, point, line):
        res = []
        try:
            res.append(point+(line[0],line[1]))
            res.append(point+(line[2],line[3]))
        except Exception as e:
            print ('error in rectangular.createNewLine:' + e.message)
        return res

    def pointOnLine(self, m,n,x1,y1,x2,y2):
        px = (m*(x2-x1)**2 + n*(y2-y1)*(x2-x1) + (x1*y2 - x2*y1)*(y2 - y1)) / ((x2-x1)**2 + (y2 -y1)**2 + 0.0000001)
        py = (m*(x2-x1)*(y2-y1) + n*(y2-y1)**2 + (x2*y1 - x1*y2)*(x2 - x1)) / ((x2-x1)**2 + (y2 -y1)**2 + 0.0000001)

        if (px-x1)*(px-x2) <= 0 or (py-y1)*(py-y2) <= 0:
            # newLines = [(px,py)]
            # newLines.append((x1, y1, px, py))
            # newLines.append((x2, y2, px, py))
            # newLines.append((m, n, px, py))
            # return newLines
            return (px,py),(m-px)**2 + (n-py)**2  #返回交点，距离^2
        else:
            return None,None

if __name__ == '__main__':
    try:
        line=(0,1,1,0)
        res = Rectangular()
        d = res.pointOnLine(1,2,*line)
        print(d)
    except Exception as e:
        print(e.message)

    try:
        lines = [(-2,0,0,3),(0,3,4,0),(4,0,6,2)]
        stp = (0,0)
        edp = (6,1)
        res = Rectangular(lines,stp,edp)
        res.process()
        d = res.output()
        print(d)
    except Exception as e:
        print(e.message)