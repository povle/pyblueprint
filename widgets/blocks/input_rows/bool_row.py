from PyQt5 import QtWidgets


class BoolInputRow(QtWidgets.QCheckBox):
    def __init__(self, arg_name, *args, **kwargs):
        super().__init__(text=arg_name, *args, **kwargs)
        self.arg_name = arg_name

    def getVal(self):
        return self.isChecked()
