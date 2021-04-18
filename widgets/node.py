from PyQt5 import QtWidgets, QtCore
import typing
from . import Edge


class Node(QtWidgets.QGraphicsRectItem):
    def __init__(self, nodeWidget: QtWidgets.QRadioButton,
                 parent: QtWidgets.QGraphicsItem, allowed_type=None,
                 is_input=False):
        super().__init__(0, 0, nodeWidget.width(), nodeWidget.height(), parent)
        self.widget = nodeWidget
        self.widget.clicked.connect(self.onClick)
        self.updatePos()
        self.is_input = is_input
        self.allowed_type = allowed_type
        self.edge = None

    def onClick(self, checked):
        if not self.edge:
            node = self
        else:
            node = self.edge.start if self.is_input else self.edge.end
            self.removeEdge()
        self.widget.connecting.emit((node, self))

    def onConnectingStarted(self, node):
        if node is self:
            return
        if not self.compatibleWith(node):
            self.widget.setEnabled(False)

    def onConnectingStopped(self, node):
        self.widget.setEnabled(True)

    def removeEdge(self):
        if self.edge is not None:
            self.edge.remove()

    def setEdge(self, edge: Edge):
        self.removeEdge()
        self.edge = edge
        self.widget.setChecked(True)

    def centerPos(self):
        return (self.scenePos().x() + self.rect().width()/2,
                self.scenePos().y() + self.rect().height()/2)

    def updatePos(self):
        self.setPos(self.widget.x()+self.widget.parentWidget().x(),
                    self.widget.y()+self.widget.parentWidget().y())

    def updateEdge(self):
        if self.edge is not None:
            self.edge.updatePos()

    def connectTo(self, b):
        if self.is_input:
            edge = Edge(b, self)
        else:
            edge = Edge(self, b)
        self.setEdge(edge)
        b.setEdge(edge)
        self.scene().addItem(edge)

    def compatibleWith(self, b) -> bool:
        if self.parentItem() is b.parentItem():
            return False

        inp = self if self.is_input else b
        out = b if not b.is_input else self
        if inp is out:
            return False

        out_type = out.allowed_type
        in_type = inp.allowed_type
        if not issubclass(out_type, typing.get_args(in_type) or in_type):
            return False

        return True


class NodeWidget(QtWidgets.QRadioButton):
    connecting = QtCore.pyqtSignal(object)
