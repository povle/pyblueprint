from PyQt5 import QtWidgets, QtCore
import typing
from . import Edge


class Node(QtWidgets.QGraphicsRectItem):
    """Узел, соответствующий месту соединения блока и ребра."""

    def __init__(self, nodeWidget: QtWidgets.QRadioButton,
                 parent: QtWidgets.QGraphicsItem, allowedType=None,
                 isInput=False):
        super().__init__(0, 0, nodeWidget.width(), nodeWidget.height(), parent)
        self.edge = None
        self.widget = nodeWidget
        self.widget.clicked.connect(self.onClick)
        self.updatePos()
        self.isInput = isInput
        self.allowedType = allowedType

    def onClick(self, checked):
        """Обработать нажатие."""
        if not self.edge:
            node = self
        else:
            node = self.edge.start if self.isInput else self.edge.end
            self.removeEdge()
        self.widget.connecting.emit((node, self))

    def onConnectingStarted(self, node):
        """Обработать начало режима соединения."""
        if node is self:
            return
        if not self.compatibleWith(node):
            self.widget.setEnabled(False)

    def onConnectingStopped(self, node):
        """Обработать завершение режима соединения."""
        self.widget.setEnabled(True)

    def removeEdge(self):
        """Удалить ребро этого узла, если оно существует."""
        if self.edge is not None:
            self.edge.remove()

    def setEdge(self, edge: Edge):
        """Устанавливает ребро для этого узла."""
        self.removeEdge()
        self.edge = edge
        self.widget.setChecked(True)

    def centerPos(self):
        """Возвращает позицию центра узла в виде (x, y)."""
        return (self.scenePos().x() + self.rect().width()/2,
                self.scenePos().y() + self.rect().height()/2)

    def updatePos(self):
        """Обновить позицию узла."""
        self.setPos(self.widget.x()+self.widget.parentWidget().x(),
                    self.widget.y()+self.widget.parentWidget().y())
        self.updateEdge()

    def updateEdge(self):
        """Обновить позицию ребра этого узла, если оно существует."""
        if self.edge is not None:
            self.edge.updatePos()

    def connectTo(self, b):
        """Соединить узел с узлом b."""
        if self.isInput:
            edge = Edge(b, self)
        else:
            edge = Edge(self, b)
        self.setEdge(edge)
        b.setEdge(edge)
        self.scene().addItem(edge)

    def compatibleWith(self, b) -> bool:
        """Возвращает True если узел совместим с узлом b."""
        if self.parentItem() is b.parentItem():
            return False

        inp = self if self.isInput else b
        out = b if not b.isInput else self
        if inp is out:
            return False

        outType = out.allowedType
        inType = inp.allowedType
        if not issubclass(outType, typing.get_args(inType) or inType):
            return False

        return True


class NodeWidget(QtWidgets.QRadioButton):
    """Виджет, соответствующий узлу"""
    connecting = QtCore.pyqtSignal(object)
