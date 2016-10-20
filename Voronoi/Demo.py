# -*- coding: utf-8 -*-
import Tkinter as tk
import numpy as np
from Voronoi import Voronoi
import geometry
from PIL import Image, ImageTk

class MainWindow:
    # radius of drawn points on canvas
    RADIUS = 3

    # flag to lock the canvas when drawn
    LOCK_FLAG = False
    
    def __init__(self, master):
        # master.attributes('-alpha', 0.5)
        self.master = master
        self.master.title("Voronoi or Delaunay")
        self.points = set()

        self.im = ImageTk.PhotoImage(Image.open("basemap800x750.png"))
        # Image.open("basemap800x750.png").show()
        ##!!dont know why yet
        self.width, self.height = [ x/2 for x in self.im._PhotoImage__size]



        # <Button-1>:left click
        # <Button-2>:middle click
        # <Button-3>:right click
        # <Double-Button-1>:left-double click
        # <Triple-Button-1>:left-triple click
        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()
        ##calculate voronoi gram
        self.btnCalculateVoro = tk.Button(self.frmButton, text='Cal voro', width=20, command=self.onClickCalculateVoro)
        self.btnCalculateVoro.pack(side=tk.LEFT)
        ##generate delaunay gram
        self.btnCalculateDelau = tk.Button(self.frmButton, text = 'Cal Delau', width = 20, command = self.onClickCalculateDelau)
        self.btnCalculateDelau.pack(side = tk.LEFT)
        ##generate random points
        self.btnRandom = tk.Button(self.frmButton, text='Random', width=20, command=self.onClickGenerate)
        self.btnRandom.pack(side=tk.LEFT)
        ##clear
        self.btnClear = tk.Button(self.frmButton, text='Clear', width=20, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=self.width, height=self.height)
        self.w.config(background='white')

        self.w.bind('<Button-1>', self.onSingleClick)
        #添加底图
        self.w.create_image(0, 0,anchor = tk.CENTER, image = self.im, tag = 'map')
        self.w.pack()


    def onClickCalculateVoro(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True

            pObj = self.w.find_all()
            points = []
            for p in pObj:
                coord = self.w.coords(p)
                points.append((coord[0]+self.RADIUS, coord[1]+self.RADIUS))

            vp = Voronoi(points)
            vp.process()
            lines = vp.get_output()
            self.drawLinesOnCanvas(lines, tag = 'Voro')
            
            print(lines)
            # # 测试用
            # p2 = self.pointOnLine(points[0][0], points[0][1], lines[0][0],lines[0][1],lines[0][2],lines[0][3])
            # self.w.create_line(points[0][0], points[0][1], p2[0], p2[1], fill='red', tag=None)


    def onClickCalculateDelau(self):
        pObj = self.w.find_all()
        points = []
        for p in pObj:
            coord = self.w.coords(p)
            points.append(geometry.Point(coord[0]+self.RADIUS, coord[1]+self.RADIUS))
        print(points)
        triangles = geometry.delaunay_triangulation(points)
        for tri in triangles:
            self.drawPolyOnCanvas(tri, tag = 'Delau')
        print(triangles)

    #generate random points
    def onClickGenerate(self):
        if not self.LOCK_FLAG:
            point_number = 30
            rand_x = self.width * np.random.rand(point_number)
            rand_y = self.height * np.random.rand(point_number)
            rand_point = list(zip(rand_x,rand_y))
            for i in rand_point:
                self.w.create_oval(i[0]-self.RADIUS, i[1]-self.RADIUS, i[0]+self.RADIUS, i[1]+self.RADIUS, fill="yellow")



    def onClickClear(self):
        self.LOCK_FLAG = False
        self.w.delete('Voro','Delau')

    def onSingleClick(self, event):
        if not self.LOCK_FLAG:
            self.w.create_oval(event.x-self.RADIUS, event.y-self.RADIUS, event.x+self.RADIUS, event.y+self.RADIUS, fill="black")

    def drawLinesOnCanvas(self, lines, tag):
        for l in lines:
            self.w.create_line(l[0], l[1], l[2], l[3], fill='blue', tag = tag)

    def drawPolyOnCanvas(self, poly, tag):
        for point in poly:
            if point.x >= self.width or point.x <= 0 or point.y >= self.width or point.y <= 0:
                return None
        self.w.create_polygon(poly.a.x, poly.a.y, poly.b.x, poly.b.y, poly.c.x, poly.c.y, fill = '', outline = 'black', tag = tag)

    def pointOnLine(self, m, n, x1, y1, x2, y2):
        px = (m * (x2 - x1) ** 2 + n * (y2 - y1) * (x2 - x1) + (x1 * y2 - x2 * y1) * (y2 - y1)) / (
        (x2 - x1) ** 2 + (y2 - y1) ** 2 + 0.0000001)

        py = (m * (x2 - x1) * (y2 - y1) + n * (y2 - y1) ** 2 + (x2 * y1 - x1 * y2) * (x2 - x1)) / (
        (x2 - x1) ** 2 + (y2 - y1) ** 2 + 0.0000001)
        return (px, py)

def main(): 
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
