from PyQt5 import QtGui, QtWidgets, uic
from functions import input as _input, output, processing, visualisation
from widgets import Scene
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


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/LoginWindow.ui', self)
        self.loginPushButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        if (self.usernameLineEdit.text() == 'foo'
            and self.passwordLineEdit.text() == 'bar'):
            self.accept()
        else:
            self.warningLabel: QtWidgets.QLabel
            self.warningLabel.setText('Неверное имя пользователя или пароль')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    login_window = LoginWindow()
    if login_window.exec_() == QtWidgets.QDialog.Accepted:
        w = MainWindow()
        w.show()
        app.exec_()
