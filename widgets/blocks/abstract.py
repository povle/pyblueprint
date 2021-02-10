from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets


class AbstractBlock(QtWidgets.QGraphicsRectItem):
    def __init__(self, widget, pos=(0, 0), parent=None):
        QtWidgets.QGraphicsRectItem.__init__(self, 0, 0, 0, 0, parent=parent)
        self.setPos(*pos)

        self.widget = widget
        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(*pos)
        self.setRect(*pos, self.widget.width(), self.widget.height())

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))

        self.nodes = []

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            [x.updateEdge() for x in self.nodes]
        return super().itemChange(change, value)

    def connectTo(self, b):
        self.outputNode.connectTo(b.inputNode)

    def acceptInput(self, val):
        raise NotImplementedError
