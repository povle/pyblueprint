from PyQt5 import QtWidgets, QtCore, uic
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)
from matplotlib.figure import Figure
from . import AbstractBlock


class VisualisationBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(widget=VisualisationBlockWidget(),
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['axes'])

        self.plot = PlotWindow()
        self.widget.plotButton.clicked.connect(self.plot.show)

    def processData(self, data):
        result = self.executeFunction(data=data, axes=self.plot.axes)
        self.widget.plotButton.setEnabled(result is not None)
        return data


class VisualisationBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/VisualisationBlock.ui', self)


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
