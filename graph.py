# use numpy
# line graph -- creates line segements between points
# make it as a widget so it can be embedded in the main interface
# treat it like an oscilloscope (sec/div, volts/div)
# should be able to make the graph any size, and it will size everything within it automatically

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy

class Grapher(QWidget):
    def __init__(self):
        super().__init__()

        #self.initUI()

    #def initUI(self):
       # self.show()

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
        qp.drawLine(0, height, width, height)
        qp.drawLine(0, 0, width, 0)

        qp.drawLine(0, 0, 0, height)
        qp.drawLine(width, 0, width, height)

        qp.setPen(QColor(100,100,100))
        divisions = 10
        height_divisions = height/divisions
        current_height = 0
        for i in range(divisions):
            qp.drawLine(0, 25, 0, 25)
            current_height = current_height + height_divisions
            qp.drawLine(0, current_height, width, current_height)


        # pen.setStyle(Qt.DashLine)
        # qp.setPen(pen)
        # qp.drawLine(0, 80, width, 80)
        #
        # pen.setStyle(Qt.DashDotLine)
        # qp.setPen(pen)
        # qp.drawLine(0, 120, width, 120)
        #
        # pen.setStyle(Qt.DotLine)
        # qp.setPen(pen)
        # qp.drawLine(0, 160, width, 160)
        #
        # pen.setStyle(Qt.DashDotDotLine)
        # qp.setPen(pen)
        # qp.drawLine(0, 200, width, 200)
        #
        # pen.setStyle(Qt.CustomDashLine)
        # pen.setDashPattern([1, 4, 5, 4])
        # qp.setPen(pen)
        # qp.drawLine(0, 240, width, 240)

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(300, 300, 280, 270)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        self.graph = Grapher()
        layout.addWidget(self.graph)

    def handleButton(self):
        print ('Update')
        #self.graph.update()

app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec_())