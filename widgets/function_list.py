from PyQt5 import QtWidgets, QtCore
from types import ModuleType
from typing import Callable, Type
from .blocks import AbstractBlock
import inspect


class FunctionListItem(QtWidgets.QListWidgetItem):
    """Элемент списка функций."""

    def __init__(self,
                 function: Callable,
                 blockClass: Type[AbstractBlock],
                 name: str,
                 parent: QtWidgets.QListWidget):
        super().__init__(name, parent, 1001)
        self.function = function
        self.blockClass = blockClass
        self.setToolTip(inspect.getdoc(function))


class FunctionList(QtWidgets.QListWidget):
    """Список функций."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = {}

    def addFunctions(self, module: ModuleType,
                     blockClass: Type[AbstractBlock],
                     sepTitle=None):
        """Добавить в список модуль функций."""
        if sepTitle is not None:
            self.insertSeparator(sepTitle)
        functions = dict(inspect.getmembers(module,
                                            predicate=inspect.isfunction))
        self.functions.update(functions)
        for n, name in enumerate(sorted(functions.keys())):
            self.addItem(FunctionListItem(function=self.functions[name],
                                          blockClass=blockClass,
                                          name=name,
                                          parent=self))
            self.updateSize()

    def insertSeparator(self, title=''):
        """Вставить в список разделитель."""
        separator = QtWidgets.QListWidgetItem(title.center(21, '-'),
                                              parent=self)

        font = separator.font()
        font.setBold(True)
        separator.setFont(font)

        separator.setFlags(separator.flags()
                           & ~QtCore.Qt.ItemFlag.ItemIsSelectable
                           & ~QtCore.Qt.ItemFlag.ItemIsDragEnabled)

        self.addItem(separator)
        self.updateSize()

    def updateSize(self):
        """Обновить размер списка."""
        self.setMinimumWidth(self.sizeHintForColumn(0) + 2*self.frameWidth())
