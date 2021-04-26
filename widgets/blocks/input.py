import inspect
from PyQt5.QtWidgets import QFileDialog
from . import AbstractBlock


class InputBlock(AbstractBlock):
    """Блок получения данных."""

    def __init__(self, function, pos=(0, 0), parent=None, movable=True):
        super().__init__(uifile='./ui/InputBlock.ui',
                         function=function,
                         pos=pos,
                         parent=parent,
                         specialArgs=['path'],
                         movable=movable)

        self.widget.fileOpenButton.clicked.connect(self.openFileDialog)
        self.filePath = None

        doc = inspect.getdoc(function)
        self.fileFilter = '*' if not doc else doc.splitlines()[0]

    def openFileDialog(self):
        """Открыть окно выбора файла и обработать результат."""
        filePath = QFileDialog.getOpenFileName(self.widget,
                                               'Выбрать файл',
                                               self.filePath or '.',
                                               f'({self.fileFilter})')[0]
        self.filePath = filePath or self.filePath
        if not self.filePath:
            self.widget.fileLabel.setText('Нет')
        else:
            self.widget.fileLabel.setText(self.filePath)

    def processData(self, data):
        if self.filePath is not None:
            return self.executeFunction(path=self.filePath)
