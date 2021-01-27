from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5 import QtGui, QtWidgets, uic

BLACK = QtGui.QColor(0, 0, 0)


class Edge(QtWidgets.QGraphicsLineItem):
    def __init__(self, a, b):
        super().__init__(*a, *b)
        self.a = a
        self.b = b
        self.setPen(QtGui.QPen(BLACK))

    def update(self, a=None, b=None):
        a = a or self.a
        b = b or self.b
        self.setLine(*a, *b)


class Node(QtWidgets.QRadioButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edge = None
        self.is_input = False

    def set_edge(self, edge: Edge):
        self.edge = edge

    def update_edge(self, pos):
        if self.edge is None:
            return
        if self.is_input:
            self.edge.update(b=pos)
        else:
            self.edge.update(a=pos)


class BlockItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, pos=(0, 0), label='None', parent=None):
        QtWidgets.QGraphicsRectItem.__init__(self, *pos, 0, 0,
                                             parent=parent)

        self.block = Block()
        self.block.label.setText(label)
        self.input_node = self.block.inputNode
        self.output_node = self.block.outputNode
        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.block)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(BLACK))
        self.setBrush(QtGui.QBrush(BLACK))
        self.setRect(*pos, self.block.width(), self.block.height())

    def input_node_pos(self):
        x = self.input_node.x() + self.x()
        y = self.input_node.y() + self.y()
        return (x, y)

    def output_node_pos(self):
        x = self.output_node.x() + self.x()
        y = self.output_node.y() + self.y()
        return (x, y)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            self.input_node.update_edge(self.input_node_pos())
            self.output_node.update_edge(self.output_node_pos())
        return super().itemChange(change, value)


class Block(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./Block.ui', self)
        self.inputNode.is_input = True


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./proto.ui', self)
        self.setWindowTitle('test')
        self.scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.rects = []

        self.addRectButton.clicked.connect(self.on_addRect_click)
        self.connectButton.clicked.connect(self.on_connect_click)

        self.keys = {45: self.zoom_out, 61: self.zoom_in}

    def on_connect_click(self):
        for a, b in zip(self.rects[:-1], self.rects[1:]):
            self.connect_blocks(a, b)

    def connect_blocks(self, a, b):
        edge = Edge(a.output_node_pos(), b.input_node_pos())
        a.output_node.set_edge(edge)
        b.input_node.set_edge(edge)
        self.scene.addItem(edge)

    def on_addRect_click(self):
        self.add_rect()
        print([(r.x(), r.y()) for r in self.rects])

    def add_rect(self):
        r = BlockItem()
        self.scene.addItem(r)
        self.rects.append(r)

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
    w = GUI()
    w.show()
    app.exec_()
