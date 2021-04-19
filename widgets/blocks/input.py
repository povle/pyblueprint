import inspect
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from . import AbstractBlock


class InputBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(uifile='./ui/InputBlock.ui',
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['path'])

        self.widget.fileOpenButton.clicked.connect(self.openFileDialog)
        self.file_path = None

        doc = inspect.getdoc(function)
        self.file_filter = '*' if not doc else doc.splitlines()[0]

    def openFileDialog(self):
        file_path = QFileDialog.getOpenFileName(self.widget,
                                                'Select a file',
                                                self.file_path or '.',
                                                f'({self.file_filter})')[0]
        self.file_path = file_path or self.file_path
        if not self.file_path:
            self.widget.fileLabel.setAlignment(QtCore.Qt.AlignLeft)
            self.widget.fileLabel.setText('None')
        else:
            self.widget.fileLabel.setAlignment(QtCore.Qt.AlignRight)
            self.widget.fileLabel.setText(self.file_path)

    def processData(self, data):
        if self.file_path is not None:
            return self.executeFunction(path=self.file_path)
