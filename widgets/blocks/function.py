from PyQt5 import QtWidgets, uic
import typing
import pandas
from .. import Node
from . import AbstractBlock, PlotWindow


class BoolInputRow(QtWidgets.QCheckBox):
    def __init__(self, arg_name, *args, **kwargs):
        super().__init__(text=arg_name, *args, **kwargs)
        self.arg_name = arg_name

    def getVal(self):
        return self.isChecked()


class IntInputRow(QtWidgets.QWidget):
    def __init__(self, arg_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/IntInputRow.ui', self)
        self.label.setText(arg_name)
        self.arg_name = arg_name

    def getVal(self):
        return self.spinBox.value()


class FunctionBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/FunctionBlock.ui', self)


class FunctionBlock(AbstractBlock):
    INPUT_ROW_TYPES = {bool: BoolInputRow, int: IntInputRow}

    def __init__(self, function, pos=(0, 0), parent=None):
        widget = FunctionBlockWidget()
        widget.label.setText(function.__name__)
        hints = typing.get_type_hints(function)
        data_hint = hints.pop('data', None)
        return_hint = hints.pop('return', None)

        self.inputRows = {}
        for arg_name, arg_type in hints.items():
            if arg_type in self.INPUT_ROW_TYPES:
                row = self.INPUT_ROW_TYPES[arg_type](arg_name=arg_name)
                self.inputRows[arg_name] = row
                widget.inputRowVerticalLayout.addWidget(row)

        super().__init__(widget, pos=pos, parent=parent)
        self.function = function

        self.inputNode = Node(self.widget.inputRadioButton, self,
                              allowed_type=data_hint, is_input=True)
        self.outputNode = Node(self.widget.outputRadioButton, self,
                               allowed_type=return_hint)
        self.nodes = [self.inputNode, self.outputNode]

        self.result = None
        self.errorBox = None

        self.widget.errorButton.clicked.connect(self.showErrorBox)
        self.widget.plotButton.clicked.connect(self.showPlot)

    def showPlot(self):
        if type(self.result) is pandas.DataFrame:
            self.plot = PlotWindow()
            self.plot.show()
            self.result.plot(ax=self.plot.axes)

    def showErrorBox(self):
        if self.errorBox is not None:
            self.errorBox.show()

    def propagate(self, val):
        self.widget.plotButton.setEnabled(False)
        self.plot = None
        try:
            kwargs = {arg_name: row.getVal()
                      for arg_name, row in self.inputRows.items()}
            self.result = self.function(data=val, **kwargs)
        except Exception as e:
            self.errorBox = QtWidgets.QMessageBox(0, 'Error', repr(e))
            self.widget.errorButton.setEnabled(True)
        else:
            self.errorBox = None
            self.widget.errorButton.setEnabled(False)
            if type(self.result) is pandas.DataFrame:
                self.widget.plotButton.setEnabled(True)
            if self.outputNode.edge:
                self.outputNode.edge.endBlock().propagate(self.result)
