import sqlite3


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

import sqlite3

def update_user_balance(username, new_balance):
    """
    Met à jour le solde de l'utilisateur dans la base de données.
    """
    try:
        conn = sqlite3.connect('User.sqlite')  # Chemin vers votre base de données SQLite
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET kontostand = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la mise à jour du solde : {e}")
        raise
