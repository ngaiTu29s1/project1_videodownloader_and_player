import sys
from PySide6.QtWidgets import QApplication
from views.py.loginView import LoginWindow
from models.loginModel import LoginModel
from controllers.loginController import LoginController


def main():
    app = QApplication(sys.argv)

    # Initialize the model, view, and controller
    model = LoginModel()
    view = LoginWindow()
    controller = LoginController(model, view)

    # Show the login window
    view.show()

    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()