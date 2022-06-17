from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
from matplotlib.figure import Figure
# подключение библиотек


class MplDiagramma(QWidget):  # класс круговой диаграммы
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        vertical_layout = QVBoxLayout()       # отступы
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot()    # вид диаграммы
        self.setLayout(vertical_layout)
