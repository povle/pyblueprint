from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets, uic, QtCore

BLACK = QtGui.QColor(0, 0, 0)


class Line(QtWidgets.QGraphicsLineItem):
    def __init__(self, startPos: tuple, endPos: tuple):
        super().__init__(*startPos, *endPos)
        self.startPos = startPos
        self.endPos = endPos
        self.setPen(QtGui.QPen(BLACK))

    def updatePos(self, startPos=None, endPos=None):
        self.startPos = startPos or self.startPos
        self.endPos = endPos or self.endPos
        self.setLine(*self.startPos, *self.endPos)


class Edge(Line):
    def __init__(self, start, end):
        super().__init__(start.centerPos(), end.centerPos())
        self.start = start
        self.end = end

    def updatePos(self):
        super().updatePos(self.start.centerPos(), self.end.centerPos())

    def remove(self):
        self.start.edge = None
        self.start.widget.setChecked(False)
        self.end.edge = None
        self.end.widget.setChecked(False)
        self.scene().removeItem(self)


class Node(QtWidgets.QGraphicsRectItem):
    def __init__(self, nodeWidget: QtWidgets.QRadioButton,
                 parent: QtWidgets.QGraphicsItem, is_input=False):
        super().__init__(0, 0, nodeWidget.width(), nodeWidget.height(), parent)
        self.widget = nodeWidget
        self.widget.clicked.connect(self.onClick)
        self.setPos(nodeWidget.x(), nodeWidget.y())
        self.is_input = is_input
        self.edge = None

    def onClick(self, checked):
        if not self.edge:
            node = self
        else:
            node = self.edge.start if self.is_input else self.edge.end
            self.removeEdge()
        node.widget.setChecked(True)
        self.widget.connecting.emit((node, self))

    def removeEdge(self):
        if self.edge:
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


class NodeWidget(QtWidgets.QRadioButton):
    connecting = QtCore.pyqtSignal(object)


class Block(QtWidgets.QGraphicsRectItem):
    def __init__(self, pos=(0, 0), label='None', parent=None):
        QtWidgets.QGraphicsRectItem.__init__(self, *pos, 0, 0, parent=parent)

        self.widget = BlockWidget()
        self.widget.label.setText(label)
        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.setRect(*pos, self.widget.width(), self.widget.height())

        self.inputNode = Node(self.widget.inputRadioButton, self, True)
        self.outputNode = Node(self.widget.outputRadioButton, self)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(BLACK))
        self.setBrush(QtGui.QBrush(BLACK))

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            self.inputNode.updateEdge()
            self.outputNode.updateEdge()
        return super().itemChange(change, value)


class BlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./Block.ui', self)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = []
        self.connectingLine = None
        self.connectingFrom = None

    def addBlock(self):
        block = Block()
        self.addItem(block)
        self.blocks.append(block)
        block.inputNode.widget.connecting.connect(self.onConnecting)
        block.outputNode.widget.connecting.connect(self.onConnecting)

    def connectAllBlocks(self):
        for a, b in zip(self.blocks[:-1], self.blocks[1:]):
            self.connectBlocks(a, b)

    def connectNodes(self, a: Node, b: Node):
        edge = Edge(a, b)
        a.setEdge(edge)
        b.setEdge(edge)
        self.addItem(edge)

    def connectBlocks(self, a: Block, b: Block):
        self.connectNodes(a.outputNode, b.inputNode)

    def onConnecting(self, nodes: tuple):
        mousePos = self.parent().mapFromGlobal(QtGui.QCursor.pos())
        mousePos = self.parent().mapToScene(mousePos)
        mousePos = (mousePos.x(), mousePos.y())

        # nodes[0] is the node we are connecting from, nodes[1] is the sender
        if self.connectingLine is None:
            self.connectingFrom = nodes[0]
            self.connectingLine = Line(nodes[0].centerPos(), mousePos)
            self.addItem(self.connectingLine)
        else:
            connectingTo = nodes[1]
            connectingFrom = self.connectingFrom
            self.stopConnecting()
            connectingTo.widget.setChecked(False)
            a = connectingFrom if connectingTo.is_input else connectingTo
            b = connectingFrom if connectingFrom.is_input else connectingTo
            if a is not b and a.parentItem() is not b.parentItem():
                self.connectNodes(a, b)

    def stopConnecting(self):
        if self.connectingLine is not None:
            self.removeItem(self.connectingLine)
        if self.connectingFrom is not None:
            self.connectingFrom.widget.setChecked(False)
        self.connectingLine = None
        self.connectingFrom = None

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if self.connectingLine is not None:
            mousePos = (event.scenePos().x(), event.scenePos().y())
            self.connectingLine.updatePos(endPos=mousePos)
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        items = self.items(event.scenePos())
        if not any(type(x) is Node for x in items):
            self.stopConnecting()
        return super().mousePressEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./proto.ui', self)
        self.setWindowTitle('test')
        self.scene = Scene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)

        self.addRectButton.clicked.connect(self.scene.addBlock)
        self.connectButton.clicked.connect(self.scene.connectAllBlocks)

        self.keys = {
                    45: self.zoom_out,  # -
                    61: self.zoom_in,  # +
                    16777216: self.scene.stopConnecting,  # esc
                     }

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        self.keys.get(key, lambda: None)()
        super().keyPressEvent(event)

    def zoom_out(self):
        self.zoom(zoom_out=True)

    def zoom_in(self):
        self.zoom(zoom_out=False)

    def zoom(self, zoom_out):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        if not zoom_out:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.graphicsView.scale(zoomFactor, zoomFactor)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    app.exec_()
