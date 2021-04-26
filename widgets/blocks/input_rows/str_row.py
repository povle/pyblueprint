from PyQt5 import QtWidgets, uic


class StrInputRow(QtWidgets.QWidget):
    def __init__(self, argName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/StrInputRow.ui', self)
        self.label.setText(argName)
        self.argName = argName

    def getVal(self):
        return self.lineEdit.text()
