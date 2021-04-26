from PyQt5 import QtGui, QtWidgets, QtCore

NORMAL = QtGui.QIcon.Mode.Normal
DISABLED = QtGui.QIcon.Mode.Disabled
ACTIVE = QtGui.QIcon.Mode.Active
SELECTED = QtGui.QIcon.Mode.Selected

ON = QtGui.QIcon.State.On
OFF = QtGui.QIcon.State.Off


class ErrorButton(QtWidgets.QToolButton):
    """Индикатор ошибки и кнопка, открывающая содержание ошибки."""

    modes = [NORMAL, DISABLED, ACTIVE, SELECTED]
    states = [ON, OFF]

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        icon = QtGui.QIcon()
        for mode in self.modes:
            for state in self.states:
                if mode == DISABLED:
                    path = 'resources/transparent.png'
                else:
                    path = 'resources/alert-triangle.png'
                icon.addFile(path, QtCore.QSize(16, 16), mode, state)

        self.setIcon(icon)
        self.installEventFilter(self)
