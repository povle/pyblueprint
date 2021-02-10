from PyQt5 import QtWidgets, uic
from .. import Node
from . import AbstractBlock


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
        uic.loadUi('./ui/InputBlock.ui', self)
