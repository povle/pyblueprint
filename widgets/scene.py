from PyQt5 import QtGui, QtWidgets, QtCore
from . import Node, Line
from .blocks import AbstractBlock, InputBlock


class Scene(QtWidgets.QGraphicsScene):
    """Сцена, содержащая блоки."""

    connectingStarted = QtCore.pyqtSignal(object)
    connectingStopped = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = []
        self.connectingLine = None
        self.connectingFrom = None
        self.movable = True

    def _addBlock(self, block: AbstractBlock):
        """Добавить существующий блок."""
        self.addItem(block)
        self.blocks.append(block)
        for node in block.nodes:
            node.widget.connecting.connect(self.onConnecting)
            self.connectingStarted.connect(node.onConnectingStarted)
            self.connectingStopped.connect(node.onConnectingStopped)

    def addBlock(self, function, blockClass, pos=(0, 0)):
        """Инициализировать и добавить блок."""
        self._addBlock(blockClass(function=function,
                                  pos=pos,
                                  movable=self.movable))

    def onConnecting(self, nodes: tuple):
        """Обработать начало или завершения соединения блоков."""
        mousePos = self.parent().mapFromGlobal(QtGui.QCursor.pos())
        mousePos = self.parent().mapToScene(mousePos)
        mousePos = (mousePos.x(), mousePos.y())

        # nodes[0] is the node we are connecting from, nodes[1] is the sender
        if self.connectingLine is None:
            self.connectingFrom = nodes[0]
            self.connectingFrom.widget.setChecked(True)
            self.connectingLine = Line(nodes[0].centerPos(), mousePos)
            self.addItem(self.connectingLine)
            self.connectingStarted.emit(nodes[0])
        else:
            connectingTo = nodes[1]
            connectingFrom = self.connectingFrom
            self.stopConnecting()
            connectingTo.widget.setChecked(False)
            if connectingFrom.compatibleWith(connectingTo):
                connectingFrom.connectTo(connectingTo)

    def stopConnecting(self):
        """Выйти из режима соединения блоков."""
        if self.connectingLine is not None:
            self.removeItem(self.connectingLine)
        if self.connectingFrom is not None:
            self.connectingFrom.widget.setChecked(False)
        connectingFrom = self.connectingFrom
        self.connectingLine = None
        self.connectingFrom = None
        self.connectingStopped.emit(connectingFrom)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """Обработать движение мыши."""
        if self.connectingLine is not None:
            mousePos = (event.scenePos().x(), event.scenePos().y())
            self.connectingLine.updatePos(endPos=mousePos)
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        """Обработать нажатие мыши."""
        items = self.items(event.scenePos())
        if self.connectingFrom and\
            not any(type(x) is Node and x.compatibleWith(self.connectingFrom)
                    for x in items):
            self.stopConnecting()
        else:
            return super().mousePressEvent(event)

    def dragMoveEvent(self, event: QtWidgets.QGraphicsSceneDragDropEvent):
        """Обработать перетаскивание заголовка функции."""
        mimeData = event.mimeData()
        if mimeData.hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            return super().dragMoveEvent(event)

    def dropEvent(self, event: QtWidgets.QGraphicsSceneDragDropEvent):
        """Обработать завершение перетаскивания заголовка функции."""
        mimeData = event.mimeData()
        if mimeData.hasFormat('application/x-qabstractitemmodeldatalist'):
            item = event.source().selectedItems()[0]
            if item.type() == 1001:
                pos = (event.scenePos().x()/2,
                       event.scenePos().y()/2)
                self.addBlock(function=item.function,
                              blockClass=item.blockClass,
                              pos=pos)
            event.accept()
        else:
            return super().dropEvent(event)

    def setPositionsFixed(self, state: bool):
        """Зафиксировать позиции блоков."""
        self.movable = not state
        for block in self.blocks:
            block.setMovable(not state)

    def run(self):
        """Запустить выполнение цепочки блоков."""
        for block in self.blocks:
            if type(block) is InputBlock:
                block.propagate(None)
