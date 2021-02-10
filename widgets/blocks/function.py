from PyQt5 import QtWidgets, uic
import typing
from .. import Node
from . import AbstractBlock


class FunctionBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(FunctionBlockWidget(), pos=pos, parent=parent)
        self.widget.label.setText(function.__name__)
        self.function = function
        hints = typing.get_type_hints(function)
        data_hint = hints.get('data', None)
        return_hint = hints.get('return', None)

        self.inputNode = Node(self.widget.inputRadioButton, self,
                              allowed_type=data_hint, is_input=True)
        self.outputNode = Node(self.widget.outputRadioButton, self,
                               allowed_type=return_hint)
        self.nodes = [self.inputNode, self.outputNode]
        self.result = None

    def acceptInput(self, val):
        self.result = self.function(data=val)
        if self.outputNode.edge:
            self.outputNode.edge.endBlock().acceptInput(self.result)


class FunctionBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/FunctionBlock.ui', self)
