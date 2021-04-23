from PyQt5 import QtWidgets, uic


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/LoginWindow.ui', self)
        self.loginPushButton.clicked.connect(self.handleLogin)

    def handleLogin(self):
        # FIXME  add a proper login system
        if (self.usernameLineEdit.text() == 'foo'
                and self.passwordLineEdit.text() == 'bar'):
            self.accept()
        else:
            self.warningLabel.setText('Неверное имя пользователя или пароль')
