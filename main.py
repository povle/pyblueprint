from PyQt5 import QtGui, QtWidgets, uic
from functions import input as _input, output, processing, visualisation
from widgets import Scene, LoginWindow
from widgets.blocks import (InputBlock, OutputBlock,
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

        self.functionList.addFunctions(module=_input,
                                       block_class=InputBlock,
                                       sep_title='Input')
        self.functionList.addFunctions(module=processing,
                                       block_class=ProcessingBlock,
                                       sep_title='Processing')
        self.functionList.addFunctions(module=visualisation,
                                       block_class=VisualisationBlock,
                                       sep_title='Visualisation')
        self.functionList.addFunctions(module=output,
                                       block_class=OutputBlock,
                                       sep_title='Output')

        self.keys = {
                    45: self.zoom_out,  # -
                    61: self.zoom_in,  # +
                    16777216: self.scene.stopConnecting,  # esc
                     }

        self.initMenubar()

    def initMenubar(self):
        self.menuBar().setNativeMenuBar(False)

        fixPosAct = QtWidgets.QAction('Fix positions', self)
        fixPosAct.setCheckable(True)
        fixPosAct.triggered.connect(self.scene.setPositionsFixed)

        prefMenu = self.menuBar().addMenu('&Preferences')
        prefMenu.addAction(fixPosAct)

        self.menuBar().addMenu('&Edit')

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
