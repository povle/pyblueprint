from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets, uic
from .. import Node
from .input_rows import INPUT_ROW_TYPES
import typing


class AbstractBlock(QtWidgets.QGraphicsRectItem):
    def __init__(self, uifile, function,
                 pos=(0, 0), parent=None, special_args=[]):
        self.nodes = []
        self.widget = BlockWidget(uifile=uifile, block=self)

        self.function = function
        hints = typing.get_type_hints(function)
        data_hint = hints.pop('data', None)
        return_hint = hints.pop('return', None)
        for arg in special_args:
            hints.pop(arg, None)

        self.inputRows = {}
        for arg_name, arg_type in hints.items():
            if arg_type in INPUT_ROW_TYPES:
                row = INPUT_ROW_TYPES[arg_type](arg_name=arg_name)
                self.inputRows[arg_name] = row
                self.widget.inputRowVerticalLayout.addWidget(row)

        QtWidgets.QGraphicsRectItem.__init__(self, 0, 0, 0, 0, parent=parent)
        self.setPos(*pos)

        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(*pos)
        self.updateSize()
        self.widget.label.setText(function.__name__)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))

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

    def updateSize(self):
        self.setRect(self.widget.pos().x(),
                     self.widget.pos().y(),
                     self.widget.width(),
                     self.widget.height())
        for node in self.nodes:
            node.updatePos()


class BlockWidget(QtWidgets.QWidget):
    def __init__(self, uifile, block: AbstractBlock, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(uifile, self)
        self.block = block

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.block.updateSize()
        return super().resizeEvent(a0)
