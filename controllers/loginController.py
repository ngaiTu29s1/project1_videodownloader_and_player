from PySide6.QtWidgets import QMessageBox

class LoginController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect view signals to controller methods
        self.view.ui.loginButton.clicked.connect(self.handle_login)
        self.view.ui.guestButton.clicked.connect(self.handle_guest_login)

    def handle_login(self):
        """
        Handle the login button click event.
        """
        username = self.view.ui.usernameLE.text().strip()
        password = self.view.ui.passwordLE.text()

        if not username or not password:
            self.show_message("Error", "Please enter both username and password.")
            return

        # Authenticate using the model
        if self.model.authenticate(username, password):
            self.show_message("Success", f"Welcome, {username}!")
            # TODO: Transition to the main application window
        else:
            self.show_message("Error", "Invalid username or password.")
            self.view.ui.usernameLE.clear()
            self.view.ui.passwordLE.clear()

    def handle_guest_login(self):
        """
        Handle the guest login button click event.
        """
        self.show_message("Guest Login", "Welcome, Guest!")
        # TODO: Transition to the main application window

    def show_message(self, title, message):
        """
        Show a message box with the given title and message.
        """
        QMessageBox.information(self.view, title, message)