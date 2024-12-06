import sqlite3

import bcrypt


conn = sqlite3.connect('User.sqlite')
cursor = conn.cursor()
conn.execute('PRAGMA foreign_keys = ON')

def get_user_balance(name):
    conn = sqlite3.connect('User.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                SELECT kontostand FROM User WHERE username = ?
            ''', (name,))
    balance = cursor.fetchone()
    return balance[0] if balance else 0
