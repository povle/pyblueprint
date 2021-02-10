from PyQt5 import QtGui, QtWidgets, uic
import inspect
import functions
from widgets import Scene


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('./ui/proto.ui', self)
        self.setWindowTitle('test')
        self.scene = Scene(self.graphicsView)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setMouseTracking(True)

        self.addBlockButton.clicked.connect(self.addFunctionBlock)
        self.runButton.clicked.connect(self.scene.run)

        self.functions = {name: func for name, func in
                          inspect.getmembers(functions,
                                             predicate=inspect.isfunction)}

        self.functionSelectBox.addItems(sorted(self.functions.keys()))

        self.keys = {
                    45: self.zoom_out,  # -
                    61: self.zoom_in,  # +
                    16777216: self.scene.stopConnecting,  # esc
                     }

    def addFunctionBlock(self):
        function = self.functions[self.functionSelectBox.currentText()]
        self.scene.addFunctionBlock(function)

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
    w = MainWindow()
    w.show()
    app.exec_()
