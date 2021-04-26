from PyQt5 import QtWidgets, uic


class FloatInputRow(QtWidgets.QWidget):
    """Виджет ввода параметра типа float."""

    def __init__(self, argName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/FloatInputRow.ui', self)
        self.label.setText(argName)
        self.argName = argName

    def getVal(self):
        """Возвращает значение параметра."""
        return self.spinBox.value()
