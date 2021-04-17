from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog
from . import AbstractBlock


class InputBlock(AbstractBlock):
    def __init__(self, function, pos=(0, 0), parent=None):
        super().__init__(widget=InputBlockWidget(),
                         function=function,
                         pos=pos,
                         parent=parent,
                         special_args=['path'])

        self.widget.fileOpenButton.clicked.connect(self.openFileDialog)
        self.file_path = None

    def openFileDialog(self):
        file_path = QFileDialog.getOpenFileName(self.widget, 'Select a file',
                                                '.', 'CSV files (*.csv)')[0]
        self.file_path = file_path or self.file_path
        if not self.file_path:
            # FIXME: для имени файла должно быть отдельное поле
            self.widget.label.setAlignment(QtCore.Qt.AlignHCenter)
            self.widget.label.setText('Select a file...')
        else:
            self.widget.label.setAlignment(QtCore.Qt.AlignRight)
            self.widget.label.setText(self.file_path)

    def processData(self, data):
        if self.file_path is not None:
            return self.executeFunction(path=self.file_path)


class InputBlockWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/FileInputBlock.ui', self)
