import inspect
from PyQt5.QtWidgets import QFileDialog
from . import AbstractBlock


class OutputBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None, movable=True):
        super().__init__(uifile='./ui/OutputBlock.ui',
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['path'],
                         movable=movable)

        self.widget.fileOpenButton.clicked.connect(self.openFileDialog)
        self.file_path = None

        doc = inspect.getdoc(function)
        self.file_filter = '*' if not doc else doc.splitlines()[0]

    def openFileDialog(self):
        file_path = QFileDialog.getSaveFileName(self.widget,
                                                'Select a file',
                                                self.file_path or '.',
                                                f'({self.file_filter})')[0]
        self.file_path = file_path
        if file_path:
            self.executeFunction(data=self.result, path=self.file_path)

    def processData(self, data):
        self.result = data
        self.widget.fileOpenButton.setEnabled(True)
        return data
