from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog
from .. import Node
from . import AbstractBlock


class FileInputBlock(AbstractBlock):
    def __init__(self, pos=(0, 0), parent=None):
        super().__init__(InputBlockWidget(), pos=pos, parent=parent)
        self.outputNode = Node(self.widget.outputRadioButton, self,
                               allowed_type=str)
        self.nodes = [self.outputNode]
        self.widget.fileOpenButton.clicked.connect(self.openFileDialog)
        self.file_name = ''
        self.result = None

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(self.widget, 'Select a file',
                                                '.', 'Text files (*.txt)')[0]
        self.file_name = file_name or self.file_name
        if not self.file_name:
            self.widget.label.setAlignment(QtCore.Qt.AlignHCenter)
            self.widget.label.setText('Select a file...')
            self.result = None
        else:
            self.widget.label.setAlignment(QtCore.Qt.AlignRight)
            self.widget.label.setText(self.file_name)
            with open(self.file_name) as f:
                self.result = f.read().replace('\n', '')

    def startChain(self):
        if self.outputNode.edge and self.result:
            self.outputNode.edge.endBlock().acceptInput(self.result)


class InputBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/FileInputBlock.ui', self)
