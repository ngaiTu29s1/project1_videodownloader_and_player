from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from views.py.loginScreen import LoginWindow


if __name__ == "__main__":
    app = QApplication()
    window = LoginWindow()
    window.show()
    app.exec()

