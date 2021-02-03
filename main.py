from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtGui, QtWidgets, uic, QtCore
import inspect
import functions

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

    def startBlock(self):
        return self.start.parentItem()

    def endBlock(self):
        return self.end.parentItem()

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
        edge = Edge(self, b)
        self.setEdge(edge)
        b.setEdge(edge)
        self.scene().addItem(edge)


class NodeWidget(QtWidgets.QRadioButton):
    connecting = QtCore.pyqtSignal(object)


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
        self.setPen(QtGui.QPen(BLACK))
        self.setBrush(QtGui.QBrush(BLACK))

        self.nodes = []

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            [x.updateEdge() for x in self.nodes]
        return super().itemChange(change, value)

    def connectTo(self, b):
        self.outputNode.connectTo(b.inputNode)

    def acceptInput(self, val):
        raise NotImplementedError


class FunctionBlock(AbstractBlock):
    def __init__(self, function=functions.bypass, pos=(0, 0), parent=None):
        super().__init__(FunctionBlockWidget(), pos=pos, parent=parent)
        self.widget.label.setText(function.__name__)
        self.function = function
        self.inputNode = Node(self.widget.inputRadioButton, self, True)
        self.outputNode = Node(self.widget.outputRadioButton, self)
        self.nodes = [self.inputNode, self.outputNode]
        self.result = None

    def acceptInput(self, val):
        self.result = self.function(val)
        if self.outputNode.edge:
            self.outputNode.edge.endBlock().acceptInput(self.result)


class FunctionBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./FunctionBlock.ui', self)


class OutputBlock(AbstractBlock):
    def __init__(self, pos=(0, 0), parent=None):
        super().__init__(OutputBlockWidget(), pos=pos, parent=parent)
        self.inputNode = Node(self.widget.inputRadioButton, self, True)
        self.nodes = [self.inputNode]

    def acceptInput(self, val):
        self.widget.label.setText(str(val))


class OutputBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./OutputBlock.ui', self)


class InputBlock(AbstractBlock):
    def __init__(self, pos=(0, 0), parent=None):
        super().__init__(InputBlockWidget(), pos=pos, parent=parent)
        self.outputNode = Node(self.widget.outputRadioButton, self)
        self.nodes = [self.outputNode]

    def startChain(self):
        val = self.widget.lineEdit.text()
        if self.outputNode.edge:
            self.outputNode.edge.endBlock().acceptInput(val)


class InputBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./InputBlock.ui', self)


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = []
        self.connectingLine = None
        self.connectingFrom = None
        self.inputBlock = InputBlock((0, -50))
        self.addBlock(self.inputBlock)
        self.outputBlock = OutputBlock((0, 50))
        self.addBlock(self.outputBlock)

    def addBlock(self, block: AbstractBlock):
        self.addItem(block)
        self.blocks.append(block)
        for node in block.nodes:
            node.widget.connecting.connect(self.onConnecting)

    def addFunctionBlock(self, function):
        self.addBlock(FunctionBlock(function))

    def onConnecting(self, nodes: tuple):
        mousePos = self.parent().mapFromGlobal(QtGui.QCursor.pos())
        mousePos = self.parent().mapToScene(mousePos)
        mousePos = (mousePos.x(), mousePos.y())

        # nodes[0] is the node we are connecting from, nodes[1] is the sender
        if self.connectingLine is None:
            self.connectingFrom = nodes[0]
            self.connectingFrom.widget.setChecked(True)
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
                a.connectTo(b)

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

    def run(self):
        self.inputBlock.startChain()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./proto.ui', self)
        self.setWindowTitle('test')
        self.scene = Scene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)

        self.addBlockButton.clicked.connect(self.addFunctionBlock)
        self.runButton.clicked.connect(self.scene.run)

        self.functions = {name: func for name, func in
                          inspect.getmembers(functions,
                                             predicate=inspect.isfunction)}

        self.functionSelectBox.addItems(sorted(self.functions.keys()))

        self.keys = {
                    45: self.zoom_out,  # -
                    61: self.zoom_in,  # +
                    16777216: self.scene.stopConnecting,  # esc
                     }

    def addFunctionBlock(self):
        function = self.functions[self.functionSelectBox.currentText()]
        self.scene.addFunctionBlock(function)

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
