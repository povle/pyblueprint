from PyQt5 import QtWidgets, uic


class StrInputRow(QtWidgets.QWidget):
    """Виджет ввода параметра типа str."""

    def __init__(self, argName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/StrInputRow.ui', self)
        self.label.setText(argName)
        self.argName = argName

    def getVal(self):
        """Возвращает значение параметра."""
        return self.lineEdit.text()
