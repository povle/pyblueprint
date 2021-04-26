from PyQt5 import QtWidgets


class BoolInputRow(QtWidgets.QCheckBox):
    def __init__(self, argName, *args, **kwargs):
        super().__init__(text=argName, *args, **kwargs)
        self.argName = argName

    def getVal(self):
        return self.isChecked()
