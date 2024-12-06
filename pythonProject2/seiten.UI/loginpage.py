from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, \
    QVBoxLayout, QHBoxLayout, QFrame, QFormLayout
from PyQt5.QtGui import QPixmap

from fonctionalitee import VoyageApp
from utiles import show_success_message ,show_warning_message , is_valid_email
from database_action import *
import re
import sqlite3
import random
import sys


conn = sqlite3.connect('User.sqlite')
# Erstellt die connexion zur Database
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        kontostand INTEGER NOT NULL
    )
''')
conn.commit()


class LoginRegisterPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(1700, 1200)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        self.setStyleSheet("""
            QMainWindow {background-color: #f0f5f9;}
            QLabel {font-size: 16px; color: #333;}
            QLineEdit {font-size: 14px;padding: 8px;border: 1px solid #a0a0a0;border-radius: 5px;width: 200px;}
            """)

        # Créer un widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(50, 50, 50, 50)

        # Créer un QFrame pour le formulaire et les boutons
        self.form_frame = QFrame()
        self.form_frame.setFixedWidth(900)
        self.form_frame.setFixedHeight(1200)
        self.form_frame.setStyleSheet("background-color: white; padding: 20px; border-radius: 10px;")
        self.main_layout.addWidget(self.form_frame)

        # Layout pour les éléments du formulaire avec QVBoxLayout
        self.grid_layout = QVBoxLayout(self.form_frame)
        self.grid_layout.setContentsMargins(20, 20, 20, 40)
        self.grid_layout.setSpacing(15)

        self.label_1 = QLabel("Finde dein Traumziel")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078d7;")
        self.grid_layout.addWidget(self.label_1)

        # Image
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap("../images/ships-6073537_640.jpg")
        self.image_label.setPixmap(self.image_pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedHeight(400)
        self.grid_layout.addWidget(self.image_label)

        # Titre
        self.title = QLabel("Willkommen! Bitte anmelden oder registrieren")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("font-size:20px; font-weight: bold; color: #0078d7;")
        self.grid_layout.addWidget(self.title)

        # Layout pour le formulaire avec espacement réduit entre les labels et les champs
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(50)  # Espacement entre label et input

        # Benutzername Label und Eingabefeld
        self.username_label = QLabel("Benutzername:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername")
        self.username_input.setFixedWidth(600)
        self.form_layout.addRow(self.username_label, self.username_input)

        # Passwort Label und Eingabefeld
        self.password_label = QLabel("Passwort:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setFixedWidth(600)
        self.form_layout.addRow(self.password_label, self.password_input)
        self.form_layout.setSpacing(40)

        # Ajouter le layout du formulaire au layout principal
        self.grid_layout.addLayout(self.form_layout)

        # Layout des boutons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(40)

        # Login-Button
        self.login_button = QPushButton("Anmelden", self)
        self.login_button.setFixedSize(140, 60)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet("""
            font-size: 16px;
            background-color: #0078d7;
            color: white;
            padding: 12px;
            border-radius: 10px;
            min-width: 140px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

        self.button_layout.addWidget(self.login_button)
        self.button_layout.setContentsMargins(0, 40, 0, 20)
        self.grid_layout.addLayout(self.button_layout)

        self.register_prompt_btn = QPushButton("Noch  kein Konto? Jetzt registrieren", self)
        self.register_prompt_btn.setStyleSheet("""
            QPushButton {
                color: #0078d7;
                font-size: 16px; 
                cursor: pointer; 
                border: none;
                background-color : transparent;
            }
                """)
        self.register_prompt_btn.clicked.connect(self.show_registration_form)
        self.grid_layout.addWidget(self.register_prompt_btn)

        # Registrieren-Button
        self.register_button = QPushButton("Registrieren", self)
        self.register_button.setFixedSize(140, 60)
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setStyleSheet("""
                    font-size: 14px;
                    background-color: #0078d7;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                    min-width: 140px;
                    }
                    QPushButton:hover {
                       background-color: #005a9e;
                    }

                """)
        self.register_button.hide()
        self.button_layout.addWidget(self.register_button)

    def show_registration_form(self,event):
        self.title.setText("Registrieren Sie sich")

        #self.grid_layout.removeWidget(self.password_input)
        #self.grid_layout.removeWidget(self.password_label)

        if not hasattr(self, "email_input"):
            self.email_label = QLabel("Email:")
            self.email_input = QLineEdit()
            self.email_input.setPlaceholderText("E-Mail-Adresse")
            self.email_input.setFixedWidth(600)
            self.form_layout.insertRow(1, self.email_label, self.email_input)  # 2te Position

            if not hasattr(self, "confirm_passwort_input"):

                self.confirm_password_label = QLabel("Passwort bestätigen:")
                self.confirm_password_input = QLineEdit()
                self.confirm_password_input.setEchoMode(QLineEdit.Password)
                self.confirm_password_input.setPlaceholderText("Passwort bestätigen")
                self.confirm_password_input.setFixedWidth(600)
                self.form_layout.addRow(self.confirm_password_label, self.confirm_password_input)

        self.login_button.hide()
        self.register_prompt_btn.hide()
        self.register_button.show()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        #cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
        #user = cursor.fetchone()
        cursor.execute("SELECT id, kontostand FROM User WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            user_id,current_kontostand = user # Tuple ou la ligne  du tableau que renvoi ma requette select plus haut

            #random Zahl
            additional_kontostand = random.randint(1000,3000)
            new_kontostand = current_kontostand + additional_kontostand

            if new_kontostand >20000:
                new_kontostand =20000

            cursor.execute("UPDATE User SET kontostand=? WHERE id=?", (new_kontostand, user_id))
            conn.commit()

            self.username_input.clear()
            self.password_input.clear()


            self.main_page = VoyageApp()
            self.main_page.header_user_name_edit.setText(f"{username}")
            self.main_page.kontostand_amont_edit.setText(f"{new_kontostand}€")
            #self.main_page.set_current_user(user_id, username, new_kontostand)
            self.main_page.show()
            self.close()  # close loginpage


        else:
            show_warning_message("Fehler" , "Ungültige Benutzername oder Passwort!" )



    def handle_register(self):
        username = self.username_input.text()
        email = self.email_input.text() if hasattr(self, 'email_input') else None
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text() if hasattr(self, 'confirm_password_input') else None

        if not username or not email or not password or not confirm_password:
            show_warning_message(  "Fehler", "Bitte alle Felder ausfüllen!")
            return
        if not is_valid_email(email):
            show_warning_message("Fehler", "Bitte eine gültige E-Mail-Adresse eingeben!")
            return
        if password != confirm_password:
            show_warning_message("Fehler", "Die Passwörter stimmen nicht überein!")
            return

        try:
            cursor.execute("INSERT INTO User (username,email,password,kontostand) VALUES (?,?,?,?)",
                           (username,email,password,0))
            conn.commit()


            show_success_message("Erfolg", "Registrierung erfolgreich! Bitte anmelden.!")
            self.reset_form()

        except sqlite3.IntegrityError:
            show_warning_message("Fehler","Benutzername oder E-mail bereits vorhanden.")

    def reset_form(self):
        self.title.setText("Willkommen! Bitte anmelden oder registrieren")

        if hasattr(self, 'email_label'):  # if email_label existiert
            self.email_label.deleteLater()  # deleteLater löscht das Widget ordnunggemäß
            self.email_input.deleteLater()

        if hasattr(self, 'confirm_password_label'):
            self.confirm_password_label.deleteLater()
            self.confirm_password_input.deleteLater()

        self.login_button.show()
        self.register_button.hide()
        self.register_prompt_btn.show()

        self.username_input.clear()
        self.password_input.clear()


def main():
    app = QApplication(sys.argv)
    window = LoginRegisterPage()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
