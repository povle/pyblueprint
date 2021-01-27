from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5 import QtGui, QtWidgets, uic

BLACK = QtGui.QColor(0, 0, 0)


class Edge(QtWidgets.QGraphicsLineItem):
    def __init__(self, a, b):
        super().__init__(*a, *b)
        self.setPen(QtGui.QPen(BLACK))
        self.setBrush(QtGui.QBrush(BLACK))

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
        self.update_edge()

    def update_edge(self):
        if self.edge is None:
            return
        pos = (self.x(), self.y())
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
        self.proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.block)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)
        self.setPen(QtGui.QPen(BLACK))
        self.setBrush(QtGui.QBrush(BLACK))
        self.setRect(*pos, self.block.width(), self.block.height())


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
        self.rects = set()

        self.addRectButton.clicked.connect(self.on_click)

        self.keys = {45: self.zoom_out, 61: self.zoom_in}

    def on_click(self):
        self.add_rect()
        print([(r.x(), r.y()) for r in self.rects])

    def add_rect(self):
        r = BlockItem()
        self.scene.addItem(r)
        self.rects.add(r)

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
