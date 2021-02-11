from PyQt5 import QtWidgets, uic
import typing
from .. import Node
from . import AbstractBlock


class OutputBlock(AbstractBlock):
    def __init__(self, pos=(0, 0), parent=None):
        super().__init__(OutputBlockWidget(), pos=pos, parent=parent)
        self.inputNode = Node(self.widget.inputRadioButton, self,
                              is_input=True,
                              allowed_type=typing.Union[str, int])
        self.nodes = [self.inputNode]

    def propagate(self, val):
        self.widget.label.setText(str(val))


class OutputBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/OutputBlock.ui', self)
