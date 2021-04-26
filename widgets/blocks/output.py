import inspect
from PyQt5.QtWidgets import QFileDialog
from . import AbstractBlock


class OutputBlock(AbstractBlock):
    """Блок сохранения данных."""

    def __init__(self, function, pos=(0, 0), parent=None, movable=True):
        super().__init__(uifile='./ui/OutputBlock.ui',
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
        filePath = QFileDialog.getSaveFileName(self.widget,
                                               'Выбрать файл',
                                               self.filePath or '.',
                                               f'({self.fileFilter})')[0]
        self.filePath = filePath
        if filePath:
            self.executeFunction(data=self.result, path=self.filePath)

    def processData(self, data):
        self.result = data
        self.widget.fileOpenButton.setEnabled(True)
        return data
