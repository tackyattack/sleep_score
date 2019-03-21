from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy as np
import graph
import edf


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

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(500)
        self.sl.setValue(0)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(1)
        self.sl.valueChanged.connect(self.slvaluechange)
        layout.addWidget(self.sl)

        self.data_graph = graph.Grapher()
        layout.addWidget(self.data_graph)

        self.fft_graph = graph.Grapher()
        layout.addWidget(self.fft_graph)

    def slvaluechange(self):
        shift = int(self.sl.value())
        e = edf.EDF_file()
        #e.open_EDF("../test_vectors/test_generator_2.edf")
        e.open_EDF("../test_vectors/eeg_recording/ma0844az_1-1+.edf")
        e.parse_header()
        samples = np.array(e.get_signal_samples(0+shift*200, 500, "EEG F3"))
        self.data_graph.setVerticalGraphShift(300)
        self.data_graph.setYDivs(5)
        self.data_graph.setYMax(300)
        self.data_graph.setData(samples)

        samples = np.pad(samples, (0,1500), 'constant')
        fft = np.fft.fft(samples)
        spec = np.abs(fft[:len(fft)//2])
        spec = np.square(spec)
        spec = spec / (2000*200)
        # 200 / (1500+500) = 0.1 Hz resolution
        spec = spec[0:400] # 0 - 40Hz

        self.fft_graph.setVerticalGraphShift(300)
        self.fft_graph.setYDivs(100)
        self.fft_graph.setYMax(100)
        self.fft_graph.setData(spec)
        self.fft_graph.setXDivs(1)

        #print(e.get_signal_sample_rate("EEG F3"))

    def handleButton(self):
        print ('Update')


app = QApplication(sys.argv)

window = Window()
window.show()
window.slvaluechange()

sys.exit(app.exec_())