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
    Aktualisiert den Kontostand des Nutzers in der Datenbank.
    """
    try:
        conn = sqlite3.connect('User.sqlite')  # Chemin vers votre base de données SQLite
        cursor = conn.cursor()
        cursor.execute("UPDATE User SET kontostand = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Fehler bei der Aktualisierung des Saldos : {e}")
        raise

def get_user_info(header_user_name_edit):
        """
        Rufen Sie die Benutzerinformationen aus der Datenbank ab.
        Passen Sie diese Methode an die Struktur Ihrer Datenbank an.
        """
        try:
            username = header_user_name_edit.text()
            cursor.execute("SELECT id,username, email, kontostand FROM User WHERE username = ?", (username,))
            user_row = cursor.fetchone()
            if user_row:
                return {
                    "id": user_row[0],
                    "username": user_row[1],
                    "email": user_row[2],
                    "kontostand": user_row[3],
                }
            else:
                return None
        except Exception:
            return None