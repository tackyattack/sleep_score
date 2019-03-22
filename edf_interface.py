from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import numpy as np
import graph
import edf
import scorer


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(300, 300, 1000, 270)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(800)
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
        #signal_name = "sine 15"

        e.open_EDF("../test_vectors/eeg_recording/SC4011E0-PSG.edf")
        signal_name = "EEG Pz"

        #e.open_EDF("../test_vectors/eeg_recording/ma0844az_1-1+.edf")
        #signal_name = "EEG F3"

        e.parse_header()
        sr = e.get_signal_sample_rate(signal_name)

        start_time_min = 0
        start_pos = start_time_min*60*sr+shift*2000
        print("min:" + str(start_pos/sr/60))
        samples = np.array(e.get_signal_samples(start_pos, 4000, signal_name))
        self.data_graph.setVerticalGraphShift(1000)
        self.data_graph.setYDivs(10)
        self.data_graph.setYMax(300)
        self.data_graph.setData(samples)

        spec = scorer.score_epoch(samples, sr)

        self.fft_graph.setVerticalGraphShift(300)
        self.fft_graph.setYDivs(100)
        self.fft_graph.setYMax(100)
        self.fft_graph.setData(spec)
        self.fft_graph.setXDivs(1)

    def handleButton(self):
        print ('Update')


app = QApplication(sys.argv)

window = Window()
window.show()
window.slvaluechange()

sys.exit(app.exec_())