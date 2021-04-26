from PyQt5 import QtWidgets


class BoolInputRow(QtWidgets.QCheckBox):
    """Виджет ввода параметра типа bool."""

    def __init__(self, argName, *args, **kwargs):
        super().__init__(text=argName, *args, **kwargs)
        self.argName = argName

    def getVal(self):
        """Возвращает значение параметра."""
        return self.isChecked()
