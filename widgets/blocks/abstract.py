from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets, uic
from .. import Node
import typing


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


class AbstractBlock(QtWidgets.QGraphicsRectItem):
    INPUT_ROW_TYPES = {bool: BoolInputRow, int: IntInputRow}

    def __init__(self, widget, function,
                 pos=(0, 0), parent=None, special_args=[]):

        self.function = function
        hints = typing.get_type_hints(function)
        data_hint = hints.pop('data', None)
        return_hint = hints.pop('return', None)
        for arg in special_args:
            hints.pop(arg, None)

        self.inputRows = {}
        for arg_name, arg_type in hints.items():
            if arg_type in self.INPUT_ROW_TYPES:
                row = self.INPUT_ROW_TYPES[arg_type](arg_name=arg_name)
                self.inputRows[arg_name] = row
                widget.inputRowVerticalLayout.addWidget(row)

        QtWidgets.QGraphicsRectItem.__init__(self, 0, 0, 0, 0, parent=parent)
        self.setPos(*pos)

        self.widget = widget
        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(*pos)
        self.setRect(*pos, self.widget.width(), self.widget.height())
        widget.label.setText(function.__name__)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))

        self.nodes = []
        if data_hint is not None:
            self.inputNode = Node(self.widget.inputRadioButton, self,
                                  allowed_type=data_hint, is_input=True)
            self.nodes.append(self.inputNode)
        self.outputNode = Node(self.widget.outputRadioButton, self,
                               allowed_type=return_hint)
        self.nodes.append(self.outputNode)

        self.result = None
        self.errorBox = None

        self.widget.errorButton.clicked.connect(self.showErrorBox)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            [x.updateEdge() for x in self.nodes]
        return super().itemChange(change, value)

    def connectTo(self, b):
        self.outputNode.connectTo(b.inputNode)

    def showErrorBox(self):
        if self.errorBox is not None:
            self.errorBox.show()

    def executeFunction(self, *args, **kwargs):
        try:
            kwargs.update({arg_name: row.getVal()
                           for arg_name, row in self.inputRows.items()})
            return self.function(*args, **kwargs)
        except Exception as e:
            self.errorBox = QtWidgets.QMessageBox(0, 'Error', repr(e))
            self.widget.errorButton.setEnabled(True)
            return None

    def processData(self, data):
        raise NotImplementedError

    def propagate(self, data):
        self.result = self.processData(data)
        if self.outputNode.edge and self.result is not None:
            self.outputNode.edge.endBlock().propagate(self.result)
