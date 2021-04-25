from PyQt5 import QtWidgets, uic
import sqlite3
import bcrypt


def createTable():
    with sqlite3.connect('./users.db') as db:
        c = db.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
            username text PRIMARY KEY,
            password text NOT NULL
        );"""
        )


def getUser(username: str):
    with sqlite3.connect('./users.db') as db:
        c = db.cursor()
        c.execute('SELECT * FROM users WHERE username=?', (username,))
        user = c.fetchone()
        if user is not None:
            return user[1].encode('utf8')
        return None


def addUser(username: str, password: str):
    password = password.encode('utf8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf8')
    with sqlite3.connect('./users.db') as db:
        c = db.cursor()
        c.execute('INSERT INTO users(username,password) VALUES(?,?)',
                  (username, hashed))
        db.commit()


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/LoginWindow.ui', self)
        createTable()
        self.loginPushButton.clicked.connect(self.handleLogin)
        self.registerPushButton.clicked.connect(self.handleRegister)

    def handleLogin(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text().encode('utf8')
        hash = getUser(username)
        if hash is not None and bcrypt.checkpw(password, hash):
            self.accept()
        else:
            self.warningLabel.setText('Неверное имя пользователя или пароль')

    def handleRegister(self):
        RegisterWindow(parent=self).show()


class RegisterWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('./ui/RegisterWindow.ui', self)
        self.registerPushButton.clicked.connect(self.handleRegister)
        self.validationHash = \
            b'$2b$12$LnxesfT3kv3.5cY2SW1NQeZG5slMnJFqhwM73g6MvYFnqIyHQPfSW'

    def handleRegister(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        validationCode = self.validationLineEdit.text().encode('utf8')
        if not bcrypt.checkpw(validationCode, self.validationHash):
            self.warningLabel.setText('Неверный код регистрации')
        elif len(username) < 1:
            self.warningLabel.setText('Введите имя пользователя')
        elif getUser(username) is not None:
            self.warningLabel.setText('Выбранное пользователя уже занято')
        elif len(password) < 6:
            self.warningLabel.setText('В пароле должно быть от 6 символов')
        else:
            addUser(username, password)
            self.accept()
