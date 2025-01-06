from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, \
    QVBoxLayout, QFormLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap

from HomePage import TravelApp
from checking_funktion import show_success_message ,show_warning_message , is_valid_email
from database_action import *
from styles import *
import sqlite3
import random


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
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Die Größe des Fensters Bildschirmgröße ändern
        self.resize(int(screen_width * 0.5), int(screen_height * 0.7))  # In ganze Zahlen umwandeln

        # Mindestmaße festlegen, um zu verhindern, dass das Fenster zu klein wird
        self.setMinimumSize(800, 600)
        self.setStyleSheet(loginmainstyle)

        # Erstellen eines zentralen Widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(50, 50, 50, 50)
        self.main_layout.setSpacing(50)

        # Title
        self.title = QLabel("Willkommen! Bitte anmelden oder registrieren")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet(logintitlestyle)
        self.main_layout.addWidget(self.title)

        # Image
        self.image_label = QLabel()
        self.image_pixmap = QPixmap("../images/ships-6073537_640.jpg")
        self.image_label.setPixmap(self.image_pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setMaximumHeight(500)
        self.image_label.setStyleSheet(loginimagestyle)
        self.main_layout.addWidget(self.image_label)

        #Formular
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(20, 20, 20, 20)
        self.form_layout.setSpacing(20)



        # Benutzername Label und Eingabefeld
        username_label = QLabel("Benutzername:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername")
        self.username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Passwort Label und Eingabefeld
        password_label = QLabel("Passwort:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.form_layout.addRow(username_label, self.username_input)
        self.form_layout.setSpacing(50)
        self.form_layout.addRow(password_label, self.password_input)
        self.main_layout.addLayout(self.form_layout)

        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout des boutons
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(30)


        # Login-Button
        self.login_button = QPushButton("Anmelden")
        self.login_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet(loginbuttonstyle)

        self.register_prompt_btn = QPushButton("Noch  kein Konto? Jetzt registrieren")
        self.register_prompt_btn.setStyleSheet(registerpromptstyle)
        self.register_prompt_btn.clicked.connect(self.show_registration_form)

        # Registrieren-Button
        self.register_button = QPushButton("Registrieren")
        self.register_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setStyleSheet(loginbuttonstyle)
        self.register_button.hide()

        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.register_prompt_btn)
        self.button_layout.addWidget(self.register_button)
        self.main_layout.addLayout(self.button_layout)


    def show_registration_form(self,event):
        self.title.setText("Registrieren Sie sich")

        if not hasattr(self, "email_input"):
            self.email_label = QLabel("Email:")
            self.email_input = QLineEdit()
            self.email_input.setPlaceholderText("E-Mail-Adresse")
            self.form_layout.insertRow(1, self.email_label, self.email_input)  # 2te Position

            if not hasattr(self, "confirm_passwort_input"):

                self.confirm_password_label = QLabel("Passwort bestätigen:")
                self.confirm_password_input = QLineEdit()
                self.confirm_password_input.setEchoMode(QLineEdit.Password)
                self.confirm_password_input.setPlaceholderText("Passwort bestätigen")
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


            self.main_page = TravelApp()
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
