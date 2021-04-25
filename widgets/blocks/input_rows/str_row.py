from PyQt5 import QtWidgets, uic


class StrInputRow(QtWidgets.QWidget):
    def __init__(self, arg_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/StrInputRow.ui', self)
        self.label.setText(arg_name)
        self.arg_name = arg_name

    def getVal(self):
        return self.lineEdit.text()
