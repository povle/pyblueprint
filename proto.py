from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsView
from PyQt5 import QtGui, QtWidgets, uic, QtCore

BLACK = QtGui.QColor(0, 0, 0)


class Edge(QtWidgets.QGraphicsLineItem):
    def __init__(self, a, b):
        super().__init__(*a, *b)
        self.a = a
        self.b = b
        self.setPen(QtGui.QPen(BLACK))

    def update(self, a=None, b=None):
        self.a = a or self.a
        self.b = b or self.b
        self.setLine(*self.a, *self.b)


# class NodeItem(QtWidgets.QGraphicsRectItem):
#     def __init__(self, pos=(0, 0), parent=None):
#         QtWidgets.QGraphicsRectItem.__init__(self, *pos, 0, 0,
#                                              parent=parent)
#         self.node = Node('')
#         self.proxy = QtWidgets.QGraphicsProxyWidget(self)
#         self.proxy.setWidget(self.node)


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

        self.connecting = False
        self.connecting_from_input = False

    def node_pos(self, node):
        x = node.x() + node.width()/2 + self.x()
        y = node.y() + node.height()/2 + self.y()
        return (x, y)

    def in_node(self, point, node):
        pos = self.node_pos(node)
        return all(abs(a-b) < c/2 for a, b, c in
                   zip(point, pos, (node.width(), node.height())))

    def input_node_pos(self):
        return self.node_pos(self.input_node)

    def output_node_pos(self):
        return self.node_pos(self.output_node)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            self.input_node.update_edge(self.input_node_pos())
            self.output_node.update_edge(self.output_node_pos())
        return super().itemChange(change, value)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        pos = event.buttonDownScenePos(QtCore.Qt.LeftButton)
        if pos:
            if self.in_node((pos.x(), pos.y()), self.input_node):
                self.connecting = True
                self.connecting_from_input = True
                node = self.input_node
            elif self.in_node((pos.x(), pos.y()), self.output_node):
                self.connecting = True
                self.connecting_from_input = False
                node = self.output_node
        if self.connecting:
            edge = Edge(self.node_pos(node), self.node_pos(node))
            self.scene().addItem(edge)
            node.set_edge(edge)
        else:
            return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        pos = (event.pos().x(), event.pos().y())
        if self.connecting:
            if self.connecting_from_input:
                self.input_node.edge.update(a=pos)
            else:
                self.output_node.edge.update(b=pos)
        else:
            return super().mouseMoveEvent(event)


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
