from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt


class UserInfoWindow(QWidget):
    def __init__(self, return_callback=None):
        super().__init__()
        self.setWindowTitle("User Profile")
        self.setMinimumSize(500, 400)

        # Callback pour retourner à la page précédente
        self.return_callback = return_callback

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Header section
        self.header_label = QLabel("User Profile")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        self.main_layout.addWidget(self.header_label)

        # Information utilisateur
        self.info_layout = QVBoxLayout()

        self.user_id_label = QLabel("User ID:")
        self.user_id_label.setAlignment(Qt.AlignLeft)
        self.user_id_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.username_label = QLabel("Username:")
        self.username_label.setAlignment(Qt.AlignLeft)
        self.username_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.email_label = QLabel("Email:")
        self.email_label.setAlignment(Qt.AlignLeft)
        self.email_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        self.kontostand_label = QLabel("Account Balance:")
        self.kontostand_label.setAlignment(Qt.AlignLeft)
        self.kontostand_label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")

        # Ajouter les labels au layout des informations
        self.info_layout.addWidget(self.user_id_label)
        self.info_layout.addWidget(self.username_label)
        self.info_layout.addWidget(self.email_label)
        self.info_layout.addWidget(self.kontostand_label)

        # Ajouter un QFrame pour un style visuel
        info_frame = QFrame()
        info_frame.setLayout(self.info_layout)
        info_frame.setStyleSheet("border: 1px solid #ccc; padding: 10px; border-radius: 8px;")
        self.main_layout.addWidget(info_frame)

        # Spacer pour équilibrer les éléments
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Bouton Quit
        button_layout = QHBoxLayout()
        self.quit_button = QPushButton("Quit")
        self.quit_button.setStyleSheet(
            """
            QPushButton {
                background-color: red;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: white;
                color:black;
            }
            """
        )
        self.quit_button.clicked.connect(self.handle_quit_button)

        button_layout.addStretch()
        button_layout.addWidget(self.quit_button)
        button_layout.addStretch()

        self.main_layout.addLayout(button_layout)

    def update_user_info(self, user_data):
        """
        Met à jour les informations utilisateur affichées sur la page.
        :param user_data: dict contenant les informations utilisateur.
        """
        self.user_id_label.setText(f"User ID: {user_data.get('id', '')}")
        self.username_label.setText(f"Username: {user_data.get('username', '')}")
        self.email_label.setText(f"Email: {user_data.get('email', '')}")
        self.kontostand_label.setText(f"Account Balance: {user_data.get('kontostand', '')} €")

    def handle_quit_button(self):
        if self.return_callback:
            self.return_callback()
