import sys
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CanvasOnWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._fig = Figure()
        self.canv = FigureCanvas(self._fig)
        layout.addWidget(self.canv)

        ax = self._fig.add_subplot(111)
        ax.plot(range(10),range(10))
        self._fig.canvas.mpl_connect('button_press_event', self._resize)

    def _resize(self, event):
        w,h = self._fig.get_size_inches()
        dw = self.size().width()-w*self._fig.dpi
        dh = self.size().height()-h*self._fig.dpi
        if event.button == 1: # left click
            h-=1
        elif event.button == 3: # right click
            h+=1
        self._fig.set_size_inches(1, 10)

        self._fig.canvas.draw()
        # self.resize(w*100+dw,h*100+dh)

        print (self.size())
        print (self._fig.canvas.size())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = CanvasOnWidget()
    main.show()
    sys.exit(app.exec_())