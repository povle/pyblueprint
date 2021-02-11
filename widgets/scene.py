from PyQt5 import QtGui, QtWidgets, QtCore
from . import Node, Line
from .blocks import AbstractBlock, FunctionBlock, FileInputBlock, OutputBlock


class Scene(QtWidgets.QGraphicsScene):
    connectingStarted = QtCore.pyqtSignal(object)
    connectingStopped = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = []
        self.connectingLine = None
        self.connectingFrom = None
        self.inputBlock = FileInputBlock((0, -50))
        self.addBlock(self.inputBlock)
        self.outputBlock = OutputBlock((0, 50))
        self.addBlock(self.outputBlock)

    def addBlock(self, block: AbstractBlock):
        self.addItem(block)
        self.blocks.append(block)
        for node in block.nodes:
            node.widget.connecting.connect(self.onConnecting)
            self.connectingStarted.connect(node.onConnectingStarted)
            self.connectingStopped.connect(node.onConnectingStopped)

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
            self.connectingStarted.emit(nodes[0])
        else:
            connectingTo = nodes[1]
            connectingFrom = self.connectingFrom
            self.stopConnecting()
            connectingTo.widget.setChecked(False)
            if connectingFrom.compatibleWith(connectingTo):
                connectingFrom.connectTo(connectingTo)

    def stopConnecting(self):
        if self.connectingLine is not None:
            self.removeItem(self.connectingLine)
        if self.connectingFrom is not None:
            self.connectingFrom.widget.setChecked(False)
        connectingFrom = self.connectingFrom
        self.connectingLine = None
        self.connectingFrom = None
        self.connectingStopped.emit(connectingFrom)

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if self.connectingLine is not None:
            mousePos = (event.scenePos().x(), event.scenePos().y())
            self.connectingLine.updatePos(endPos=mousePos)
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        items = self.items(event.scenePos())
        if self.connectingFrom and\
            not any(type(x) is Node and x.compatibleWith(self.connectingFrom)
                    for x in items):
            self.stopConnecting()
        else:
            return super().mousePressEvent(event)

    def run(self):
        self.inputBlock.propagate()
