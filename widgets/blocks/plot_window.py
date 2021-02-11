from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)
from matplotlib.figure import Figure


class PlotWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent, flags=QtCore.Qt.Window)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)

        toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
