from PyQt5 import QtWidgets, uic


class IntInputRow(QtWidgets.QWidget):
    def __init__(self, arg_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/IntInputRow.ui', self)
        self.label.setText(arg_name)
        self.arg_name = arg_name

    def getVal(self):
        return self.spinBox.value()
