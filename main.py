import os
import importlib
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from types import ModuleType
from typing import Type
from functions import input as _input, output, processing, visualisation
from widgets import Scene, LoginWindow
from widgets.blocks import (AbstractBlock, InputBlock, OutputBlock,
                            ProcessingBlock, VisualisationBlock)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно приложения."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/MainWindow.ui', self)
        self.scene = Scene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setAcceptDrops(True)

        self.runButton.clicked.connect(self.scene.run)

        self.initMenubar()
        self.loadFunctions()

        self.keys = {
                    16777216: self.scene.stopConnecting,  # esc
                     }

    def initMenubar(self):
        """Инициализировать строку меню."""
        self.menuBar().setNativeMenuBar(False)

        fixPosAct = QtWidgets.QAction('Зафиксировать блоки', self)
        fixPosAct.setCheckable(True)
        fixPosAct.triggered.connect(self.scene.setPositionsFixed)

        self.prefMenu = self.menuBar().addMenu('&Настройки')
        self.prefMenu.addAction(fixPosAct)

        self.editMenu = self.menuBar().addMenu('&Редактировать')

        reloadAct = QtWidgets.QAction('Перезагрузить функции', self)
        reloadAct.triggered.connect(self.reloadFunctions)
        self.editMenu.addAction(reloadAct)

    def reloadFunctions(self):
        """Перезагрузить модули функций."""
        self.functionList.clear()
        self.loadFunctions(reload=True)

    def loadFunctions(self, reload=False):
        """Инициализировать все модули функций."""
        self.addFunctions(module=_input, blockClass=InputBlock,
                          title='Ввод', reload=reload)
        self.addFunctions(module=processing, blockClass=ProcessingBlock,
                          title='Обработка', reload=reload)
        self.addFunctions(module=visualisation, blockClass=VisualisationBlock,
                          title='Визуализация', reload=reload)
        self.addFunctions(module=output, blockClass=OutputBlock,
                          title='Сохранение', reload=reload)

    def addFunctions(self, module: ModuleType,
                     blockClass: Type[AbstractBlock],
                     title=None, reload=False):
        """Инициализировать модуль функций."""
        if reload:
            importlib.reload(module)
        else:
            editAct = QtWidgets.QAction(title, self)
            editAct.triggered.connect(lambda: self.editModule(module))
            self.editMenu.addAction(editAct)
        self.functionList.addFunctions(module=module,
                                       blockClass=blockClass,
                                       sepTitle=title)

    @staticmethod
    def editModule(module: ModuleType):
        """Открыть окно редактирования модуля функций."""
        path = os.path.abspath(module.__file__)
        QtCore.QProcess().startDetached(f'notepad.exe {path}')

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """Обработать нажатие на клавишу."""
        key = event.key()
        self.keys.get(key, lambda: None)()
        super().keyPressEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    login_window = LoginWindow()
    if login_window.exec_() == QtWidgets.QDialog.Accepted:
        w = MainWindow()
        w.show()
        app.exec_()
