from PyQt5 import QtWidgets, QtCore
from . import Edge


class Node(QtWidgets.QGraphicsRectItem):
    def __init__(self, nodeWidget: QtWidgets.QRadioButton,
                 parent: QtWidgets.QGraphicsItem, is_input=False):
        super().__init__(0, 0, nodeWidget.width(), nodeWidget.height(), parent)
        self.widget = nodeWidget
        self.widget.clicked.connect(self.onClick)
        self.setPos(nodeWidget.x()+nodeWidget.parentWidget().x(),
                    nodeWidget.y()+nodeWidget.parentWidget().y())
        self.is_input = is_input
        self.edge = None

    def onClick(self, checked):
        if not self.edge:
            node = self
        else:
            node = self.edge.start if self.is_input else self.edge.end
            self.removeEdge()
        self.widget.connecting.emit((node, self))

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
        identity_compatible = self.parentItem() is not b.parentItem()
        input_compatible = (self.is_input and not b.is_input or
                            not self.is_input and b.is_input)
        return identity_compatible and input_compatible


class NodeWidget(QtWidgets.QRadioButton):
    connecting = QtCore.pyqtSignal(object)
