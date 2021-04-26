from PyQt5 import QtWidgets, uic


class IntInputRow(QtWidgets.QWidget):
    """Виджет ввода параметра типа int."""

    def __init__(self, argName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/IntInputRow.ui', self)
        self.label.setText(argName)
        self.argName = argName

    def getVal(self):
        """Возвращает значение параметра."""
        return self.spinBox.value()
