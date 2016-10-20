# -*- coding: utf-8 -*-

"""
用于约束路径集合，在指定区域内
输入线段集合，起点、终点坐标。
输出线段集合
"""

class Rectangular:
    def __init__(self,lineList = None, startPoint = None , endPoint = None):
        self.lines = lineList
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.resLines = []

    def process(self):
        pass


    def pointOnLine(self, m,n,x1,y1,x2,y2):
        px = (m*(x2-x1)**2 + n*(y2-y1)*(x2-x1) + (x1*y2 - x2*y1)*(y2 - y1)) / ((x2-x1)**2 + (y2 -y1)**2 + 0.0000001)

        py = (m*(x2-x1)*(y2-y1) + n*(y2-y1)**2 + (x2*y1 - x1*y2)*(x2 - x1)) / ((x2-x1)**2 + (y2 -y1)**2 + 0.0000001)
        return (px,py)