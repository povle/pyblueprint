from PyQt5 import QtWidgets
from types import ModuleType
from typing import Callable
import inspect


class FunctionListItem(QtWidgets.QListWidgetItem):
    def __init__(self,
                 function: Callable,
                 name: str,
                 parent: QtWidgets.QListWidget):
        super().__init__(name, parent, 1001)
        self.function = function


class FunctionList(QtWidgets.QListWidget):
    def __init__(self, functions: ModuleType = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.functions = {}
        if functions is not None:
            self.addFunctions(functions)

    def addFunctions(self, functions_module: ModuleType):
        functions = dict(inspect.getmembers(functions_module,
                                            predicate=inspect.isfunction))
        self.functions.update(functions)
        for name in sorted(functions.keys()):
            self.addItem(FunctionListItem(function=self.functions[name],
                                          name=name,
                                          parent=self))
