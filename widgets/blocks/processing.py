from PyQt5 import QtWidgets, uic
from . import AbstractBlock


class ProcessingBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(widget=ProcessingBlockWidget(),
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['path'])

    def processData(self, data):
        return self.executeFunction(data=data)


class ProcessingBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/ProcessingBlock.ui', self)
