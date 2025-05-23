import hashlib
import sqlite3
import os

DB_FOLDER = os.path.join("core", "db")
ACCOUNT_DB_FILE = os.path.join(DB_FOLDER, "account.db")

class LoginModel:
    def __init__(self):
        pass  # No hardcoded users

    def authenticate(self, username, password):
        """
        Authenticate the user by checking the username and password in the database.
        Returns True if valid, False otherwise.
        """
        conn = sqlite3.connect(ACCOUNT_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM accounts WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0] == password
        return False