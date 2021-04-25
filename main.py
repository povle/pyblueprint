from PyQt5 import QtGui, QtWidgets, uic
from types import ModuleType
from typing import Type
from functions import input as _input, output, processing, visualisation
from widgets import Scene, LoginWindow
from widgets.blocks import (AbstractBlock, InputBlock, OutputBlock,
                            ProcessingBlock, VisualisationBlock)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/MainWindow.ui', self)
        self.setWindowTitle('test')
        self.scene = Scene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setAcceptDrops(True)

        self.runButton.clicked.connect(self.scene.run)

        self.initMenubar()

        self.addFunctions(module=_input, block_class=InputBlock,
                          title='Ввод')
        self.addFunctions(module=processing, block_class=ProcessingBlock,
                          title='Обработка')
        self.addFunctions(module=visualisation, block_class=VisualisationBlock,
                          title='Визуализация')
        self.addFunctions(module=output, block_class=OutputBlock,
                          title='Сохранение')

        self.keys = {
                    45: self.zoom_out,  # -
                    61: self.zoom_in,  # +
                    16777216: self.scene.stopConnecting,  # esc
                     }

    def initMenubar(self):
        self.menuBar().setNativeMenuBar(False)

        fixPosAct = QtWidgets.QAction('Зафиксировать блоки', self)
        fixPosAct.setCheckable(True)
        fixPosAct.triggered.connect(self.scene.setPositionsFixed)

        self.prefMenu = self.menuBar().addMenu('&Настройки')
        self.prefMenu.addAction(fixPosAct)

        self.editMenu = self.menuBar().addMenu('&Редактировать')

    def addFunctions(self, module: ModuleType,
                     block_class: Type[AbstractBlock],
                     title=None):
        self.functionList.addFunctions(module=module,
                                       block_class=block_class,
                                       sep_title=title)
        editAct = QtWidgets.QAction(title, self)
        # TODO open Notepad on click
        self.editMenu.addAction(editAct)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        self.keys.get(key, lambda: None)()
        super().keyPressEvent(event)

    def zoom_out(self):
        self.zoom(zoom_out=True)

    def zoom_in(self):
        self.zoom(zoom_out=False)

    def zoom(self, zoom_out):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        if not zoom_out:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.graphicsView.scale(zoomFactor, zoomFactor)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    # FIXME temporarily disabled login
    # login_window = LoginWindow()
    # if login_window.exec_() == QtWidgets.QDialog.Accepted:
    w = MainWindow()
    w.show()
    app.exec_()
