import sqlite3

import bcrypt

class DatabaseAction:
    def __init__(self):
        self.conn = sqlite3.connect('User.sqlite')
        self.cursor = self.conn.cursor()
        self.conn.execute('PRAGMA foreign_keys = ON')
    def add_user(self, username, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            self.cursor.execute("INSERT INTO Userr (username,email,password,kontostand) VALUES (?,?,?,?)",
                                (username, email, hashed_password, 0))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False