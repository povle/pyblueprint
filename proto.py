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
        self.widget.connecting.emit(node)

    def setEdge(self, edge: Edge):
        if self.edge:
            self.scene().removeItem(self.edge)
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

    def addBlock(self):
        block = Block()
        self.addItem(block)
        self.blocks.append(block)
        block.inputNode.widget.connecting.connect(self.onConnecting)
        block.outputNode.widget.connecting.connect(self.onConnecting)

    def connectAllBlocks(self):
        for a, b in zip(self.blocks[:-1], self.blocks[1:]):
            self.connectBlocks(a, b)

    def connectBlocks(self, a: Block, b: Block):
        edge = Edge(a.outputNode, b.inputNode)
        a.outputNode.setEdge(edge)
        b.inputNode.setEdge(edge)
        self.addItem(edge)

    def onConnecting(self, node: Node):
        mousePos = self.parent().mapFromGlobal(QtGui.QCursor.pos())
        mousePos = self.parent().mapToScene(mousePos)
        mousePos = (mousePos.x(), mousePos.y())
        if self.connectingLine is None:
            self.connectingLine = Line(node.centerPos(), mousePos)
            self.addItem(self.connectingLine)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        mousePos = (event.scenePos().x(), event.scenePos().y())
        if self.connectingLine is not None:
            self.connectingLine.updatePos(endPos=mousePos)
        return super().mouseMoveEvent(event)


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

        self.keys = {45: self.zoom_out, 61: self.zoom_in}

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        self.keys.get(key, lambda: None)()

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


'''
https://doc.qt.io/qt-5/qtwidgets-graphicsview-diagramscene-example.html
что переделать:
# общую структуру
вынести сцену из окна
за соединение должна отвечать вся сцена - это объективно другой режим
объекты должны быть абстрактнее - BlockItem должен наследоваться не от QtWidgets.QGraphicsRectItem, а от некого AbstractSceneItem
мб не совсем так но энивей должна быть возможность нацепить на конец стрелки невидимый объект - тогда будет нормально работать скролл и все такое
то есть: на неактивной ноде лежит этот невидимый объект. когда мы двигаем весь блок то объект двигаем вместе с ней "вручную".
когда схватились за объект то оставляем стандартное поведение. когда его отпустили то надо проверить где он лежит - если на противоположной ноде другого блока то сцепляем.
очень ли это нужно? хз. попробовать имплементировать пример по ссылке.
разобраться с системой координат, то что ноды не знают где они - не норма.
'''
