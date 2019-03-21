# use numpy
# line graph -- creates line segements between points
# make it as a widget so it can be embedded in the main interface
# treat it like an oscilloscope (sec/div, volts/div)
# should be able to make the graph any size, and it will size everything within it automatically

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy as np

class Grapher(QWidget):
    def __init__(self):
        super().__init__()
        self.y_divs = 1
        self.x_divs = 1
        self.x_max = 1
        self.y_max = 4
        self.v_shift = 0.0
        self.data = np.array([1,2,3,4])

        self.initUI()

    def initUI(self):
        self.show()

    def setData(self, array):
        self.data = array # could have option for 2D array that contains the x line spacing (optional)
        self.x_max = len(self.data) - 1
        self.repaint()

    def setVerticalGraphShift(self, v):
        self.v_shift = v
        self.repaint()

    def setYDivs(self, yd):
        self.y_divs = yd

    def setYMax(self, ym):
        self.y_max = ym

    def setXMax(self, xm):
        self.x_max = xm

    def setXDivs(self, xd):
        self.x_divs = xd

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        # updates every time window resizes

        # todo: use three boxes: one for the graph, and one for each axis for holding the axis values

        pen = QPen(Qt.white, 1, Qt.SolidLine)

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        qp.setPen(pen)


        qp.setPen(QColor(100,100,100))
        divisions = 10
        height_divisions = height/divisions
        current_height = 0
        for i in range(divisions):
            qp.drawLine(0, 25, 0, 25)
            current_height = current_height + height_divisions
            qp.drawLine(0, current_height, width, current_height)

        # draw line plot
        #self.y_max = np.max(self.data)
        qp.setPen(Qt.yellow)
        for i in range(len(self.data)-1):
            y1 = ((self.data[i]+self.v_shift)/self.y_divs)/self.y_max # normalize
            y1 = height - y1*height
            x1 = i/self.x_divs/self.x_max
            x1 = x1*width

            y2 = ((self.data[i+1]+self.v_shift)/self.y_divs)/self.y_max # normalize
            y2 = height - y2*height
            x2 = (i+1)/self.x_divs/self.x_max
            x2 = x2*width

            qp.drawLine(int(x1), int(y1), int(x2), int(y2))

        # draw bounding box
        qp.setPen(Qt.white)
        qp.drawLine(0, height, width, height)
        qp.drawLine(0, 0, width, 0)

        qp.drawLine(0, 0, 0, height)
        qp.drawLine(width, 0, width, height)

