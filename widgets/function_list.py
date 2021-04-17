from PyQt5 import QtWidgets
from types import ModuleType
from typing import Callable, Type
from .blocks import AbstractBlock
import inspect


class FunctionListItem(QtWidgets.QListWidgetItem):
    def __init__(self,
                 function: Callable,
                 block_class: Type[AbstractBlock],
                 name: str,
                 parent: QtWidgets.QListWidget):
        super().__init__(name, parent, 1001)
        self.function = function
        self.block_class = block_class


class FunctionList(QtWidgets.QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = {}

    def addFunctions(self, module: ModuleType,
                     block_class: Type[AbstractBlock]):
        functions = dict(inspect.getmembers(module,
                                            predicate=inspect.isfunction))
        self.functions.update(functions)
        for name in sorted(functions.keys()):
            self.addItem(FunctionListItem(function=self.functions[name],
                                          block_class=block_class,
                                          name=name,
                                          parent=self))
