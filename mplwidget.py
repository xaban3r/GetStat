from PySide2.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MplWidget(QWidget):   # класс виджета график
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = FigureCanvas(Figure())
        vertical_layout = QVBoxLayout()   # отступы
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))  # вспомогательная панель снизу
        spacing = 0.25
        self.canvas.figure.subplots_adjust(bottom=spacing)      # отступ снизу
        self.canvas.axes = self.canvas.figure.add_subplot(111)    # вид графика
        self.setLayout(vertical_layout)