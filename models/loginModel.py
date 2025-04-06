class LoginModel:
    def __init__(self):
        # Test data
        self.valid_users = {
            "admin": "password123"
        }

    def authenticate(self, username, password):
        """
        Authenticate the user by checking the username and password.
        Returns True if valid, False otherwise.
        """
        return self.valid_users.get(username) == password