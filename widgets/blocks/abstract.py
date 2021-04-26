from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets, uic
from .. import Node
from .input_rows import INPUT_ROW_TYPES
import typing


class AbstractBlock(QtWidgets.QGraphicsRectItem):
    """
    Абстрактный блок.

    Реализует все необходимые блоку методы, кроме processData.
    """

    def __init__(self, uifile, function,
                 pos=(0, 0), parent=None, specialArgs=[], movable=True):
        self.nodes = []
        self.widget = BlockWidget(uifile=uifile, block=self)

        self.function = function
        hints = typing.get_type_hints(function)
        dataHint = hints.pop('data', None)
        returnHint = hints.pop('return', None)
        for arg in specialArgs:
            hints.pop(arg, None)

        self.inputRows = {}
        for argName, argType in hints.items():
            if argType in INPUT_ROW_TYPES:
                row = INPUT_ROW_TYPES[argType](argName=argName)
                self.inputRows[argName] = row
                self.widget.inputRowVerticalLayout.addWidget(row)

        QtWidgets.QGraphicsRectItem.__init__(self, 0, 0, 0, 0, parent=parent)
        self.setPos(*pos)

        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(*pos)
        self.updateSize()
        self.widget.label.setText(function.__name__)

        self.setMovable(movable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))

        if dataHint is not None:
            self.inputNode = Node(self.widget.inputRadioButton, self,
                                  allowedType=dataHint, isInput=True)
            self.nodes.append(self.inputNode)
        self.outputNode = Node(self.widget.outputRadioButton, self,
                               allowedType=returnHint)
        self.nodes.append(self.outputNode)

        self.result = None
        self.errorBox = None

        self.widget.errorButton.clicked.connect(self.showErrorBox)
        self.widget.removeButton.clicked.connect(self.remove)

    def itemChange(self, change, value):
        """Обработать изменение позиции блока."""
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            [x.updateEdge() for x in self.nodes]
        return super().itemChange(change, value)

    def connectTo(self, b):
        """Соединить блок с блоком b."""
        self.outputNode.connectTo(b.inputNode)

    def showErrorBox(self):
        """Показать сообщение об ошибке."""
        if self.errorBox is not None:
            self.errorBox.show()

    def remove(self):
        """Удалить блок."""
        for node in self.nodes:
            node.removeEdge()
        self.scene().removeItem(self)

    def executeFunction(self, *args, **kwargs):
        """
        Выполнить функцию блока.

        Возвращает ее результат при успешном выполнении, None при исключении.
        """
        try:
            kwargs.update({argName: row.getVal()
                           for argName, row in self.inputRows.items()})
            res = self.function(*args, **kwargs)
        except Exception as e:
            self.errorBox = QtWidgets.QMessageBox(0, 'Ошибка', repr(e))
            self.widget.errorButton.setEnabled(True)
            return None
        else:
            if self.errorBox is not None:
                self.errorBox.deleteLater()
                self.errorBox = None
            self.widget.errorButton.setEnabled(False)
            return res

    def setMovable(self, state: bool):
        """Изменить подвижность блока."""
        self.setFlag(QGraphicsItem.ItemIsMovable, state)

    def processData(self, data):
        """Обработать входящие данные."""
        raise NotImplementedError

    def propagate(self, data):
        """Передать результат выполнения в следующий блок цепочки."""
        self.result = self.processData(data)
        if self.outputNode.edge and self.result is not None:
            self.outputNode.edge.endBlock().propagate(self.result)

    def updateSize(self):
        """Обновить размер блока."""
        self.setRect(self.widget.pos().x(),
                     self.widget.pos().y(),
                     self.widget.width(),
                     self.widget.height())
        for node in self.nodes:
            node.updatePos()


class BlockWidget(QtWidgets.QWidget):
    """Виджет, соответствующий блоку."""

    def __init__(self, uifile, block: AbstractBlock, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(uifile, self)
        self.block = block

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        """Обработать изменение размеров виджета."""
        self.block.updateSize()
        return super().resizeEvent(a0)
