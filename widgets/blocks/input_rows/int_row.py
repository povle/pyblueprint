from PyQt5 import QtWidgets, uic


class IntInputRow(QtWidgets.QWidget):
    def __init__(self, argName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/IntInputRow.ui', self)
        self.label.setText(argName)
        self.argName = argName

    def getVal(self):
        return self.spinBox.value()
